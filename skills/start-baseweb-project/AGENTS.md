# AGENTS.md

This file provides information about this project and instructions on how to develop code for it.

## Information

* The `README.md` file contains a section titled “Functionality” that describes the intended functionality of the application.

## Commands

The application and its Pyenv environments are managed using a `Makefile`:

- `make env-dev`: Activates the Pyenv development environment. This must be done before executing any Python code.
- `make run`: Activates the Pyenv run environment and starts the development server using gunicorn with eventlet workers.
- `make lint`: Activates the Pyenv development environment and runs `ruff` to detect linting mistakes.
- `make test`: Activates the Pyenv development environment and runs all tests. 
- `make coverage`: Provides a tabular overview of the test code coverage.
- Add new Python dependencies to `requirements.base.txt` without specifying versions, AND add them with version to `requirements.txt`. Then, run `make envs` to install these dependencies in all Pyenv environments.
- Always run `make lint`, `make test` and `make coverage` after making changes to verify the code is lint-free and tests pass and maintain coverage.

## Dependencies

The project uses two requirements files:

- `requirements.base.txt`: Base dependencies without version constraints. Used by `tox` for testing environments. **Always add new dependencies here first.**
- `requirements.txt`: Locked dependencies with specific versions. Used by the runtime environment.

When adding a new dependency:
1. Add the package name to `requirements.base.txt` (no version)
2. Add the package with version to `requirements.txt`
3. Run `make envs` to update all environments

## Architecture

The codebase is organized into two directories: `modulename` and `tests`.

- The `module` directory contains the main application logic.
- The `tests` directory contains unit and integration tests.

The application is built using `Baseweb`, a wrapper around `Flask`. It also provides a configured `Flask-RESTful` instance and access to `Flask-SocketIO`. Front-end support is provided through `Vue` and `Vuetify`. Backend Python code and frontend JavaScript code are kept together in a module directory, which is imported from the main application logic.

## Best Practices to Strictly Follow

* VERY IMPORTANT: You MUST avoid using the Bash tool for search commands like find and grep. Instead use Grep, Glob, or Task to search.
* Always begin with an overview of your plan
* Always explain your actions before executing them.
* Always use two spaces for indentation in all file types.
* Always write tests for new functionality and integrate them into the `tests` directory.
* Ensure that all tests are working at all times.
* Maintain test coverage.
* Ensure that every exception in the backend code is captured gracefully and reported back to the client in a human readable format. Also log the problem with context.
* Ignore the `.local` folder.
* Ignore the `notes` folder.
* Continue working on unchecked tasks from the `TODO.md` file in a top-down manner. Treat each task as the next prompt to process. Cross the Markdown checkbox when a task is completed and move it to the bottom of the file. At the end of each task, request a review before proceeding to the next task.
