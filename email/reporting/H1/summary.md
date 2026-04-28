# Task Summary: H1 - Fix Non-atomic move_message

## What Was Implemented

Fixed non-atomic `move_message` operation by adding IMAP MOVE extension (RFC 6851) support with graceful fallback to COPY+STORE+EXPUNGE for legacy servers.

## Location

- **File**: `src/email_mcp/imap/client.py`
- **Lines**: 41, 84-95, 101-105, 221-258

## Changes

### 1. Added Capability Caching

```python
def __init__(self, account: EmailAccount) -> None:
  # ...
  self._capabilities: set[str] = set()
```

### 2. Query Capabilities on Connect

```python
# Query and cache server capabilities
try:
  response = await self._client.capability()
  if response.result == "OK" and response.lines:
    caps_str = response.lines[0].decode().upper()
    self._capabilities = set(caps_str.split())
except Exception:
  # Non-fatal: continue without cached capabilities
  self._capabilities = set()
```

### 3. Added has_capability() Method

```python
def has_capability(self, name: str) -> bool:
  """Check if server supports a capability."""
  return name.upper() in self._capabilities
```

### 4. Updated move_message() to Use Atomic MOVE

```python
# Use atomic MOVE if server supports RFC 6851
if self.has_capability("MOVE"):
  status, _ = await client.move(message_id, dest_folder)
  if status != "OK":
    raise RuntimeError(f"Failed to move message: {status}")
  return True

# Fallback: non-atomic COPY+STORE+EXPUNGE
# WARNING: Not atomic - message may exist in both folders on failure
```

## Key Decisions

1. **Capability caching**: Single query on connect, reused for all operations (no per-operation overhead)
2. **Graceful degradation**: Servers without MOVE extension still work with documented limitation
3. **Case-insensitive capability lookup**: `has_capability("move")` == `has_capability("MOVE")`
4. **Non-fatal capability query**: Connection succeeds even if capability query fails

## Tests Added

`tests/test_imap_client.py::TestMoveMessageAtomic` (8 tests):
- `test_uses_move_when_capability_present`: Verifies atomic MOVE used when available
- `test_fallback_when_move_not_supported`: Verifies fallback to COPY+STORE+EXPUNGE
- `test_move_failure_raises_error`: Verifies error handling on MOVE failure
- `test_capability_cached_on_connect`: Verifies single capability query
- `test_has_capability_returns_true_when_present`: Verifies capability lookup
- `test_has_capability_is_case_insensitive`: Verifies case-insensitive matching
- `test_capability_query_failure_falls_back_gracefully`: Verifies graceful degradation
- `test_capabilities_cleared_on_disconnect`: Verifies state cleanup

## Files Modified

| File | Change |
|------|--------|
| `src/email_mcp/imap/client.py` | Added capability caching, has_capability(), atomic MOVE support |
| `tests/test_imap_client.py` | Added 8 tests for atomic move functionality |
| `TODO.md` | Marked H1 as complete |
| `docs/bug-analysis/H1.md` | Bug analysis report |

## Lessons Learned

- IMAP MOVE extension (RFC 6851) provides atomic move operation
- Most modern IMAP servers (Gmail, Outlook, iCloud, Fastmail) support MOVE
- Capability detection should be done once per connection and cached
- Fallback to non-atomic approach should be clearly documented

## Risk Assessment

**No breaking changes**:
- Existing behavior unchanged for servers without MOVE extension
- Servers with MOVE extension now use atomic operation (improved reliability)
- Public API unchanged (only new method `has_capability()` added)