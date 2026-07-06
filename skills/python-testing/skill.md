---
name: python-testing
description: Use this skill when writing or reviewing Python tests. Provides guidelines for relevant and tight testing - focus on behavior, not implementation; test what matters, not everything.
---

# Python Testing Guidelines

## Core Principle

**Test behavior, not implementation. Write tests until fear turns to boredom.**

Stop testing when you've covered important cases and further testing feels tedious. Tests should catch real bugs, enable refactoring, and survive implementation changes.

---

## 1. What to Test (DO)

### Business Logic and Complex Calculations

✅ **Test:** Core business rules, algorithms, calculations, decision-making logic.

```python
def test_loan_approval_requires_credit_score_above_700():
    """Test that loans are only approved for credit scores > 700."""
    application = LoanApplication(credit_score=650, income=50000)
    assert not can_approve(application)

def test_compound_interest_calculation():
    """Test compound interest formula."""
    principal = 1000
    rate = 0.05
    years = 10
    result = calculate_compound_interest(principal, rate, years)
    expected = 1000 * (1.05 ** 10)
    assert abs(result - expected) < 0.01
```

### Public APIs and Contracts

✅ **Test:** Public methods that other code will call. The stable interface.

```python
def test_process_order_returns_order_id():
    """Public API: processing an order returns a valid order ID."""
    order = Order(items=[Item(sku='ABC123', quantity=2)])
    order_id = process_order(order)
    assert order_id is not None
    assert isinstance(order_id, str)
    assert len(order_id) == 36  # UUID format
```

### Edge Cases and Boundary Conditions

✅ **Test:** Boundary values, empty inputs, null values, extreme cases.

```python
@pytest.mark.parametrize("input_value,expected", [
    ("", ""),                    # Empty string
    ("hello", "HELLO"),          # Normal case
    ("Hello World", "HELLO WORLD"),  # Multiple words
    ("123", "123"),              # Numbers
    ("!@#", "!@#"),              # Special characters
    ("a" * 1000, "A" * 1000),    # Long string
])
def test_uppercase_handles_edge_cases(input_value, expected):
    assert uppercase(input_value) == expected
```

### Error Handling and Failure Modes

✅ **Test:** Exception paths, error conditions, invalid inputs.

```python
def test_parse_config_raises_on_missing_required_field():
    """Test that missing required field raises ConfigurationError."""
    config = {"name": "app"}  # missing 'version' field
    with pytest.raises(ConfigurationError) as exc_info:
        parse_config(config)
    assert "required field" in str(exc_info.value).lower()

def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

### Critical User Journeys

✅ **Test:** End-to-end workflows that users depend on.

```python
def test_user_can_complete_purchase():
    """Test complete purchase workflow."""
    user = create_user(email="buyer@example.com")
    product = create_product(price=29.99)
    cart = add_to_cart(user, product, quantity=2)

    checkout = start_checkout(cart)
    payment = process_payment(checkout, card_token="test_token")
    order = complete_order(payment)

    assert order.status == "completed"
    assert order.total == 59.98
```

### Regression Tests (Production Bugs)

✅ **Test:** Every bug discovered in production should become a test.

```python
def test_order_with_negative_quantity_does_not_crash():
    """Regression test: Bug #2345 - negative quantities caused crash.
    
    Previous behavior: process_order() raised IndexError
    Expected behavior: Reject order with ValidationError
    """
    order = Order(items=[Item(sku='ABC123', quantity=-5)])

    with pytest.raises(ValidationError) as exc_info:
        process_order(order)

    assert "quantity must be positive" in str(exc_info.value)
```

---

## 2. What NOT to Test (DON'T)

### 2.1 Trivial Code

❌ **Don't Test:** Simple assignments, getters, setters, obvious logic.

```python
# ❌ BAD: Testing trivial code
def test_display_name_returns_name():
    user = User("Alice", "alice@example.com")
    assert user.display_name == "Alice"  # Just duplicates the code

# ❌ BAD: Testing dataclass defaults
def test_config_defaults():
    config = HarnessConfig()
    assert config.name == "yoker"      # Testing default value
    assert config.version == "1.0"     # Testing default value

# ❌ BAD: Testing frozen dataclass
def test_frozen_dataclass():
    stats = ContextStatistics()
    with pytest.raises(AttributeError):
        stats.message_count = 100      # Testing @dataclass(frozen=True)

# ✅ GOOD: Test the business logic that uses User
def test_user_can_be_created_and_authenticated():
    """Test that User objects work in the authentication system."""
    user = create_user("Alice", "alice@example.com", password="secret")
    assert authenticate("alice@example.com", "secret") == user
```

**Why:** If `a = b + 1` is wrong, you'll see it immediately. The test would just duplicate the code.

---

### 2.2 Private Methods

❌ **Don't Test:** Private/internal methods directly. Test public interface instead.

```python
# ❌ BAD: Testing private method directly
class OrderProcessor:
    def process(self, order):
        if self._validate_order(order):  # private method
            return self._calculate_total(order)
        raise ValidationError()

    def _validate_order(self, order):
        return order.items and order.customer

def test_validate_order():  # ❌ BAD: Testing private method
    processor = OrderProcessor()
    assert processor._validate_order(Order(items=[])) == False

# ✅ GOOD: Test public interface
def test_process_order_validates_items():
    """Test that processing invalid order raises ValidationError."""
    processor = OrderProcessor()
    empty_order = Order(items=[])

    with pytest.raises(ValidationError):
        processor.process(empty_order)
```

**If a private method is complex enough to need testing:** Extract it to a separate class where it becomes public, then test it there.

---

### 2.3 Third-Party Library Code

❌ **Don't Test:** Code from external libraries/frameworks. Trust it, test YOUR integration.

```python
# ❌ BAD: Testing third-party library
def test_datetime_now_returns_current_time():  # Testing Python stdlib
    now = datetime.now()
    assert now <= datetime.now()

def test_json_dumps_converts_to_string():  # Testing json library
    result = json.dumps({"key": "value"})
    assert result == '{"key": "value"}'

# ✅ GOOD: Test your usage of the library
def test_serialize_order_to_json():
    """Test that Order can be serialized for API response."""
    order = Order(id=123, total=45.67)
    result = serialize_order(order)

    assert json.loads(result) == {
        "order_id": 123,
        "total": 45.67
    }
```

---

### 2.4 Implementation Details

❌ **Don't Test:** HOW code works internally. Test WHAT it does (observable behavior).

```python
# ❌ BAD: Testing implementation
class ShoppingCart:
    def __init__(self):
        self._items = []  # Internal list (implementation detail)

    def add_item(self, item):
        self._items.append(item)

    def total(self):
        return sum(item.price for item in self._items)

def test_add_item_appends_to_internal_list():
    cart = ShoppingCart()
    item = Item(price=10)
    cart.add_item(item)
    assert len(cart._items) == 1      # ❌ Coupled to implementation
    assert cart._items[0] == item      # ❌ Will break if we change to dict

# ✅ GOOD: Test observable behavior
def test_add_item_increases_total():
    """Test that adding items increases cart total."""
    cart = ShoppingCart()
    cart.add_item(Item(price=10))
    cart.add_item(Item(price=20))
    assert cart.total() == 30  # Tests result, not how it's stored
```

---

### 2.5 Framework/Boilerplate Code

❌ **Don't Test:** Configuration, simple models, URL routing, framework-generated code.

```python
# ❌ BAD: Testing framework configuration
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

def test_user_has_name_field():  # ❌ Testing Django internals
    assert 'name' in User._meta.get_all_field_names()

# ❌ BAD: Testing URL routing
urlpatterns = [
    path('users/', UserListView.as_view()),
]

def test_users_url_resolves():  # ❌ Testing Django URL resolver
    url = reverse('user-list')
    assert url == '/users/'

# ✅ GOOD: Test your view logic
def test_user_list_returns_active_users():
    """Test that UserListView only returns active users."""
    User.objects.create(name="Active", is_active=True)
    User.objects.create(name="Inactive", is_active=False)

    request = RequestFactory().get('/users/')
    view = UserListView.as_view()
    response = view(request)

    users = response.context_data['users']
    assert users.count() == 1
    assert users[0].name == "Active"
```

---

### 2.6 Tests That Never Fail

❌ **Don't Write:** Tests that always pass, regardless of code correctness.

```python
# ❌ BAD: Test that never fails
def test_process_order_executes():
    """This test passes even if process_order does nothing."""
    order = Order()
    process_order(order)  # No assertion!
    # Test passes but verifies nothing

# ❌ BAD: Assertion that's always True
def test_order_has_items():
    order = Order()
    items = order.items  # Returns empty list
    assert items is not None or items is None  # Always True!

# ❌ BAD: Mock assertion without setup
def test_sends_email():
    with patch('module.send_email') as mock_send:
        process_order(Order())
        # Forgot to call mock_send.assert_called()
        # Test passes but doesn't verify email was sent

# ✅ GOOD: Test with meaningful assertion
def test_process_order_creates_order_record():
    """Test that processing creates an order in database."""
    order = Order(items=[Item(price=100)])
    result = process_order(order)

    assert Order.objects.filter(id=result.id).exists()
    assert Order.objects.get(id=result.id).status == "completed"
```

---

### 2.7 Exact Output Strings

❌ **Don't Test:** Exact message content, console output, log messages (unless critical).

```python
# ❌ BAD: Testing exact string content
def test_welcome_message():
    motd = get_message_of_the_day()
    assert motd == "Welcome to our system! Have a great day!"
    # Breaks when you change "great" to "wonderful"

def test_error_message():
    result = validate("")
    assert result.error == "Name cannot be empty"
    # Breaks when you improve the message

def test_prints_message_of_the_day():
    motd = get_message_of_the_day()
    assert motd == "Welcome to our system! Today is a great day."
    # Breaks on any wording change

# ✅ GOOD: Test presence/structure (if critical)
def test_error_message_indicates_problem():
    result = validate("")
    assert "name" in result.error.lower()
    assert "empty" in result.error.lower()

# ✅ GOOD: No test at all (for informational messages)
# If the message isn't critical, don't test it
```

**When to test message content:**
- Security-critical messages (must contain specific info)
- Legal disclaimers (exact wording matters)
- API contracts (message format is documented)

**Otherwise:** Don't test message wording - it's a presentation detail.

---

## 3. Anti-Patterns to Avoid

### 3.1 Over-Mocking

❌ **Anti-Pattern:** Complex mock setups that mirror implementation details.

```python
# ❌ BAD: Over-mocking (testing implementation)
def test_process_order_with_mocks():
    with patch('module.Database') as mock_db, \
         patch('module.EmailService') as mock_email, \
         patch('module.PaymentProcessor') as mock_payment, \
         patch('module.InventoryService') as mock_inventory:

        mock_db.return_value.save.return_value = True
        mock_email.return_value.send.return_value = True
        mock_payment.return_value.charge.return_value = PaymentResult(success=True)
        mock_inventory.return_value.reserve.return_value = True

        order = Order()
        result = process_order(order)

        # Verifying all the mock calls - testing wiring!
        mock_db.return_value.save.assert_called_once()
        mock_email.return_value.send.assert_called_once()

# ✅ GOOD: Use fakes or real implementations
class FakePaymentService:
    """Lightweight fake for testing."""
    def __init__(self):
        self.charges = []

    def charge(self, amount):
        self.charges.append(amount)
        return {'success': True, 'transaction_id': 'test-txn'}

@pytest.fixture
def services():
    return {
        'payment': FakePaymentService(),
        'email': FakeEmailService()
    }

def test_process_order_charges_correct_amount(services):
    """Test that order processing charges the correct amount."""
    order = Order(total=100.00, customer_email='buyer@example.com')

    result = process_order(order, services)

    assert result.status == 'completed'
    assert len(services['payment'].charges) == 1
    assert services['payment'].charges[0] == 100.00
```

**Signs you're over-mocking:**
- Mocks that return mocks
- Mock setup is longer than test logic
- Tests verify call sequences rather than outcomes
- Tests break during unrelated refactoring

---

### 3.2 Excessive Assertions

❌ **Anti-Pattern:** Testing every property and field in a single test.

```python
# ❌ BAD: Too many assertions, unclear focus
def test_user_creation():
    user = create_user("Alice", "alice@example.com")

    # Testing everything at once
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.id is not None
    assert user.created_at is not None
    assert user.is_active == True
    assert user.role == "user"
    assert len(user.preferences) == 0
    assert user.last_login is None

# ✅ GOOD: One concept per test
def test_user_creation_sets_basic_fields():
    """Test that basic fields are set correctly."""
    user = create_user("Alice", "alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"

def test_user_creation_generates_id():
    """Test that user creation generates unique ID."""
    user1 = create_user("Alice", "alice@example.com")
    user2 = create_user("Bob", "bob@example.com")
    assert user1.id != user2.id

def test_user_creation_sets_default_status():
    """Test that new users are active by default."""
    user = create_user("Alice", "alice@example.com")
    assert user.is_active == True
```

---

### 3.3 Code Duplication in Tests

❌ **Anti-Pattern:** Copy-pasting setup code across multiple tests.

```python
# ❌ BAD: Duplicated setup
def test_order_with_one_item():
    order = Order()
    order.customer = Customer(name="Alice")
    order.items.append(Item(sku="ABC", price=10, quantity=1))
    order.shipping_address = Address(street="123 Main", city="NYC")
    # ... repeated in every test

def test_order_with_multiple_items():
    order = Order()
    order.customer = Customer(name="Alice")  # Duplicated!
    order.items.append(Item(sku="ABC", price=10, quantity=2))
    order.shipping_address = Address(street="123 Main", city="NYC")
    # ...

# ✅ GOOD: Use fixtures or builders
@pytest.fixture
def order():
    """Standard order for testing."""
    order = Order()
    order.customer = Customer(name="Test Customer")
    order.shipping_address = Address(street="123 Main", city="NYC")
    return order

def test_order_with_one_item(order):
    order.add_item(Item(sku="ABC", price=10, quantity=1))
    assert order.total() == 10

def test_order_with_multiple_items(order):
    order.add_item(Item(sku="ABC", price=10, quantity=2))
    order.add_item(Item(sku="DEF", price=20, quantity=1))
    assert order.total() == 40
```

---

## 4. Test Quality Indicators

### Good Tests:

| Indicator | Description |
|-----------|-------------|
| **Catches real bugs** | Would this test fail if code were broken? |
| **Enables refactoring** | Can you change implementation without changing test? |
| **Is readable** | Clear intent, obvious structure |
| **Runs fast** | Milliseconds, not seconds |
| **Is deterministic** | Same result every time |

### Low-Value Tests:

| Indicator | Description |
|-----------|-------------|
| **Tests trivial code** | Simple assignment, getter, obvious behavior |
| **Duplicates coverage** | Same behavior tested multiple times |
| **Tests implementation** | HOW not WHAT, breaks during refactoring |
| **Requires complex mocking** | Mock setup longer than test |
| **Never fails** | Would pass even with broken code |

---

## 5. Decision Tree: Should I Write a Test?

```
Is the code I'm testing trivial? (simple assignment, getter/setter, obvious logic)
└─ YES → Don't test. Save time for meaningful tests.

Is this a private method?
└─ YES → Don't test directly. Test the public interface instead.
         If it's complex, extract to a public class.

Is this third-party library code?
└─ YES → Don't test their code. Test YOUR integration with it.

Am I testing HOW it works (implementation)?
└─ YES → Refactor test to test WHAT it does (behavior).

Am I testing exact string content (messages, output)?
└─ YES → Don't test unless it's security-critical or a legal requirement.
         Test presence/structure instead, or delete the test.

Does a similar test already exist?
└─ YES → Don't duplicate. Extend the existing test if needed.

Would this test catch a real bug?
└─ NO → Don't write it. Focus on tests that provide value.

Is this testing a critical path or business logic?
└─ YES → Write the test! High value.

Is this testing edge cases or error handling?
└─ YES → Write the test! Edge cases are where bugs hide.

Is this a regression test for a production bug?
└─ YES → Write the test! Highest priority.

Can I write this test to survive refactoring?
├─ YES → Write it focused on behavior.
└─ NO → Reconsider the approach. Implementation-focused tests break.

Will this test run fast (<100ms)?
├─ YES → Write the test.
└─ NO → Consider if it's worth the slowdown. Can it be faster?

✅ WRITE THE TEST IF:
   - Tests business logic or critical functionality
   - Tests edge cases or error handling
   - Tests a regression for a bug
   - Verifies public API contracts
   - Catches real bugs
   - Enables refactoring
   - Runs fast

❌ DON'T WRITE THE TEST IF:
   - Code is trivial
   - It's a private method
   - It tests implementation details
   - Similar test exists
   - It wouldn't catch real bugs
   - It's framework/boilerplate code
   - It requires excessive mocking
   - It tests exact string content
```

---

## 6. Property-Based Testing (Hypothesis)

**One property test can replace dozens of manual test cases.**

```python
from hypothesis import given, strategies as st
from collections import Counter

# ❌ LIMITED: Manual test cases
def test_sort_empty_list():
    assert sort([]) == []

def test_sort_single_element():
    assert sort([1]) == [1]

def test_sort_two_elements():
    assert sort([2, 1]) == [1, 2]

def test_sort_duplicates():
    assert sort([2, 1, 2, 1]) == [1, 1, 2, 2]

# Still missing: already sorted, reverse sorted, large lists, etc.

# ✅ POWERFUL: Property-based testing
@given(st.lists(st.integers()))
def test_sort_always_returns_sorted_list(items):
    """Property: sort always returns a sorted list."""
    result = sort(items)
    assert result == sorted(items)  # Compare to reference implementation

@given(st.lists(st.integers()))
def test_sort_preserves_all_elements(items):
    """Property: sort preserves all elements (no loss, no duplication)."""
    result = sort(items)
    assert Counter(result) == Counter(items)

@given(st.lists(st.integers()))
def test_sort_is_idempotent(items):
    """Property: sorting already-sorted list returns same list."""
    sorted_once = sort(items)
    assert sort(sorted_once) == sorted_once
```

**Benefits:**
- Hypothesis generates hundreds of test cases automatically
- Finds edge cases humans miss
- Shrinking for debugging (finds minimal failing case)
- Tests properties/invariants, not examples
- Less code, more coverage

---

## 7. Test Organization

### Project Structure

```
project/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   ├── test_core.py         # Tests for core.py
│   ├── test_utils.py        # Tests for utils.py
│   └── integration/
│       └── test_api.py      # Integration tests
└── pytest.ini               # pytest configuration
```

### Naming Convention

```python
# test_<module>_<function>_<scenario>
def test_calculate_discount_premium_customer():
    ...

def test_calculate_discount_regular_customer():
    ...

def test_calculate_discount_invalid_customer_type():
    ...
```

### Group Related Tests

```python
class TestOrderProcessor:
    """Tests for OrderProcessor."""

    def test_process_valid_order(self):
        ...

    def test_process_order_with_no_items_raises(self):
        ...

    class TestCalculateTotal:
        """Tests for total calculation."""

        def test_sums_item_prices(self):
            ...

        def test_applies_discount(self):
            ...
```

---

## 8. Coverage Guidance

### Coverage is a Guardrail, Not a Target

**Use Coverage For:**
- Finding untested code paths
- Identifying gaps in testing
- Preventing coverage regression
- Guiding test prioritization

**Don't Use Coverage For:**
- Team performance metrics
- Mandatory percentage targets
- Quality assurance certification
- Replacing code review

### Risk-Based Coverage Matrix

| Code Type | Business Impact | Recommended Coverage | Test Focus |
|-----------|----------------|---------------------|------------|
| Payment processing | Critical | 95%+ | Comprehensive + property-based |
| Authentication | Critical | 95%+ | Security + edge cases |
| Business rules | High | 80-90% | Logic + calculations |
| API endpoints | Medium | 70-80% | Contracts + error handling |
| Data transformations | Medium | 70-80% | Edge cases + validation |
| Simple CRUD | Low | 50-60% | Basic functionality |
| Configuration | Low | Minimal | Integration test only |
| Trivial code | None | None | Don't test |

---

## 9. Summary Checklist

For every test, ask:

- [ ] Does this test catch real bugs?
- [ ] Does this test enable refactoring?
- [ ] Am I testing behavior (WHAT), not implementation (HOW)?
- [ ] Is this test testing something meaningful, or just executing code?
- [ ] Would this test survive implementation changes?
- [ ] Is this test testing a public interface, not private methods?
- [ ] Am I testing my code, not framework/library code?
- [ ] Is this test focused on one concept?
- [ ] Does this test run fast (<100ms)?
- [ ] Is this test deterministic (same result every time)?

---

## 10. Key Takeaways

1. **Test behavior, not implementation** - Tests should verify WHAT code does, not HOW.
2. **Test until fear turns to boredom** - Stop when important cases are covered.
3. **Delete trivial tests** - Getters, setters, dataclass defaults don't need tests.
4. **Don't test exact strings** - Message content is presentation detail.
5. **Avoid over-mocking** - Use fakes or real implementations when possible.
6. **Use property-based testing** - One property test > dozens of manual cases.
7. **Coverage is a signal, not a target** - Use it to find gaps, not game metrics.
8. **Tests must earn their keep** - Value must exceed maintenance cost.

---

**Golden Rule:** "A test is valuable if it catches bugs, enables refactoring, and survives implementation changes. Everything else is noise."