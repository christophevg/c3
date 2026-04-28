"""Async IMAP client using aioimaplib."""

from __future__ import annotations

import asyncio
import email
import hashlib
import os
import re
import ssl
from email.header import decode_header
from pathlib import Path
from typing import Any

from aioimaplib import IMAP4_SSL

from email_mcp.config import EmailAccount
from email_mcp.safety.audit import log_auth_attempt, log_attachment_download

# Default workspace for attachment downloads
DEFAULT_WORKSPACE = Path(os.environ.get("EMAIL_WORKSPACE", "/tmp/email_workspace"))

# IMAP search criteria validation
IMAP_CRITERIA_PATTERN = re.compile(r"^[\w\s\(\)\*\<\>\[\]=!\"'-]+$")


class IMAPClient:
  """Async IMAP client with connection pooling."""

  def __init__(self, account: EmailAccount) -> None:
    self.account = account
    self._client: IMAP4_SSL | None = None
    self._selected_folder: str | None = None
    self._lock = asyncio.Lock()

  async def connect(self) -> IMAP4_SSL:
    """Establish IMAP connection with SSL verification."""
    async with self._lock:
      if self._client is not None:
        return self._client

      # Create SSL context with certificate verification and TLS 1.2 minimum
      context = ssl.create_default_context()
      context.minimum_version = ssl.TLSVersion.TLSv1_2

      self._client = IMAP4_SSL(
        host=self.account.imap_host,
        port=self.account.imap_port,
        ssl_context=context,
      )

      await self._client.wait_hello_from_server()

      # Authenticate
      try:
        if self.account.auth_method == "oauth2" and self.account.oauth2_token:
          token = self.account.oauth2_token.get_secret_value()
          auth_string = f"user={self.account.username}\x01auth=Bearer {token}\x01\x01"
          await self._client.authenticate("XOAUTH2", auth_string)
          log_auth_attempt(self.account.name, True, "oauth2")
        elif self.account.password:
          await self._client.login(
            self.account.username,
            self.account.password.get_secret_value(),
          )
          log_auth_attempt(self.account.name, True, "password")
        else:
          raise ValueError("No credentials available")
      except Exception as e:
        log_auth_attempt(self.account.name, False, self.account.auth_method, str(e))
        raise RuntimeError("Authentication failed. Check server logs for details.")

      return self._client

  async def disconnect(self) -> None:
    """Close IMAP connection."""
    if self._client:
      await self._client.logout()
      self._client = None
      self._selected_folder = None

  async def list_folders(self) -> list[dict[str, Any]]:
    """List all folders/mailboxes."""
    client = await self.connect()
    # iCloud requires specific quoting format
    status, data = await client.list('""', '"*"')

    if status != "OK":
      raise RuntimeError(f"Failed to list folders: {status}")

    folders = []
    for item in data:
      if isinstance(item, bytes):
        item = item.decode()
      if not item:
        continue
      # Parse: (flags) "delimiter" "name"
      parts = item.split('"')
      if len(parts) >= 3:
        folders.append({
          "flags": parts[0].strip("() "),
          "delimiter": parts[1],
          "name": parts[3] if len(parts) > 3 else parts[1],
        })

    return folders

  async def select_folder(self, folder: str = "INBOX") -> dict[str, int]:
    """Select a folder and return message count."""
    client = await self.connect()
    status, data = await client.select(folder)

    if status != "OK":
      raise RuntimeError(f"Failed to select folder {folder}: {status}")

    self._selected_folder = folder
    # Parse EXISTS from response - data contains lines like b'2 EXISTS'
    count = 0
    for item in data:
      if isinstance(item, bytes) and b'EXISTS' in item:
        try:
          count = int(item.split()[0])
        except (ValueError, IndexError):
          pass
        break
    return {"folder": folder, "count": count}

  async def search(
    self,
    folder: str = "INBOX",
    criteria: str = "ALL",
    limit: int = 50,
  ) -> list[str]:
    """Search for messages matching criteria."""
    await self.select_folder(folder)
    client = await self.connect()

    # Validate criteria to prevent IMAP injection
    if not IMAP_CRITERIA_PATTERN.match(criteria):
      raise ValueError("Invalid search criteria")

    result = await client.search(criteria)

    if result.result != "OK":
      raise RuntimeError("Search failed")

    # Handle response - may be empty or contain message IDs
    # iCloud returns: b'SEARCH completed (took X ms)' when no messages
    # Standard IMAP returns: b'SEARCH 1 2 3' with message IDs
    if not result.lines or not result.lines[0]:
      return []

    # Check if this is iCloud's "no messages" status response
    line = result.lines[0].decode()
    if line.startswith("SEARCH ") and "completed" in line.lower():
      # No actual message IDs, just a status message
      return []

    # Parse message IDs from standard response
    ids = line.split()
    # Remove 'SEARCH' prefix if present (some servers include it)
    if ids and ids[0].upper() == "SEARCH":
      ids = ids[1:]
    return ids[-limit:] if limit else ids

  async def fetch_message(
    self,
    message_id: str,
    folder: str = "INBOX",
  ) -> dict[str, Any]:
    """Fetch a single message by ID."""
    await self.select_folder(folder)
    client = await self.connect()

    # Fetch headers and body
    status, data = await client.fetch(message_id, "(BODY.PEEK[] FLAGS)")

    if status != "OK":
      raise RuntimeError(f"Failed to fetch message {message_id}: {status}")

    # Parse the response
    # Format: [b'1 FETCH (BODY[] {size}', bytearray(content), b' FLAGS (...)', b'FETCH completed']
    result = {"id": message_id, "folder": folder}

    raw_message = None
    for item in data:
      if isinstance(item, bytearray):
        raw_message = bytes(item)
      elif isinstance(item, tuple) and len(item) == 2:
        # Alternative format
        raw_message = item[1] if isinstance(item[1], (bytes, bytearray)) else None

    if raw_message:
      msg = email.message_from_bytes(raw_message)
      result["subject"] = self._decode_header(msg.get("Subject", ""))
      result["from"] = self._decode_header(msg.get("From", ""))
      result["to"] = self._decode_header(msg.get("To", ""))
      result["date"] = msg.get("Date", "")
      result["body"] = self._get_body(msg)
      result["attachments"] = self._list_attachments(msg)

    return result

  async def move_message(
    self,
    message_id: str,
    source_folder: str,
    dest_folder: str,
  ) -> bool:
    """Move a message between folders."""
    await self.select_folder(source_folder)
    client = await self.connect()

    # Copy to destination
    status, _ = await client.copy(message_id, dest_folder)
    if status != "OK":
      raise RuntimeError(f"Failed to copy message: {status}")

    # Mark as deleted in source
    await client.store(message_id, "+FLAGS", "\\Deleted")

    # Permanently remove from source so it no longer appears in searches
    await client.expunge()

    return True

  async def delete_message(
    self,
    message_id: str,
    folder: str = "INBOX",
    expunge: bool = True,
  ) -> bool:
    """Delete a message."""
    await self.select_folder(folder)
    client = await self.connect()

    # Mark as deleted
    await client.store(message_id, "+FLAGS", "\\Deleted")

    if expunge:
      await client.expunge()

    return True

  async def mark_message(
    self,
    message_id: str,
    folder: str,
    flag: str,
    action: str = "add",
  ) -> bool:
    """Add or remove flags from a message."""
    await self.select_folder(folder)
    client = await self.connect()

    flag_action = "+FLAGS" if action == "add" else "-FLAGS"
    status, _ = await client.store(message_id, flag_action, flag)

    return status == "OK"

  async def download_attachment(
    self,
    message_id: str,
    folder: str,
    filename: str,
    output_dir: str,
  ) -> str:
    """Download an attachment from a message with workspace confinement."""
    # Validate and resolve output directory
    output_path = Path(output_dir).resolve()
    workspace = DEFAULT_WORKSPACE.resolve()

    # Ensure workspace exists
    workspace.mkdir(parents=True, exist_ok=True)

    # Workspace confinement check
    try:
      output_path.relative_to(workspace)
    except ValueError:
      raise ValueError(f"output_dir must be within workspace: {workspace}")

    # Sanitize filename - remove path separators
    safe_filename = os.path.basename(filename)
    # Hash for uniqueness and additional safety
    hashed_prefix = hashlib.sha256(filename.encode()).hexdigest()[:16]
    final_filename = f"{hashed_prefix}_{safe_filename}"

    await self.select_folder(folder)
    client = await self.connect()

    status, data = await client.fetch(message_id, "(BODY.PEEK[])")

    if status != "OK":
      raise RuntimeError("Failed to fetch message")

    for item in data:
      if isinstance(item, tuple) and len(item) == 2:
        raw_message = item[1]
        if isinstance(raw_message, bytes):
          msg = email.message_from_bytes(raw_message)
          for part in msg.walk():
            if part.get_filename() == filename:
              payload = part.get_payload(decode=True)
              if payload:
                # Ensure output directory exists
                output_path.mkdir(parents=True, exist_ok=True)
                file_path = output_path / final_filename
                with open(file_path, "wb") as f:
                  f.write(payload)
                log_attachment_download(self.account.name, filename, str(file_path))
                return str(file_path)

    raise FileNotFoundError(f"Attachment not found in message")

  def _decode_header(self, header: str) -> str:
    """Decode MIME header."""
    if not header:
      return ""
    decoded_parts = decode_header(header)
    result = []
    for part, charset in decoded_parts:
      if isinstance(part, bytes):
        result.append(part.decode(charset or "utf-8", errors="replace"))
      else:
        result.append(part)
    return "".join(result)

  def _get_body(self, msg: email.message.Message) -> str:
    """Extract plain text body from message."""
    if msg.is_multipart():
      for part in msg.walk():
        content_type = part.get_content_type()
        if content_type == "text/plain":
          payload = part.get_payload(decode=True)
          if payload:
            return payload.decode("utf-8", errors="replace")
      return ""
    else:
      payload = msg.get_payload(decode=True)
      if payload:
        return payload.decode("utf-8", errors="replace")
      return ""

  def _list_attachments(self, msg: email.message.Message) -> list[str]:
    """List attachment filenames."""
    attachments = []
    for part in msg.walk():
      filename = part.get_filename()
      if filename:
        attachments.append(filename)
    return attachments