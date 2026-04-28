# Summary: P1-C1 Fix IMAP Connection Race Condition

**Date**: 2026-04-28
**Task**: C1 Fix IMAP connection race condition
**Status**: Completed

---

## What Was Implemented

### Problem
The `IMAPClient` class used a single `asyncio.Lock` (`_lock`) that only wrapped `connect()`, leaving all subsequent IMAP command sequences unprotected. Concurrent tool calls for the same account shared one `IMAP4_SSL` connection and interleaved commands on the wire, causing tag collisions, response misrouting, and data corruption.

### Solution
Implemented operation-level locking in `IMAPClient`:

1. **Renamed `_lock` to `_connect_lock`** — This lock continues to protect connection establishment (TLS handshake, authentication).

2. **Added `_operation_lock = asyncio.Lock()`** — A new lock that serializes all IMAP operations.

3. **Wrapped all public IMAP methods** with `async with self._operation_lock:`:
   - `list_folders()`
   - `select_folder()`
   - `search()`
   - `fetch_message()`
   - `move_message()`
   - `delete_message()`
   - `mark_message()`
   - `download_attachment()`
   - `disconnect()`

4. **Refactored internal calls** — Methods that previously called `select_folder()` (which called `connect()`) now call `connect()` and `client.select()` directly inside the same `_operation_lock` scope, avoiding redundant connection calls and preventing nested-lock deadlock.

### Files Modified

- `src/email_mcp/imap/client.py` — Added operation-level locking, refactored method internals
- `tests/test_imap_client.py` — New test file with 21 tests

### Key Design Decisions

- **Operation-level locking chosen** over checkout/checkin pool for simplicity and lower risk (per API Architect and Security Engineer consensus).
- **No changes to `ConnectionPool` or `server.py`** — the fix is entirely within `IMAPClient`.
- **`_selected_folder` is effectively synchronized** because the operation lock serializes all state mutations.

### Testing

- Added 21 new tests in `tests/test_imap_client.py`:
  - Concurrent `connect()` serialization (verifies `_connect_lock`)
  - Connect idempotency
  - Concurrent search serialization (verifies `_operation_lock`)
  - Lock held during full operation with yield point
  - Lock separation verification
  - Disconnect state cleanup
  - Error paths: select failure, search failure, fetch failure, auth failure, move copy failure
  - All public method happy paths
  - `download_attachment` with workspace confinement
  - `mark_message` add and remove branches
- Full test suite: 41 passed, 3 pre-existing failures (unrelated environment config + whitelist bugs).

### Review Cycle

| Reviewer | Status | Notes |
|----------|--------|-------|
| functional-analyst | Approved | Fix correctly addresses race condition, all methods protected, no deadlock |
| code-reviewer | Approved | Clean implementation, pre-existing blocking I/O noted for follow-up |
| testing-engineer | Approved (after iteration) | All gaps addressed: connect race tested, download_attachment tested, error paths covered |

### Security Impact

- Fixes cross-folder information disclosure within an account
- Fixes tampering (wrong folder operations due to race conditions)
- Eliminates timing side-channels from unprotected IMAP commands
- Account isolation remains intact (no cross-account leakage)
