# Security Review: simple-email-gw Package Extraction

**Date:** 2026-05-07
**Status:** Complete

## Executive Summary

The email MCP server is well-designed with robust security features including TLS 1.2 minimum enforcement, CRLF injection protection in critical paths, path traversal defenses with post-write verification, rate limiting, audit logging, and recipient whitelisting. The codebase is already standalone-ready with no C3-specific dependencies. However, several **HIGH and CRITICAL** vulnerabilities remain unaddressed that must be fixed before PyPI distribution.

---

## Critical Findings (CVSS 9.0-10.0)

### C1. IMAP Folder CRLF Injection (OWASP A03: Injection) - TODO.md H11

- **Location**: `email/src/email_mcp/imap/client.py:166-170,194-199,237-243`
- **Impact**: Folder names passed to `select()` without sanitization. Attackers with control over folder names (e.g., from malicious email metadata) could inject CRLF to execute arbitrary IMAP commands.
- **Remediation**: Add `sanitize_folder_name()` function similar to `sanitize_subject()`. Apply to all folder operations.
- **Reference**: [CWE-93: CRLF Injection](https://cwe.mitre.org/data/definitions/93.html)

### C2. Attachment Filename CRLF Injection (OWASP A03: Injection) - TODO.md H12

- **Location**: `email/src/email_mcp/smtp/client.py:307-311`
- **Impact**: `_add_attachments()` uses filename directly in `Content-Disposition` header without sanitization. Malicious filenames with CRLF can inject arbitrary email headers.
- **Remediation**: Add `sanitize_filename()` function. Apply before setting `Content-Disposition` header.
- **Reference**: [CWE-93: CRLF Injection](https://cwe.mitre.org/data/definitions/93.html)

---

## High Findings (CVSS 7.0-8.9)

### H1. IMAP Message ID Injection (OWASP A03: Injection) - TODO.md H13

- **Location**: `email/src/email_mcp/imap/client.py:243,305-307,324-325`
- **Impact**: Message IDs passed to `fetch()`, `move()`, `store()` without validation. While typically numeric, they could allow injection if server accepts non-numeric IDs.
- **Remediation**: Add `sanitize_message_id_numeric()` for IMAP operations. Validate that IDs are numeric or match expected format.
- **Reference**: [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)

### H2. Unbounded Attachment Size (OWASP A06: Insecure Design) - TODO.md M8

- **Location**: `email/src/email_mcp/smtp/client.py:296-311`
- **Impact**: `_add_attachments()` reads entire files into memory without size limits. Large attachments can cause OOM, enabling DoS attacks.
- **Remediation**: Add configurable `MAX_ATTACHMENT_SIZE` with streaming support. Reject oversized files before loading.
- **Reference**: [CWE-770: Allocation of Resources Without Limits](https://cwe.mitre.org/data/definitions/770.html)

### H3. Path Leakage in Error Messages (OWASP A01: Broken Access Control) - TODO.md M10

- **Location**: `email/src/email_mcp/server.py:227-228`
- **Impact**: `FileNotFoundError` sends full filesystem path to client. Internal paths may reveal directory structure.
- **Remediation**: Catch `FileNotFoundError` and return generic error message, logging details server-side.
- **Reference**: [CWE-209: Information Exposure Through Error Message](https://cwe.mitre.org/data/definitions/209.html)

### H4. Non-Monotonic Clock in Rate Limiter (OWASP A06: Insecure Design) - TODO.md H8

- **Location**: `email/src/email_mcp/safety/rate_limiter.py:31`
- **Impact**: `time.time()` is vulnerable to system clock jumps. NTP adjustments or manual changes can bypass rate limits or extend lockouts.
- **Remediation**: Replace with `time.monotonic()` for rate limiting logic.
- **Reference**: [CWE-366: Race Condition within a Thread](https://cwe.mitre.org/data/definitions/366.html)

### H5. Error Message Sanitization Gap (OWASP A09: Security Logging Failures) - TODO.md H5

- **Location**: `email/src/email_mcp/server.py:170-175`
- **Impact**: `download_attachment` passes raw exception message to user. May leak internal details like file paths, server names.
- **Remediation**: Use generic error messages for client, log full details server-side.
- **Reference**: [CWE-209: Information Exposure Through Error Message](https://cwe.mitre.org/data/definitions/209.html)

---

## Medium Findings (CVSS 4.0-6.9)

### M1. Dependency Pinning Strategy (OWASP A03: Supply Chain)

- **Location**: `email/requirements.txt:1-5`
- **Impact**: Dependencies use `>=` versioning without upper bounds. Breaking changes in dependencies could introduce vulnerabilities silently.
- **Remediation**: Pin exact versions for release, allow `>=` in development. Consider dependency locking with `uv.lock`.

### M2. Missing PyPI Security Configuration (OWASP A03: Supply Chain)

- **Impact**: PyPI packages should have security metadata: security policy, vulnerability reporting channel, signed releases.
- **Remediation**: Add `SECURITY.md` with disclosure process, enable PyPI 2FA, consider signed releases with Sigstore.

### M3. Credential Exposure in Environment Variables (OWASP A07: Authentication Failures)

- **Location**: `email/src/email_mcp/config.py:14-30`
- **Impact**: `.env` file loading with rudimentary parser. Secrets in environment variables may be logged or leaked in process listings.
- **Remediation**: Document that production deployments should use proper secret management (HashiCorp Vault, cloud KMS). Recommend `python-dotenv` as required dependency for development.

### M4. No Attachment Size Limits for IMAP Downloads (OWASP A06: Insecure Design)

- **Location**: `email/src/email_mcp/imap/client.py:352-427`
- **Impact**: `download_attachment()` fetches `BODY.PEEK[]` (entire message) to extract one attachment. Excessive memory/bandwidth consumption.
- **Remediation**: Use `BODYSTRUCTURE` to find part number, fetch only `BODY.PEEK[<part>]` for the specific attachment.

### M5. OAuth2 Token Handling Without Refresh (OWASP A07: Authentication Failures)

- **Location**: `email/src/email_mcp/config.py:46`
- **Impact**: OAuth2 tokens are static access tokens without refresh mechanism. Expired tokens cause authentication failures.
- **Remediation**: Document that OAuth2 tokens must be long-lived app passwords, or implement OAuth2 refresh flow for short-lived tokens.

### M6. Missing Authentication for MCP Server (OWASP A01: Broken Access Control)

- **Location**: `email/src/email_mcp/server.py`
- **Impact**: MCP server has no authentication. Any process that can connect to the server can access all email accounts.
- **Remediation**: Document that MCP server should only be run in trusted environments. For production, consider API key or token authentication.

---

## Low Findings (CVSS 0.1-3.9)

### L1. Weak Email Address Validation (OWASP A03: Injection)

- **Location**: `email/src/email_mcp/smtp/client.py:26-49`
- **Impact**: Regex doesn't handle all valid addresses (quoted local parts, internationalized domains).
- **Remediation**: Consider using `email_validator` library for comprehensive validation.

### L2. Dead Code in Tool Definitions (OWASP A06: Insecure Design)

- **Location**: `email/src/email_mcp/tools/definitions.py:1-324`
- **Impact**: Pydantic classes not used by FastMCP. Increases attack surface unnecessarily.
- **Remediation**: Remove file or wire into build process.

### L3. Unexposed `forward_email` Method (OWASP A06: Insecure Design)

- **Location**: `email/src/email_mcp/smtp/client.py:235-250`
- **Impact**: Method exists but not exposed as MCP tool. Does not forward attachments - potential data loss.
- **Remediation**: Expose as tool or remove.

---

## Package Distribution Security

### Dependency Security

| Dependency | Version | Recommendation |
|------------|---------|----------------|
| fastmcp | >=3.0.0 | Pin exact version for release |
| aioimaplib | >=1.0.0 | Pin exact version for release |
| aiosmtplib | >=3.0.0 | Pin exact version for release |
| pydantic | >=2.0.0 | Pin exact version for release |
| pydantic-settings | >=2.0.0 | Pin exact version for release |

**Recommendations**:
1. Run `pip-audit` or `safety` check on all dependencies before release
2. Add `requirements-lock.txt` with exact versions and hashes
3. Enable Dependabot or similar for dependency updates
4. Use `uv.lock` for reproducible builds

### Version Pinning Strategy

```python
# Development (pyproject.toml)
dependencies = [
  "fastmcp>=3.0.0,<4.0.0",  # Major version constraint
  "aioimaplib>=1.0.0,<2.0.0",
  ...
]

# Release (lock file)
fastmcp==3.0.0 \
  --hash=sha256:...
```

### Secret Management for Package Users

**Current State**: Secrets loaded from environment variables or `.env` files.

**Requirements for Package Users**:
1. **Never** commit credentials to version control
2. Use `.env` files only for development
3. For production, use:
   - Environment variables injected by orchestration system
   - Secret management systems (HashiCorp Vault, AWS Secrets Manager)
   - Cloud KMS for OAuth2 tokens
4. Document `EMAIL_*` environment variable requirements

**Security Documentation Needed**:
- `SECURITY.md` with:
  - Secret management best practices
  - Vulnerability reporting process
  - Security update policy
  - Threat model for the package

---

## MCP Server Security Considerations

### Tool Exposure Risk Levels

| Tool | Risk Level | Mitigation |
|------|------------|------------|
| `list_accounts` | Low | Returns only name/username (no passwords) |
| `list_folders` | Low | IMAP metadata exposure |
| `search_emails` | Medium | Limit search scope, rate limiting |
| `get_email` | Medium | Contains sensitive content |
| `download_attachment` | **High** | Path traversal, malware |
| `send_email` | **High** | Phishing, spam vector |
| `reply_email` | **High** | Phishing vector |
| `move_email` | Medium | Data modification |
| `delete_email` | **High** | Data destruction |
| `mark_email_read` | Low | Metadata modification |

**Mitigation Requirements**:
- `download_attachment`: Workspace confinement (implemented), add size limits
- `send_email`/`reply_email`: Recipient whitelist (implemented), add content filtering
- `delete_email`: Require explicit confirmation in client
- All write operations: Audit logging (implemented)

### Authentication Requirements

**Current State**: No authentication for MCP server itself. Relies on transport security.

**Requirements**:
1. Document that server should only run on localhost or trusted network
2. For production deployments, recommend:
   - API key authentication
   - TLS for MCP transport (if supported)
   - Rate limiting at connection level
3. Consider adding authentication in future version

---

## Recommendations for Package Release

### Before PyPI Publication (Blocking)

1. **Fix C1, C2 (Critical CRLF Injection)**: Add folder name and attachment filename sanitization
2. **Fix H1 (IMAP Message ID)**: Add message ID validation
3. **Fix H4 (Rate Limiter)**: Replace `time.time()` with `time.monotonic()`
4. **Add SECURITY.md**: Vulnerability disclosure process, security policy
5. **Pin Dependencies**: Exact versions with hashes in lock file
6. **Run Dependency Audit**: `pip-audit` or `safety` check

### Before First Stable Release (High Priority)

1. **Fix H2 (Attachment Size)**: Add configurable size limits
2. **Fix H3, H5 (Error Messages)**: Sanitize error messages for client exposure
3. **Fix M4 (IMAP Optimization)**: Fetch specific attachment parts
4. **Document Secret Management**: Add security documentation for users
5. **Add API Stability Guarantees**: Document public API surface

### Future Enhancements (Medium Priority)

1. **MCP Authentication**: Consider API key or token authentication
2. **OAuth2 Refresh Flow**: Support short-lived tokens with refresh
3. **Internationalized Email**: Support IDN domains in email validation
4. **Remove Dead Code**: Clean up `tools/definitions.py`
5. **Improve Test Coverage**: Add integration tests for IMAP/SMTP operations

---

## Security Testing Requirements

### Required Before Release

1. **Static Analysis**: Run `bandit` on all Python files
2. **Dependency Scan**: Run `pip-audit` or `safety`
3. **Secret Scan**: Run `detect-secrets` or `trufflehog`
4. **CRLF Injection Tests**: Add tests for folder names, filenames
5. **Fuzz Testing**: Fuzz IMAP/SMTP inputs with malformed data

### Ongoing Security Testing

1. **CI/CD Integration**: Run security scans on every PR
2. **Dependency Updates**: Automated PR for security updates
3. **CVE Monitoring**: Subscribe to security advisories for dependencies
4. **Penetration Testing**: Annual security review for production deployments

---

## Summary Classification

| Finding | Classification | Action |
|---------|---------------|--------|
| IMAP folder CRLF injection | **Blocking** | Fix in current task |
| Attachment filename CRLF injection | **Blocking** | Fix in current task |
| IMAP message ID validation | **Blocking** | Fix in current task |
| Rate limiter non-monotonic clock | **Blocking** | Fix in current task |
| Unbounded attachment size | Related | Add to current task scope |
| Path leakage in errors | Related | Add to current task scope |
| Error message sanitization | Related | Add to current task scope |
| Dependency pinning | Related | Configure for release |
| Missing PyPI security config | New | Add to backlog |
| OAuth2 token handling | New | Document limitation |
| MCP authentication | New | Add to backlog as future enhancement |