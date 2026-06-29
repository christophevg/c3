# Clevis Bug Hunt Session

Complete example of systematic bug hunting on a configuration library.

## Project Overview

**Clevis** is a Python library for loading configuration from TOML files into dataclasses. It uses decorators to transform dataclasses into configuration loaders.

**Key Features:**
- `@configclass` decorator for automatic configuration loading
- Support for subcommands with command-specific config sections
- Type coercion and validation
- Default values and inheritance

## Session Approach

### Phase 1: Architecture Understanding

We started by understanding the codebase:

1. **Read Core Files:**
   - `src/clevis/config.py` - Core decorator and config loading
   - `src/clevis/types.py` - Type handling and coercion
   - `src/clevis/decorators.py` - Decorator implementations

2. **Identified Key Data Flow:**
   ```
   TOML file → extract section → resolve defaults → validate types → instantiate dataclass
   ```

3. **Mapped Critical Boundaries:**
   - Decorator application (`@configclass`)
   - TOML extraction (section selection)
   - Type coercion (string to typed value)
   - Dataclass instantiation

4. **Documented Assumptions:**
   - TOML sections exist for subcommands
   - Types match between dataclass and TOML
   - Field names don't conflict with command names
   - Single decoration (no double-decorating)

### Phase 2: Core Bug Identification

We systematically traced through operations:

**Bug 1: Subcommand Config Extraction**

```python
@configclass(cmd="print")
class PrintConfig:
  message: str

# TOML:
[print]
message = "hello"

# Expected: PrintConfig(message="hello")
# Actual: PrintConfig(message="hello", **all_root_fields)  # Root fields leaked in!
```

**Root Cause:** TOML extraction didn't properly scope subcommand sections.

**Bug 2: Root Field Leakage**

```python
# TOML:
message = "root message"

[print]
message = "hello"

# Expected: PrintConfig(message="hello")
# Actual: PrintConfig(message="root message")  # Root overrode subcommand!
```

**Root Cause:** Root-level fields were being merged into subcommand configs.

**Bug 3: Silent Type Mismatch**

```python
# TOML:
[print]
# String instead of dict
subcommand = "not a dict"

# Expected: Error about wrong type
# Actual: Silent failure, unexpected behavior
```

**Root Cause:** Type validation didn't check for dict types in TOML sections.

**Bug 4: cmd/prefix Conflict**

```python
@configclass(cmd="print", prefix="print")
class PrintConfig:
  message: str

# Both cmd and prefix set - confusing behavior
```

**Root Cause:** No validation to prevent conflicting parameters.

**Bug 5: Literal Type Support**

```python
class Config:
  mode: Literal["A", "B"]

# Literal types not recognized, treated as complex union
```

**Root Cause:** Type coercion didn't handle `Literal` types.

**Bug 6: Container Type Support**

```python
class Config:
  items: list[str]
  mapping: dict[str, int]
  tuple_data: tuple[str, ...]

# Container types not properly coerced
```

**Root Cause:** Type coercion didn't handle generic container types.

### Phase 3: Test-Driven Fixing

For each bug, we followed TDD:

**Example: Fixing Subcommand Extraction**

1. **Created failing test:**
   ```python
   def test_subcommand_config_extracts_correct_section():
     """Bug: Subcommand config doesn't extract correct TOML section.
     
     Expected: Only fields from subcommand section
     Actual: Root fields leaking into subcommand config
     """
     # Current behavior (proves bug exists)
     config = load_config(PrintConfig)
     assert "root_field" not in config  # Fails - root fields present
   ```

2. **Implemented minimal fix:**
   ```python
   # In config.py
   def extract_config(cls, data):
     cmd = getattr(cls, '_cmd', None)
     if cmd:
       # Only extract subcommand section, not root
       return data.get(cmd, {})
     return data
   ```

3. **Updated test to expect correct behavior:**
   ```python
   def test_subcommand_config_extracts_correct_section():
     config = load_config(PrintConfig)
     assert "root_field" not in config  # Now passes
     assert config.message == "hello"  # Correct value
   ```

4. **Ran all tests:**
   ```bash
   pytest tests/test_config.py -v
   # All tests pass
   ```

### Phase 4: Edge Case Hunting

After fixing core bugs, we hunted for edge cases:

#### Inheritance Edge Cases

```python
@configclass(cmd="base")
class BaseConfig:
  name: str

@configclass(cmd="derived")
class DerivedConfig(BaseConfig):
  value: int

# Test: Does derived inherit cmd?
# Test: Do both configs work correctly?
# Test: Can derived override base fields?
```

#### Command Name Collisions

```python
@configclass(cmd="print")
class PrintConfig:
  pass

@configclass(cmd="print")  # Duplicate!
class AnotherPrint:
  pass

# Test: What happens with duplicate cmd?
# Found: No validation - confusing behavior
```

#### TOML Structure Edge Cases

```python
# Empty section
[print]

# Wrong type
print = "not a section"

# Nested sections
[print]
[print.subsection]

# Multiple levels
[level1]
[level1.level2]
[level1.level2.level3]
```

#### Field Name Overlaps

```python
@configclass(cmd="print")
class Config:
  print: str  # Same as cmd name!
  
# Test: Does field name conflict with cmd?
```

#### Double Decoration

```python
@configclass
@configclass  # Double decoration
class Config:
  pass

# Test: What happens with double decoration?
```

#### Required Fields

```python
@configclass(cmd="print")
class Config:
  required_field: str  # No default

# TOML missing the field
[print]

# Test: Does it error correctly?
```

#### Multiple Config Calls

```python
config1 = load_config(Config)
config2 = load_config(Config)  # Second call

# Test: Does second call work?
# Test: Are they independent?
```

### Phase 5: Fix and Verify

For each discovered issue, we:

1. **Documented the Bug:**
   ```markdown
   ## Bug: Root Field Leakage
   
   ### Severity
   High (S2) - Core feature broken, workaround exists
   
   ### Description
   Root-level TOML fields leak into subcommand configurations.
   
   ### Reproduction
   1. Create TOML with root fields
   2. Create subcommand config
   3. Load subcommand config
   4. Observe root fields present
   
   ### Expected Behavior
   Only subcommand section fields should be present.
   
   ### Actual Behavior
   Root fields merged into subcommand config.
   
   ### Root Cause
   TOML extraction merges root with subcommand section.
   
   ### Fix
   Extract only subcommand section when cmd is set.
   
   ### Test Coverage
   - test_subcommand_extracts_only_section
   - test_root_fields_not_leaked
   - test_empty_root_section
   ```

2. **Wrote Tests**

3. **Implemented Fixes**

4. **Ran Full Suite:**
   ```bash
   make test    # Unit tests
   make lint    # Linting
   make typecheck  # Type checking
   make coverage  # Coverage report
   ```

5. **Created Regression Tests:**
   ```python
   # Regression test for bug #X
   def test_no_root_field_leakage():
     """Ensures root fields don't leak into subcommand configs.
     
     Bug: Root-level TOML fields were being merged into subcommand configs.
     Fixed: Extract only subcommand section when cmd is set.
     """
     # ... test implementation
   ```

6. **Real-World Validation:**
   - Tested against actual project schemas
   - Tested with production-like TOML files
   - Verified no regressions in dependent code

## Results Summary

### Bugs Found

| Bug | Severity | Discovery Method |
|-----|----------|------------------|
| Subcommand config extraction | High | Architecture analysis |
| Root field leakage | High | Edge case testing |
| Silent type mismatch | High | Edge case testing |
| cmd/prefix conflict | Medium | Edge case testing |
| Literal type support | Medium | Feature request + testing |
| Container type support | Medium | Feature request + testing |

### Edge Cases Tested

| Category | Count | Issues Found |
|----------|-------|--------------|
| Input boundaries | 8 | 2 |
| Configuration edge cases | 12 | 4 |
| Inheritance edge cases | 6 | 1 |
| TOML structure edge cases | 10 | 2 |
| Field name overlaps | 4 | 1 |
| **Total** | **40** | **10** |

### Test Coverage Increase

- **Before:** 45% coverage
- **After:** 92% coverage
- **New Tests:** 28 tests added

## Lessons Learned

### What Worked Well

1. **Architecture Understanding First:** Understanding the data flow before hunting revealed bugs faster.

2. **TDD Approach:** Writing tests first ensured we understood the bug before fixing.

3. **Systematic Categories:** Edge case categories helped find bugs we wouldn't have thought of.

4. **Real-World Validation:** Testing against actual schemas caught issues unit tests missed.

### What We Missed Initially

1. **Container Types:** Didn't initially test `list[str]`, `dict[str, int]`, etc.

2. **Inheritance Interactions:** Didn't test how cmd parameter behaves with inheritance.

3. **Command Collisions:** Didn't validate uniqueness of cmd values.

### Process Improvements for Next Time

1. **Start with Type Testing:** Create a type test matrix early:
   ```python
   # Test matrix for all supported types
   types_to_test = [
     str, int, float, bool,
     List[str], Dict[str, int],
     Optional[str], Literal["A", "B"],
     # ... etc
   ]
   ```

2. **Inheritance Test Suite:** Create standard inheritance tests:
   ```python
   # Standard inheritance test cases
   - Single inheritance
   - Multiple inheritance
   - Diamond inheritance
   - Inheritance with overrides
   - Inheritance with additional fields
   ```

3. **Decorator Test Suite:** Test decorator edge cases:
   ```python
   # Standard decorator test cases
   - Single decoration
   - Double decoration
   - Stacked with other decorators
   - Order of decorators
   ```

4. **Configuration Test Suite:** Test configuration edge cases:
   ```python
   # Standard config test cases
   - Empty config
   - Missing sections
   - Wrong types
   - Duplicate keys
   - Circular references
   ```

## Key Takeaways

### Bug Hunting is Systematic

Following a structured approach:
1. Understand architecture
2. Identify core bugs
3. Write tests first
4. Hunt edge cases systematically
5. Verify with real-world usage

### Edge Cases are Everywhere

Every assumption is a potential edge case:
- What if it's None?
- What if it's empty?
- What if it's wrong type?
- What if it's duplicated?
- What if it's inherited?

### Tests are Documentation

Good tests document expected behavior:
```python
def test_subcommand_config_extracts_only_section():
  """Subcommand configs should only extract their section from TOML.
  
  Given a TOML file with root fields and a subcommand section,
  only fields from the subcommand section should be present.
  """
```

### Real-World Validation Matters

Unit tests are necessary but not sufficient:
- Test against actual project schemas
- Test with production-like data
- Verify no regressions in dependent code

## Appendix: Test Examples

### Property-Based Testing

```python
from hypothesis import given, strategies as st

@given(st.text(), st.integers())
def test_config_with_arbitrary_values(name, count):
  """Test config parsing with arbitrary input."""
  config = create_config(name=name, count=count)
  assert config.name == name
  assert config.count == count
```

### Fuzzing

```python
def fuzz_toml_parsing(iterations=100):
  """Fuzz TOML parsing with random inputs."""
  for _ in range(iterations):
    toml = generate_random_toml()
    try:
      result = parse_toml(toml)
      validate_structure(result)
    except ExpectedError:
      pass  # Expected errors are OK
    except Exception as e:
      log_unexpected_bug(toml, e)
```

### Mutation Testing

```python
# Original
def extract_config(cls, data):
  cmd = getattr(cls, '_cmd', None)
  if cmd:
    return data.get(cmd, {})
  return data

# Mutants to test:
# 1. Remove if check
# 2. Change .get to direct access
# 3. Remove default {}
# Tests should catch these mutations
```

This session demonstrates that systematic bug hunting finds more bugs faster than ad-hoc testing, and that TDD ensures fixes are correct and don't regress.