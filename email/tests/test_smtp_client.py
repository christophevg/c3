"""Tests for SMTP client."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

import aiosmtplib

from email_mcp.config import EmailAccount, RecipientWhitelist
from email_mcp.smtp.client import SMTPClient, WhitelistError


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
def mock_whitelist_enabled():
  """Create a whitelist that blocks external.com domain."""
  return RecipientWhitelist(
    enabled=True,
    domains=["test.com"],
    addresses=[],
  )


class TestReplyEmailWhitelist:
  """Tests that reply_email enforces whitelist (C3 bug fix)."""

  async def test_reply_email_bypasses_whitelist(self, mock_account, mock_whitelist_enabled):
    """BUG: reply_email() sends to blocked recipient without raising WhitelistError."""
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.get_recipient_whitelist", return_value=mock_whitelist_enabled):
      with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
        mock_send.return_value = (None, "OK")

        # This should raise WhitelistError because attacker@external.com is blocked
        with pytest.raises(WhitelistError) as exc_info:
          await client.reply_email(
            to="attacker@external.com",
            subject="Re: Test",
            body="Reply body",
            in_reply_to="msg@123",
          )

        assert "not in whitelist" in str(exc_info.value)
        # aiosmtplib.send should NOT have been called
        mock_send.assert_not_called()

  async def test_reply_email_allows_whitelisted(self, mock_account, mock_whitelist_enabled):
    """reply_email should succeed for whitelisted recipient."""
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.get_recipient_whitelist", return_value=mock_whitelist_enabled):
      with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
        mock_send.return_value = (None, "OK")

        result = await client.reply_email(
          to="user@test.com",
          subject="Re: Test",
          body="Reply body",
          in_reply_to="msg@123",
        )

        assert result["status"] == "sent"
        mock_send.assert_called_once()

  async def test_reply_email_disabled_whitelist_allows_all(self, mock_account):
    """reply_email should allow any recipient when whitelist is disabled."""
    disabled_whitelist = RecipientWhitelist(enabled=False, domains=[], addresses=[])
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.get_recipient_whitelist", return_value=disabled_whitelist):
      with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
        mock_send.return_value = (None, "OK")

        result = await client.reply_email(
          to="anyone@external.com",
          subject="Re: Test",
          body="Reply body",
          in_reply_to="msg@123",
        )

        assert result["status"] == "sent"
        mock_send.assert_called_once()


class TestReplyEmailValidation:
  """Tests that reply_email validates email format."""

  async def test_reply_email_invalid_address(self, mock_account):
    """reply_email should reject invalid email addresses."""
    client = SMTPClient(mock_account)

    with pytest.raises(ValueError) as exc_info:
      await client.reply_email(
        to="not-an-email",
        subject="Re: Test",
        body="Reply body",
        in_reply_to="msg@123",
      )

    assert "Invalid email address" in str(exc_info.value)

  async def test_reply_email_missing_at_symbol(self, mock_account):
    """reply_email should reject email without @ symbol."""
    client = SMTPClient(mock_account)

    with pytest.raises(ValueError) as exc_info:
      await client.reply_email(
        to="user.example.com",
        subject="Re: Test",
        body="Reply body",
        in_reply_to="msg@123",
      )

    assert "Invalid email address" in str(exc_info.value)


class TestSMTPExceptionChaining:
  """Tests that SMTP exceptions preserve exception chain (C5 bug fix)."""

  async def test_smtp_exception_chain_preserved(self, mock_account):
    """SMTPException should be chained to RuntimeError via 'from'.

    Verifies that exception chain is preserved for debugging while keeping
    user-facing message generic. The __cause__ attribute should contain the
    original SMTPException.
    """
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
      mock_send.side_effect = aiosmtplib.SMTPException("Authentication failed")

      with pytest.raises(RuntimeError) as exc_info:
        await client.send_email(
          to=["user@test.com"],
          subject="Test",
          body="Body",
        )

      # Verify exception chain is preserved via 'from e' syntax
      assert exc_info.value.__cause__ is not None, (
        "Exception chain not preserved - __cause__ is None. "
        "Use 'raise RuntimeError(...) from e' to preserve chain."
      )
      assert isinstance(exc_info.value.__cause__, aiosmtplib.SMTPException)
      assert "Authentication failed" in str(exc_info.value.__cause__)

  async def test_smtp_exception_message_unchanged(self, mock_account):
    """RuntimeError message should remain generic for user-facing output."""
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
      mock_send.side_effect = aiosmtplib.SMTPException("Any error")

      with pytest.raises(RuntimeError) as exc_info:
        await client.send_email(
          to=["user@test.com"],
          subject="Test",
          body="Body",
        )

      # The user-facing message should be generic
      assert "Failed to send email" in str(exc_info.value)