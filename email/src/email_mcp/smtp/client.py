"""Async SMTP client using aiosmtplib."""

from __future__ import annotations

import asyncio
import os
import re
import ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import aiosmtplib

from email_mcp.config import EmailAccount, get_recipient_whitelist
from email_mcp.safety.audit import log_email_sent

# Email address validation pattern
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def validate_email(address: str) -> str:
  """Validate email address format."""
  if not EMAIL_PATTERN.match(address):
    raise ValueError(f"Invalid email address: {address}")
  return address


class WhitelistError(Exception):
  """Raised when recipient is not in whitelist."""
  pass


class SMTPClient:
  """Async SMTP client with connection management."""

  def __init__(self, account: EmailAccount) -> None:
    self.account = account
    self._lock = asyncio.Lock()

  async def send_email(
    self,
    to: list[str],
    subject: str,
    body: str,
    cc: list[str] | None = None,
    bcc: list[str] | None = None,
    html_body: str | None = None,
    attachments: list[str] | None = None,
  ) -> dict[str, str]:
    """Send an email message."""
    # Validate email addresses
    for addr in to:
      validate_email(addr)
    if cc:
      for addr in cc:
        validate_email(addr)
    if bcc:
      for addr in bcc:
        validate_email(addr)

    # Check recipient whitelist
    whitelist = get_recipient_whitelist()
    all_recipients = to + (cc or []) + (bcc or [])
    allowed, blocked = whitelist.filter_recipients(all_recipients)

    if blocked:
      raise WhitelistError(
        f"Recipients not in whitelist: {', '.join(blocked)}"
      )

    # Create message
    if html_body or attachments:
      msg = MIMEMultipart("alternative" if html_body else "mixed")
    else:
      msg = EmailMessage()

    msg["From"] = self.account.username
    msg["To"] = ", ".join(to)
    msg["Subject"] = subject

    if cc:
      msg["Cc"] = ", ".join(cc)
    if bcc:
      msg["Bcc"] = ", ".join(bcc)

    if isinstance(msg, EmailMessage):
      msg.set_content(body)
      if html_body:
        msg.add_alternative(html_body, subtype="html")
    else:
      msg.attach(MIMEText(body, "plain"))
      if html_body:
        msg.attach(MIMEText(html_body, "html"))

    # Add attachments
    has_attachments = bool(attachments)
    if attachments:
      await self._add_attachments(msg, attachments)

    # Send
    result = await self._send(msg, to + (cc or []) + (bcc or []))

    # Audit log
    log_email_sent(
      account=self.account.name,
      recipients=to,
      subject=subject,
      has_attachments=has_attachments,
    )

    return result

  async def reply_email(
    self,
    to: str,
    subject: str,
    body: str,
    in_reply_to: str,
    references: list[str] | None = None,
    html_body: str | None = None,
  ) -> dict[str, str]:
    """Send a reply preserving thread context."""
    msg = EmailMessage()

    msg["From"] = self.account.username
    msg["To"] = to
    msg["Subject"] = subject
    msg["In-Reply-To"] = in_reply_to

    if references:
      msg["References"] = " ".join(references)

    msg.set_content(body)
    if html_body:
      msg.add_alternative(html_body, subtype="html")

    return await self._send(msg, [to])

  async def forward_email(
    self,
    to: list[str],
    subject: str,
    original_from: str,
    original_date: str,
    original_body: str,
  ) -> dict[str, str]:
    """Forward an email with original content."""
    forward_body = f"\n\n---------- Forwarded message ----------\nFrom: {original_from}\nDate: {original_date}\n\n{original_body}"

    return await self.send_email(
      to=to,
      subject=f"Fwd: {subject}",
      body=forward_body,
    )

  async def _send(self, msg: EmailMessage, recipients: list[str]) -> dict[str, str]:
    """Send message via SMTP with TLS 1.2 minimum."""
    async with self._lock:
      # Create SSL context with TLS 1.2 minimum
      context = ssl.create_default_context()
      context.minimum_version = ssl.TLSVersion.TLSv1_2

      try:
        # Connect and send
        if self.account.use_starttls:
          # STARTTLS (port 587)
          result = await aiosmtplib.send(
            msg,
            hostname=self.account.smtp_host,
            port=self.account.smtp_port,
            username=self.account.username,
            password=self.account.password.get_secret_value() if self.account.password else None,
            start_tls=True,
            tls_context=context,
          )
        else:
          # Implicit TLS (port 465)
          result = await aiosmtplib.send(
            msg,
            hostname=self.account.smtp_host,
            port=self.account.smtp_port,
            username=self.account.username,
            password=self.account.password.get_secret_value() if self.account.password else None,
            use_tls=True,
            tls_context=context,
          )

        return {
          "status": "sent",
          "recipients": ", ".join(recipients),
          "message": str(result[1]) if result else "OK",
        }
      except aiosmtplib.SMTPException as e:
        raise RuntimeError("Failed to send email. Check server logs for details.")

  async def _add_attachments(
    self,
    msg: MIMEMultipart,
    attachment_paths: list[str],
  ) -> None:
    """Add file attachments to message."""
    for path in attachment_paths:
      if not os.path.exists(path):
        raise FileNotFoundError(f"Attachment file not found: {path}")

      filename = os.path.basename(path)
      with open(path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
          "Content-Disposition",
          f'attachment; filename="{filename}"',
        )
        msg.attach(part)