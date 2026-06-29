---
name: bug-hunting
description: Systematic bug hunting workflow for finding edge cases and hidden bugs. Use after implementing features, before releases, or when asked to find bugs, probe for holes, or stress-test code. Examples: "hunt for edge cases", "what could go wrong", "stress-test config parsing".
---

# Bug Hunting

Systematic workflow for finding edge cases and hidden bugs before they reach production.

## Overview

| Capability | Description |
|------------|-------------|
| Architecture analysis | Understand codebase structure before hunting |
| Edge case generation | Systematically probe for boundary conditions |
| Test-driven fixing | Write tests before implementing fixes |
| Severity prioritization | Rank bugs by impact and fix effort |
| Real-world validation | Test against actual project schemas |

## When to Use This Skill

Use this skill when:
- User asks to "find bugs", "hunt for edge cases", "probe for holes"
- After implementing a feature (verification hunting)
- Before releasing (pre-release hunting)
- User says "what could go wrong?"
- User wants to stress-test code or configuration

## Bug Hunting Workflow

### Phase 1: Architecture Understanding

Before hunting, understand what you're hunting in:

**1. Read Core Documentation:**
- `CLAUDE.md` - Project conventions and patterns
- `AGENTS.md` - Best practices and testing patterns
- `README.md` - Usage examples and common patterns
- Architecture diagrams or design docs

**2. Identify Key Data Flows:**
- Where does data enter the system?
- What transformations happen?
- Where does data exit or get stored?
- What are the boundaries between components?

**3. Map Critical Paths:**
- Happy path (expected usage)
- Alternative paths (valid but less common)
- Error paths (how failures are handled)
- Edge case paths (boundary conditions)

**4. Document Assumptions:**
- What does the code assume about input?
- What implicit contracts exist?
- What dependencies are assumed?

**Example from Clevis session:**
```
Architecture Understanding:
- Core: @configclass decorator transforms dataclasses into config loaders
- Flow: TOML file → extract section → resolve defaults → validate types → instantiate
- Key boundaries: Decorator application, TOML extraction, type coercion
- Assumptions: TOML sections exist, types match, field names don't conflict
```

### Phase 2: Core Bug Identification

Systematically find existing bugs:

**1. Trace Critical Operations:**
```python
# For each critical operation:
def critical_operation(data):
  # Trace: What does this assume?
  # Trace: What could go wrong?
  # Trace: What edge cases exist?
```

**2. Check Error Handling:**
- Are all exceptions caught?
- Are errors logged with context?
- Do errors provide actionable messages?
- Is cleanup handled on failure?

**3. Validate Assumptions:**
- What if input is None?
- What if input is wrong type?
- What if input is empty?
- What if input is too large?
- What if input has unexpected structure?

**4. Test Boundary Conditions:**
- Empty collections vs None
- Single element vs multiple
- Minimum vs maximum values
- Unicode vs ASCII
- Nested vs flat structures

**Example bug found in Clevis:**
```python
# Assumption: TOML section for subcommand exists
# Reality: Section might be missing, code crashed
# Bug: Silent failure when TOML section not found

# Found by asking: "What if subcommand config is missing from TOML?"
```

### Phase 3: Test-Driven Fixing

**CRITICAL: Write tests BEFORE fixing bugs.**

**1. Create Failing Test:**
```python
def test_bug_name():
  """Bug: [Description of bug]
  
  Expected: [What should happen]
  Actual: [What currently happens]
  """
  # Arrange - Set up minimal reproduction
  config_data = {...}
  
  # Act - Trigger the bug
  result = operation(config_data)
  
  # Assert - Current behavior (test passes, proving bug exists)
  assert result.has_issue  # Documents current broken behavior
```

**2. Verify Test Reproduces Bug:**
```bash
pytest tests/test_bug.py -v
# Should PASS (proving bug exists)
```

**3. Implement Minimal Fix:**
- Change only what's necessary
- Don't refactor while fixing
- Keep change scope minimal

**4. Update Test to Expect Correct Behavior:**
```python
def test_bug_name():
  # ... arrange and act same as before
  
  # Assert - Expected behavior (test should now pass)
  assert result.is_correct  # Expects fixed behavior
```

**5. Verify Fix:**
```bash
pytest tests/test_bug.py -v
# Should PASS (proving fix works)
```

**Test Stub Workflow (when working with testing-engineer):**
```
tests/test_{module}_{feature}.py  ←  Created by testing-engineer (FAILING)
        ↓
You read stubs to understand expected behavior
        ↓
You implement the feature
        ↓
You UPDATE stubs to real test assertions
        ↓
All tests transition from FAIL → PASS
```

### Phase 4: Edge Case Hunting

After fixing known bugs, hunt for unknown ones:

**Categories of Edge Cases:**

#### Input Boundaries
- Empty inputs (`[]`, `{}`, `""`, None)
- Single element (`[x]`, `{k: v}`, `"a"`)
- Maximum sizes (memory limits, overflow)
- Special characters (unicode, control chars, delimiters)
- Encodings (UTF-8, UTF-16, ASCII)

#### Configuration Edge Cases
- Missing sections/keys
- Empty files
- Wrong types (string where number expected)
- Circular references
- Deep nesting (recursion limits)
- Duplicate keys
- Invalid values

#### Concurrency Edge Cases
- Race conditions (TOCTOU bugs)
- Resource contention
- Deadlocks
- Thread safety violations

#### Security Edge Cases
- Injection attacks (SQL, command, path)
- Path traversal
- Privilege escalation
- Resource exhaustion (DoS)
- Input validation bypasses

#### Integration Edge Cases
- Missing dependencies
- Version mismatches
- Network failures
- Timeout scenarios
- Partial failures

#### Performance Edge Cases
- Large inputs (memory/timeout)
- Deeply nested structures
- Many concurrent operations
- Resource limits (file descriptors, connections)

**Systematic Hunting Process:**

```markdown
For each category:
1. Generate test cases for each edge case
2. Run tests
3. Document failures
4. Prioritize by severity
5. Fix in order of priority
```

**Edge Case Generation Techniques:**

1. **Equivalence Partitioning:**
   - Divide input space into classes
   - Test one representative from each class
   - Example: Valid, invalid, boundary values

2. **Boundary Value Analysis:**
   - Test at boundaries (min, min-1, max, max+1)
   - Test just inside and outside boundaries
   - Example: 0, -1, 1 for numeric fields

3. **Decision Table Testing:**
   - List all conditions and actions
   - Create table of all combinations
   - Test each combination

4. **State Transition Testing:**
   - Model system as state machine
   - Test valid and invalid transitions
   - Test unreachable states

5. **Error Guessing:**
   - Use experience to guess likely errors
   - Common mistake patterns
   - Platform-specific issues

### Phase 5: Fix and Verify

**Prioritization Framework:**

| Severity | Criteria | Action |
|----------|----------|--------|
| Critical | Data loss, security vulnerability, crash | Fix immediately |
| High | Feature broken, no workaround | Fix before release |
| Medium | Feature impaired, workaround exists | Fix soon |
| Low | Minor issue, cosmetic | Document as known issue |

**Fix Process:**

1. **Document the Bug:**
   ```markdown
   ## Bug: [Title]
   
   ### Severity
   [Critical/High/Medium/Low]
   
   ### Description
   [What's wrong]
   
   ### Reproduction
   [Steps to reproduce]
   
   ### Expected Behavior
   [What should happen]
   
   ### Actual Behavior
   [What actually happens]
   
   ### Root Cause
   [Why it happens]
   
   ### Fix
   [How to fix it]
   
   ### Test Coverage
   [What tests were added]
   ```

2. **Write Test (Phase 3)**

3. **Implement Fix:**
   - Minimal change
   - No refactoring
   - Clear comments

4. **Run Full Test Suite:**
   ```bash
   make test  # Must pass
   make lint  # Must pass
   make typecheck  # Must pass
   ```

5. **Create Regression Tests:**
   - Test that specifically covers this bug
   - Prevents future regressions
   - Documents expected behavior

6. **Real-World Validation:**
   - Test against actual project schemas
   - Test against production-like data
   - Verify no regressions

## Advanced Techniques

See `patterns/advanced-techniques.md` for:
- Property-based testing with Hypothesis
- Fuzzing strategies
- Mutation testing
- Static analysis beyond linting
- Security-focused testing
- Performance edge cases

## Integration Workflow

See `patterns/integration-workflow.md` for:
- Pre-commit bug hunting
- Continuous integration setup
- Bug hunting checklist

## Bug Report Template

See `templates/bug-report.md` for the bug report template.

## Edge Case Categories Reference

See `patterns/edge-case-categories.md` for comprehensive list of edge case categories organized by:
- Input boundaries
- Configuration edge cases
- Concurrency edge cases
- Security edge cases
- Integration edge cases
- Performance edge cases

## Bug Severity Definitions

See `patterns/bug-severity.md` for detailed severity classification:
- Critical: Data loss, security vulnerability, crash
- High: Feature broken, no workaround
- Medium: Feature impaired, workaround exists
- Low: Minor issue, cosmetic

## Example: Clevis Bug Hunt Session

See `examples/clevis-session.md` for a complete example of systematic bug hunting on a real project, including:
- Architecture analysis
- Bugs discovered
- Edge cases tested
- Lessons learned

## Related Skills

- **bug-fixing** - Systematic bug fixing with TDD
- **commit** - Commit fixes with proper messages
- **release** - Release after fixes
- **code-reviewer** - Code quality review

## Related Agents

- **testing-engineer** - Can create test stubs for TDD workflow
- **code-reviewer** - Can review fixes for quality
- **security-engineer** - Can perform security-focused testing