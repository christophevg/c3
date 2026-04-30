"""Tests for header sanitization functions (H4 - CRLF injection protection).

These tests verify that header values are properly sanitized to prevent
CRLF injection attacks in SMTP email operations.
"""

from __future__ import annotations

import pytest

from email_mcp.safety.sanitize import (
  sanitize_header_value,
  sanitize_message_id,
  sanitize_references,
  sanitize_subject,
)


class TestSanitizeMessageID:
  """Tests for sanitize_message_id() function.

  The function should validate and sanitize Message-ID headers to prevent
  CRLF injection attacks. Message-IDs must conform to RFC 5322 format:
  angle-bracketed email-like strings (<id@domain>).
  """

  def test_valid_message_id_accepted(self):
    """
    Given: A valid angle-bracketed Message-ID
    When: sanitize_message_id() is called
    Then: The Message-ID is returned unchanged
    """
    result = sanitize_message_id("<abc123@mail.example.com>")
    assert result == "<abc123@mail.example.com>"

  def test_valid_complex_message_id_accepted(self):
    """
    Given: A valid Message-ID with multiple parts
    When: sanitize_message_id() is called
    Then: The Message-ID is returned unchanged
    """
    result = sanitize_message_id("<message-id-with-dashes.123@example.domain.org>")
    assert result == "<message-id-with-dashes.123@example.domain.org>"

  def test_rejects_cr_injection_in_message_id(self):
    """
    Given: A Message-ID containing carriage return character
    When: sanitize_message_id() is called
    Then: ValueError is raised with message about newline characters
    """
    with pytest.raises(ValueError, match="newline"):
      sanitize_message_id("<valid@id.com>\r\nBcc: attacker@evil.com")

  def test_rejects_lf_injection_in_message_id(self):
    """
    Given: A Message-ID containing line feed character
    When: sanitize_message_id() is called
    Then: ValueError is raised with message about newline characters
    """
    with pytest.raises(ValueError, match="newline"):
      sanitize_message_id("<valid@id.com>\nX-Injected: evil")

  def test_rejects_crlf_injection_in_message_id(self):
    """
    Given: A Message-ID containing CRLF sequence
    When: sanitize_message_id() is called
    Then: ValueError is raised with message about newline characters
    """
    with pytest.raises(ValueError, match="newline"):
      sanitize_message_id("<valid@id.com>\r\n\r\nInjected body")

  def test_rejects_unbracketed_message_id(self):
    """
    Given: A Message-ID without angle brackets
    When: sanitize_message_id() is called
    Then: ValueError is raised indicating Message-ID must be angle-bracketed
    """
    with pytest.raises(ValueError, match="angle-bracketed"):
      sanitize_message_id("plain@id.com")

  def test_rejects_message_id_missing_opening_bracket(self):
    """
    Given: A Message-ID missing opening angle bracket
    When: sanitize_message_id() is called
    Then: ValueError is raised indicating Message-ID must be angle-bracketed
    """
    with pytest.raises(ValueError, match="angle-bracketed"):
      sanitize_message_id("plain@id.com>")

  def test_rejects_message_id_missing_closing_bracket(self):
    """
    Given: A Message-ID missing closing angle bracket
    When: sanitize_message_id() is called
    Then: ValueError is raised indicating Message-ID must be angle-bracketed
    """
    with pytest.raises(ValueError, match="angle-bracketed"):
      sanitize_message_id("<plain@id.com")

  def test_rejects_embedded_angle_brackets(self):
    """
    Given: A Message-ID with embedded angle brackets
    When: sanitize_message_id() is called
    Then: ValueError is raised indicating invalid characters
    """
    with pytest.raises(ValueError, match="invalid characters"):
      sanitize_message_id("<a<b>@domain.com>")

  def test_rejects_empty_message_id(self):
    """
    Given: An empty string as Message-ID
    When: sanitize_message_id() is called
    Then: ValueError is raised indicating invalid format
    """
    with pytest.raises(ValueError, match="empty"):
      sanitize_message_id("")

  def test_rejects_message_id_with_only_brackets(self):
    """
    Given: A Message-ID that is only angle brackets '<>'
    When: sanitize_message_id() is called
    Then: ValueError is raised indicating invalid format
    """
    with pytest.raises(ValueError, match="empty content"):
      sanitize_message_id("<>")


class TestSanitizeReferences:
  """Tests for sanitize_references() function.

  The function should validate and sanitize a list of Message-ID references
  to prevent CRLF injection attacks in the References header.
  """

  def test_valid_references_list_accepted(self):
    """
    Given: A list of valid Message-IDs
    When: sanitize_references() is called
    Then: The list is returned unchanged
    """
    refs = ["<msg1@id.com>", "<msg2@id.com>"]
    result = sanitize_references(refs)
    assert result == refs

  def test_empty_references_list_accepted(self):
    """
    Given: An empty list of references
    When: sanitize_references() is called
    Then: An empty list is returned
    """
    result = sanitize_references([])
    assert result == []

  def test_rejects_invalid_reference_in_list(self):
    """
    Given: A list containing one invalid Message-ID (unbracketed, no CRLF)
    When: sanitize_references() is called
    Then: ValueError is raised for the invalid Message-ID
    """
    refs = ["<msg1@id.com>", "invalid@id.com"]  # Unbracketed, no CRLF
    with pytest.raises(ValueError, match="angle-bracketed"):
      sanitize_references(refs)

  def test_rejects_crlf_injection_in_reference(self):
    """
    Given: A list with a Message-ID containing CRLF
    When: sanitize_references() is called
    Then: ValueError is raised with message about newline characters
    """
    refs = ["<msg1@id.com>", "<msg2@id.com>\r\nBcc: evil"]
    with pytest.raises(ValueError, match="newline"):
      sanitize_references(refs)

  def test_all_references_validated(self):
    """
    Given: A list with multiple Message-IDs, one invalid
    When: sanitize_references() is called
    Then: ValueError is raised for the first invalid Message-ID
    """
    refs = ["<valid@id.com>", "<also@valid.com>", "not-bracketed@id.com"]
    with pytest.raises(ValueError, match="angle-bracketed"):
      sanitize_references(refs)


class TestSanitizeHeaderValue:
  """Tests for generic header value sanitization.

  This function should remove CRLF sequences from arbitrary header values
  to prevent header injection attacks.
  """

  def test_removes_cr_from_header(self):
    """
    Given: A header value containing carriage return
    When: sanitize_header_value() is called
    Then: CR character is removed
    """
    result = sanitize_header_value("Test\rValue")
    assert result == "TestValue"

  def test_removes_lf_from_header(self):
    """
    Given: A header value containing line feed
    When: sanitize_header_value() is called
    Then: LF character is removed
    """
    result = sanitize_header_value("Test\nValue")
    assert result == "TestValue"

  def test_removes_crlf_from_header(self):
    """
    Given: A header value containing CRLF sequence
    When: sanitize_header_value() is called
    Then: CRLF is removed
    """
    result = sanitize_header_value("Test\r\nInjected: evil")
    assert result == "TestInjected: evil"

  def test_preserves_valid_header(self):
    """
    Given: A header value without special characters
    When: sanitize_header_value() is called
    Then: The value is returned unchanged
    """
    result = sanitize_header_value("Normal Header Value")
    assert result == "Normal Header Value"

  def test_rejects_empty_header(self):
    """
    Given: An empty string as header value
    When: sanitize_header_value() is called
    Then: ValueError is raised
    """
    with pytest.raises(ValueError, match="empty"):
      sanitize_header_value("")

  def test_rejects_whitespace_only_header(self):
    """
    Given: A header value with only CRLF characters
    When: sanitize_header_value() is called
    Then: ValueError is raised
    """
    with pytest.raises(ValueError, match="only invalid characters"):
      sanitize_header_value("\r\n\r\n")


class TestSanitizeSubject:
  """Tests for subject line sanitization.

  The subject parameter in send_email() should be sanitized to prevent
  CRLF injection attacks through the Subject header.
  """

  def test_removes_cr_from_subject(self):
    """
    Given: A subject containing carriage return
    When: sanitize_subject() is called
    Then: CR is replaced with space
    """
    result = sanitize_subject("Test\rSubject")
    assert "\r" not in result
    assert "Test Subject" == result

  def test_removes_lf_from_subject(self):
    """
    Given: A subject containing line feed
    When: sanitize_subject() is called
    Then: LF is replaced with space
    """
    result = sanitize_subject("Test\nSubject")
    assert "\n" not in result
    assert "Test Subject" == result

  def test_removes_crlf_injection_from_subject(self):
    """
    Given: A subject with CRLF followed by injected header
    When: sanitize_subject() is called
    Then: CRLF is replaced with space, injection prevented
    """
    result = sanitize_subject("Test\r\nBcc: attacker@evil.com")
    assert "\r" not in result
    assert "\n" not in result
    assert "Test Bcc: attacker@evil.com" == result

  def test_preserves_valid_subject(self):
    """
    Given: A normal subject line
    When: sanitize_subject() is called
    Then: Subject is returned unchanged
    """
    result = sanitize_subject("Normal Subject Line")
    assert result == "Normal Subject Line"

  def test_handles_multibyte_characters_in_subject(self):
    """
    Given: A subject with multibyte/unicode characters
    When: sanitize_subject() is called
    Then: Unicode characters are preserved, CRLF removed
    """
    result = sanitize_subject("Test 中文 Subject\r\nInjected")
    assert "中文" in result  # Chinese characters preserved
    assert "\r" not in result
    assert "\n" not in result

  def test_rejects_empty_subject(self):
    """
    Given: An empty string as subject
    When: sanitize_subject() is called
    Then: ValueError is raised
    """
    with pytest.raises(ValueError, match="empty"):
      sanitize_subject("")

  def test_collapses_multiple_spaces(self):
    """
    Given: A subject with multiple CRLF sequences creating multiple spaces
    When: sanitize_subject() is called
    Then: Multiple spaces are collapsed to single spaces
    """
    result = sanitize_subject("Test\r\n\r\nSubject")
    assert result == "Test Subject"