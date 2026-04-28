"""Tests for email MCP server tool error handling."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastmcp.exceptions import ToolError

from email_mcp import server as server_module
from email_mcp.config import EmailAccount
from email_mcp.connections.pool import RateLimitError


@pytest.fixture
def mock_account():
  """Create a mock email account."""
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
def mock_pool(mock_account):
  """Create a mock connection pool."""
  pool = AsyncMock()
  pool.get_accounts = AsyncMock(return_value=[mock_account])

  # Create mock IMAP client
  imap_client = AsyncMock()
  imap_client.list_folders = AsyncMock()
  imap_client.search = AsyncMock(return_value=["1", "2"])
  imap_client.fetch_message = AsyncMock(return_value={"subject": "Test"})
  imap_client.download_attachment = AsyncMock(return_value="/tmp/test.txt")
  imap_client.move_message = AsyncMock()
  imap_client.delete_message = AsyncMock()
  imap_client.mark_message = AsyncMock()

  # Create mock SMTP client
  smtp_client = AsyncMock()
  smtp_client.send_email = AsyncMock(return_value={"status": "sent"})
  smtp_client.reply_email = AsyncMock(return_value={"status": "sent"})

  pool.get_imap_client = AsyncMock(return_value=imap_client)
  pool.get_smtp_client = AsyncMock(return_value=smtp_client)

  return pool, imap_client, smtp_client


class TestRuntimeErrorMapping:
  """Tests that non-rate-limit RuntimeErrors are NOT reported as rate limits."""

  async def test_imap_auth_failure_not_rate_limit(self, mock_pool):
    """Auth failure RuntimeError should return generic error, not rate limit."""
    pool, imap_client, _ = mock_pool
    imap_client.list_folders = AsyncMock(
      side_effect=RuntimeError("Authentication failed")
    )

    with patch("email_mcp.server.get_pool", return_value=pool):
      with pytest.raises(ToolError) as exc_info:
        await server_module.list_folders(account="test")

    assert "Rate limit" not in str(exc_info.value)
    assert "Failed to list folders" in str(exc_info.value)

  async def test_fetch_message_failure_not_rate_limit(self, mock_pool):
    """Fetch failure RuntimeError should return generic error, not rate limit."""
    pool, imap_client, _ = mock_pool
    imap_client.fetch_message = AsyncMock(
      side_effect=RuntimeError("Failed to fetch message")
    )

    with patch("email_mcp.server.get_pool", return_value=pool):
      with pytest.raises(ToolError) as exc_info:
        await server_module.get_email(account="test", message_id="123")

    assert "Rate limit" not in str(exc_info.value)
    assert "Failed to fetch message" in str(exc_info.value)

  async def test_search_failure_not_rate_limit(self, mock_pool):
    """Search failure RuntimeError should return generic error, not rate limit."""
    pool, imap_client, _ = mock_pool
    imap_client.search = AsyncMock(side_effect=RuntimeError("Search failed"))

    with patch("email_mcp.server.get_pool", return_value=pool):
      with pytest.raises(ToolError) as exc_info:
        await server_module.search_emails(account="test")

    assert "Rate limit" not in str(exc_info.value)
    assert "Failed to search emails" in str(exc_info.value)

  async def test_smtp_send_failure_not_rate_limit(self, mock_pool):
    """SMTP failure RuntimeError should return generic error, not rate limit."""
    pool, _, smtp_client = mock_pool
    smtp_client.send_email = AsyncMock(
      side_effect=RuntimeError("Failed to send email")
    )

    with patch("email_mcp.server.get_pool", return_value=pool):
      with pytest.raises(ToolError) as exc_info:
        await server_module.send_email(
          account="test",
          to=["recipient@test.com"],
          subject="Test",
          body="Test body",
        )

    assert "Rate limit" not in str(exc_info.value)
    assert "Failed to send email" in str(exc_info.value)

  async def test_move_message_failure_not_rate_limit(self, mock_pool):
    """Move failure RuntimeError should return generic error, not rate limit."""
    pool, imap_client, _ = mock_pool
    imap_client.move_message = AsyncMock(
      side_effect=RuntimeError("Failed to copy message")
    )

    with patch("email_mcp.server.get_pool", return_value=pool):
      with pytest.raises(ToolError) as exc_info:
        await server_module.move_email(
          account="test",
          message_id="123",
          source_folder="INBOX",
          dest_folder="Archive",
        )

    assert "Rate limit" not in str(exc_info.value)
    assert "Failed to move message" in str(exc_info.value)

  async def test_delete_message_failure_not_rate_limit(self, mock_pool):
    """Delete failure RuntimeError should return generic error, not rate limit."""
    pool, imap_client, _ = mock_pool
    imap_client.delete_message = AsyncMock(
      side_effect=RuntimeError("Failed to select folder INBOX: NO")
    )

    with patch("email_mcp.server.get_pool", return_value=pool):
      with pytest.raises(ToolError) as exc_info:
        await server_module.delete_email(account="test", message_id="123")

    assert "Rate limit" not in str(exc_info.value)
    assert "Failed to delete message" in str(exc_info.value)

  async def test_mark_read_failure_not_rate_limit(self, mock_pool):
    """Mark read failure RuntimeError should return generic error, not rate limit."""
    pool, imap_client, _ = mock_pool
    imap_client.mark_message = AsyncMock(
      side_effect=RuntimeError("Failed to select folder INBOX: NO")
    )

    with patch("email_mcp.server.get_pool", return_value=pool):
      with pytest.raises(ToolError) as exc_info:
        await server_module.mark_email_read(account="test", message_id="123")

    assert "Rate limit" not in str(exc_info.value)
    assert "Failed to mark message as read" in str(exc_info.value)

  async def test_reply_email_failure_not_rate_limit(self, mock_pool):
    """Reply failure RuntimeError should return generic error, not rate limit."""
    pool, _, smtp_client = mock_pool
    smtp_client.reply_email = AsyncMock(
      side_effect=RuntimeError("Failed to send email")
    )

    with patch("email_mcp.server.get_pool", return_value=pool):
      with pytest.raises(ToolError) as exc_info:
        await server_module.reply_email(
          account="test",
          to="recipient@test.com",
          subject="Re: Test",
          body="Reply body",
          in_reply_to="msg@123",
        )

    assert "Rate limit" not in str(exc_info.value)
    assert "Failed to send reply" in str(exc_info.value)

  async def test_download_attachment_failure_not_rate_limit(self, mock_pool):
    """Download failure RuntimeError should return generic error, not rate limit."""
    pool, imap_client, _ = mock_pool
    imap_client.download_attachment = AsyncMock(
      side_effect=RuntimeError("Failed to fetch message")
    )

    with patch("email_mcp.server.get_pool", return_value=pool):
      with pytest.raises(ToolError) as exc_info:
        await server_module.download_attachment(
          account="test",
          message_id="123",
          filename="test.txt",
          output_dir="/tmp",
        )

    assert "Rate limit" not in str(exc_info.value)
    assert "Failed to download attachment" in str(exc_info.value)


class TestRateLimitError:
  """Tests that actual rate limit errors are correctly reported."""

  async def test_rate_limit_error_from_pool(self, mock_pool):
    """Rate limit errors from connection pool should report correctly."""
    pool, _, _ = mock_pool
    pool.get_imap_client = AsyncMock(
      side_effect=RateLimitError("IMAP rate limit exceeded")
    )

    with patch("email_mcp.server.get_pool", return_value=pool):
      with pytest.raises(ToolError) as exc_info:
        await server_module.list_folders(account="test")

    assert "Rate limit exceeded" in str(exc_info.value)

  async def test_smtp_rate_limit_error_from_pool(self, mock_pool):
    """SMTP rate limit errors from connection pool should report correctly."""
    pool, _, _ = mock_pool

    pool.get_smtp_client = AsyncMock(
      side_effect=RateLimitError("SMTP rate limit exceeded")
    )

    with patch("email_mcp.server.get_pool", return_value=pool):
      with pytest.raises(ToolError) as exc_info:
        await server_module.send_email(
          account="test",
          to=["recipient@test.com"],
          subject="Test",
          body="Test body",
        )

    assert "Rate limit exceeded" in str(exc_info.value)
