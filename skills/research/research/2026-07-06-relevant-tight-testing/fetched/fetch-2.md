# The Practical Test Pyramid - Ham Vocke

Source: https://martinfowler.com/articles/practical-test-pyramid.html
Fetched: 2026-07-06T00:00:04Z

---

## What to Test

**Test the Public Interface**
The article recommends focusing on testing a class's "public interface." Private methods "can't be tested anyways since you simply can't call them from a different test class."

**Test Observable Behavior, Not Implementation**
The article warns against tests "too close to the production code" that break during refactoring. Instead: "Test for observable behaviour instead." Think in terms of: "if I enter values `x` and `y`, will the result be `z`?" rather than verifying internal method call sequences.

## What NOT to Test

**Private Methods**
The article frames the urge to test private methods as "more of a design problem than a scoping problem." The recommended solution is extracting the complex private method into a separate class where it becomes public and testable, thereby improving code structure.

**Trivial Code**
"Don't test trivial code" including simple getters, setters, or code without conditional logic. The article references Kent Beck's stance: "You won't gain anything from testing simple getters or setters."

## Avoiding Test Bloat

The article warns: "there's no such thing as too many tests let me assure you, there is." Two key principles:

1. **If a higher-level test catches an error with no lower-level test failing, write a lower-level test**
2. **Push tests as far down the pyramid as possible**

Higher-level tests should focus only on what lower-level tests cannot cover. The article recommends being "rigorous when it comes to eliminating tests that don't provide any value" and not falling for the sunk cost fallacy.