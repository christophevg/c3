---
name: python-comments
type: knowledge
description: |
  Use this skill when writing or reviewing Python code comments and docstrings. Provides guidelines for tight, relevant comments that explain WHY not WHAT.
---

# Python Code Commenting Guidelines

## Core Principle

**Code should be self-documenting first. Comments explain WHY, not WHAT.**

## 1. Self-Documenting Code Before Comments

Before adding comments, ensure your code is readable:

```python
# ❌ Bad - Needs comment to explain
def f(x):
    return x * 0.15

# ✅ Good - Self-documenting
LOYALTY_DISCOUNT_RATE = 0.15

def calculate_loyalty_discount(price: float) -> float:
    return price * LOYALTY_DISCOUNT_RATE
```

**Five Principles:**
1. **Descriptive names** - `calculate_area()` not `f()`
2. **Type hints** - Signatures document themselves
3. **Small functions** - One responsibility each
4. **Named conditions** - Extract complex logic to booleans
5. **Named constants** - `HTTP_OK = 200` not magic numbers

## 2. Docstrings (PEP 257)

### When to Use
- **Always** for public APIs: modules, classes, public methods
- **Never** for private/internal methods (prefix with `_`)

### Format Rules

**One-line docstrings** (for simple functions):
```python
def calculate_total(items: list[Item]) -> float:
    """Calculate the total price including tax and shipping."""
```

**Multi-line docstrings** (for complex functions):
```python
def process_payment(
    amount: float,
    currency: str,
    customer_id: str
) -> PaymentResult:
    """Process a payment for a customer.
    
    Validates the customer exists and has sufficient credit limit,
    then processes the payment through the payment gateway.
    
    Raises:
        InvalidCurrencyError: If currency code is not supported.
        CreditLimitExceededError: If amount exceeds customer's limit.
    """
```

## 3. Args/Returns: Only When Needed

**Skip Args/Returns when:**
- Type hints already convey the information
- Parameter names are self-explanatory (`url`, `timeout`, `items`)
- No special semantics or constraints to document

**Use Args/Returns when:**
- Return type doesn't reveal structure (`-> dict` but what keys?)
- Arguments have semantic constraints (valid values, special meanings)
- Side effects or behavior differs based on arguments
- Business rules apply

### Examples

```python
# ✅ Tight: Signature is self-documenting - NO Args/Returns needed
def calculate_total(items: list[Item]) -> float:
    """Calculate the total price including tax and shipping."""

# ✅ Tight: Only document what adds information
def get_user(user_id: str) -> User:
    """Retrieve a user by their unique identifier.
    
    Raises:
        NotFoundError: If user does not exist.
    """
    # No Args/Returns - type hints already clear
    # Raises IS needed - not in signature

# ✅ Useful Returns: Describes structure not in type
def fetch_data(url: str, timeout: int = 30) -> dict:
    """Fetch data from a remote API.
    
    Returns:
        Dictionary with keys: 'status', 'data', 'error_message'.
        The 'data' key contains the parsed JSON response.
    """

# ✅ Useful Args: Constraints not in types
def retry(func: Callable, max_attempts: int = 3, *, 
          delay: float = 1.0, 
          exponential_backoff: bool = True) -> Any:
    """Execute func with automatic retry on failure.
    
    Args:
        max_attempts: Maximum retry attempts (1-10). Defaults to 3.
        delay: Initial delay between retries in seconds. 
            When exponential_backoff is True, subsequent delays
            double each time (1s, 2s, 4s, ...).
    """
```

## 4. Type Hints + Docstrings

**Critical:** Type hints document types. Don't repeat in docstrings.

```python
# ✅ Good: Type hints handle types, docstring explains purpose
def add_item(self, key: str, value: int) -> None:
    """Add an item to the dictionary.
    
    Args:
        key: The unique identifier for the item.
        value: The numeric value to store.
    """

# ❌ Bad: Redundant type information
def add_item(self, key: str, value: int) -> None:
    """Add an item to the dictionary.
    
    Args:
        key (str): The unique identifier.  # Redundant!
        value (int): The numeric value.    # Redundant!
    """
```

**Exception:** Document exceptions (no type hint syntax for these).

## 5. Inline Comments

**Use sparingly** - only when code is genuinely non-obvious.

✅ **Good - Explains WHY or non-obvious logic:**
```python
if i & (i - 1) == 0:  # True if i is 0 or a power of 2
discount_rate = 0.15  # Loyalty program discount (approved by board Q3 2024)
# Using binary search because array is sorted and we need O(log n)
```

❌ **Bad - Explains WHAT (redundant):**
```python
counter = 0      # Initialize counter to zero
x = x + 1        # Increment x
name = name      # No change needed
```

**Rule of thumb:** If you need an inline comment, consider refactoring first.

## 6. Block Comments

Use for:
- Complex algorithms
- Design decisions
- Non-obvious constraints

```python
# We use a weighted dictionary search to find out where i is in
# the array. We extrapolate position based on the largest number
# in the array and the array size, then do binary search to
# get the exact number.
#
# This algorithm is O(log n) for sorted arrays.
```

**Format:**
- Start with `#` and a space
- Separate paragraphs with blank comment lines
- Keep at same indent level as surrounding code

## 6b. Branch Comments: Label, Don't Narrate

For a cascade or switch, label each branch tersely. Don't narrate the algorithm in prose above the block.

```python
# ❌ Narrates the algorithm
# Resolve the primary agent definition via a best-effort cascade: first
# check the registry by name, then fall back to the explicit path, then
# the default location, and finally raise if nothing matched.
if name in registry:
  definition = registry[name]
elif path is not None and path.exists():
  definition = load(path)
elif default_path.exists():
  definition = load(default_path)
else:
  raise NotFoundError(name)

# ✅ Labels each branch
if name in registry:          # option 1: registry
  definition = registry[name]
elif path and path.exists():  # option 2: explicit path
  definition = load(path)
elif default_path.exists():   # option 3a: default location
  definition = load(default_path)
else:                         # option 3b: nothing matched
  raise NotFoundError(name)
```

A one-word label per branch lets the reader scan the alternatives; a prose preamble forces them to read the algorithm twice.

## 7. Module-Level Comments

```python
"""User authentication and session management.

This module provides decorators and utilities for managing user
sessions, including login, logout, and session validation.

Example:
    >>> from auth import require_login
    >>> @require_login
    ... def dashboard():
    ...     return "Welcome back!"
"""

import hashlib
from datetime import timedelta
from functools import wraps
# ...
```

## 8. TODO/FIXME Conventions

**Format:**
```python
# TODO(issue-tracker/url): Brief description
# TODO(#1234): Add condition for when val is None
# TODO(crbug.com/192795): Investigate cpufreq optimizations
# FIXME(#567): This fails for empty lists
```

**Rules:**
- Include issue tracker reference (preferred over `@username`)
- Be specific and actionable
- Remove when resolved

## 9. Exception Class Docstrings

For exception classes, avoid redundant `Attributes:` sections - type hints already document:

```python
# ❌ Bad - Redundant Attributes section
class ConfigurationError(YokerError):
    """Exception for configuration-related errors.

    Attributes:
        setting: The configuration setting that caused the error.
        expected: Description of expected value format.
        message: Custom error message.
    """

# ✅ Good - One-liner is sufficient
class ConfigurationError(YokerError):
    """Exception for configuration-related errors."""
```

**Exception:** Dataclass `Attributes:` sections are appropriate when attributes have semantic meaning beyond their types.

## 10. What NOT to Do

### Don't Comment Out Code
```python
# ❌ Bad
# old_implementation = legacy_fetch(url)
# if old_implementation:
#     data = transform(old_implementation)

# ✅ Good - Use version control
data = fetch(url)
```

### Don't Keep Dead Branches With Apologetic Comments

If a branch can't be reached in this path, delete it — don't leave it with a comment explaining why it's empty.

```python
# ❌ Dead branch kept "just in case"
if resolved_definition is None and agent_path is None:
  pass  # name in registry (none here)

# ✅ Deleted — the branch can't be reached in this path
```

Git remembers the code you removed. A comment is not a reason to keep unreachable logic.

### Don't Repeat Function Names
```python
# ❌ Bad
def calculate_total():
    """Calculate the total."""  # Redundant with function name
    
# ✅ Good
def calculate_total():
    """Return the sum of all line items including tax and shipping."""
```

### Don't Repeat Type Hints
```python
# ❌ Bad
def process(name: str) -> int:
    """Process the name.
    
    Args:
        name (str): The name to process.  # Redundant!
    
    Returns:
        int: The result.  # Redundant!
    """

# ✅ Good
def process(name: str) -> int:
    """Return the processing result for the given name."""
```

## 11. Comment Quality Indicators

**Good comments explain:**
- Business rules and regulatory requirements
- Non-obvious algorithms or optimizations
- Design decisions (why this approach?)
- Known limitations (TODO, FIXME, NOTE)
- Gotchas and edge cases

**Comment code smell (refactor instead):**
- Explains what code does → Code should speak for itself
- Outdated → Update or delete
- Commented-out code → Delete (use git history)
- Redundant type info → Use type hints

## 12. Decision Tree

```
Is the code self-documenting?
├─ NO → Refactor first! (better names, smaller functions, type hints)
└─ YES
    └─ Is there something non-obvious?
        ├─ NO → No comment needed
        └─ YES
            └─ Add comment explaining WHY (not what)
                ├─ Public API? → Use docstring
                ├─ Complex algorithm? → Use block comment
                └─ Single line? → Use inline comment
```

## 13. Tooling

| Tool | Purpose |
|------|---------|
| `ruff` or `pydocstyle` | Check docstring compliance |
| `mypy` | Type checking (reduces type comments) |
| `sphinx + napoleon` | Generate docs from Google/NumPy style |
| `black` | Auto-format (reduces style debates) |

## Summary Checklist

For every comment, ask:

- [ ] Does this explain WHY (not WHAT)?
- [ ] Is it relevant and tight (no fluff)?
- [ ] Could I refactor instead?
- [ ] For docstrings: Is it a public API?
- [ ] For docstrings: Did I avoid repeating type hints?
- [ ] For TODOs: Is there an issue reference?
- [ ] Will this stay accurate over time?

---

**Golden Rule:** "Code tells you HOW. Comments tell you WHY." — Write code that doesn't need comments, then add comments for everything else.
## Related

- `python` — code standards this commenting guidance complements
- `python-testing` — test-writing guidelines from the same family
