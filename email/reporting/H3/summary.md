# Task Summary: H3 - Tighten IMAP Criteria Regex

## What Was Implemented

Fixed IMAP search criteria validation regex by removing single quotes and adding valid IMAP characters.

## Location

- **File**: `src/email_mcp/imap/client.py`
- **Lines**: 26-29

## Changes

### Before
```python
# IMAP search criteria validation
IMAP_CRITERIA_PATTERN = re.compile(r"^[\w\s\(\)\*\<\>\[\]=!\"'-]+$")
```

### After
```python
# IMAP search criteria validation
# Single quotes removed - not part of IMAP string syntax (RFC 3501 uses double quotes only)
# Added @ . : % \ for valid IMAP SEARCH syntax (email addresses, dates, flags)
IMAP_CRITERIA_PATTERN = re.compile(r"^[\w\s\(\)\*\<\>\[\]=!\"@\.:%\\-]+$")
```

## Key Decisions

1. **Removed single quote (`'`)**: Not part of IMAP string syntax per RFC 3501 - servers use double quotes only
2. **Added `@`**: For email addresses (e.g., `FROM test@example.com`)
3. **Added `.`**: For domain names and header parts
4. **Added `:`**: For header extensions
5. **Added `%`**: For wildcards in SEARCH extensions
6. **Added `\`**: For flag prefixes (e.g., `\Seen`, `\Deleted`)

## Tests Added

`tests/test_imap_client.py::TestIMAPCriteriaValidation` (6 tests):
- `test_valid_criteria_with_double_quotes`: Verifies double quotes work
- `test_valid_criteria_all`: Verifies simple criteria
- `test_valid_criteria_date_format`: Verifies date syntax
- `test_single_quote_rejected`: Verifies single quotes rejected
- `test_injection_attempt_rejected`: Verifies IMAP injection blocked
- `test_special_characters_allowed`: Verifies valid IMAP syntax accepted

## Files Modified

| File | Change |
|------|--------|
| `src/email_mcp/imap/client.py` | Updated regex pattern |
| `tests/test_imap_client.py` | Added 6 tests for criteria validation |
| `TODO.md` | Marked H3 as complete |
| `docs/bug-analysis/H3.md` | Bug analysis report |

## Lessons Learned

- IMAP protocol uses double quotes for strings, not single quotes
- Input validation regex should match actual protocol requirements
- Defense in depth: validation happens before server-side processing

## Risk Assessment

**Low risk, defense-in-depth improvement**:
- Single quote removal prevents potential injection on non-standard servers
- Added characters are all valid IMAP syntax per RFC 3501
- No breaking changes to existing functionality