# Security Review: simple-email-gw Package

**Date:** 2026-05-07
**Status:** ❌ Security Issues Identified - Blocking Release

## Executive Summary

The simple-email-gw package has one security fix implemented (rate limiter using monotonic clock) but **four critical/high vulnerabilities remain unaddressed**. The package requires security hardening before PyPI distribution.

---

## Issues Fixed ✅

### H4: Rate Limiter Uses Monotonic Clock

**Status:** ✅ **IMPLEMENTED CORRECTLY**

**Location:** `src/simple_email_gw/safety/rate_limiter.py:31,53,54`

The rate limiter correctly uses `time.monotonic()` for all time measurements.

---

## Issues Still Open ❌

### C1: IMAP Folder CRLF Injection (CRITICAL - NOT FIXED)

**Status:** ❌ **NOT IMPLEMENTED**

**Location:** `src/simple_email_gw/imap/client.py:170,196,237,285,318,341,374`

**Impact:** Folder names passed directly to `client.select()` without sanitization across 7 methods.

**Remediation:** Create `sanitize_folder_name()` function and apply to all folder operations.

### C2: Attachment Filename CRLF Injection (CRITICAL - NOT FIXED)

**Status:** ❌ **NOT IMPLEMENTED**

**Location:** `src/simple_email_gw/smtp/client.py:307-311`

**Impact:** Filenames inserted directly into `Content-Disposition` header without sanitization.

**Remediation:** Create `sanitize_filename()` function and apply in `_add_attachments()`.

### H1: IMAP Message ID Validation (HIGH - NOT FIXED)

**Status:** ❌ **NOT IMPLEMENTED**

**Location:** `src/simple_email_gw/imap/client.py:243,292,305,324,348,379`

**Impact:** Message IDs passed to IMAP commands without validation.

**Remediation:** Create `sanitize_message_id_numeric()` function and apply to all message operations.

### H3: Path Leakage in Error Messages (MEDIUM - PARTIALLY FIXED)

**Status:** ⚠️ **PARTIALLY IMPLEMENTED**

**Location:** `server.py:230-231` - Passes full FileNotFoundError message to client.

**Remediation:** Catch FileNotFoundError and return generic message.

### H2: Unbounded Attachment Size (HIGH - NOT FIXED)

**Status:** ❌ **NOT IMPLEMENTED**

**Location:** `src/simple_email_gw/smtp/client.py:303`

**Remediation:** Add configurable `MAX_ATTACHMENT_SIZE` with streaming support.

### M1: Dependency Pinning (MEDIUM - NOT FIXED)

**Status:** ❌ **NOT IMPLEMENTED**

**Remediation:** Pin exact versions with upper bounds in pyproject.toml.

---

## Recommended Actions

### Immediate (Blocking Release)

1. Fix C1: Add `sanitize_folder_name()`
2. Fix C2: Add `sanitize_filename()`
3. Fix H1: Add `sanitize_message_id_numeric()`
4. Fix H3: Fix path leakage in error messages

### High Priority (Before Stable Release)

5. Fix H2: Add attachment size limits
6. Fix M1: Pin dependencies with upper bounds

---

## Classification Summary

| Finding | Status | Action |
|---------|--------|--------|
| IMAP folder CRLF injection | ❌ Blocking | Fix before release |
| Attachment filename CRLF injection | ❌ Blocking | Fix before release |
| IMAP message ID validation | ❌ Blocking | Fix before release |
| Rate limiter monotonic clock | ✅ Fixed | No action needed |
| Path leakage in errors | ❌ Blocking | Fix in current task |
| Unbounded attachment size | Related | Add to scope |
| Dependency pinning | Related | Configure for release |