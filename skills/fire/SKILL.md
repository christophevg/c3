---
name: fire-best-practices
description: Use this skill any time when creating code using Fire
---

# Fire Best Practices

When creating code using Fire, use the base practices in the sections below.

## Naming __main__

When invoking Fire from `__main__.py`, add an explicit name argument, with the top-level module's name or the project name.

### Example

```python
    fire.Fire({
      "exposed name" : function
    }, name="projectname")
```

## Function Parameters

Always expose configurable variables, used in exposed functions, as function parameters. Add sensible defaults, using environment variables if possibly available.

### Example

```python
def a_command(an_argument=None):
  if an_argument is None:
    an_argument = os.environ.get("ARGUMENT_ENV_VAR_NAME", "a sensible default")
  # perform logic using `an_argument`
```
