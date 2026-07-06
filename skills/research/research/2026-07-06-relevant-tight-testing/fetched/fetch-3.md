# Don't Overuse Mocks - Google Testing Blog

Source: https://testing.googleblog.com/2013/05/testing-on-toilet-dont-overuse-mocks.html
Fetched: 2026-07-06T00:00:07Z

---

## Why Overusing Mocks is Problematic

- Complex mock setups create "brittle tests that break when you make unrelated changes"
- Mocks that require multiple mocks returning other mocks indicate overuse
- "The problem with mocks is they duplicate the logic of the code itself - instantly breaking DRY"
- Over-mocking creates tests "that are hard to maintain"
- Tests become "separated from reality" the more mocks are used

## Code Smells to Avoid

- Code that "reaches through 4 levels of dependencies" (Law of Demeter violations)
- "Partial mocks" which add complexity
- Mocks that need to "talk to each other"
- Indiscriminately mocking "all dependencies"

## Better Alternatives

- Use "a fake in-memory version" of the dependency
- Start up "a local version of the server for the test"
- Refactor to separate business logic from infrastructure concerns
- Use integration/component tests for collaboration between services
- Consider fakes over mocks for complex dependencies

## When Mocks Work Well

- Testing interactions between components
- When you need your code in "a certain state" (e.g., returning empty list)
- For simple interfaces with straightforward behavior
- When dependencies are heavyweight (network calls, slow operations)

## Key Recommendation

Focus tests on behavior, not implementation details. As one commenter noted: "programmers tend to use mocks to test the implementation and not behavior" leading to "tests with high coupling with the code."