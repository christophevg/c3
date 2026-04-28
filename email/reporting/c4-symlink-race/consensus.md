# Consensus Summary: C4 - Attachment Download Symlink Race Fix

**Date**: 2026-04-28
**Task**: Fix TOCTOU vulnerability in `download_attachment()`

---

## Agent Agreement

Both domain agents (security-engineer, api-architect) **agree** on the recommended approach:

### Core Solution: Post-Write Verification

1. Use `os.path.realpath()` to resolve all symlinks after file write
2. Verify the real path is within the real workspace
3. Clean up escaped files if verification fails
4. Raise `SecurityError` for security violations

### Key Decisions

| Decision | Agents | Rationale |
|----------|--------|-----------|
| Post-write verification approach | Both | Minimal code change, catches all symlink escapes |
| `os.path.realpath()` for resolution | Both | Resolves symlinks at verification time, not check time |
| New `SecurityError` exception | Both | Distinct from generic errors, allows specific handling |
| File cleanup on violation | Both | Remove escaped files before raising error |
| Generic error message to client | Both | Don't leak internal paths |

### Implementation Steps

1. Add `SecurityError` exception class
2. Update `download_attachment()` with post-write verification
3. Update `server.py` to catch `SecurityError` and return generic error
4. Add symlink escape detection tests
5. Add audit logging for security violations

---

## Additional Considerations

### From Security Engineer

- Consider workspace path validation at startup
- Add tests for symlink detection
- Document the security rationale

### From API Architect

- SMTP attachment uploads have similar vulnerability (M8)
- Apply same pattern to SMTP in future work
- No breaking changes to MCP tool interface

---

## Files to Modify

| File | Changes |
|------|---------|
| `src/email_mcp/errors.py` | Add `SecurityError` exception |
| `src/email_mcp/imap/client.py` | Add post-write verification |
| `src/email_mcp/server.py` | Catch `SecurityError`, log internally |
| `tests/test_imap_client.py` | Add symlink escape tests |

---

## Approval

✅ Security Engineer: Agrees with post-write verification approach
✅ API Architect: Agrees with minimal change, no breaking changes

**Ready for implementation planning.**