# Test Creation Patterns

Platform-specific guidance for creating tests that demonstrate bugs.

## TDD for Bugs: Two-Phase Approach

### Phase 1: Demonstrate the Bug

Create a test that **passes with current (incorrect) behavior**.

```python
# Example: Bug causes login to fail
def test_login_with_valid_credentials_fails():
    """This test passes, proving the bug exists."""
    result = login(username="user", password="valid_pass")
    assert result.success == False  # Currently fails, so test passes
```

### Phase 2: Fix and Update

After fixing, update the test to expect correct behavior.

```python
def test_login_with_valid_credentials_succeeds():
    """This test verifies the fix works."""
    result = login(username="user", password="valid_pass")
    assert result.success == True  # Now expects correct behavior
```

## Test Type Selection

| Bug Location | Bug Type | Recommended Test |
|--------------|----------|------------------|
| Single function/method | Logic, calculation | Unit test |
| Class/module boundary | Integration | Integration test |
| API endpoint | Contract, validation | Integration test |
| Database | Query, transaction | Integration test |
| User flow | End-to-end | E2E test |
| UI component | Rendering, interaction | Component test |

## Frontend Bug Patterns

### Async Race Conditions

**Symptoms:** Intermittent failures, stale data, unexpected state

**Test Pattern:**
```javascript
// Demonstrate race condition
test('async operations complete in order', async () => {
  const results = [];
  
  // Simulate concurrent requests
  await Promise.all([
    fetchUser(1).then(r => results.push(r)),
    fetchUser(2).then(r => results.push(r))
  ]);
  
  // Bug: results may be in wrong order
  expect(results[0].id).toBe(1); // May fail intermittently
});
```

**Fix Pattern:**
- Use `Promise.all` with ordered results
- Implement request queuing
- Use `AbortController` for cancellation

### Stale State

**Symptoms:** UI shows old data after updates

**Test Pattern:**
```javascript
test('state updates reflect immediately', () => {
  const { result } = renderHook(() => useCounter());
  
  act(() => {
    result.current.increment();
  });
  
  // Bug: May show stale value
  expect(result.current.count).toBe(1);
});
```

**Fix Pattern:**
- Create new object references (immutability)
- Use state management patterns correctly
- Ensure proper reactivity

### Rendering Bugs

**Symptoms:** Component doesn't update, wrong display

**Test Pattern:**
```javascript
test('component re-renders on prop change', () => {
  const { rerender } = render(<Component value={1} />);
  
  rerender(<Component value={2} />);
  
  // Bug: May show old value
  expect(screen.getByText('2')).toBeInTheDocument();
});
```

## Backend Bug Patterns

### N+1 Query Bug

**Symptoms:** Slow page loads, many database queries

**Test Pattern:**
```python
def test_no_n_plus_one_queries():
    """Demonstrate N+1 query bug."""
    queries = []
    
    # Patch or mock query counter
    with QueryCounter() as counter:
        users = User.query.all()
        for user in users:
            _ = user.posts  # Bug: Triggers query per user
    
    # Bug: Queries = 1 (users) + N (posts per user)
    assert counter.count == 1 + len(users)  # Should fail
```

**Fix Pattern:**
```python
# Django
User.objects.select_related('profile').all()

# Rails
User.includes(:posts).all

# SQLAlchemy
session.query(User).options(joinedload(User.posts)).all()
```

### Missing Index Bug

**Symptoms:** Queries slow progressively, DB CPU high

**Test Pattern:**
```python
def test_query_uses_index():
    """Demonstrate missing index bug."""
    # Create large dataset
    for i in range(10000):
        factory.create_record(field=i)
    
    import time
    start = time.time()
    Record.query.filter_by(field=5000).first()
    duration = time.time() - start
    
    # Bug: Should be < 50ms with index, but is > 500ms without
    assert duration < 0.05  # Fails without index
```

**Fix Pattern:**
```sql
CREATE INDEX CONCURRENTLY idx_records_field ON records(field);
```

### Connection Pool Exhaustion

**Symptoms:** Timeouts, not crashes

**Test Pattern:**
```python
def test_connection_pool_not_exhausted():
    """Demonstrate connection pool bug."""
    # Simulate concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(api_call) for _ in range(100)]
        results = [f.result() for f in futures]
    
    # Bug: Some requests timeout
    assert all(r.status == 200 for r in results)  # May fail
```

## Mobile Bug Patterns

### Device/OS Variations

**Test Pattern:**
```swift
// iOS
func testButtonVisibleOnAllDevices() {
    // Bug: Button may be cut off on smaller screens
    let deviceNames = ["iPhone 13 mini", "iPhone 14 Pro Max", "iPad Pro"]
    
    for device in deviceNames {
        let frame = calculateButtonFrame(for: device)
        XCTAssert(frame.width > 0 && frame.height > 0)
    }
}
```

**Fix Pattern:**
- Use Auto Layout / Constraint Layout
- Test on multiple device sizes
- Use size classes

### Memory Leaks

**Test Pattern:**
```swift
func testNoMemoryLeak() {
    weak var weakReference: AnyObject?
    
    autoreleasepool {
        let object = createObject()
        weakReference = object
    }
    
    // Bug: If leaked, reference still exists
    XCTAssertNil(weakReference)
}
```

## Database Bug Patterns

### Transaction Deadlock

**Test Pattern:**
```python
def test_no_deadlock_concurrent_updates():
    """Demonstrate deadlock bug."""
    def update_both():
        with transaction():
            a = A.get(1)
            b = B.get(1)
            a.value += 1
            b.value += 1
    
    # Run concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(update_both) for _ in range(10)]
        results = [f.result() for f in futures]
    
    # Bug: Some may deadlock
    assert all(r.success for r in results)
```

**Fix Pattern:**
- Always acquire locks in consistent order
- Use context managers for transactions
- Keep transactions short

## Test Framework Detection

### Python Projects

| File | Framework |
|------|-----------|
| `pytest.ini` | pytest |
| `setup.cfg` with `[tool:pytest]` | pytest |
| `tox.ini` with `[pytest]` | pytest |
| `unittest` imports | unittest |

### JavaScript/TypeScript Projects

| File | Framework |
|------|-----------|
| `jest.config.js` | Jest |
| `vitest.config.ts` | Vitest |
| `mocha.opts` | Mocha |
| `karma.conf.js` | Karma |

### Other Projects

| File | Framework |
|------|-----------|
| `Gemfile` with `rspec` | RSpec (Ruby) |
| `pom.xml` with `junit` | JUnit (Java) |
| `go.mod` with testing package | Go testing |
| `Cargo.toml` with `[dev-dependencies]` | Rust tests |

## Test Creation Checklist

- [ ] Test is minimal (only essential code)
- [ ] Test is reproducible (runs consistently)
- [ ] Test has clear expected vs actual
- [ ] Test documents the bug it demonstrates
- [ ] Test covers the specific failure mode
- [ ] Test can be run in under 60 seconds
- [ ] Test includes necessary setup/teardown