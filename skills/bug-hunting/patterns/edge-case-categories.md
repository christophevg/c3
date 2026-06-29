# Edge Case Categories

Comprehensive categorization of edge cases for systematic bug hunting.

## Input Boundaries

### Empty Values
- Empty collections: `[]`, `{}`, `set()`, `""`, `b""`
- None/null values: `None`, `null`, `nil`
- Zero values: `0`, `0.0`, `0j`
- False values: `False`, `no`, `off`

### Single Element
- Single-item collections: `[x]`, `{k: v}`
- One-character strings: `"a"`
- Minimal valid input

### Maximum Sizes
- Memory limits: Very large collections
- Integer overflow: `sys.maxsize + 1`
- String limits: Very long strings
- Recursion depth: Exceeding maximum recursion

### Boundary Values
- Minimum: `-sys.maxsize - 1`, smallest float
- Maximum: `sys.maxsize`, largest float
- Zero: `0`, `0.0`, `-0.0`
- One-off: `min - 1`, `max + 1`

### Special Characters
- Unicode: Non-ASCII, emoji, combining characters
- Control characters: `\0`, `\n`, `\r`, `\t`
- Delimiters: Quotes, brackets, separators
- Escape sequences: `\\`, `\n`, `\"`

### Encodings
- UTF-8, UTF-16, UTF-32
- ASCII vs non-ASCII
- Byte order marks
- Invalid encoding sequences

## Configuration Edge Cases

### Missing Data
- Missing required fields
- Missing optional fields
- Missing sections/keys
- Missing default values

### Empty Files
- Empty configuration file
- Empty sections
- Whitespace-only files
- Comments-only files

### Type Mismatches
- String where number expected
- Array where object expected
- Boolean where string expected
- Null where value required

### Circular References
- Direct circular dependency
- Indirect circular dependency
- Self-referencing structures
- Mutually referencing configs

### Duplicate Keys
- Duplicate keys in same section
- Case-sensitive duplicates
- Duplicate with different types
- Duplicate across inheritance

### Invalid Values
- Out-of-range values
- Invalid enum values
- Malformed values
- Incompatible format values

### Deep Nesting
- Exceeding recursion limit
- Very deep object hierarchies
- Mixed nesting patterns
- Unbalanced structures

### Inheritance Issues
- Multiple inheritance conflicts
- Diamond problem
- Missing parent config
- Circular inheritance

## Concurrency Edge Cases

### Race Conditions
- Time-of-check to time-of-use (TOCTOU)
- Read-modify-write races
- Initialization races
- Lazy initialization races

### Resource Contention
- Database connection limits
- File handle exhaustion
- Memory pressure
- CPU saturation

### Deadlocks
- Lock ordering issues
- Circular wait conditions
- Resource starvation
- Priority inversion

### Thread Safety
- Shared mutable state
- Atomic operation failures
- Non-thread-safe collections
- Singleton initialization

### Async Issues
- Awaiting multiple coroutines
- Cancellation during operation
- Timeout handling
- Exception propagation in async

## Security Edge Cases

### Injection Attacks
- SQL injection
- Command injection
- Code injection
- Template injection
- LDAP injection
- XPath injection

### Path Traversal
- Directory traversal: `../`
- Absolute paths
- Symbolic links
- URL encoding bypasses

### Privilege Escalation
- Horizontal escalation
- Vertical escalation
- Privilege confusion
- Missing authorization checks

### Resource Exhaustion
- Memory exhaustion (OOM)
- CPU exhaustion (DoS)
- Disk exhaustion
- Connection exhaustion

### Input Validation Bypasses
- Unicode normalization
- Encoding tricks
- Null byte injection
- Length limit bypasses

### Authentication Edge Cases
- Empty passwords
- Very long passwords
- Special characters in credentials
- Token expiration edge cases
- Session fixation

### Authorization Edge Cases
- Missing permissions
- Empty roles
- Conflicting permissions
- Inheritance edge cases

### Cryptographic Issues
- Weak randomness
- Timing attacks
- Padding oracle
- Key management

## Integration Edge Cases

### Missing Dependencies
- Optional dependencies
- Version mismatches
- Missing transitive deps
- Platform-specific deps

### API Version Mismatches
- Breaking changes
- Deprecated endpoints
- Feature flags
- Version negotiation

### Network Failures
- Connection timeout
- Read timeout
- Write timeout
- DNS resolution failure
- Connection refused

### Partial Failures
- Partial writes
- Incomplete responses
- Interrupted transfers
- Recovery from partial state

### Timeout Scenarios
- Zero timeout
- Very short timeout
- Very long timeout
- Timeout during cleanup

### Retry Scenarios
- Immediate retry
- Exponential backoff
- Retry budget exhaustion
- Idempotency violations

### Order-Dependent Operations
- Out-of-order messages
- Missing prerequisite
- Duplicate operations
- Competing operations

## Performance Edge Cases

### Large Inputs
- Memory limits
- Processing time
- Garbage collection pressure
- Cache efficiency

### Deeply Nested Structures
- Stack overflow
- Recursion limits
- Parsing time
- Memory fragmentation

### Concurrent Operations
- Lock contention
- Resource limits
- Queue saturation
- Thread pool exhaustion

### Resource Limits
- File descriptors
- Database connections
- Network sockets
- Memory limits

### Scaling Edge Cases
- Zero to N transition
- N to N+1 transition
- Negative scaling
- Rapid scaling

### Caching Edge Cases
- Cache stampede
- Cache invalidation
- Stale cache
- Cache poisoning

### Memory Edge Cases
- Memory fragmentation
- Large object allocation
- Garbage collection timing
- Memory leaks

## Data Flow Edge Cases

### Transformation Chain
- Identity transformation
- Null propagation
- Error propagation
- Type coercion edge cases

### Validation Chain
- Multiple validators
- Conflicting validators
- Validator ordering
- Early vs late validation

### Serialization Edge Cases
- Circular references
- Non-serializable objects
- Format edge cases
- Encoding edge cases

### State Machine Edge Cases
- Invalid state transitions
- Missing state handlers
- Concurrent state changes
- State corruption

## Platform Edge Cases

### Operating System
- File path separators
- Line endings
- Environment variables
- Signal handling

### Python Version
- Version-specific features
- Standard library changes
- Syntax differences
- Performance differences

### File System
- Case sensitivity
- Permission issues
- Disk full
- Read-only filesystems

### Time and Date
- Timezone handling
- Daylight saving transitions
- Leap seconds
- Date parsing edge cases

## Error Handling Edge Cases

### Exception Chaining
- Nested exceptions
- Exception during exception handling
- Lost exception context

### Recovery
- Partial recovery
- Recovery failure
- Resource cleanup failure

### Logging
- Log failures
- Very large log messages
- Log rotation
- Structured logging edge cases

### User Messaging
- Error message clarity
- Error message security
- Localization issues
- Missing error messages