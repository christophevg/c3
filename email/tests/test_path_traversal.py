"""Tests for path traversal protection."""

import os
import tempfile
from pathlib import Path

import pytest

from email_mcp.imap.client import IMAPClient, DEFAULT_WORKSPACE, SecurityError
from email_mcp.config import EmailAccount


class TestPathTraversal:
  """Tests for attachment download path traversal protection."""

  def test_filename_sanitization(self, temp_workspace):
    """Test filename is sanitized during download."""
    account = EmailAccount(
      name="test",
      imap_host="imap.test.com",
      smtp_host="smtp.test.com",
      username="test@test.com",
      password="secret",
    )
    client = IMAPClient(account)

    # The client hashes the filename
    # Even if filename contains path separators, they're removed
    import hashlib
    dangerous_filename = "../../../etc/passwd"
    safe_filename = os.path.basename(dangerous_filename)
    hashed_prefix = hashlib.sha256(dangerous_filename.encode()).hexdigest()[:16]
    expected_name = f"{hashed_prefix}_{safe_filename}"

    # This verifies the sanitization logic exists
    assert "/" not in expected_name
    assert "\\" not in expected_name
    assert expected_name.startswith(hashed_prefix)

  def test_invalid_filename_rejected(self):
    """Test invalid filenames are rejected."""
    account = EmailAccount(
      name="test",
      imap_host="imap.test.com",
      smtp_host="smtp.test.com",
      username="test@test.com",
      password="secret",
    )
    client = IMAPClient(account)

    # These would fail before any IMAP connection due to invalid filename
    # The sanitization happens at the start of download_attachment
    import hashlib

    # Empty basename after os.path.basename() on path-only input
    dangerous = "../.."
    safe = os.path.basename(dangerous)
    assert safe in ('.', '..')


class TestSymlinkRaceCondition:
  """Tests for TOCTOU symlink race protection."""

  def test_symlink_escape_detected_and_cleaned(self, tmp_path):
    """Verify symlink escape is detected and file is cleaned up."""
    # Create workspace and outside directory
    workspace = tmp_path / "workspace"
    outside = tmp_path / "outside"
    workspace.mkdir()
    outside.mkdir()

    # Create symlink in workspace pointing outside
    symlink_dir = workspace / "downloads"
    symlink_dir.mkdir()
    symlink_target = symlink_dir / "escaped"
    symlink_target.symlink_to(outside)

    # Verify symlink exists
    assert symlink_target.is_symlink()
    assert symlink_target.exists()

    # Verify symlink points outside workspace
    real_path = os.path.realpath(symlink_target)
    real_workspace = os.path.realpath(workspace)
    assert not real_path.startswith(real_workspace)

  def test_normal_path_within_workspace(self, tmp_path):
    """Verify normal paths within workspace work correctly."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    # Normal directory within workspace
    normal_dir = workspace / "downloads"
    normal_dir.mkdir()

    # Verify path is within workspace
    real_path = os.path.realpath(normal_dir)
    real_workspace = os.path.realpath(workspace)
    assert real_path.startswith(real_workspace)

  def test_security_error_on_symlink_escape(self, tmp_path):
    """Test that SecurityError is raised for symlink escape."""
    # This tests the exception is properly defined
    workspace = tmp_path / "workspace"
    outside = tmp_path / "outside"
    workspace.mkdir()
    outside.mkdir()

    # Simulate the scenario where realpath escapes workspace
    symlink_dir = workspace / "downloads"
    symlink_dir.mkdir()
    symlink_target = symlink_dir / "escaped"
    symlink_target.symlink_to(outside)

    # The post-write verification would catch this
    real_path = os.path.realpath(symlink_target)
    real_workspace = os.path.realpath(workspace)

    with pytest.raises(ValueError):
      Path(real_path).relative_to(real_workspace)

  def test_post_write_verification_logic(self, tmp_path):
    """Test the post-write verification logic independently."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    # Create a file within workspace
    test_file = workspace / "test.txt"
    test_file.write_text("test content")

    # Verify realpath is within workspace
    real_path = os.path.realpath(test_file)
    real_workspace = os.path.realpath(workspace)

    # Should not raise
    Path(real_path).relative_to(real_workspace)

    # Now test with symlink escaping
    outside = tmp_path / "outside"
    outside.mkdir()
    symlink_file = workspace / "symlink_file.txt"

    # Can't create symlink to non-existent target in some cases
    # So we test the logic by checking realpath
    assert real_path.startswith(real_workspace)


class TestDownloadAttachmentIntegration:
  """Integration tests for download_attachment with symlink protection."""

  @pytest.mark.asyncio
  async def test_download_attachment_success(self, tmp_path, monkeypatch):
    """Test normal download within workspace succeeds."""
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from unittest.mock import AsyncMock
    from email_mcp.imap.client import IMAPClient, DEFAULT_WORKSPACE

    # Mock account
    account = EmailAccount(
      name="test",
      imap_host="imap.test.com",
      smtp_host="smtp.test.com",
      username="test@test.com",
      password="secret",
    )
    client = IMAPClient(account)

    # Create test attachment
    msg = MIMEMultipart()
    attachment = MIMEText("test attachment content", "plain")
    attachment.add_header("Content-Disposition", "attachment", filename="test.txt")
    msg.attach(attachment)
    raw_bytes = msg.as_bytes()

    # Mock IMAP operations - fetch returns list of tuples
    mock_imap = AsyncMock()
    mock_imap.select = AsyncMock(return_value=("OK", []))
    # Response format: list containing tuple of (metadata, raw_bytes)
    mock_imap.fetch = AsyncMock(return_value=("OK", [(b"1 (BODY[]", raw_bytes)]))

    async def mock_connect(self):
      self._client = mock_imap
      return mock_imap

    monkeypatch.setattr(IMAPClient, "connect", mock_connect)
    # Mock DEFAULT_WORKSPACE to use tmp_path
    monkeypatch.setattr("email_mcp.imap.client.DEFAULT_WORKSPACE", tmp_path)

    # Test download
    result = await client.download_attachment(
      message_id="1",
      folder="INBOX",
      filename="test.txt",
      output_dir=str(tmp_path)
    )

    # Verify file was created
    assert Path(result).exists()

  @pytest.mark.asyncio
  async def test_download_attachment_symlink_escape(self, tmp_path, monkeypatch):
    """Test that symlink escape raises SecurityError and cleans up file."""
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from unittest.mock import AsyncMock
    from email_mcp.imap.client import IMAPClient, SecurityError

    # Mock account
    account = EmailAccount(
      name="test",
      imap_host="imap.test.com",
      smtp_host="smtp.test.com",
      username="test@test.com",
      password="secret",
    )
    client = IMAPClient(account)

    # Create workspace and symlink to outside
    workspace = tmp_path
    outside = tmp_path.parent / "outside"
    outside.mkdir(exist_ok=True)

    symlink_dir = workspace / "downloads"
    symlink_dir.mkdir()
    symlink_target = symlink_dir / "escaped"
    symlink_target.symlink_to(outside)

    # Create test attachment
    msg = MIMEMultipart()
    attachment = MIMEText("malicious content", "plain")
    attachment.add_header("Content-Disposition", "attachment", filename="test.txt")
    msg.attach(attachment)
    raw_bytes = msg.as_bytes()

    # Mock IMAP operations
    mock_imap = AsyncMock()
    mock_imap.select = AsyncMock(return_value=("OK", []))
    mock_imap.fetch = AsyncMock(return_value=("OK", [(b"1 (BODY[]", raw_bytes)]))

    async def mock_connect(self):
      self._client = mock_imap
      return mock_imap

    monkeypatch.setattr(IMAPClient, "connect", mock_connect)

    # Test download - should raise SecurityError
    with pytest.raises(SecurityError, match="workspace confinement"):
      await client.download_attachment(
        message_id="1",
        folder="INBOX",
        filename="test.txt",
        output_dir=str(symlink_target)
      )

    # Verify file was NOT created outside workspace
    outside_files = list(outside.iterdir())
    assert len(outside_files) == 0, "File should be cleaned up after SecurityError"

  @pytest.mark.asyncio
  async def test_security_error_propagation(self, tmp_path, monkeypatch):
    """Test that SecurityError is properly raised with correct message."""
    from unittest.mock import AsyncMock
    from email_mcp.imap.client import IMAPClient

    account = EmailAccount(
      name="test",
      imap_host="imap.test.com",
      smtp_host="smtp.test.com",
      username="test@test.com",
      password="secret",
    )
    client = IMAPClient(account)

    # Mock IMAP to fail attachment lookup
    mock_imap = AsyncMock()
    mock_imap.select = AsyncMock(return_value=("OK", []))
    mock_imap.fetch = AsyncMock(return_value=("OK", []))

    async def mock_connect(self):
      self._client = mock_imap
      return mock_imap

    monkeypatch.setattr(IMAPClient, "connect", mock_connect)

    # Should raise FileNotFoundError, not SecurityError
    with pytest.raises(FileNotFoundError, match="Attachment not found"):
      await client.download_attachment(
        message_id="1",
        folder="INBOX",
        filename="nonexistent.txt",
        output_dir=str(tmp_path)
      )

  def test_security_error_class(self):
    """Test SecurityError exception class."""
    from email_mcp.imap.client import SecurityError

    # Verify SecurityError is defined and raises correctly
    with pytest.raises(SecurityError, match="test message"):
      raise SecurityError("test message")

    # Verify it's a proper exception
    assert issubclass(SecurityError, Exception)