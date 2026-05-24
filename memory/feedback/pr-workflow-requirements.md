# PR Workflow Requirements

## Issues Are Urgent

When GitHub issues exist without status labels:
- **Do NOT ask for confirmation**
- Automatically start working on them
- Issues represent urgent user needs

## CI Must Pass

PR creation is not complete until CI passes:
1. Create PR
2. Monitor CI status
3. Fix any failures
4. Push fixes
5. Repeat until CI passes
6. Only then report PR complete to user

## Always Assign AND Request Review

Both actions are required:
```bash
gh pr edit {number} --add-assignee {user}
gh pr edit {number} --add-reviewer {user}
```

This ensures:
- User is notified for review
- PR is tracked in user's assigned list