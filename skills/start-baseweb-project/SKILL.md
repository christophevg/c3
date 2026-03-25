---
name: start-baseweb-project
description: Use this skill to start a new Baseweb-based project.
---

# Start Project

This skill is invoked by the user to start a new Baseweb-based project.

## Workflow Overview

When activated, follow this sequential workflow:

### Phase 1: Set up a baseweb demo setup as a template to start from

- Execute in the current folder: `git clone -b bare --single-branch https://github.com/christophevg/baseweb-demo`.
- Remove the `.git` folder from the newly cloned folder.
- Ask the user for the project name and a module name. The project name can include space, the module name can't. By default propose a module name, based on the project name, lowercase and without spaces, but let the user confirm the module name.
- Rename the newly cloned baseweb-demo folder to the chosen module name. Even if the module name is the same as the current folder, keep the nested folder structure. Don't try to merge its contents with the current folder.

### Phase 2: Add the Makefile to manage the project

- Copy the `Makefile` from this skill's folder to the current folder.
- Edit the `Makefile`, adding the provided module name as value for the `PROJECT` variable.

### Phase 3: Setup Baseweb requirements

- Copy the `requirements.base.txt` from this skill's folder to the current folder.
- Run `make envs` to create the virtual environments for development and running the project.

### Phase 4: Setup testing infrastructure

- Copy the `tests/` folder from this skill's folder to the current folder.
- Edit the `tests/test_setup.py` replacing "modulename" with the provided module name.

### Phase 4: Add the AGENTS.md file

- If there is no `AGENTS.md` file in the current folder, create one using the `AGENTS.md` file in this skill's folder as a template.

### Phase 5: Collect High Level Requirements

- If there is no `README.md` in the current folder, create one using the `README.md` file in this skill's folder as a template. Ask the user for a high level description of the intended functionality and store it in the `README.md` file.

### Phase 6: Setup Git Repository

- If there is no `.git` folder in the current folder, initialize the git repository using `git init`.
- If there is no `.gitignore` in the current folder, copy it from this skill's folder.
- Add everything to the git repository. Ask confirmation from the user to proceed with committing, using a sensible commit message for this initial/setup commit.
