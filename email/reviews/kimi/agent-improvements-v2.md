# Proposed Improvements to c3:code-reviewer Agent

**Date**: 2026-04-28
**Context**: After comparing two independent code reviews of the email MCP server, significant gaps were identified. Both reviews missed different categories of issues. This document proposes concrete improvements to the agent's review process to ensure comprehensive coverage.

---

## Executive Summary

The comparison of Kimi vs Qwen reviews revealed that **no single review caught all issues**. The gaps fall into four categories:

1. **Cross-method security comparison** — Checking that security controls in one method are present in related methods
2. **Exception hierarchy analysis** — Verifying `except` clauses don't catch control signals
3. **Header/payload injection** — Checking user input that flows into headers, commands, or structured data
4. **Pattern consistency** — Ensuring related methods follow the same error handling, return type, and validation patterns

**These are exactly the kinds of issues that require explicit comparison prompts or grep-based checks. They cannot be reliably caught by reading files sequentially.**

---

## New Checklist Sections

### Section A: Cross-Method Security Comparison (NEW — High Impact)

**Purpose**: Ensure security controls applied to one method are not missing from related methods in the same class.

**Checklist**:
- [ ] For each class with multiple public methods, identify all security checks (validation, sanitization, authorization, rate limiting)
- [ ] Verify each security check is present in ALL methods that perform the same category of operation
- [ ] Flag methods that bypass controls present in sibling methods

**Prompt Template**:
```markdown
## Cross-Method Security Comparison

For each class that performs security-sensitive operations:

1. List all public methods and categorize them by operation type (read, write, delete, send, etc.)
2. For each method, identify every security check performed:
   - Input validation (format, range, type)
   - Authorization (whitelists, permissions)
   - Sanitization (escaping, encoding)
   - Rate limiting
   - Audit logging
3. Compare the security check lists across methods of the same category
4. Flag any method that is missing a security check present in a sibling method

Example: If `send_email()` validates recipients against a whitelist, does `reply_email()` also check the whitelist?
```

**Detection Strategy**:
```bash
# Find classes with multiple public methods
grep -n "async def " src/email_mcp/smtp/client.py

# For each method, extract the first 20 lines (where validation typically lives)
# Compare validation patterns across methods
```

**Catch Rate**: Would have caught:
- `reply_email()` whitelist bypass (Qwen C3)
- `reply_email()` missing `validate_email()` (Kimi T2)

---

### Section B: Exception Hierarchy Analysis (NEW — High Impact)

**Purpose**: Prevent `except` clauses from catching control signals or hiding error context.

**Checklist**:
- [ ] Flag all bare `except Exception:` clauses
- [ ] Verify they don't catch `KeyboardInterrupt`, `SystemExit`, or `GeneratorExit`
- [ ] Check that `except Exception:` is not used where `except StandardError:` or specific exceptions would suffice
- [ ] Verify original exception chains are preserved with `raise ... from e`

**Prompt Template**:
```markdown
## Exception Hierarchy Check

1. Find all `except Exception:` clauses in the codebase
2. For each one, verify:
   - Does it need to catch EVERYTHING, or would specific exceptions suffice?
   - Could a `KeyboardInterrupt` or `SystemExit` reach this handler?
   - Is the original exception preserved with `raise ... from e`?
3. Find all `except Exception as e: raise NewError(str(e))` patterns
4. Verify the original exception chain is not broken

Command: `grep -rn "except Exception:" src/`
```

**Catch Rate**: Would have caught:
- Bare `except Exception` catching signals (Qwen H1)
- Exception swallowing in SMTP client (Qwen C1 / Kimi H2)
- Exception swallowing in auth (Qwen C2 / Kimi H3)

---

### Section C: Header / Command / Payload Injection (NEW — Critical Impact)

**Purpose**: Identify user input that flows into structured contexts (email headers, IMAP commands, SQL queries, file paths) without sanitization.

**Checklist**:
- [ ] Trace user input parameters into header assignments (email, HTTP, etc.)
- [ ] Check for CRLF (`\r\n`) sanitization before header assignment
- [ ] Check for command injection in protocol commands (IMAP, SMTP, SQL)
- [ ] Verify regex-based validation actually blocks injection payloads
- [ ] Test regex patterns against a corpus of injection attempts

**Prompt Template**:
```markdown
## Injection Analysis

For each protocol client (IMAP, SMTP, etc.):

1. Identify all user-provided parameters that flow into protocol commands or headers
2. For email headers (Subject, To, From, In-Reply-To, References):
   - Is CRLF (`\r\n`) stripped before assignment?
   - Are newlines (`\n`) sanitized?
3. For IMAP commands:
   - Is the search criteria regex tested against injection payloads?
   - Does it block single quotes, backslashes, and other metacharacters?
4. For file paths:
   - Is path traversal blocked (basename, realpath)?
   - Is there a time-of-check vs time-of-use race?

Test payloads for regex validation:
- `' OR '1'='1`
- `\r\nInjected-Header: value`
- `../../../etc/passwd`
- `ALL) OR (1=1`
```

**Detection Strategy**:
```bash
# Find header assignments with user input
grep -rn 'msg\[.*\] = ' src/email_mcp/smtp/client.py

# Find regex patterns
grep -rn "re.compile" src/

# Find IMAP command construction
grep -rn "client\.search\|client\.fetch\|client\.store" src/
```

**Catch Rate**: Would have caught:
- CRLF injection in `reply_email()` (Qwen H2)
- IMAP regex allowing single quotes (Qwen H3)
- Symlink race in attachment download (Qwen C4)

---

### Section D: Pattern Consistency Analysis (NEW — Medium Impact)

**Purpose**: Ensure related methods follow consistent patterns for error handling, return types, and validation.

**Checklist**:
- [ ] Compare return types across methods in the same class
- [ ] Compare error handling patterns (raise vs return vs silent)
- [ ] Compare validation sequences across similar entry points
- [ ] Check for redundant calls (method A calls method B, then caller also calls B)

**Prompt Template**:
```markdown
## Pattern Consistency Check

For each class, analyze all public methods:

1. **Return Types**: List the return type of each method
   - Do methods in the same category return the same shape?
   - Example: Do all mutation tools return `{status, message_id}`?

2. **Error Handling**: For each method, note the error pattern:
   - Returns `True` / `False`
   - Returns `bool` based on status
   - Raises specific exception
   - Raises generic exception
   - Returns partial data silently
   - Flag inconsistencies

3. **Redundant Calls**: Trace the call graph:
   - Does method A call method B?
   - Does the caller of A also call B?
   - Example: `select_folder()` calls `connect()`. Does `search()` call `connect()` again after calling `select_folder()`?

4. **Validation Sequence**: Compare the first N lines of each method
   - Are validation steps in the same order?
   - Are any validation steps missing from any method?
```

**Detection Strategy**:
```bash
# Extract return statements from a class
sed -n '/class SMTPClient/,/^class /p' src/email_mcp/smtp/client.py | grep -n "return"

# Extract error handling patterns
sed -n '/class IMAPClient/,/^class /p' src/email_mcp/imap/client.py | grep -n "raise\|return True\|return False"

# Find methods that call connect()
grep -n "await self.connect()" src/email_mcp/imap/client.py
```

**Catch Rate**: Would have caught:
- Inconsistent error handling patterns (Qwen MAINT-5)
- Redundant `select_folder()` + `connect()` calls (Qwen MAINT-6)
- Inconsistent tool return types (Qwen MAINT-7)

---

### Section E: Literal Value Extraction (NEW — Low Impact, High Frequency)

**Purpose**: Identify repeated string and number literals that should be constants.

**Checklist**:
- [ ] Find string literals repeated 3+ times in the same file
- [ ] Find number literals used as thresholds or defaults
- [ ] Check if literals are already defined as constants elsewhere
- [ ] Suggest constant names for repeated values

**Prompt Template**:
```markdown
## Magic Value Detection

1. For each source file, find string literals repeated 3+ times:
   `grep -o '"[^"]*"' file.py | sort | uniq -c | sort -rn | head -20`

2. For each source file, find number literals that look like configuration:
   `grep -oE '\b[0-9]+\b' file.py | sort | uniq -c | sort -rn | head -20`

3. Check if these literals are:
   - Protocol constants (IMAP flags, folder names)
   - Default values (limits, timeouts)
   - Error codes or status strings

4. Suggest extracting to module-level constants
```

**Catch Rate**: Would have caught:
- `\Deleted` repeated in `move_message` and `delete_message` (Qwen L6)
- `INBOX` repeated across method signatures (Qwen L7)
- `ALL` repeated as search default (Qwen L8)
- `50` and `500` as search limits (Qwen L1)

---

### Section F: Tool Registration Verification (NEW — Medium Impact)

**Purpose**: Ensure all public methods in client classes are exposed as MCP tools.

**Checklist**:
- [ ] List all public methods in client classes
- [ ] Search for each method name in `server.py`
- [ ] Flag methods with no corresponding `@mcp.tool` decorator
- [ ] Flag `@mcp.tool` decorators with no corresponding client method

**Prompt Template**:
```markdown
## Tool Registration Verification

1. List all public methods in each client class:
   `grep -n "async def " src/email_mcp/imap/client.py`
   `grep -n "async def " src/email_mcp/smtp/client.py`

2. For each method, check if it's called in `server.py`:
   `grep -n "method_name" src/email_mcp/server.py`

3. List all `@mcp.tool` decorated functions:
   `grep -n "@mcp.tool" src/email_mcp/server.py`

4. For each tool, verify it calls a client method (not inline logic)

5. Flag methods that exist in clients but have no tool wrapper
```

**Catch Rate**: Would have caught:
- `forward_email()` exists but not exposed as tool (Qwen M6)

---

### Section G: Framework Constructor Completeness (NEW — Low Impact)

**Purpose**: Ensure framework objects are configured with all relevant optional parameters.

**Checklist**:
- [ ] Check FastMCP/Flask/Django constructors for missing `description`
- [ ] Check Pydantic Settings for missing `env_prefix` or `case_sensitive`
- [ ] Check async clients for missing `timeout` or `retry` parameters

**Prompt Template**:
```markdown
## Framework Constructor Check

For each framework object instantiation:

1. Identify the framework class (FastMCP, Flask, BaseSettings, etc.)
2. Look up the constructor signature in the framework documentation
3. Check which optional parameters are commonly recommended:
   - `description` for MCP servers
   - `title` / `version` for API frameworks
   - `validate_assignment` for Pydantic models
   - `frozen` for immutable configs
4. Flag missing optional parameters that would improve usability
```

**Catch Rate**: Would have caught:
- FastMCP server missing description (Qwen M2)

---

### Section H: Prompt Security Review (NEW — Medium Impact)

**Purpose**: Ensure MCP prompt templates don't encourage insecure behavior.

**Checklist**:
- [ ] Check prompt templates for guidance about sensitive data (credentials, PII)
- [ ] Verify prompts don't suggest actions that could leak data
- [ ] Check for prompt injection vulnerabilities (user content inserted without escaping)

**Prompt Template**:
```markdown
## Prompt Security Check

For each `@mcp.prompt` decorated function:

1. Read the prompt template content
2. Check if it handles sensitive data:
   - Does it warn against including passwords/tokens?
   - Does it suggest sanitizing PII?
3. Check for prompt injection risks:
   - Is user content inserted with f-string formatting?
   - Could the user content override system instructions?
4. Suggest security guidance to add to the prompt
```

**Catch Rate**: Would have caught:
- Prompt templates lack PII/credential guidance (Qwen M5)

---

### Section I: Time-of-Check vs Time-of-Use (TOCTOU) (NEW — High Impact)

**Purpose**: Identify filesystem or state checks that are not atomic with the subsequent use.

**Checklist**:
- [ ] Find patterns where a path is validated, then used later
- [ ] Check if symlink races are possible between validation and use
- [ ] Verify `os.path.realpath()` is used before validation
- [ ] Check if file existence checks are followed by file operations

**Prompt Template**:
```markdown
## TOCTOU Race Condition Check

Find all filesystem operations with this pattern:

```python
# Validation
if is_valid(path):
    # Use
    with open(path) as f:
        ...
```

Questions:
1. Can `path` change between `is_valid()` and `open()`?
2. Is `os.path.realpath()` used to resolve symlinks?
3. Is the validation check atomic with the use?
4. Could an attacker create a symlink between check and use?

Fix pattern:
```python
real_path = os.path.realpath(path)
if is_within_workspace(real_path):
    with open(real_path) as f:
        ...
```
```

**Catch Rate**: Would have caught:
- Attachment download symlink race (Qwen C4)

---

## Integration into Agent Definition

Add these sections to the code-reviewer agent's **Review Checklist**:

```markdown
### Structural Quality & Duplication (Existing)
- [ ] DRY principle followed
- [ ] No dead code or unused imports
- [ ] ...

### Cross-Method Security (NEW)
- [ ] Security checks are consistent across related methods
- [ ] No method bypasses controls present in siblings

### Exception Safety (NEW)
- [ ] Bare `except Exception:` flagged and justified
- [ ] Original exception chains preserved with `raise ... from e`
- [ ] Control signals (`KeyboardInterrupt`) not caught

### Injection Prevention (NEW)
- [ ] User input sanitized before header/command insertion
- [ ] Regex validation tested against injection payloads
- [ ] Path traversal blocked with realpath + basename

### Pattern Consistency (NEW)
- [ ] Related methods have consistent return types
- [ ] Error handling patterns uniform across a class
- [ ] No redundant nested calls (A calls B, caller also calls B)

### Magic Value Detection (NEW)
- [ ] Repeated literals (3+) extracted as constants
- [ ] Default values named, not inlined

### Tool Registration (NEW)
- [ ] All client methods have corresponding tool wrappers
- [ ] No orphaned tools or dead client methods

### Framework Completeness (NEW)
- [ ] Constructors include recommended optional parameters
- [ ] Prompts include security guidance

### TOCTOU Safety (NEW)
- [ ] Path validation uses realpath before check
- [ ] Validation and use are atomic or race-safe
```

---

## Concrete Grep Commands to Add

Add these commands to the agent's **tool usage instructions**:

```markdown
## Mandatory Grep Commands for Every Review

### Security
```bash
# Find bare except Exception
grep -rn "except Exception:" src/

# Find header assignments with user input
grep -rn '\[.*\] = .*[^"]' src/email_mcp/smtp/client.py

# Find regex patterns
grep -rn "re.compile(" src/

# Find path validation patterns
grep -rn "relative_to\|realpath\|resolve" src/
```

### Consistency
```bash
# Find all return statements in a class
sed -n '/class IMAPClient/,/^class /p' src/email_mcp/imap/client.py | grep -n "return"

# Find methods that call the same helper
grep -n "await self.connect()" src/email_mcp/imap/client.py

# Find error handling patterns
grep -n "raise\|return True\|return False" src/email_mcp/imap/client.py
```

### Dead Code
```bash
# Find modules never imported
grep -rn "from email_mcp.tools" src/  # Should show imports

# Find methods never called
for method in $(grep -oP 'async def \K\w+' src/email_mcp/smtp/client.py); do
  count=$(grep -rn "\.$method(" src/email_mcp/server.py | wc -l)
  if [ "$count" -eq 0 ]; then echo "Orphaned: $method"; fi
done
```

### Magic Values
```bash
# Repeated string literals
for file in src/email_mcp/**/*.py; do
  echo "=== $file ==="
  grep -oE '"[^"]{3,}"' "$file" | sort | uniq -c | sort -rn | head -5
done

# Number literals that might be configuration
grep -rnE '\b(50|100|500|1000|3600)\b' src/
```
```

---

## Why These Were Missed (Root Causes)

| Issue Category | Why Both Agents Missed It | Solution |
|----------------|---------------------------|----------|
| Cross-method security | Agents read methods in isolation; no explicit prompt to compare sibling methods | Add "Cross-Method Security Comparison" checklist |
| Exception hierarchy | Focused on error message quality, not exception taxonomy | Add "Exception Safety" checklist with `KeyboardInterrupt` check |
| Header injection | Looked at parameter validation but not header assignment flows | Add "Injection Prevention" checklist with header-specific checks |
| Pattern consistency | Looked for duplication but not inconsistency | Add "Pattern Consistency Analysis" with return type/error handling comparison |
| Magic values | No prompt to look for repeated literals | Add "Magic Value Detection" grep commands |
| TOCTOU races | Looked at path validation but not timing | Add "TOCTOU Safety" checklist with `realpath` requirement |
| Tool registration | No prompt to verify client methods are exposed | Add "Tool Registration Verification" step |
| Prompt security | Skipped prompt templates as "not code" | Add "Prompt Security Review" checklist |

---

## Implementation Priority

| Priority | Improvement | Files to Modify | Effort | Impact |
|----------|-------------|----------------|--------|--------|
| **P0** | Add "Cross-Method Security Comparison" section | `agents/code-reviewer.md` | Low | Critical (catches whitelist bypass) |
| **P0** | Add "Exception Safety" section with `KeyboardInterrupt` check | `agents/code-reviewer.md` | Low | Critical |
| **P0** | Add "Injection Prevention" section with header/command checks | `agents/code-reviewer.md` | Low | Critical |
| **P1** | Add mandatory grep commands to tool instructions | `agents/code-reviewer.md` | Low | High |
| **P1** | Add "Pattern Consistency Analysis" section | `agents/code-reviewer.md` | Low | High |
| **P1** | Add "TOCTOU Safety" section | `agents/code-reviewer.md` | Low | High |
| **P2** | Add "Tool Registration Verification" section | `agents/code-reviewer.md` | Low | Medium |
| **P2** | Add "Magic Value Detection" grep commands | `agents/code-reviewer.md` | Low | Medium |
| **P2** | Add "Prompt Security Review" section | `agents/code-reviewer.md` | Low | Medium |
| **P3** | Add "Framework Constructor Completeness" section | `agents/code-reviewer.md` | Low | Low |

---

## Testing the Improved Agent

To validate these improvements, re-run the agent on the email MCP server with the new checklist and verify it catches:

- [ ] `reply_email()` whitelist bypass
- [ ] Bare `except Exception` catching signals
- [ ] CRLF injection in `reply_email()` headers
- [ ] IMAP regex single quote issue
- [ ] Inconsistent error handling in IMAP methods
- [ ] Redundant `select_folder()` + `connect()` calls
- [ ] Inconsistent tool return types
- [ ] Magic strings (`\Deleted`, `INBOX`, `ALL`)
- [ ] `forward_email()` not exposed as tool
- [ ] Attachment download symlink race
- [ ] FastMCP missing description
- [ ] Prompt templates lacking security guidance
