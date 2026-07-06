# Canon TDD - Kent Beck

Source: https://newsletter.kentbeck.com/p/canon-tdd
Fetched: 2026-07-06T00:00:02Z

---

## The Five Steps of Canon TDD

1. **Write a test list** - List all expected variants in the new behavior. This is "behavioral analysis" thinking through all different cases. Avoid mixing in implementation design decisions.

2. **Write one test** - Create "a really truly automated test, with setup & invocation & assertions." Design decisions here are "primarily interface decisions." Don't convert all list items to tests at once—this causes rework if early tests change your thinking.

3. **Make it pass** - "Change the system so the test passes." Key mistakes to avoid: deleting assertions, copying actual values into expected values, or mixing refactoring into this step. When making a test pass, add newly discovered tests to the list.

4. **Optionally refactor** - "Now you get to make implementation design decisions." Key mistakes: refactoring further than necessary or abstracting too soon ("Duplication is a hint, not a command").

5. **Repeat until empty** - "Keep testing & coding until your fear for the behavior of the code has been transmuted into boredom."

## When and How Much to Test

The test list determines scope: "You'll never know when you're done" is incorrect—the list provides completion criteria. Add tests to the list as you discover them during implementation.

Picking test order matters: "The order of the tests can significantly affect both the experience of programming & the final result."

## The "Fear to Boredom" Philosophy

The testing continues until you have sufficient confidence—marked by boredom rather than fear about the code's behavior.

## TDD's Purpose

TDD helps programmers create system states where:
- "Everything that used to work still works"
- "The new behavior works as expected"
- "The system is ready for the next change"
- "The programmer & their colleagues feel confident"