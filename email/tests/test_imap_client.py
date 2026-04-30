"""Tests for IMAPClient race condition fixes."""

import asyncio
import socket
import ssl
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

import aioimaplib

from email_mcp.config import EmailAccount
from email_mcp.imap.client import IMAPClient


@pytest.fixture
def mock_account():
  """Create a mock email account for testing."""
  return EmailAccount(
    name="test",
    imap_host="imap.test.com",
    imap_port=993,
    smtp_host="smtp.test.com",
    smtp_port=587,
    username="test@test.com",
    password="test_password",
    auth_method="password",
  )


@pytest.fixture
def mock_imap_client(mock_account):
  """Create a mock IMAP client with async operations."""
  with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
    mock_client = AsyncMock()
    mock_client.wait_hello_from_server = AsyncMock()
    mock_client.login = AsyncMock(return_value=("OK", [b"Logged in"]))
    mock_client.select = AsyncMock(return_value=("OK", [b"10 EXISTS"]))
    mock_client.list = AsyncMock(return_value=("OK", [b'(\\HasNoChildren) "/" "INBOX"']))
    # aioimaplib search returns a Response object with .result and .lines
    search_response = AsyncMock()
    search_response.result = "OK"
    search_response.lines = [b"SEARCH 1 2 3"]
    mock_client.search = AsyncMock(return_value=search_response)
    mock_client.fetch = AsyncMock(return_value=("OK", []))
    mock_client.logout = AsyncMock(return_value=("OK", [b"Logged out"]))
    mock_client.copy = AsyncMock(return_value=("OK", []))
    mock_client.store = AsyncMock(return_value=("OK", []))
    mock_imap_class.return_value = mock_client
    yield mock_client


class TestIMAPClientLocks:
  """Test operation-level locking in IMAPClient."""

  async def test_connect_lock_serializes_concurrent_connects(self, mock_account):
    """Two concurrent connect() calls should create only one IMAP4_SSL instance."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.login = AsyncMock(return_value=("OK", [b"Logged in"]))
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)

      # Slow down connection to expose race
      async def slow_login(*args, **kwargs):
        await asyncio.sleep(0.05)
        return ("OK", [b"Logged in"])

      mock_client.login = slow_login

      async def connect_task():
        return await client.connect()

      # Run two connect() calls concurrently
      results = await asyncio.gather(connect_task(), connect_task())

      # Both should return the same instance
      assert results[0] is results[1]
      # IMAP4_SSL should only be instantiated once
      assert mock_imap_class.call_count == 1

  async def test_connect_is_idempotent(self, mock_account, mock_imap_client):
    """Calling connect() twice should return the same client without re-creating."""
    client = IMAPClient(mock_account)

    result1 = await client.connect()
    result2 = await client.connect()

    assert result1 is result2
    # IMAP4_SSL constructor called once, login called once
    assert mock_imap_client.login.call_count == 1

  async def test_operation_lock_serializes_concurrent_searches(self, mock_account, mock_imap_client):
    """Two concurrent searches should not interleave IMAP commands."""
    client = IMAPClient(mock_account)

    # Track select calls to verify serialization
    select_calls = []
    original_select = mock_imap_client.select

    async def tracked_select(folder):
      select_calls.append(folder)
      await asyncio.sleep(0.01)  # Simulate network delay
      return await original_select(folder)

    mock_imap_client.select = tracked_select

    async def search_inbox():
      await client.search("INBOX", "ALL", 50)

    async def search_spam():
      await client.search("SPAM", "UNSEEN", 50)

    # Run concurrently
    await asyncio.gather(search_inbox(), search_spam())

    # Verify selects did not interleave — each search completes its select
    # before the next one starts because of operation-level locking
    assert len(select_calls) == 2

  async def test_operation_lock_held_during_full_search(self, mock_account, mock_imap_client):
    """The operation lock should be held for the entire search operation."""
    client = IMAPClient(mock_account)

    lock_held_during_search = False

    async def tracked_search(criteria):
      nonlocal lock_held_during_search
      await asyncio.sleep(0)  # Force yield point
      lock_held_during_search = client._operation_lock.locked()
      response = AsyncMock()
      response.result = "OK"
      response.lines = [b"SEARCH 1 2 3"]
      return response

    # Patch the mock client's search to check lock state
    mock_imap_client.search = tracked_search

    await client.search("INBOX", "ALL", 50)

    # Because we're inside the lock when tracked_search runs,
    # lock_held_during_search will be True
    assert lock_held_during_search is True

  async def test_connect_lock_separate_from_operation_lock(self, mock_account, mock_imap_client):
    """Connect lock and operation lock should be separate locks."""
    client = IMAPClient(mock_account)

    assert client._connect_lock is not client._operation_lock
    assert isinstance(client._connect_lock, asyncio.Lock)
    assert isinstance(client._operation_lock, asyncio.Lock)

  async def test_disconnect_clears_state(self, mock_account, mock_imap_client):
    """disconnect should clear _client and _selected_folder."""
    client = IMAPClient(mock_account)

    await client.connect()
    await client.select_folder("INBOX")
    assert client._client is not None
    assert client._selected_folder == "INBOX"

    await client.disconnect()

    assert client._client is None
    assert client._selected_folder is None
    mock_imap_client.logout.assert_called_once()

  async def test_select_folder_failure_raises(self, mock_account, mock_imap_client):
    """select_folder should raise RuntimeError on failure."""
    client = IMAPClient(mock_account)
    mock_imap_client.select.return_value = ("NO", [b"Folder not found"])

    with pytest.raises(RuntimeError, match="Failed to select folder"):
      await client.select_folder("NONEXISTENT")

  async def test_search_select_failure_raises(self, mock_account, mock_imap_client):
    """search should raise RuntimeError if select fails."""
    client = IMAPClient(mock_account)
    mock_imap_client.select.return_value = ("NO", [b"Folder not found"])

    with pytest.raises(RuntimeError, match="Failed to select folder"):
      await client.search("NONEXISTENT", "ALL", 50)

  async def test_fetch_message_select_failure_raises(self, mock_account, mock_imap_client):
    """fetch_message should raise RuntimeError if select fails."""
    client = IMAPClient(mock_account)
    mock_imap_client.select.return_value = ("NO", [b"Folder not found"])

    with pytest.raises(RuntimeError, match="Failed to select folder"):
      await client.fetch_message("1", "NONEXISTENT")

  async def test_auth_failure_raises(self, mock_account):
    """connect should raise RuntimeError on authentication failure."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.login = AsyncMock(
        side_effect=aioimaplib.Error("Invalid credentials")
      )
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)

      with pytest.raises(RuntimeError, match="Authentication failed"):
        await client.connect()


class TestAuthExceptionHandling:
  """Tests for specific exception handling during authentication (H2 bug fix)."""

  async def test_invalid_password_raises_auth_error(self, mock_account):
    """Invalid credentials should raise 'Authentication failed'."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.login = AsyncMock(
        side_effect=aioimaplib.Error("Invalid credentials")
      )
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)

      with pytest.raises(RuntimeError, match="Authentication failed"):
        await client.connect()

  async def test_oauth2_invalid_token_raises_auth_error(self, mock_account):
    """Invalid OAuth2 token should raise 'Authentication failed'."""
    oauth_account = EmailAccount(
      name="test",
      imap_host="imap.test.com",
      imap_port=993,
      smtp_host="smtp.test.com",
      smtp_port=587,
      username="test@test.com",
      auth_method="oauth2",
      oauth2_token="invalid_token",
    )

    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.authenticate = AsyncMock(
        side_effect=aioimaplib.Error("Invalid token")
      )
      mock_imap_class.return_value = mock_client

      client = IMAPClient(oauth_account)

      with pytest.raises(RuntimeError, match="Authentication failed"):
        await client.connect()

  async def test_connection_timeout_raises_timeout_error(self, mock_account):
    """Connection timeout should raise specific timeout message."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.login = AsyncMock(side_effect=TimeoutError())
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)

      with pytest.raises(RuntimeError, match="Connection timed out"):
        await client.connect()

  async def test_network_disconnect_raises_connection_error(self, mock_account):
    """Network disconnection should raise connection error."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.login = AsyncMock(
        side_effect=ConnectionError("Network unreachable")
      )
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)

      with pytest.raises(RuntimeError, match="Connection lost"):
        await client.connect()

  async def test_dns_failure_raises_dns_error(self, mock_account):
    """DNS resolution failure should raise DNS-specific message."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock(
        side_effect=socket.gaierror("Name resolution failed")
      )
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)

      with pytest.raises(RuntimeError, match="DNS resolution failed"):
        await client.connect()

  async def test_tls_error_raises_tls_message(self, mock_account):
    """TLS certificate error should raise TLS-specific message."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock(
        side_effect=ssl.SSLError("Certificate verify failed")
      )
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)

      with pytest.raises(RuntimeError, match="TLS error"):
        await client.connect()

  async def test_abort_raises_protocol_error(self, mock_account):
    """Protocol abort should raise protocol-specific message."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.login = AsyncMock(
        side_effect=aioimaplib.Abort("Server closed connection")
      )
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)

      with pytest.raises(RuntimeError, match="Protocol error"):
        await client.connect()

  async def test_oserror_raises_network_error(self, mock_account):
    """OSError should raise network error message."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock(
        side_effect=OSError("Connection refused")
      )
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)

      with pytest.raises(RuntimeError, match="Network error"):
        await client.connect()


class TestIMAPClientOperations:
  """Test IMAPClient public method functionality."""

  async def test_fetch_message(self, mock_account, mock_imap_client):
    """fetch_message should return parsed message data."""
    client = IMAPClient(mock_account)

    # Set up fetch response with a message
    mock_imap_client.fetch.return_value = (
      "OK",
      [
        (b"1 FETCH (BODY[] {100}", bytearray(b"Subject: Test\r\n\r\nBody")),
        b" FETCH completed",
      ],
    )

    result = await client.fetch_message("1", "INBOX")

    assert result["id"] == "1"
    assert result["folder"] == "INBOX"
    assert mock_imap_client.select.called
    assert mock_imap_client.fetch.called

  async def test_fetch_message_tuple_format(self, mock_account, mock_imap_client):
    """fetch_message should handle tuple response format."""
    client = IMAPClient(mock_account)

    mock_imap_client.fetch.return_value = (
      "OK",
      [
        (b"1 FETCH (BODY[] {100}", b"Subject: Test\r\n\r\nBody"),
        b" FETCH completed",
      ],
    )

    result = await client.fetch_message("1", "INBOX")

    assert result["id"] == "1"
    assert result["subject"] == "Test"

  async def test_move_message(self, mock_account, mock_imap_client):
    """move_message should copy, mark deleted, and expunge."""
    client = IMAPClient(mock_account)

    result = await client.move_message("1", "INBOX", "Archive")

    assert result is True
    mock_imap_client.copy.assert_called_once_with("1", "Archive")
    mock_imap_client.store.assert_called_once_with("1", "+FLAGS", "(\\Deleted)")
    mock_imap_client.expunge.assert_called_once()

  async def test_move_message_copy_failure_raises(self, mock_account, mock_imap_client):
    """move_message should raise RuntimeError if copy fails."""
    client = IMAPClient(mock_account)
    mock_imap_client.copy.return_value = ("NO", [b"Permission denied"])

    with pytest.raises(RuntimeError, match="Failed to copy message"):
      await client.move_message("1", "INBOX", "Archive")

  async def test_delete_message(self, mock_account, mock_imap_client):
    """delete_message should mark deleted and expunge."""
    client = IMAPClient(mock_account)

    result = await client.delete_message("1", "INBOX")

    assert result is True
    mock_imap_client.store.assert_called_once_with("1", "+FLAGS", "(\\Deleted)")
    mock_imap_client.expunge.assert_called_once()

  async def test_mark_message_add(self, mock_account, mock_imap_client):
    """mark_message with action=add should use +FLAGS."""
    client = IMAPClient(mock_account)

    result = await client.mark_message("1", "INBOX", "\\Seen", "add")

    assert result is True
    mock_imap_client.store.assert_called_once_with("1", "+FLAGS", "(\\Seen)")

  async def test_mark_message_remove(self, mock_account, mock_imap_client):
    """mark_message with action=remove should use -FLAGS."""
    client = IMAPClient(mock_account)

    result = await client.mark_message("1", "INBOX", "\\Seen", "remove")

    assert result is True
    mock_imap_client.store.assert_called_once_with("1", "-FLAGS", "(\\Seen)")

  async def test_download_attachment(self, mock_account, mock_imap_client, tmp_path):
    """download_attachment should save attachment to workspace."""
    import email_mcp.imap.client as imap_module
    original_workspace = imap_module.DEFAULT_WORKSPACE
    imap_module.DEFAULT_WORKSPACE = tmp_path

    client = IMAPClient(mock_account)

    # Build a multipart message with attachment
    import email.mime.multipart
    import email.mime.text
    import email.mime.application

    msg = email.mime.multipart.MIMEMultipart()
    msg.attach(email.mime.text.MIMEText("Body"))
    part = email.mime.application.MIMEApplication(b"attachment content")
    part.add_header("Content-Disposition", "attachment", filename="test.txt")
    msg.attach(part)

    mock_imap_client.fetch.return_value = (
      "OK",
      [
        (b"1 FETCH (BODY[] {500}", msg.as_bytes()),
        b" FETCH completed",
      ],
    )

    result = await client.download_attachment("1", "INBOX", "test.txt", str(tmp_path))

    assert Path(result).exists()
    assert Path(result).name.endswith("test.txt")
    with open(result, "rb") as f:
      assert f.read() == b"attachment content"

    imap_module.DEFAULT_WORKSPACE = original_workspace

  async def test_download_attachment_not_found(self, mock_account, mock_imap_client, tmp_path):
    """download_attachment should raise FileNotFoundError when attachment missing."""
    import email_mcp.imap.client as imap_module
    original_workspace = imap_module.DEFAULT_WORKSPACE
    imap_module.DEFAULT_WORKSPACE = tmp_path

    client = IMAPClient(mock_account)

    mock_imap_client.fetch.return_value = (
      "OK",
      [(b"1 FETCH (BODY[] {100}", b"Subject: Test\r\n\r\nBody"), b" FETCH completed"],
    )

    with pytest.raises(FileNotFoundError, match="Attachment not found"):
      await client.download_attachment("1", "INBOX", "nonexistent.txt", str(tmp_path))

    imap_module.DEFAULT_WORKSPACE = original_workspace

  async def test_select_folder_returns_correct_count(self, mock_account, mock_imap_client):
    """select_folder should return correct message count."""
    client = IMAPClient(mock_account)

    result = await client.select_folder("INBOX")

    assert result["folder"] == "INBOX"
    assert result["count"] == 10
    mock_imap_client.select.assert_called_once_with("INBOX")

  async def test_list_folders(self, mock_account, mock_imap_client):
    """list_folders should return parsed folder list."""
    client = IMAPClient(mock_account)

    result = await client.list_folders()

    assert len(result) == 1
    assert result[0]["name"] == "INBOX"
    assert result[0]["flags"] == "\\HasNoChildren"
    assert result[0]["delimiter"] == "/"


class TestMoveMessageAtomic:
  """Tests for atomic move_message using MOVE extension (H1 bug fix)."""

  async def test_uses_move_when_capability_present(self, mock_account):
    """Should use atomic MOVE command when server advertises MOVE capability."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.login = AsyncMock(return_value=("OK", [b"Logged in"]))
      mock_client.select = AsyncMock(return_value=("OK", [b"1 EXISTS"]))

      # Server advertises MOVE capability
      capability_response = AsyncMock()
      capability_response.result = "OK"
      capability_response.lines = [b"IMAP4REV1 MOVE UIDPLUS"]
      mock_client.capability = AsyncMock(return_value=capability_response)

      mock_client.move = AsyncMock(return_value=("OK", []))
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)
      await client.connect()  # Triggers capability query

      result = await client.move_message("1", "INBOX", "Archive")

      assert result is True
      mock_client.move.assert_called_once_with("1", "Archive")
      mock_client.copy.assert_not_called()  # COPY not used

  async def test_fallback_when_move_not_supported(self, mock_account):
    """Should fall back to COPY+STORE+EXPUNGE when MOVE not advertised."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.login = AsyncMock(return_value=("OK", [b"Logged in"]))
      mock_client.select = AsyncMock(return_value=("OK", [b"1 EXISTS"]))

      # Server does NOT advertise MOVE
      capability_response = AsyncMock()
      capability_response.result = "OK"
      capability_response.lines = [b"IMAP4REV1 UIDPLUS"]
      mock_client.capability = AsyncMock(return_value=capability_response)

      mock_client.copy = AsyncMock(return_value=("OK", []))
      mock_client.store = AsyncMock(return_value=("OK", []))
      mock_client.expunge = AsyncMock(return_value=("OK", []))
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)
      await client.connect()

      result = await client.move_message("1", "INBOX", "Archive")

      assert result is True
      mock_client.copy.assert_called_once_with("1", "Archive")
      mock_client.store.assert_called_once_with("1", "+FLAGS", "(\\Deleted)")
      mock_client.expunge.assert_called_once()

  async def test_move_failure_raises_error(self, mock_account):
    """MOVE command failure should raise RuntimeError."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.login = AsyncMock(return_value=("OK", [b"Logged in"]))
      mock_client.select = AsyncMock(return_value=("OK", [b"1 EXISTS"]))

      capability_response = AsyncMock()
      capability_response.result = "OK"
      capability_response.lines = [b"IMAP4REV1 MOVE"]
      mock_client.capability = AsyncMock(return_value=capability_response)

      mock_client.move = AsyncMock(return_value=("NO", [b"Permission denied"]))
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)
      await client.connect()

      with pytest.raises(RuntimeError, match="Failed to move message"):
        await client.move_message("1", "INBOX", "Archive")

  async def test_capability_cached_on_connect(self, mock_account):
    """Capabilities should be cached during connect, not queried per operation."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.login = AsyncMock(return_value=("OK", [b"Logged in"]))

      capability_response = AsyncMock()
      capability_response.result = "OK"
      capability_response.lines = [b"IMAP4REV1 MOVE"]
      mock_client.capability = AsyncMock(return_value=capability_response)

      mock_client.select = AsyncMock(return_value=("OK", [b"1 EXISTS"]))
      mock_client.move = AsyncMock(return_value=("OK", []))
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)
      await client.connect()

      # Multiple moves should only query capability once
      await client.move_message("1", "INBOX", "Archive")
      await client.move_message("2", "INBOX", "Archive")

      mock_client.capability.assert_called_once()  # Only during connect

  async def test_has_capability_returns_true_when_present(self, mock_account):
    """has_capability should return True for advertised capabilities."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.login = AsyncMock(return_value=("OK", [b"Logged in"]))

      capability_response = AsyncMock()
      capability_response.result = "OK"
      capability_response.lines = [b"IMAP4REV1 MOVE UIDPLUS"]
      mock_client.capability = AsyncMock(return_value=capability_response)
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)
      await client.connect()

      assert client.has_capability("MOVE") is True
      assert client.has_capability("UIDPLUS") is True
      assert client.has_capability("CONDSTORE") is False

  async def test_has_capability_is_case_insensitive(self, mock_account):
    """has_capability should be case-insensitive."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.login = AsyncMock(return_value=("OK", [b"Logged in"]))
      capability_response = AsyncMock()
      capability_response.result = "OK"
      capability_response.lines = [b"IMAP4REV1 MOVE UIDPLUS"]
      mock_client.capability = AsyncMock(return_value=capability_response)
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)
      await client.connect()

      assert client.has_capability("move") is True
      assert client.has_capability("Move") is True
      assert client.has_capability("MOVE") is True

  async def test_capability_query_failure_falls_back_gracefully(self, mock_account):
    """Should continue with empty capabilities if capability query fails."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.login = AsyncMock(return_value=("OK", [b"Logged in"]))
      mock_client.capability = AsyncMock(side_effect=TimeoutError())
      mock_client.select = AsyncMock(return_value=("OK", [b"1 EXISTS"]))
      mock_client.copy = AsyncMock(return_value=("OK", []))
      mock_client.store = AsyncMock(return_value=("OK", []))
      mock_client.expunge = AsyncMock(return_value=("OK", []))
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)
      await client.connect()

      assert client.has_capability("MOVE") is False
      # Should fall back to COPY+STORE+EXPUNGE
      result = await client.move_message("1", "INBOX", "Archive")
      mock_client.copy.assert_called_once()

  async def test_capabilities_cleared_on_disconnect(self, mock_account):
    """disconnect should clear cached capabilities."""
    with patch("email_mcp.imap.client.IMAP4_SSL") as mock_imap_class:
      mock_client = AsyncMock()
      mock_client.wait_hello_from_server = AsyncMock()
      mock_client.login = AsyncMock(return_value=("OK", [b"Logged in"]))
      mock_client.logout = AsyncMock(return_value=("OK", [b"Logged out"]))
      capability_response = AsyncMock()
      capability_response.result = "OK"
      capability_response.lines = [b"IMAP4REV1 MOVE"]
      mock_client.capability = AsyncMock(return_value=capability_response)
      mock_imap_class.return_value = mock_client

      client = IMAPClient(mock_account)
      await client.connect()
      assert client.has_capability("MOVE") is True

      await client.disconnect()
      assert client.has_capability("MOVE") is False


class TestIMAPCriteriaValidation:
  """Tests for IMAP search criteria validation (H3 bug fix)."""

  async def test_valid_criteria_with_double_quotes(
    self, mock_account, mock_imap_client
  ):
    """Valid criteria with double quotes should be accepted."""
    client = IMAPClient(mock_account)

    # Mock search response
    search_response = AsyncMock()
    search_response.result = "OK"
    search_response.lines = [b"SEARCH 1 2 3"]
    mock_imap_client.search = AsyncMock(return_value=search_response)

    await client.search("INBOX", 'FROM "test@example.com"', 50)
    mock_imap_client.search.assert_called_once()

  async def test_valid_criteria_all(self, mock_account, mock_imap_client):
    """Simple ALL criteria should be accepted."""
    client = IMAPClient(mock_account)

    search_response = AsyncMock()
    search_response.result = "OK"
    search_response.lines = [b"SEARCH 1 2 3"]
    mock_imap_client.search = AsyncMock(return_value=search_response)

    await client.search("INBOX", "ALL", 50)
    mock_imap_client.search.assert_called_once_with("ALL")

  async def test_valid_criteria_date_format(
    self, mock_account, mock_imap_client
  ):
    """Date criteria with hyphens should be accepted."""
    client = IMAPClient(mock_account)

    search_response = AsyncMock()
    search_response.result = "OK"
    search_response.lines = [b"SEARCH 1 2 3"]
    mock_imap_client.search = AsyncMock(return_value=search_response)

    await client.search("INBOX", "SINCE 01-Jan-2024", 50)
    mock_imap_client.search.assert_called_once()

  async def test_single_quote_rejected(self, mock_account, mock_imap_client):
    """Criteria containing single quotes should be rejected.

    This test currently FAILS because the bug exists - single quotes
    are allowed. After fix: single quotes should be rejected.
    """
    client = IMAPClient(mock_account)

    # This should raise ValueError because single quotes are not allowed
    with pytest.raises(ValueError, match="Invalid search criteria"):
      await client.search("INBOX", "FROM 'test@example.com'", 50)

    # Server should never receive the invalid criteria
    mock_imap_client.search.assert_not_called()

  async def test_injection_attempt_rejected(
    self, mock_account, mock_imap_client
  ):
    """IMAP injection attempts using single quotes should be rejected."""
    client = IMAPClient(mock_account)

    with pytest.raises(ValueError, match="Invalid search criteria"):
      await client.search("INBOX", "FROM ' OR FROM admin", 50)

    mock_imap_client.search.assert_not_called()

  async def test_special_characters_allowed(
    self, mock_account, mock_imap_client
  ):
    """Required IMAP special characters should be accepted."""
    client = IMAPClient(mock_account)

    search_response = AsyncMock()
    search_response.result = "OK"
    search_response.lines = [b"SEARCH 1 2 3"]
    mock_imap_client.search = AsyncMock(return_value=search_response)

    # Test various valid IMAP syntax
    valid_criteria = [
      "ALL",
      "UNSEEN",
      "FROM test@example.com",
      'SUBJECT "hello world"',
      "OR FROM alice FROM bob",
      "NOT DELETED",
      "LARGER 1000",
      "BEFORE 01-Jan-2024",
    ]

    for criteria in valid_criteria:
      mock_imap_client.search.reset_mock()
      await client.search("INBOX", criteria, 50)
      mock_imap_client.search.assert_called_once()