# Bug Hunting Integration with C3

How the bug-hunting skill integrates with the C3 ecosystem.

## Skill Hierarchy

```
c3 (plugin)
├── Skills
│   ├── bug-hunting (NEW) ← Find edge cases and hidden bugs
│   ├── bug-fixing ← Fix bugs systematically with TDD
│   ├── commit ← Commit fixes with proper messages
│   ├── release ← Release after fixes
│   └── code-reviewer ← Review code quality
└── Agents
    ├── testing-engineer ← Create test stubs
    ├── code-reviewer ← Review fixes
    └── security-engineer ← Security testing
```

## Workflow Integration

### Feature Development Workflow

```
/project feature "add authentication"
        ↓
    functional-analyst
        ↓
    python-developer
        ↓
    /bug-hunting ← NEW: Find edge cases
        ↓
    testing-engineer (if needed)
        ↓
    /bug-fixing ← Fix discovered bugs
        ↓
    code-reviewer
        ↓
    /commit
```

### Bug Fix Workflow

```
User: "There's a bug in authentication"
        ↓
    /bug-fixing ← Systematic fix with TDD
        ↓
    /bug-hunting ← NEW: Hunt for related edge cases
        ↓
    testing-engineer (if needed)
        ↓
    code-reviewer
        ↓
    /commit
```

### Pre-Release Workflow

```
User: "Ready to release v2.0"
        ↓
    /bug-hunting ← NEW: Pre-release hunting
        ↓
    /bug-fixing (if bugs found)
        ↓
    security-review
        ↓
    /release
```

## Skill Coordination

### Bug Hunting → Bug Fixing

```python
# bug-hunting finds edge cases
/bug-hunting "Check config parsing for edge cases"

# Finds: Empty config causes crash
# Creates: Test demonstrating bug

# bug-fixing implements fix
/bug-fixing "Config parsing crashes on empty input"

# Uses test from bug-hunting
# Implements fix
# Verifies fix
```

### Bug Hunting + Testing Engineer

```python
# bug-hunting identifies need for comprehensive tests
/bug-hunting "Hunt for edge cases in type coercion"

# Finds many edge cases
# Suggests: Property-based testing

# testing-engineer creates test stubs
# python-developer implements
# bug-hunting verifies
```

### Bug Hunting + Code Review

```python
# After bug-hunting and fixes
code-reviewer reviews

# Checks:
# - Are fixes minimal?
# - Are tests comprehensive?
# - Are edge cases covered?
# - Are there regressions?

# Recommends:
# - Additional edge cases to test
# - Code quality improvements
# - Security considerations
```

## Use Cases

### After Feature Implementation

```bash
# Developer implements new feature
/project feature "add rate limiting"

# Bug hunting verifies edge cases
/bug-hunting "What could go wrong with rate limiting?"

# Systematic approach:
# 1. Understand rate limiting architecture
# 2. Test boundary conditions (limit = 0, limit = max)
# 3. Test concurrency (multiple simultaneous requests)
# 4. Test timing (requests near limit boundary)
# 5. Verify with realistic traffic patterns
```

### Before Release

```bash
# Pre-release bug hunting
/bug-hunting "Pre-release edge case check"

# Systematic approach:
# 1. Review all new features since last release
# 2. Check integration points
# 3. Test configuration edge cases
# 4. Verify security edge cases
# 5. Performance test with realistic data
```

### During Code Review

```bash
# Code reviewer finds suspicious code
code-reviewer: "This doesn't handle None"

# Bug hunting investigates
/bug-hunting "Check None handling throughout codebase"

# Finds all None edge cases
# Creates comprehensive test suite
# Fixes all discovered issues
```

### Security Review

```bash
# Security-focused bug hunting
/bug-hunting "Security edge cases in user input"

# Systematic approach:
# 1. SQL injection tests
# 2. Command injection tests
# 3. Path traversal tests
# 4. XSS tests
# 5. Authentication bypass tests
# 6. Authorization edge cases
```

## Comparison with Bug Fixing

| Aspect | bug-hunting | bug-fixing |
|--------|-------------|------------|
| **Purpose** | Find unknown bugs | Fix known bugs |
| **Approach** | Proactive | Reactive |
| **Input** | "What could go wrong?" | "Fix this bug" |
| **Output** | Bug reports + tests | Fixes + tests |
| **When** | After features, before release | When bug reported |
| **Workflow** | Hunt → Document → Test | Analyze → Test → Fix |

**Together:**
```
bug-hunting (find) → bug-fixing (fix) → commit (save)
```

## Agent Coordination

### Bug Hunting with Testing Engineer

```
bug-hunting identifies edge cases
        ↓
testing-engineer creates test stubs
        ↓
python-developer implements tests
        ↓
bug-hunting verifies coverage
```

### Bug Hunting with Security Engineer

```
bug-hunting finds potential vulnerabilities
        ↓
security-engineer analyzes security implications
        ↓
bug-fixing implements security fixes
        ↓
security-review verifies fixes
```

### Bug Hunting with Code Reviewer

```
bug-hunting finds edge cases
        ↓
bug-fixing implements fixes
        ↓
code-reviewer reviews quality
        ↓
bug-hunting verifies no regressions
```

## Documentation Structure

```
bug-hunting/
├── SKILL.md                      # Main workflow
├── README.md                     # Quick start
├── patterns/
│   ├── edge-case-categories.md   # Comprehensive categories
│   ├── bug-severity.md           # Severity definitions
│   └── quick-reference.md        # One-page reference
└── examples/
    └── clevis-session.md         # Real-world example
```

## Skill Metadata

```yaml
name: bug-hunting
description: Systematic bug hunting workflow for finding edge cases and hidden bugs. Use after implementing features, before releases, or when asked to find bugs, probe for holes, or stress-test code.
```

## Related Skills

- **bug-fixing**: Systematic bug fixing with TDD approach
- **commit**: Guide git commit operations
- **release**: Standardize release preparation
- **code-reviewer**: Code quality review

## Related Agents

- **testing-engineer**: Can create test stubs for TDD workflow
- **code-reviewer**: Can review fixes for quality
- **security-engineer**: Can perform security-focused testing

## Usage Examples

### Command Line

```bash
# Find bugs in configuration module
/bug-hunting "Check config.py for edge cases"

# Pre-release check
/bug-hunting "Hunt for bugs before release"

# Security edge cases
/bug-hunting "Security edge cases in authentication"

# Performance edge cases
/bug-hunting "What could go wrong with large inputs?"
```

### In Analysis

```python
# Functional analyst can invoke bug hunting
functional-analyst: "I recommend bug-hunting for this feature"

# Bug hunting finds edge cases
# Analyst incorporates findings into TODO.md
```

### In Project Management

```python
# Project manager can schedule bug hunting
/project manage

# Implementation loop includes:
# - Plan
# - Implement
# - Bug hunting ← NEW: Find edge cases
# - Review
# - Iterate
```

## Integration Points

### With TODO.md

```markdown
## Phase 2: Implementation
- [ ] Implement feature X
- [ ] /bug-hunting "Edge cases in feature X" ← NEW
- [ ] Write tests
- [ ] Code review
```

### With Reporting

```markdown
## Implementation Summary
### What was implemented
- Feature X with Y capability

### Bugs Found by bug-hunting ← NEW
- Bug #1: Edge case with empty input (S2)
- Bug #2: Race condition in concurrent access (S1)

### Tests
- 25 new tests from bug-hunting
- 100% coverage of edge cases
```

### With Commit Messages

```
fix(config): handle edge case with empty input

Found by bug-hunting: Config parsing crashed on empty TOML
- Added validation for empty config
- Added test for empty config edge case
- Verified no regressions

🤖 Implemented together with a coding agent.
```

## Future Enhancements

1. **Automated Bug Hunting**: Integrate with CI/CD for automatic edge case testing
2. **Bug Patterns Database**: Build database of common bug patterns
3. **Property-Based Testing Integration**: Auto-generate Hypothesis tests
4. **Mutation Testing Integration**: Auto-run mutmut after hunting
5. **Security Scanning Integration**: Coordinate with security tools

## Metrics

Track bug hunting effectiveness:

- **Bugs Found Per Session**: Average bugs discovered
- **Severity Distribution**: S1, S2, S3, S4 counts
- **Edge Cases Tested**: Number of edge cases tested
- **Coverage Increase**: Coverage improvement after hunting
- **Regression Rate**: Bugs that recur after fix

## Training

New team members can learn bug hunting:

1. Read `SKILL.md` for workflow
2. Review `examples/clevis-session.md` for real-world example
3. Use `patterns/quick-reference.md` during sessions
4. Reference `patterns/edge-case-categories.md` for ideas
5. Follow severity matrix in `patterns/bug-severity.md`

## Support

For questions or improvements:

1. Review existing documentation
2. Check `examples/clevis-session.md` for patterns
3. Consult `patterns/edge-case-categories.md` for edge case ideas
4. Create issue or pull request on C3 repository