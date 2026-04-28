# Consensus: P1-C1 Fix IMAP Connection Race Condition

**Date**: 2026-04-28
**Task**: C1 Fix IMAP connection race condition
**Status**: Approved for implementation

---

## Consensus Summary

Both the **API Architect** and **Security Engineer** agents reviewed P1-C1 and independently converged on the same recommendation: **operation-level locking** in `IMAPClient`.

### Agreement Points

| Aspect | api-architect | security-engineer | Consensus |
|--------|--------------|-------------------|-----------|
| Primary fix | Operation-level locking | Operation-level locking | ✅ Agreed |
| No cross-account leakage | N/A (not in scope) | Confirmed isolated | ✅ Correct |
| `_selected_folder` state | Remove or guard with lock | Guard with same lock | ✅ Guard with lock |
| Checkout/checkin pool | Future enhancement | Not needed now | ✅ Future enhancement |
| ConnectionPool changes | None needed | None needed | ✅ No changes |

### Disagreements / Additional Concerns

**None.** Both agents agreed on the fix. The security engineer raised additional concerns (timing side-channels, non-atomic multi-command operations) that are addressed by the same operation-level locking fix.

---

## Approved Design

### Changes to `src/email_mcp/imap/client.py`

1. Rename `_lock` to `_connect_lock` (protects connection establishment only)
2. Add `_operation_lock = asyncio.Lock()` (serializes all IMAP operations)
3. Create `_ensure_connected()` helper with double-checked locking
4. Wrap all public IMAP methods with `async with self._operation_lock`
5. Move `select_folder()` inside the lock scope for each operation

### Public Methods to Wrap

| Method | IMAP Commands |
|--------|---------------|
| `list_folders()` | `LIST` |
| `select_folder()` | `SELECT` |
| `search()` | `SELECT`, `SEARCH` |
| `fetch_message()` | `SELECT`, `FETCH` |
| `move_message()` | `SELECT`, `COPY`, `STORE`, `EXPUNGE` |
| `delete_message()` | `SELECT`, `STORE`, `EXPUNGE` |
| `mark_message()` | `SELECT`, `STORE` |
| `download_attachment()` | `SELECT`, `FETCH` |
| `disconnect()` | `LOGOUT` |

### Lock Pattern

```python
async def _ensure_connected(self) -> IMAP4_SSL:
    if self._client is not None:
        return self._client
    async with self._connect_lock:
        if self._client is not None:
            return self._client
        # ... create and authenticate ...
        return self._client

async def search(self, folder, criteria, limit):
    async with self._operation_lock:
        client = await self._ensure_connected()
        # ... full operation under lock ...
```

### No Changes Required

- `ConnectionPool` interface remains unchanged
- `server.py` tool handlers remain unchanged
- No changes to SMTP client

---

## Testing Requirements

1. **Concurrent search test**: Two coroutines call `search()` on same client; verify no interleaving
2. **SELECT state isolation**: Coroutine A searches folder A, coroutine B searches folder B; verify correct results
3. **Lock held assertion**: Assert `_operation_lock.locked()` during IMAP command execution
4. **Disconnect during operation**: Verify graceful handling

---

## Future Enhancement (Documented)

**Checkout/checkin connection pool** — If per-account concurrency becomes a requirement, implement a true connection pool with health checking, per-connection SELECT state tracking, and server limit awareness. See `analysis/api-c1-race-condition.md` for design.

---

## Sign-off

- ✅ api-architect: Approved
- ✅ security-engineer: Approved
