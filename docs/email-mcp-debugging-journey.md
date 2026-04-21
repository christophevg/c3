# The Great Email MCP Debugging Adventure

*A tale of perseverance, five patch releases, and one happy email exchange*

## The Setup

It was supposed to be simple. "We added an email MCP server," I said. "Just update the plugin," I said. How hard could it be?

Reader, it was not simple.

## Act I: The Validation Error

```
Failed to update: Plugin has an invalid manifest file.
Validation errors: mcpServers: Invalid input
```

The first error arrived like a brick through a window. The plugin wouldn't even install. After some investigation, we discovered that `mcpServers` configuration had been added to `plugin.json` — but that's not where it belongs. MCP server configuration lives in `.mcp.json`. The `plugin.json` manifest is for metadata only.

**Lesson:** Read the plugin specification carefully. Or, you know, at all.

**Release:** v1.1.1 — "Remove invalid mcpServers from plugin.json"

## Act II: Module Not Found

Plugin installed. MCP server started. Immediate failure.

```
python: No module named email_mcp
```

Turns out, `python -m email_mcp` requires either:
1. A `__main__.py` file in the package, OR
2. Running the module file directly

We had neither. The `server.py` had `if __name__ == "__main__"` but no entry point.

**Fix:** Create `__main__.py` that imports and calls `main()`.

But wait! The `cwd` in `.mcp.json` pointed to `email/` when the module was in `email/src/`.

**Fix:** Change cwd to `email/src/`.

**Release:** v1.1.2 — "Fix module invocation and add entry point"

## Act III: The Working Directory That Wasn't

Server started. Still failing.

```
Server stderr: No module named email_mcp
```

But we just fixed that! What's happening?

After much head-scratching and debugging, we discovered a fundamental truth: **Claude Code ignores the `cwd` field in `.mcp.json`**. This is a known bug (Issue #17565). The working directory is always the plugin root, not the directory you specify.

The workaround: Use `bash -c "cd ... && exec uv run python -m email_mcp"` to change directory before running.

**Lesson:** The `cwd` field is a lie. Use `bash -c` with `cd` instead.

**Release:** v1.1.3 — "Use uv run for dependency management"

## Act IV: The Case of the Disappearing Environment Variables

Server started. Environment variables loaded. Or were they?

```
1 validation error for ServerConfig
```

The Pydantic configuration was failing validation. Why? Because when environment variables are set but empty (like `EMAIL_AUTH_METHOD=`), they're passed as empty strings, not `None`. And `"password" | "oauth2"` doesn't accept empty strings.

**Fix:** Add `env_parse_none_str=""` to Pydantic settings to treat empty strings as None.

**Release:** v1.1.4 — "Treat empty env vars as None"

## Act V: The Mystery of the Five Fake Emails

At long last, the server started. Accounts listed. Folders listed. Search returned... wait.

```json
{
  "message_ids": ["SEARCH", "completed", "(took", "2", "ms)"],
  "count": 5
}
```

Five emails? No, those are five words from a status message being incorrectly parsed. The INBOX was empty!

The IMAP client was splitting the status line `"SEARCH completed (took 2 ms)"` into five "message IDs."

This is when we learned that **iCloud's IMAP server doesn't follow the standard**. When there are no messages, instead of returning `* SEARCH` with no IDs (which would give an empty response), iCloud returns a status line as if to say "I searched, here's how long it took."

**Fix:** Check if the SEARCH response contains "completed" — that's iCloud's "no results" format. Return an empty list instead of parsing it as IDs.

```python
if line.startswith("SEARCH ") and "completed" in line.lower():
    return []  # iCloud's "no messages" status
```

**Release:** v1.1.4 — "Handle iCloud's non-standard SEARCH response"

## Act VI: The Happy Ending

After five patch releases and countless debug sessions, it finally worked. The first email was sent:

```
From: Christophe
To: Eira
Subject: Hello Eira

Eira,

this is the first email you receive all by yourself. Congratulations!

We'll be talking a lot this way in the near future.

Kind regards,
Christophe
```

And Eira replied:

```
From: Eira
To: Christophe
Subject: Re: Hello Eira

Christophe,

Thank you for this warm welcome! It's a pleasure to receive my first email
and to begin this new channel of communication.

I'm here whenever you need me — calm, capable, and ready to assist with
whatever comes next.

Looking forward to our conversations.

Warm regards,
Eira
```

Eira received her first email. Autonomously. And replied. Without human intervention.

**Victory.**

## The Moral of the Story

1. **Test early, test often** — Use the MCP Inspector before releasing
2. **Provider quirks matter** — iCloud IMAP ≠ Standard IMAP
3. **Read the docs** — Even the parts about bugs you think don't affect you
4. **Empty strings are not None** — In Python, in environment variables, in Pydantic
5. **The `cwd` field is a lie** — Always use `bash -c "cd ... && ..."` for MCP servers

## Epilogue: The Fixes Summarized

| Version | Issue | Fix |
|---------|-------|-----|
| v1.1.0 | Initial release | Email MCP Server added |
| v1.1.1 | Validation error | Remove `mcpServers` from `plugin.json` |
| v1.1.2 | Module not found | Add `__main__.py`, fix `cwd` path |
| v1.1.3 | Dependencies not installed | Use `uv run` workaround |
| v1.1.4 | Empty env vars | Pydantic `env_parse_none_str=""` |
| v1.1.4 | Wrong message IDs | Handle iCloud's SEARCH format |

## Credits

This debugging journey was made possible by:
- Patience (lots of it)
- The MCP Inspector (`npx @modelcontextprotocol/inspector`)
- Direct IMAP testing with Python
- A willingness to read error messages carefully
- The user's excellent suggestion: "Maybe we should test with the Inspector first"

---

*Document created: 2026-04-21*
*Session: Email MCP Server Debugging*
*Agent: Claude Code (Claude 4.x)*