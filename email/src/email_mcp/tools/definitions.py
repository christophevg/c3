"""MCP tool definitions for email operations."""

from __future__ import annotations

import json
from typing import Annotated, Any

from pydantic import Field

# Tool schemas using Pydantic types for FastMCP


class ListAccountsInput:
  """Input schema for list_accounts tool."""

  # No inputs required


class ListAccountsOutput:
  """Output schema for list_accounts tool."""

  accounts: Annotated[
    list[dict[str, str]],
    Field(description="List of configured email accounts"),
  ]


class ListFoldersInput:
  """Input schema for list_folders tool."""

  account: Annotated[
    str,
    Field(description="Account name to list folders for"),
  ]


class ListFoldersOutput:
  """Output schema for list_folders tool."""

  folders: Annotated[
    list[dict[str, Any]],
    Field(description="List of mailboxes/folders"),
  ]


class SearchEmailsInput:
  """Input schema for search_emails tool."""

  account: Annotated[str, Field(description="Account name")]
  folder: Annotated[str, Field(default="INBOX", description="Folder to search")]
  criteria: Annotated[str, Field(default="ALL", description="IMAP search criteria")]
  limit: Annotated[int, Field(default=50, description="Maximum results")]


class SearchEmailsOutput:
  """Output schema for search_emails tool."""

  message_ids: Annotated[
    list[str],
    Field(description="List of message IDs"),
  ]
  count: Annotated[int, Field(description="Total matching messages")]


class GetEmailInput:
  """Input schema for get_email tool."""

  account: Annotated[str, Field(description="Account name")]
  message_id: Annotated[str, Field(description="Message ID to fetch")]
  folder: Annotated[str, Field(default="INBOX", description="Folder name")]


class GetEmailOutput:
  """Output schema for get_email tool."""

  id: Annotated[str, Field(description="Message ID")]
  folder: Annotated[str, Field(description="Folder name")]
  subject: Annotated[str, Field(description="Email subject")]
  from_: Annotated[str, Field(alias="from", description="Sender")]
  to: Annotated[str, Field(description="Recipients")]
  date: Annotated[str, Field(description="Date sent")]
  body: Annotated[str, Field(description="Plain text body")]
  attachments: Annotated[list[str], Field(description="Attachment filenames")]


class DownloadAttachmentInput:
  """Input schema for download_attachment tool."""

  account: Annotated[str, Field(description="Account name")]
  message_id: Annotated[str, Field(description="Message ID")]
  folder: Annotated[str, Field(default="INBOX", description="Folder name")]
  filename: Annotated[str, Field(description="Attachment filename")]
  output_dir: Annotated[str, Field(description="Output directory path")]


class DownloadAttachmentOutput:
  """Output schema for download_attachment tool."""

  path: Annotated[str, Field(description="Downloaded file path")]
  filename: Annotated[str, Field(description="Original filename")]


class SendEmailInput:
  """Input schema for send_email tool."""

  account: Annotated[str, Field(description="Account name")]
  to: Annotated[list[str], Field(description="Recipient addresses")]
  subject: Annotated[str, Field(description="Email subject")]
  body: Annotated[str, Field(description="Plain text body")]
  cc: Annotated[list[str] | None, Field(default=None, description="CC addresses")]
  bcc: Annotated[list[str] | None, Field(default=None, description="BCC addresses")]
  html_body: Annotated[str | None, Field(default=None, description="HTML body")]
  attachments: Annotated[
    list[str] | None,
    Field(default=None, description="Attachment file paths"),
  ]


class SendEmailOutput:
  """Output schema for send_email tool."""

  status: Annotated[str, Field(description="Send status")]
  recipients: Annotated[str, Field(description="Recipient list")]
  message: Annotated[str, Field(description="Server response")]


class ReplyEmailInput:
  """Input schema for reply_email tool."""

  account: Annotated[str, Field(description="Account name")]
  to: Annotated[str, Field(description="Recipient address")]
  subject: Annotated[str, Field(description="Email subject")]
  body: Annotated[str, Field(description="Plain text body")]
  in_reply_to: Annotated[str, Field(description="Message-ID being replied to")]
  references: Annotated[
    list[str] | None,
    Field(default=None, description="Thread references"),
  ]
  html_body: Annotated[str | None, Field(default=None, description="HTML body")]


class ReplyEmailOutput:
  """Output schema for reply_email tool."""

  status: Annotated[str, Field(description="Send status")]
  recipients: Annotated[str, Field(description="Recipient list")]


class MoveEmailInput:
  """Input schema for move_email tool."""

  account: Annotated[str, Field(description="Account name")]
  message_id: Annotated[str, Field(description="Message ID")]
  source_folder: Annotated[str, Field(description="Source folder")]
  dest_folder: Annotated[str, Field(description="Destination folder")]


class MoveEmailOutput:
  """Output schema for move_email tool."""

  status: Annotated[str, Field(description="Move status")]
  message_id: Annotated[str, Field(description="Message ID")]
  dest_folder: Annotated[str, Field(description="Destination folder")]


class DeleteEmailInput:
  """Input schema for delete_email tool."""

  account: Annotated[str, Field(description="Account name")]
  message_id: Annotated[str, Field(description="Message ID")]
  folder: Annotated[str, Field(default="INBOX", description="Folder name")]
  expunge: Annotated[bool, Field(default=True, description="Expunge after delete")]


class DeleteEmailOutput:
  """Output schema for delete_email tool."""

  status: Annotated[str, Field(description="Delete status")]
  message_id: Annotated[str, Field(description="Message ID")]


class MarkEmailReadInput:
  """Input schema for mark_email_read tool."""

  account: Annotated[str, Field(description="Account name")]
  message_id: Annotated[str, Field(description="Message ID")]
  folder: Annotated[str, Field(default="INBOX", description="Folder name")]


class MarkEmailReadOutput:
  """Output schema for mark_email_read tool."""

  status: Annotated[str, Field(description="Mark status")]
  message_id: Annotated[str, Field(description="Message ID")]


# Tool definitions as dictionaries for FastMCP registration

TOOL_SCHEMAS: dict[str, dict[str, Any]] = {
  "list_accounts": {
    "description": "List all configured email accounts.",
    "input_schema": {},
  },
  "list_folders": {
    "description": "List all folders/mailboxes for an account.",
    "input_schema": {
      "type": "object",
      "properties": {
        "account": {"type": "string", "description": "Account name"},
      },
      "required": ["account"],
    },
  },
  "search_emails": {
    "description": "Search for emails matching criteria.",
    "input_schema": {
      "type": "object",
      "properties": {
        "account": {"type": "string", "description": "Account name"},
        "folder": {"type": "string", "default": "INBOX", "description": "Folder to search"},
        "criteria": {"type": "string", "default": "ALL", "description": "IMAP search criteria"},
        "limit": {"type": "integer", "default": 50, "description": "Maximum results"},
      },
      "required": ["account"],
    },
  },
  "get_email": {
    "description": "Fetch a single email message by ID.",
    "input_schema": {
      "type": "object",
      "properties": {
        "account": {"type": "string", "description": "Account name"},
        "message_id": {"type": "string", "description": "Message ID"},
        "folder": {"type": "string", "default": "INBOX", "description": "Folder name"},
      },
      "required": ["account", "message_id"],
    },
  },
  "download_attachment": {
    "description": "Download an attachment from an email.",
    "input_schema": {
      "type": "object",
      "properties": {
        "account": {"type": "string", "description": "Account name"},
        "message_id": {"type": "string", "description": "Message ID"},
        "folder": {"type": "string", "default": "INBOX", "description": "Folder name"},
        "filename": {"type": "string", "description": "Attachment filename"},
        "output_dir": {"type": "string", "description": "Output directory"},
      },
      "required": ["account", "message_id", "filename", "output_dir"],
    },
  },
  "send_email": {
    "description": "Send a new email message.",
    "input_schema": {
      "type": "object",
      "properties": {
        "account": {"type": "string", "description": "Account name"},
        "to": {"type": "array", "items": {"type": "string"}, "description": "Recipients"},
        "subject": {"type": "string", "description": "Email subject"},
        "body": {"type": "string", "description": "Plain text body"},
        "cc": {"type": "array", "items": {"type": "string"}, "description": "CC addresses"},
        "bcc": {"type": "array", "items": {"type": "string"}, "description": "BCC addresses"},
        "html_body": {"type": "string", "description": "HTML body"},
        "attachments": {"type": "array", "items": {"type": "string"}, "description": "Attachment paths"},
      },
      "required": ["account", "to", "subject", "body"],
    },
  },
  "reply_email": {
    "description": "Reply to an existing email thread.",
    "input_schema": {
      "type": "object",
      "properties": {
        "account": {"type": "string", "description": "Account name"},
        "to": {"type": "string", "description": "Recipient address"},
        "subject": {"type": "string", "description": "Email subject"},
        "body": {"type": "string", "description": "Plain text body"},
        "in_reply_to": {"type": "string", "description": "Message-ID being replied to"},
        "references": {"type": "array", "items": {"type": "string"}, "description": "Thread references"},
        "html_body": {"type": "string", "description": "HTML body"},
      },
      "required": ["account", "to", "subject", "body", "in_reply_to"],
    },
  },
  "move_email": {
    "description": "Move an email between folders.",
    "input_schema": {
      "type": "object",
      "properties": {
        "account": {"type": "string", "description": "Account name"},
        "message_id": {"type": "string", "description": "Message ID"},
        "source_folder": {"type": "string", "description": "Source folder"},
        "dest_folder": {"type": "string", "description": "Destination folder"},
      },
      "required": ["account", "message_id", "source_folder", "dest_folder"],
    },
  },
  "delete_email": {
    "description": "Delete an email message.",
    "input_schema": {
      "type": "object",
      "properties": {
        "account": {"type": "string", "description": "Account name"},
        "message_id": {"type": "string", "description": "Message ID"},
        "folder": {"type": "string", "default": "INBOX", "description": "Folder name"},
        "expunge": {"type": "boolean", "default": True, "description": "Expunge after delete"},
      },
      "required": ["account", "message_id"],
    },
  },
  "mark_email_read": {
    "description": "Mark an email message as read.",
    "input_schema": {
      "type": "object",
      "properties": {
        "account": {"type": "string", "description": "Account name"},
        "message_id": {"type": "string", "description": "Message ID"},
        "folder": {"type": "string", "default": "INBOX", "description": "Folder name"},
      },
      "required": ["account", "message_id"],
    },
  },
}