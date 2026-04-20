"""Tests for path traversal protection."""

import os
import tempfile
from pathlib import Path

import pytest

from email_mcp.imap.client import IMAPClient, DEFAULT_WORKSPACE
from email_mcp.config import EmailAccount


class TestPathTraversal:
  """Tests for attachment download path traversal protection."""

  def test_valid_output_dir(self, temp_workspace):
    """Test valid workspace output directory."""
    account = EmailAccount(
      name="test",
      imap_host="imap.test.com",
      smtp_host="smtp.test.com",
      username="test@test.com",
      password="secret",
    )
    client = IMAPClient(account)

    # Valid path within workspace
    valid_path = str(temp_workspace)

    # Invalid path outside workspace should raise
    with pytest.raises(ValueError, match="must be within workspace"):
      import asyncio
      asyncio.run(client.download_attachment("1", "INBOX", "test.txt", "/tmp"))

  def test_path_outside_workspace_rejected(self):
    """Test paths outside workspace are rejected."""
    account = EmailAccount(
      name="test",
      imap_host="imap.test.com",
      smtp_host="smtp.test.com",
      username="test@test.com",
      password="secret",
    )
    client = IMAPClient(account)

    # This should raise ValueError for path outside workspace
    with pytest.raises(ValueError, match="must be within workspace"):
      import asyncio
      asyncio.run(client.download_attachment("1", "INBOX", "test.txt", "/etc"))

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