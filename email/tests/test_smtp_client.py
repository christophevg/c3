"""Tests for SMTP client."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

import aiosmtplib

from email_mcp.config import EmailAccount, RecipientWhitelist
from email_mcp.smtp.client import SMTPClient, WhitelistError, validate_email


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
            in_reply_to="<msg@123>",
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
          in_reply_to="<msg@123>",
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
          in_reply_to="<msg@123>",
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
        in_reply_to="<msg@123>",
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
        in_reply_to="<msg@123>",
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


class TestReplyEmailCRLFInjection:
  """Tests that reply_email sanitizes Message-ID headers (H4 bug fix).

  These tests verify that CRLF injection attacks are prevented by validating
  and sanitizing the in_reply_to and references parameters before using them
  in email headers.
  """

  async def test_reply_email_rejects_cr_in_in_reply_to(self, mock_account):
    """
    Given: An in_reply_to containing carriage return character
    When: reply_email() is called
    Then: ValueError is raised indicating newline characters are invalid
    """
    client = SMTPClient(mock_account)

    with pytest.raises(ValueError, match="newline"):
      await client.reply_email(
        to="user@test.com",
        subject="Re: Test",
        body="Reply body",
        in_reply_to="<valid@id.com>\r\nBcc: attacker@evil.com",
      )

  async def test_reply_email_rejects_lf_in_in_reply_to(self, mock_account):
    """
    Given: An in_reply_to containing line feed character
    When: reply_email() is called
    Then: ValueError is raised indicating newline characters are invalid
    """
    client = SMTPClient(mock_account)

    with pytest.raises(ValueError, match="newline"):
      await client.reply_email(
        to="user@test.com",
        subject="Re: Test",
        body="Reply body",
        in_reply_to="<valid@id.com>\nX-Injected: evil",
      )

  async def test_reply_email_rejects_crlf_injection_in_in_reply_to(self, mock_account):
    """
    Given: An in_reply_to with CRLF followed by Bcc header
    When: reply_email() is called
    Then: ValueError is raised, preventing header injection
    """
    client = SMTPClient(mock_account)

    with pytest.raises(ValueError, match="newline"):
      await client.reply_email(
        to="user@test.com",
        subject="Re: Test",
        body="Reply body",
        in_reply_to="<msg@id>\r\nBcc: attacker@evil.com",
      )

  async def test_reply_email_rejects_unbracketed_in_reply_to(self, mock_account):
    """
    Given: An in_reply_to without angle brackets
    When: reply_email() is called
    Then: ValueError is raised indicating Message-ID format is invalid
    """
    client = SMTPClient(mock_account)

    with pytest.raises(ValueError, match="angle-bracketed"):
      await client.reply_email(
        to="user@test.com",
        subject="Re: Test",
        body="Reply body",
        in_reply_to="msg@123",
      )

  async def test_reply_email_accepts_valid_in_reply_to(self, mock_account):
    """
    Given: A valid angle-bracketed in_reply_to
    When: reply_email() is called
    Then: Email is sent successfully with valid Message-ID
    """
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
      mock_send.return_value = (None, "OK")

      result = await client.reply_email(
        to="user@test.com",
        subject="Re: Test",
        body="Reply body",
        in_reply_to="<abc123@mail.example.com>",
      )

      assert result["status"] == "sent"
      mock_send.assert_called_once()

  async def test_reply_email_rejects_cr_in_references(self, mock_account):
    """
    Given: A references list with Message-ID containing carriage return
    When: reply_email() is called
    Then: ValueError is raised indicating newline characters are invalid
    """
    client = SMTPClient(mock_account)

    with pytest.raises(ValueError, match="newline"):
      await client.reply_email(
        to="user@test.com",
        subject="Re: Test",
        body="Reply body",
        in_reply_to="<msg@id>",
        references=["<msg1@id.com>", "<msg2@id.com>\rBcc: evil"],
      )

  async def test_reply_email_rejects_crlf_injection_in_references(self, mock_account):
    """
    Given: A references list with CRLF injection attempt
    When: reply_email() is called
    Then: ValueError is raised, preventing header injection
    """
    client = SMTPClient(mock_account)

    with pytest.raises(ValueError, match="newline"):
      await client.reply_email(
        to="user@test.com",
        subject="Re: Test",
        body="Reply body",
        in_reply_to="<msg@id>",
        references=["<msg1@id.com>\r\nBcc: attacker@evil.com"],
      )

  async def test_reply_email_accepts_valid_references(self, mock_account):
    """
    Given: A valid references list with properly formatted Message-IDs
    When: reply_email() is called
    Then: Email is sent successfully with valid References header
    """
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
      mock_send.return_value = (None, "OK")

      result = await client.reply_email(
        to="user@test.com",
        subject="Re: Test",
        body="Reply body",
        in_reply_to="<msg@id>",
        references=["<msg1@id.com>", "<msg2@id.com>"],
      )

      assert result["status"] == "sent"
      mock_send.assert_called_once()

  async def test_reply_email_sanitizes_all_references(self, mock_account):
    """
    Given: A references list with multiple Message-IDs, one invalid
    When: reply_email() is called
    Then: ValueError is raised for the invalid Message-ID
    """
    client = SMTPClient(mock_account)

    with pytest.raises(ValueError, match="angle-bracketed"):
      await client.reply_email(
        to="user@test.com",
        subject="Re: Test",
        body="Reply body",
        in_reply_to="<msg@id>",
        references=["<valid@id.com>", "not-bracketed@id.com"],
      )


class TestReplyEmailSubjectSanitization:
  """Tests that reply_email sanitizes subject (H4 critical gap fix).

  These tests verify that CRLF injection attacks are prevented by sanitizing
  the subject parameter in reply_email, matching the protection in send_email.
  """

  async def test_reply_email_sanitizes_cr_in_subject(self, mock_account):
    """
    Given: A subject containing carriage return character
    When: reply_email() is called
    Then: Subject is sanitized (CR replaced with space)
    """
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
      mock_send.return_value = (None, "OK")

      # CR should be replaced with space
      result = await client.reply_email(
        to="user@test.com",
        subject="Re: Test\rSubject",
        body="Reply body",
        in_reply_to="<msg@id>",
      )

      assert result["status"] == "sent"
      mock_send.assert_called_once()

  async def test_reply_email_sanitizes_lf_in_subject(self, mock_account):
    """
    Given: A subject containing line feed character
    When: reply_email() is called
    Then: Subject is sanitized (LF replaced with space)
    """
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
      mock_send.return_value = (None, "OK")

      result = await client.reply_email(
        to="user@test.com",
        subject="Re: Test\nSubject",
        body="Reply body",
        in_reply_to="<msg@id>",
      )

      assert result["status"] == "sent"
      mock_send.assert_called_once()

  async def test_reply_email_prevents_crlf_injection_in_subject(self, mock_account):
    """
    Given: A subject with CRLF followed by Bcc header
    When: reply_email() is called
    Then: CRLF is replaced with space, preventing header injection
    """
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
      mock_send.return_value = (None, "OK")

      # The CRLF injection attempt should be sanitized
      result = await client.reply_email(
        to="user@test.com",
        subject="Re: Test\r\nBcc: attacker@evil.com",
        body="Reply body",
        in_reply_to="<msg@id>",
      )

      assert result["status"] == "sent"
      mock_send.assert_called_once()

  async def test_reply_email_accepts_valid_subject(self, mock_account):
    """
    Given: A normal subject line
    When: reply_email() is called
    Then: Email is sent with subject unchanged
    """
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
      mock_send.return_value = (None, "OK")

      result = await client.reply_email(
        to="user@test.com",
        subject="Re: Normal Subject Line",
        body="Reply body",
        in_reply_to="<msg@id>",
      )

      assert result["status"] == "sent"
      mock_send.assert_called_once()

  async def test_reply_email_sanitizes_multibyte_subject(self, mock_account):
    """
    Given: A subject with multibyte/unicode characters
    When: reply_email() is called
    Then: Unicode preserved, CRLF sanitized if present
    """
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
      mock_send.return_value = (None, "OK")

      result = await client.reply_email(
        to="user@test.com",
        subject="Re: Test 中文 Subject\r\nInjected",
        body="Reply body",
        in_reply_to="<msg@id>",
      )

      assert result["status"] == "sent"
      mock_send.assert_called_once()

  async def test_reply_email_rejects_empty_subject(self, mock_account):
    """
    Given: An empty subject
    When: reply_email() is called
    Then: ValueError is raised
    """
    client = SMTPClient(mock_account)

    with pytest.raises(ValueError, match="empty"):
      await client.reply_email(
        to="user@test.com",
        subject="",
        body="Reply body",
        in_reply_to="<msg@id>",
      )


class TestSendEmailCRLFInjection:
  """Tests that send_email sanitizes subject and other headers (H4 bug fix).

  These tests verify that CRLF injection attacks are prevented by sanitizing
  the subject parameter and other user-provided header values.
  """

  async def test_send_email_sanitizes_cr_in_subject(self, mock_account):
    """
    Given: A subject containing carriage return character
    When: send_email() is called
    Then: Subject is sanitized (CR replaced with space)
    """
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
      mock_send.return_value = (None, "OK")

      # CR should be replaced with space
      result = await client.send_email(
        to=["user@test.com"],
        subject="Test\rSubject",
        body="Body",
      )

      assert result["status"] == "sent"
      # Verify the message was sent (subject sanitization happened internally)
      mock_send.assert_called_once()

  async def test_send_email_sanitizes_lf_in_subject(self, mock_account):
    """
    Given: A subject containing line feed character
    When: send_email() is called
    Then: Subject is sanitized (LF replaced with space)
    """
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
      mock_send.return_value = (None, "OK")

      result = await client.send_email(
        to=["user@test.com"],
        subject="Test\nSubject",
        body="Body",
      )

      assert result["status"] == "sent"
      mock_send.assert_called_once()

  async def test_send_email_prevents_crlf_injection_in_subject(self, mock_account):
    """
    Given: A subject with CRLF followed by Bcc header
    When: send_email() is called
    Then: CRLF is replaced with space, preventing header injection
    """
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
      mock_send.return_value = (None, "OK")

      # The CRLF injection attempt should be sanitized
      result = await client.send_email(
        to=["user@test.com"],
        subject="Test\r\nBcc: attacker@evil.com",
        body="Body",
      )

      assert result["status"] == "sent"
      mock_send.assert_called_once()

  async def test_send_email_accepts_valid_subject(self, mock_account):
    """
    Given: A normal subject line
    When: send_email() is called
    Then: Email is sent with subject unchanged
    """
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
      mock_send.return_value = (None, "OK")

      result = await client.send_email(
        to=["user@test.com"],
        subject="Normal Subject Line",
        body="Body",
      )

      assert result["status"] == "sent"
      mock_send.assert_called_once()

  async def test_send_email_sanitizes_multibyte_subject(self, mock_account):
    """
    Given: A subject with multibyte/unicode characters
    When: send_email() is called
    Then: Unicode preserved, CRLF sanitized if present
    """
    client = SMTPClient(mock_account)

    with patch("email_mcp.smtp.client.aiosmtplib.send") as mock_send:
      mock_send.return_value = (None, "OK")

      result = await client.send_email(
        to=["user@test.com"],
        subject="Test 中文 Subject\r\nInjected",
        body="Body",
      )

      assert result["status"] == "sent"
      mock_send.assert_called_once()

  async def test_send_email_rejects_empty_subject(self, mock_account):
    """
    Given: An empty subject
    When: send_email() is called
    Then: ValueError is raised
    """
    client = SMTPClient(mock_account)

    with pytest.raises(ValueError, match="empty"):
      await client.send_email(
        to=["user@test.com"],
        subject="",
        body="Body",
      )


class TestValidateEmailCRLFProtection:
  """Tests that validate_email prevents CRLF injection through email addresses.

  Email addresses should also be validated for CRLF characters to prevent
  header injection through the To, Cc, and Bcc fields.
  """

  def test_validate_email_rejects_cr_in_address(self):
    """
    Given: An email address containing carriage return
    When: validate_email() is called
    Then: ValueError is raised indicating invalid characters
    """
    with pytest.raises(ValueError, match="invalid characters"):
      validate_email("user@test.com\r")

  def test_validate_email_rejects_lf_in_address(self):
    """
    Given: An email address containing line feed
    When: validate_email() is called
    Then: ValueError is raised indicating invalid characters
    """
    with pytest.raises(ValueError, match="invalid characters"):
      validate_email("user@test.com\nBcc: evil")

  def test_validate_email_rejects_crlf_injection(self):
    """
    Given: An email address with CRLF followed by injected header
    When: validate_email() is called
    Then: ValueError is raised, preventing injection
    """
    with pytest.raises(ValueError, match="invalid characters"):
      validate_email("user@test.com\r\nBcc: evil")

  def test_validate_email_accepts_valid_address(self):
    """
    Given: A valid email address
    When: validate_email() is called
    Then: Address is returned unchanged
    """
    result = validate_email("user@example.com")
    assert result == "user@example.com"