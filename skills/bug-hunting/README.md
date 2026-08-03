# Bug Hunting Skill

Systematic workflow for finding edge cases and hidden bugs before they reach production.

## Overview

This skill provides a structured approach to bug hunting that goes beyond basic testing. It combines architecture analysis, edge case generation, test-driven development, and systematic verification to find bugs efficiently.

## Quick Start

### When to Use

- After implementing a new feature
- Before releasing to production
- When asked to "find bugs" or "probe for holes"
- When stress-testing configuration or data processing code
- When user says "what could go wrong?"

### Basic Workflow

```
1. Architecture Understanding
   └─> Read core docs, map data flows, identify boundaries

2. Core Bug Identification
   └─> Trace operations, check error handling, validate assumptions

3. Test-Driven Fixing
   └─> Write failing test → Fix → Update test to pass

4. Edge Case Hunting
   └─> Systematically probe categories of edge cases

5. Fix and Verify
   └─> Prioritize by severity → Fix → Verify with real-world usage
```

## Key Concepts

### Severity Classification

| Level | Criteria | Action |
|-------|----------|--------|
| Critical (S1) | Data loss, security vulnerability, crash | Fix immediately |
| High (S2) | Core feature broken, difficult workaround | Fix before release |
| Medium (S3) | Feature impaired, easy workaround | Fix soon |
| Low (S4) | Minor issue, cosmetic | Document as known issue |

### Edge Case Categories

- **Input Boundaries:** Empty, single, maximum, special characters
- **Configuration:** Missing sections, wrong types, circular refs
- **Concurrency:** Race conditions, deadlocks, thread safety
- **Security:** Injection, path traversal, privilege escalation
- **Integration:** Missing deps, API mismatches, network failures
- **Performance:** Large inputs, deep nesting, resource limits

### Test-Driven Bug Fixing

**CRITICAL:** Write tests BEFORE fixing bugs.

```python
# 1. Create test that demonstrates bug
def test_bug_name():
  """Bug: Description
  
  Expected: What should happen
  Actual: What currently happens
  """
  result = buggy_function()
  assert result.has_issue  # Test passes, proving bug exists

# 2. Implement fix
# 3. Update test to expect correct behavior
def test_bug_name():
  result = fixed_function()
  assert result.is_correct  # Test should now pass
```

## Advanced Techniques

### Property-Based Testing

Generate hundreds of test cases automatically with Hypothesis:

```python
from hypothesis import given, strategies as st

@given(st.dictionaries(st.text(), st.integers()))
def test_config_parsing(config):
  result = parse_config(config)
  assert result is not None
```

### Mutation Testing

Verify test quality by injecting bugs:

```bash
# Install mutmut
pip install mutmut

# Run mutation testing
mutmut run

# Check results
mutmut results
```

### Fuzzing

Generate random inputs to find crashes:

```python
def fuzz_config_parsing(iterations=1000):
  for _ in range(iterations):
    config = generate_random_config()
    try:
      result = parse(config)
      validate(result)
    except ExpectedError:
      pass
    except Exception as e:
      log_bug(config, e)
```

## Skill Files

### Main Skill
- `SKILL.md` - Complete bug hunting workflow with examples

### Patterns
- `patterns/edge-case-categories.md` - Comprehensive list of edge case types
- `patterns/bug-severity.md` - Severity definitions and prioritization

### Examples
- `examples/clevis-session.md` - Real bug hunting session on configuration library

## Integration with Other Skills

### Bug Fixing Workflow

```
bug-hunting (find bugs) → bug-fixing (fix bugs) → commit (save fixes)
```

### Development Workflow

```
implement feature → bug-hunting (verify) → release
```

### Code Review Workflow

```
code-reviewer (quality) → bug-hunting (edge cases) → security-review
```

## Related Skills

- **bug-fixing** - Systematic bug fixing with TDD
- **commit** - Commit fixes with proper messages
- **release** - Release after fixes
- **code-reviewer** - Code quality review

## Related Agents

- **testing-engineer** - Can create test stubs for TDD workflow
- **code-reviewer** - Can review fixes for quality
- **security-engineer** - Can perform security-focused testing

## Best Practices

### Do

- ✅ Understand architecture before hunting
- ✅ Write tests before fixing
- ✅ Use systematic edge case categories
- ✅ Prioritize bugs by severity
- ✅ Verify with real-world usage
- ✅ Create regression tests

### Don't

- ❌ Start fixing before understanding
- ❌ Skip writing tests
- ❌ Hunt edge cases randomly
- ❌ Fix low priority bugs first
- ❌ Trust unit tests alone
- ❌ Forget regression tests

## Common Patterns

### Pre-Commit Bug Hunting

```bash
# Before each commit
make test      # Unit tests
make lint      # Linting
make typecheck # Type checking

# Before release
make test-all  # All Python versions
make coverage  # Coverage report
bandit -r src/ # Security scan
```

### Continuous Integration

```yaml
name: Bug Hunting
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: make test
      - run: make lint
      - run: make typecheck
      - run: bandit -r src/
```

## Example Usage

### Command Line

```bash
# Find bugs in configuration module
/bug-hunting "Check config.py for edge cases"

# Pre-release bug hunting
/bug-hunting "Hunt for bugs before release"

# Stress-test data processing
/bug-hunting "What could go wrong with data import?"
```

### In Code Review

```python
# When reviewing code, ask:
# - What if input is None?
# - What if input is empty?
# - What if input is wrong type?
# - What if operation times out?
# - What if dependency fails?
```

## Contributing

To improve this skill:

1. Add edge case categories to `patterns/edge-case-categories.md`
2. Add severity examples to `patterns/bug-severity.md`
3. Add real-world examples to `examples/`
4. Update main workflow in `SKILL.md`

## License

Part of the C3 plugin. See main plugin LICENSE file.