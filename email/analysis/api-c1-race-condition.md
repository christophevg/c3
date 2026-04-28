# API Analysis: P1-C1 IMAP Connection Race Condition

**Date**: 2026-04-28
**Task**: C1 Fix IMAP connection race condition — architecture review
**Reviewer**: API Architect Agent
**Scope**: `src/email_mcp/imap/client.py`, `src/email_mcp/connections/pool.py`

---

## Executive Summary

The `IMAPClient` class uses a single `asyncio.Lock` that only wraps `connect()`, leaving all subsequent IMAP command sequences unprotected. When concurrent tool calls arrive for the same account, they share one `IMAP4_SSL` connection and interleave commands on the wire, causing tag collisions, response misrouting, and data corruption. Two architectural fixes are viable: **operation-level locking** (recommended for immediate fix) or a **checkout/checkin connection pool** (recommended as future enhancement).

---

## Current Architecture

### Connection Model

```
ConnectionPool (Singleton)
├── _imap_clients: dict[str, IMAPClient]   # One client per account
├── _smtp_clients: dict[str, SMTPClient]
└── _client_lock: asyncio.Lock             # Protects dict mutation only

IMAPClient
├── _client: IMAP4_SSL | None              # Single underlying connection
├── _selected_folder: str | None           # Mutable SELECT state
└── _lock: asyncio.Lock                    # Protects connect() ONLY
```

### The Race Condition

Every public method follows this pattern:

```python
async def search(self, ...):
    await self.select_folder(folder)        # (1) SELECT command
    client = await self.connect()           # (2) Returns shared _client
    result = await client.search(criteria)  # (3) SEARCH command — NO LOCK
```

Two concurrent `search_emails` calls for the same account:

```
Coroutine A                     Coroutine B
─────────────────────────────────────────────────
select_folder("INBOX")          select_folder("INBOX")
connect() -> shared_client      connect() -> shared_client
client.search("ALL")            client.search("UNSEEN")
  tag A01 SEARCH ALL              tag A01 SEARCH UNSEEN  ← tag collision!
  ← response for UNSEEN           ← response for ALL     ← misrouted!
```

Because `aioimaplib` uses auto-incrementing tags internally, the collision happens at the protocol level. The result is wrong message IDs, exceptions, or silent data corruption.

### Why the Current Lock is Insufficient

The `_lock` in `IMAPClient.__init__` (line 34) is acquired only inside `connect()` (line 38). Once `connect()` returns the shared `IMAP4_SSL` instance, the lock is released and the caller issues IMAP commands without any serialization.

Additionally, `_selected_folder` is mutable state that is not synchronized. Concurrent callers can overwrite each other's selected folder mid-operation.

---

## Recommendation 1: Operation-Level Locking (Immediate Fix)

### Design

Add a second `asyncio.Lock` to `IMAPClient` that wraps the entire operation from start to finish. Every public method acquires this lock and holds it until all IMAP commands complete and the response is fully consumed.

```python
class IMAPClient:
    def __init__(self, account: EmailAccount) -> None:
        self.account = account
        self._client: IMAP4_SSL | None = None
        self._selected_folder: str | None = None
        self._connect_lock = asyncio.Lock()   # Renamed from _lock
        self._operation_lock = asyncio.Lock() # NEW: serializes all IMAP ops

    async def _ensure_connected(self) -> IMAP4_SSL:
        """Connection setup under connect_lock."""
        async with self._connect_lock:
            if self._client is not None:
                return self._client
            # ... create, authenticate, return _client

    async def list_folders(self) -> list[dict[str, Any]]:
        """List all folders — fully serialized."""
        async with self._operation_lock:
            client = await self._ensure_connected()
            status, data = await client.list('""', '"*"')
            # ... parse and return
```

### Public Methods Requiring the Lock

All methods that issue IMAP commands must be wrapped:

| Method | IMAP Commands | Lock Required |
|--------|---------------|---------------|
| `list_folders()` | `LIST` | Yes |
| `select_folder()` | `SELECT`, mutates `_selected_folder` | Yes |
| `search()` | `SELECT`, `SEARCH` | Yes |
| `fetch_message()` | `SELECT`, `FETCH` | Yes |
| `move_message()` | `SELECT`, `COPY`, `STORE`, `EXPUNGE` | Yes |
| `delete_message()` | `SELECT`, `STORE`, `EXPUNGE` | Yes |
| `mark_message()` | `SELECT`, `STORE` | Yes |
| `download_attachment()` | `SELECT`, `FETCH` | Yes |
| `connect()` | `LOGIN`/`AUTHENTICATE` | Yes (via `_ensure_connected`) |
| `disconnect()` | `LOGOUT` | Yes |

### Tradeoffs

**Pros:**
- Simple, localized change
- Minimal risk of introducing new bugs
- Directly addresses the acceptance criteria
- No changes needed to `ConnectionPool` interface

**Cons:**
- Operations on the same account are fully serialized (no concurrency)
- One slow operation (e.g., large FETCH) blocks all others for that account
- Underutilizes the network connection

### Why This is Acceptable for MCP

MCP tool calls are coarse-grained and relatively infrequent in interactive use:
- A typical session: list folders (1x), search (1-2x), fetch a few messages (3-5x)
- Throughput is not a design goal; correctness is
- IMAP servers themselves are often rate-limited or connection-limited
- Serialization per account is a reasonable tradeoff for an MCP server

---

## Recommendation 2: Checkout/Checkin Connection Pool (Future Enhancement)

### Design

Replace the singleton `IMAPClient` per account with a pool of `N` connections (e.g., `max_connections=3`). The `ConnectionPool` becomes a true pool manager:

```python
class ConnectionPool:
    def __init__(self):
        self._imap_pools: dict[str, IMAPConnectionPool] = {}

class IMAPConnectionPool:
    """Per-account pool of IMAP connections with checkout/checkin."""

    def __init__(self, account: EmailAccount, max_size: int = 3):
        self.account = account
        self._max_size = max_size
        self._available: asyncio.Queue[IMAP4_SSL] = asyncio.Queue()
        self._in_use: set[IMAP4_SSL] = set()
        self._pool_lock = asyncio.Lock()

    async def checkout(self) -> IMAP4_SSL:
        """Get a ready-to-use IMAP connection."""
        async with self._pool_lock:
            if not self._available.empty():
                conn = self._available.get_nowait()
                self._in_use.add(conn)
                return conn
            if len(self._in_use) < self._max_size:
                conn = await self._create_connection()
                self._in_use.add(conn)
                return conn
        # Pool exhausted — wait for a connection to be returned
        conn = await self._available.get()
        async with self._pool_lock:
            self._in_use.add(conn)
        return conn

    async def checkin(self, conn: IMAP4_SSL) -> None:
        """Return a connection to the pool."""
        async with self._pool_lock:
            self._in_use.discard(conn)
            self._available.put_nowait(conn)
```

Each operation would then:
```python
async def search(self, folder, criteria):
    conn = await pool.checkout(account_name)
    try:
        await conn.select(folder)
        result = await conn.search(criteria)
        return result
    finally:
        await pool.checkin(conn)
```

### Additional Complexity

A true connection pool introduces significant complexity:

1. **Connection health**: Must detect and discard broken connections
2. **SELECT state**: Each connection may be in a different selected folder; operations must either `SELECT` every time or track per-connection state
3. **Server limits**: IMAP servers often limit concurrent connections per user (Gmail: ~15, iCloud: ~10)
4. **Idle timeout**: Connections time out; need keepalive or reconnection
5. **Rate limiting**: Rate limits apply per account, not per connection; pool must coordinate

### Tradeoffs

**Pros:**
- True parallelism for same-account operations
- Better throughput under concurrent load
- Industry-standard pattern for database/network clients

**Cons:**
- Substantial increase in complexity
- Requires connection health monitoring and reconnection
- Must handle per-connection SELECT state
- Need to configure and tune pool size
- More code to test (currently zero client tests)

---

## Decision

**Adopt Recommendation 1 (operation-level locking) for P1-C1.**

Rationale:
1. **Correctness over performance**: MCP servers prioritize correctness and simplicity over throughput.
2. **Minimal change**: The fix is localized to `IMAPClient` and requires no architectural changes.
3. **Risk management**: Given zero test coverage for client code, a simple change is safer.
4. **Future path**: If concurrent throughput becomes a real requirement, the checkout/checkin pool can be introduced later without changing the public `ConnectionPool` interface.

**Document Recommendation 2 in TODO.md** as a future enhancement for when throughput requirements emerge.

---

## Implementation Notes

### Lock Granularity

The `_operation_lock` should wrap the **entire** method body, including any internal calls that issue IMAP commands. This means:

- `search()` calls `select_folder()` internally; the lock must be held across both
- `move_message()` issues `COPY`, `STORE`, and `EXPUNGE`; all must be in the same critical section
- `disconnect()` must also acquire `_operation_lock` to avoid racing with an active operation

### Lock Nesting

Since `connect()` is called from within operations, we must avoid deadlock from nested locks. The safe pattern is:

```python
async def _ensure_connected(self) -> IMAP4_SSL:
    """Called only while holding _operation_lock."""
    if self._client is not None:
        return self._client
    async with self._connect_lock:
        # Double-check after acquiring lock
        if self._client is not None:
            return self._client
        # ... create and authenticate ...
        return self._client
```

This uses the standard "check-then-act with double-checked locking" pattern: the outer `_operation_lock` guarantees no concurrent callers, and `_connect_lock` protects the initialization sequence.

### SELECT State

Because the lock serializes operations, `_selected_folder` is effectively synchronized. No additional locking is needed for that field.

However, for robustness, `select_folder()` should be considered an implementation detail. Operations that need a specific folder should call `select_folder()` internally while holding the lock, rather than relying on external callers to manage SELECT state.

### ConnectionPool Impact

`ConnectionPool.get_imap_client()` returns the same `IMAPClient` instance. With operation-level locking, this is safe because all operations on that instance are serialized. No changes to `ConnectionPool` are required.

---

## Security Considerations

The race condition is not directly exploitable as an attack vector (it causes corruption, not unauthorized access), but fixing it removes a source of nondeterministic behavior that could complicate audit logging or conceal other issues.

---

## Testing Recommendations

Add the following test cases once the lock is implemented:

1. **Concurrent search**: Two coroutines call `search()` on the same `IMAPClient`; verify they complete without interleaving (mock `aioimaplib` and assert command sequence).
2. **SELECT state isolation**: One coroutine does `select_folder("A")` + `search()` while another does `select_folder("B")` + `search()`; verify each gets results from its own folder.
3. **Lock held during full operation**: Assert that `client._operation_lock.locked()` is `True` from the time the first IMAP command is sent until the response is fully parsed.
4. **Disconnect during operation**: Verify `disconnect()` waits for or cancels active operations gracefully.

---

## Action Items

| ID | Task | Priority | Owner |
|----|------|----------|-------|
| A1 | Rename `_lock` to `_connect_lock`, add `_operation_lock` to `IMAPClient` | Critical | Implementation |
| A2 | Wrap all public IMAP methods with `async with self._operation_lock` | Critical | Implementation |
| A3 | Verify no other async code paths interleave IMAP commands | High | Code Review |
| A4 | Add concurrent-operation tests for `IMAPClient` | High | Testing |
| A5 | Document checkout/checkin pool as future enhancement | Low | Documentation |
