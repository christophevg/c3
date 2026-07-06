# Sources: Relevant and Tight Testing

**Date**: 2026-07-06T00:00:00Z
**Previous Research**: none

---

## Searches

### search-1

- **Query**: Kent Beck testing philosophy "test until fear turns to boredom"
- **Timestamp**: 2026-07-06T00:00:01Z
- **Results**:
  - [Canon TDD - by Kent Beck](https://newsletter.kentbeck.com/p/canon-tdd) - Kent Beck's comprehensive explanation of TDD
  - [Quote by Kent Beck](https://www.goodreads.com/quotes/10376041-write-tests-until-fear-is-transformed-into-boredom) - The famous quote about testing philosophy
  - [Canon TDD - by Kent Beck](https://tidyfirst.substack.com/p/canon-tdd) - Substack mirror of Canon TDD article
  - [What Should we Unit Test?](https://www.philosophicalhacker.com/post/what-should-we-unit-test/) - Analysis of Beck's testing philosophy
  - [To Test or Not to Test?](https://tidyfirst.substack.com/p/to-test-or-not-to-test-thats-a-good) - Beck's article on when to test

## Fetches

### fetch-1

- **URL**: https://newsletter.kentbeck.com/p/canon-tdd
- **Timestamp**: 2026-07-06T00:00:02Z
- **Source**: search-1
- **Title**: Canon TDD - Kent Beck
- **Content**: [fetched/fetch-1.md](fetched/fetch-1.md)
- **Summary**: Complete explanation of the five canonical steps of TDD, including the "test until fear turns to boredom" philosophy, test list creation, and guidance on when and how much to test.
- **Key Excerpts**:
  - "Write a test list - List all expected variants in the new behavior. This is 'behavioral analysis' thinking through all different cases."
  - "Make it pass - Change the system so the test passes."
  - "Optionally refactor - Now you get to make implementation design decisions."
  - "Repeat until empty - Keep testing & coding until your fear for the behavior of the code has been transmuted into boredom."

### search-2

- **Query**: Martin Fowler what not to test testing private methods testing getters setters
- **Timestamp**: 2026-07-06T00:00:03Z
- **Results**:
  - [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) - Ham Vocke's comprehensive guide on testing
  - [Getter Eradicator](https://martinfowler.com/bliki/GetterEradicator.html) - Martin Fowler on getters and encapsulation
  - [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html) - Fowler's article on mock objects
  - [Self Encapsulation](https://martinfowler.com/bliki/SelfEncapsulation.html) - Fowler on self-encapsulation
  - [Should I test private methods?](https://stackoverflow.com/questions/105007/should-i-test-private-methods-or-only-public-ones) - Stack Overflow discussion on testing private methods

### fetch-2

- **URL**: https://martinfowler.com/articles/practical-test-pyramid.html
- **Timestamp**: 2026-07-06T00:00:04Z
- **Source**: search-2
- **Title**: The Practical Test Pyramid - Ham Vocke
- **Content**: [fetched/fetch-2.md](fetched/fetch-2.md)
- **Summary**: Comprehensive guide on what to test and what NOT to test, including testing public interfaces vs private methods, testing behavior vs implementation, and avoiding test bloat.
- **Key Excerpts**:
  - "Test for observable behaviour instead. Think in terms of: if I enter values x and y, will the result be z?"
  - "Private methods should generally be considered an implementation detail. That's why you shouldn't even have the urge to test them."
  - "Don't test trivial code" including simple getters, setters, or code without conditional logic.
  - "There's no such thing as too many tests let me assure you, there is."

### search-3

- **Query**: Michael Feathers Working Effectively with Legacy Code what to test test coverage seam characterization tests
- **Timestamp**: 2026-07-06T00:00:05Z
- **Results**:
  - [Chapter 11: What Methods Should I Test?](https://www.oreilly.com/library/view/working-effectively-with/0131177052/ch11.html) - Feathers on selecting methods to test
  - [Working Effectively with Legacy Code PDF](https://ptgmedia.pearsoncmg.com/images/9780131177055/samplepages/0131177052.pdf) - Sample chapter from the book
  - [Chapter 4: The Seam Model](https://www.oreilly.com/library/view/working-effectively-with/0131177052/ch04.html) - Explanation of seams for testing
  - [Testing Effectively With Legacy Code](https://www.informit.com/articles/article.aspx?p=359417) - Article by Michael Feathers
  - [Working Effectively with Legacy Code](https://www.informit.com/title/0131177052) - Book information page

### search-4

- **Query**: Google testing blog unit testing anti-patterns test bloat over-mocking excessive tests
- **Timestamp**: 2026-07-06T00:00:06Z
- **Results**:
  - [Testing on the Toilet: Don't Overuse Mocks](https://testing.googleblog.com/2013/05/testing-on-toilet-dont-overuse-mocks.html) - Google's guidance on avoiding over-mocking
  - [Increase Test Fidelity By Avoiding Mocks](https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html) - Recent article on preferring real implementations
  - [Don't Mock Types You Don't Own](https://testing.googleblog.com/2020/07/testing-on-toilet-dont-mock-types-you.html) - Anti-pattern of mocking third-party code
  - [How Much Testing is Enough?](https://testing.googleblog.com/2021/06/how-much-testing-is-enough.html) - Guidance on appropriate test coverage
  - [Test Behavior, Not Implementation](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html) - Testing behavior vs implementation details

### fetch-3

- **URL**: https://testing.googleblog.com/2013/05/testing-on-toilet-dont-overuse-mocks.html
- **Timestamp**: 2026-07-06T00:00:07Z
- **Source**: search-4
- **Title**: Testing on the Toilet: Don't Overuse Mocks
- **Content**: [fetched/fetch-3.md](fetched/fetch-3.md)
- **Summary**: Google's guidance on why over-mocking is problematic, when to use mocks vs real implementations, and alternatives like fakes.
- **Key Excerpts**:
  - "The problem with mocks is they duplicate the logic of the code itself - instantly breaking DRY"
  - "Complex mock setups create brittle tests that break when you make unrelated changes"
  - "Tests become separated from reality the more mocks are used"
  - Focus on behavior, not implementation - "programmers tend to use mocks to test the implementation and not behavior"

### search-5

- **Query**: pytest best practices what to test vs what not to test test value Python testing philosophy
- **Timestamp**: 2026-07-06T00:00:08Z
- **Results**:
  - [Testing Best Practices in Python](https://dev.to/gpuneet/testing-best-practices-in-python-33jl) - Python testing best practices guide
  - [How to write and report assertions in tests](https://docs.pytest.org/en/stable/how-to/assert.html) - Official pytest documentation
  - [Python: Testing](https://llmbestpractices.com/coding/python-testing) - Python testing best practices
  - [Testing – Python Software Best Practices](https://adacs-australia.github.io/2023-07-21_OzGrav_Python_Training/Tests/index.html) - Python testing training
  - [Pytest Best Practices 2026](https://qaskills.sh/blog/pytest-best-practices-2026) - Current pytest best practices

### search-6

- **Query**: property-based testing hypothesis pytest fewer tests comprehensive coverage
- **Timestamp**: 2026-07-06T00:00:09Z
- **Results**:
  - [Getting Started With Property-Based Testing](https://semaphore.io/blog/property-based-testing-python-hypothesis-pytest) - Hypothesis and pytest tutorial
  - [Hypothesis Documentation](https://hypothesis.readthedocs.io/en/latest/reference/integrations.html) - Official Hypothesis docs
  - [An Empirical Evaluation of Property-Based Testing in Python](https://cseweb.ucsd.edu/~mcoblenz/assets/pdf/OOPSLA_2025_PBT.pdf) - Academic research on effectiveness
  - [Hypothesis: Property-Based Testing in Python](https://robulka.com/hypothesis/) - Introduction to Hypothesis
  - [Stop writing edge case tests](https://dev.to/peytongreen_dev/stop-writing-edge-case-tests-let-hypothesis-find-them-instead-5hl0) - Practical benefits

### search-7

- **Query**: test code smells brittle tests untestable code indicators when tests add no value
- **Timestamp**: 2026-07-06T00:00:10Z
- **Results**:
  - [Test code smells catalogue](https://korban.net/posts/2024-08-05-test-code-smells-catalogue) - Comprehensive test smells catalogue
  - [Poorly Written Tests Code Smell](https://deviq.com/code-smells/poorly-written-tests/) - DevIQ on problematic tests
  - [TestSmells at XUnitPatterns.com](http://xunitpatterns.com/TestSmells.html) - Classic test smell patterns
  - [Test smells 20 years later](https://link.springer.com/content/pdf/10.1007/s10664-022-10207-5.pdf) - Academic research on test smells
  - [When Tests Become a Liability](https://www.patcahill.io/articles/when-tests-become-a-liability) - Brittle tests and cost analysis

### search-8

- **Query**: "test coverage" metric vs quality 100% coverage harmful ROI of testing effort risk mitigation
- **Timestamp**: 2026-07-06T00:00:11Z
- **Results**:
  - [Test coverage vs risk coverage](https://www.testresults.io/blog/test-coverage-vs-risk-coverage-what-matters-more) - Coverage vs business risk
  - [Test Coverage: Signal, Illusion, or Guardrail?](https://qaexplained.com/coverage-signal-or-illusion/) - Coverage as quality metric
  - [Risk-Based Testing: Budgeting Test Effort](https://insights.orangeandbronze.com/risk-based-testing-software-quality/) - Prioritizing tests by risk
  - [Coverage Obsession: The Metric That Ate Quality Engineering](https://www.viney.ca/2026/04/05/the-productivity-paradox-of-test-coverage-metrics/) - Problems with coverage targets
  - [Too much of a good thing: the trade-off we make with tests](https://www.ntietz.com/blog/too-much-of-a-good-thing-the-cost-of-excess-testing/) - Cost of excessive testing

## Citations

<!-- Track citations used in report -->

## Excluded Findings

<!-- Record information found but excluded as incorrect/irrelevant -->