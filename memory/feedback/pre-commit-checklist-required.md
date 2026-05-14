# Pre-Commit Checklist Required

**Date**: 2026-05-14
**Context**: Roomz I1-001 - User blocked commit for lacking validation

## Lesson Learned

**NEVER propose commit without validating ALL of these:**

1. ✅ **UV setup validated**
   - `uv sync` works
   - Package imports successfully
   - Tests can collect

2. ✅ **Tests pass or skip**
   - `uv run pytest -v` shows all tests passing or skipped
   - NO tests with `pass` or `assert True`
   - NO test failures

3. ✅ **Application runs**
   - `make run` works
   - Or `uv run gunicorn ...` works
   - Application loads without errors

4. ✅ **README documented**
   - README follows `c3:readme` skill
   - End-user can follow it without questions
   - Contains: Title, Quick Start, How to Run, How to Test

5. ✅ **Makefile exists**
   - Contains at least: `test`, `run` targets
   - All commands use `uv run`

6. ✅ **User acceptance completed**
   - User explicitly confirmed: "I tested it and it works"
   - User has NOT said "there's an issue" or "it doesn't work"

## Workflow

**Before Phase 6 (Commit):**

```
Phase 5f: Pre-Commit Verification
  → Verify all tests pass
  → Verify app runs
  → Verify README complete
  → Verify Makefile exists

Phase 5g: User Acceptance Testing
  → Present README to user
  → Ask user to test
  → Get explicit approval
  → ONLY THEN proceed to Phase 6
```

## User Corrections from Session

**User said:**
- "we're standardizing on uv as single python project management tool"
- "before a commit is proposed a clear checklist must be validated"
- "has the user accepted the current implementation?"
- "all tests should work with every commit"
- "test stubs should be marked as skipped"

**Why This Matters:**
- Without validation, commits may include broken code
- Without user testing, features may not work as intended
- Without README, users can't run the application
- Without checklist, steps get missed

## Memory Impact

This affects all future sessions:

**In `c3:project-manager` agent:**
- Added Phase 5g: User Acceptance Testing (MANDATORY)
- Must get explicit user approval before Phase 6

**In `c3:python-project` skill:**
- Added Phase 0: UV Setup Validation
- Must validate setup before any implementation

**In `c3:readme` skill:**
- Added End-User First philosophy
- Added validation checklist

**In `c3:testing-engineer` agent:**
- Added Test Quality Standard
- Tests must pass or be properly skipped

**In project memory:**
- UV is primary tool
- All commands use `uv run`