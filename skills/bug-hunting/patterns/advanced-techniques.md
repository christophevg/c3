# Advanced Bug Hunting Techniques

Advanced techniques for finding edge cases and hidden bugs beyond basic testing.

## Property-Based Testing (Hypothesis)

Generate hundreds of test cases automatically:

```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(x, y):
  assert add(x, y) == add(y, x)

@given(st.dictionaries(st.text(), st.integers()))
def test_config_parsing(config):
  # Test with any dictionary structure
  result = parse_config(config)
  assert result is not None
```

**Benefits:**
- Finds edge cases you didn't think of
- Shrinks failures to minimal examples
- Reproduces failures reliably

**When to Use:**
- Complex input transformations
- Configuration parsing
- Data validation logic
- Algorithm implementations

## Fuzzing

Generate random/semi-random inputs:

```python
import random
import string

def fuzz_config_parsing(iterations=1000):
  for _ in range(iterations):
    # Generate random TOML
    config = generate_random_toml()
    
    # Try parsing
    try:
      result = parse(config)
      # Validate result structure
      validate_result(result)
    except Exception as e:
      # Log unexpected failures
      if not is_expected_error(e):
        log_bug(config, e)
```

**Fuzzing Strategies:**
- Random: Pure random input
- Mutation: Modify valid input
- Guided: Focus on suspicious areas
- Coverage-guided: Maximize code coverage

## Mutation Testing

Verify test quality by injecting bugs:

```python
# Original code
def parse_config(data):
  return Config(**data)

# Mutant 1: Remove validation
def parse_config(data):
  return Config(data)  # Missing unpack

# Mutant 2: Change condition
def parse_config(data):
  if data:  # Was: if data is not None
    return Config(**data)

# Run tests - mutants should fail
# If mutant survives, tests are inadequate
```

**Tools:**
- `mutmut` for Python
- `pitest` for Java
- `stryker` for JavaScript/TypeScript

**When to Use:**
- Critical business logic
- Security-sensitive code
- Before major releases
- When test coverage seems inflated

## Static Analysis Beyond Linting

**Type Checking (mypy):**
```bash
# Basic
mypy src/

# Strict mode
mypy --strict src/

# Check untyped definitions
mypy --disallow-untyped-defs src/
```

**Security Scanners:**
```bash
# Bandit - Security issues
bandit -r src/

# Safety - Dependency vulnerabilities
safety check

# Semgrep - Custom patterns
semgrep --config=auto src/
```

**Complexity Analysis:**
```bash
# Radon - Cyclomatic complexity
radon cc src/ -a

# Vulture - Dead code
vulture src/
```

## Security-Focused Testing

**Injection Testing:**
```python
def test_command_injection():
  malicious_input = "; rm -rf /"
  result = parse_command(malicious_input)
  assert result.is_safe
  
def test_path_traversal():
  malicious_path = "../../../etc/passwd"
  result = resolve_path(malicious_path)
  assert result.is_sandboxed
```

**Configuration Security:**
```python
def test_secret_exposure():
  config = load_config()
  # Config should not log secrets
  logs = capture_logs(lambda: config.load())
  assert "password" not in logs
  assert "secret" not in logs
```

## Performance Edge Cases

**Large Input Testing:**
```python
def test_large_config():
  # Generate large but valid config
  large_config = {
    f"field_{i}": f"value_{i}" 
    for i in range(100000)
  }
  
  # Should not timeout or OOM
  result = parse_config(large_config)
  assert result is not None
  
def test_deep_nesting():
  # Generate deeply nested structure
  nested = {"level": 0}
  current = nested
  for i in range(1, 1000):
    current["nested"] = {"level": i}
    current = current["nested"]
  
  # Should handle or limit recursion
  result = parse_config(nested)
  assert result.is_valid or result.error == "max_depth_exceeded"
```