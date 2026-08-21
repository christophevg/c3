# Bug Hunting Quick Reference

One-page reference for systematic bug hunting.

## Workflow Checklist

### Phase 1: Architecture Understanding
- [ ] Review project instructions and README.md (auto-loaded where applicable)
- [ ] Map data flows and boundaries
- [ ] Identify critical paths
- [ ] Document assumptions

### Phase 2: Core Bug Identification
- [ ] Trace critical operations
- [ ] Check error handling
- [ ] Validate assumptions
- [ ] Test boundary conditions

### Phase 3: Test-Driven Fixing
- [ ] Create failing test
- [ ] Verify test reproduces bug
- [ ] Implement minimal fix
- [ ] Update test to expect correct behavior
- [ ] Verify all tests pass

### Phase 4: Edge Case Hunting
- [ ] Input boundaries (empty, single, max, special)
- [ ] Configuration edge cases
- [ ] Concurrency edge cases
- [ ] Security edge cases
- [ ] Integration edge cases
- [ ] Performance edge cases

### Phase 5: Fix and Verify
- [ ] Document each bug
- [ ] Prioritize by severity
- [ ] Fix in priority order
- [ ] Create regression tests
- [ ] Verify with real-world usage

## Edge Case Questions

### Input Boundaries
- What if input is `None`?
- What if input is empty (`[]`, `{}`, `""`)?
- What if input has single element?
- What if input is very large?
- What if input has special characters?
- What if input has wrong type?

### Configuration
- What if section/field is missing?
- What if config file is empty?
- What if values have wrong type?
- What if there are circular refs?
- What if there are duplicate keys?

### Concurrency
- What if two threads access simultaneously?
- What if operation times out?
- What if resource is locked?
- What if process crashes mid-operation?

### Security
- What if input contains injection?
- What if user tries path traversal?
- What if credentials are invalid?
- What if permissions are insufficient?

### Integration
- What if dependency is missing?
- What if API version mismatches?
- What if network fails?
- What if operation times out?

### Performance
- What if input is 10x larger?
- What if nesting is 10x deeper?
- What if 10x more concurrent operations?
- What if resources are exhausted?

## Severity Quick Guide

| Severity | Definition | Timeline |
|----------|------------|----------|
| **S1 Critical** | Data loss, security vulnerability, crash | < 4 hours |
| **S2 High** | Core feature broken, difficult workaround | < 3 days |
| **S3 Medium** | Feature impaired, easy workaround | < 2 weeks |
| **S4 Low** | Minor issue, cosmetic | Backlog |

## Test Patterns

### Property-Based Testing
```python
from hypothesis import given, strategies as st

@given(st.text(), st.integers())
def test_with_arbitrary_input(name, count):
  result = process(name, count)
  assert result.is_valid
```

### Boundary Testing
```python
@pytest.mark.parametrize("value", [0, 1, -1, MAX, MAX+1, MIN, MIN-1])
def test_boundary_values(value):
  result = process(value)
  assert result.is_valid or result.error == "expected"
```

### Error Path Testing
```python
def test_error_handling():
  with pytest.raises(ExpectedError):
    process(invalid_input)
```

### Regression Testing
```python
def test_bug_123_fixed():
  """Regression test for bug #123.
  
  Bug: Root fields leaked into subcommand configs.
  Fixed: Extract only subcommand section when cmd is set.
  """
  # Arrange
  config = create_test_config()
  
  # Act
  result = load_config(config)
  
  # Assert
  assert "root_field" not in result
```

## Common Bug Patterns

### Off-by-One Errors
- Loop boundaries: `range(n)` vs `range(n+1)`
- Array indexing: `arr[i]` vs `arr[i+1]`
- String slicing: `s[:i]` vs `s[:i+1]`

### Null/None Handling
- Missing null checks
- Null propagation
- Null vs empty confusion

### Type Confusion
- String vs bytes
- Integer vs float
- List vs tuple
- Dict vs list of tuples

### State Management
- Uninitialized state
- Stale state
- Race conditions
- State mutation

### Resource Management
- Unclosed files
- Unclosed connections
- Memory leaks
- Resource exhaustion

## Bug Report Template

```markdown
## Bug: [Title]

**Severity:** [S1-S4]
**Priority:** [P0-P5]

### Description
[What's wrong]

### Reproduction
1. [Step 1]
2. [Step 2]
3. [Bug occurs]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Root Cause
[Why it happens]

### Fix
[How to fix it]

### Test Coverage
- test_name_1
- test_name_2
```

## Test Commands

```bash
# Run all tests
make test

# Run specific test
pytest tests/test_file.py::test_name -v

# Run with coverage
make coverage

# Run type checking
make typecheck

# Run linting
make lint

# Run security scan
bandit -r src/

# Run mutation testing
mutmut run
```

## Pre-Commit Checklist

```bash
# Before each commit
make test && make lint && make typecheck

# Before release
make test-all && make coverage && bandit -r src/
```

## Quick Diagnostics

### Is it a Bug?
1. Does it violate specification? → Bug
2. Does it cause unexpected behavior? → Bug
3. Does it crash or corrupt data? → Critical Bug
4. Is it just inconvenient? → Enhancement

### How to Find Root Cause?
1. Reproduce consistently
2. Minimize reproduction case
3. Add logging/prints
4. Compare working vs broken
5. Hypothesize and test (one variable at a time)

### When to Ask for Help?
- Cannot reproduce after 30 minutes
- Multiple fix attempts fail
- Severity is Critical
- Affects production users
- Security implications discovered

## Resources

- **Edge Cases:** `patterns/edge-case-categories.md`
- **Severity:** `patterns/bug-severity.md`
- **Examples:** `examples/clevis-session.md`
- **Full Guide:** `SKILL.md`