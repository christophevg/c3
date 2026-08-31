---
name: fire
type: knowledge
description: Use this skill any time when creating code using Fire
---

# Fire Best Practices

When creating code using Fire, use the base practices in the sections below.

## When to Use

Use this skill whenever you create or edit code that uses [Fire](https://github.com/google/python-fire) for CLI generation — scaffolding a Fire CLI, exposing functions or objects as commands, or configuring `__main__` invocation.

## Naming __main__

When invoking Fire from `__main__.py`, add an explicit name argument, with the top-level module's name or the project name.

### Naming example

```python
    fire.Fire({
      "exposed name" : function
    }, name="projectname")
```

## Function Parameters

Always expose configurable variables, used in exposed functions, as function parameters. Add sensible defaults, using environment variables if possibly available.

### Parameter example

```python
def a_command(an_argument=None):
  if an_argument is None:
    an_argument = os.environ.get("ARGUMENT_ENV_NAME", "a sensible default")
  # perform logic using `an_argument`
```
## Related

- `python` — general code standards for Fire-based CLIs
- `rich` — styled console output commonly combined with Fire CLIs
