PROJECT =
PYTHON_VERSION ?= 3.11.12
RUFF_PYTHON_VERSION ?= py311
MODEL ?= glm-5:cloud

all: test run

claude: env-dev
	ollama launch claude --model ${MODEL}

lint: env-dev
	ruff check --target-version=$(RUFF_PYTHON_VERSION) .

test: env-dev
	coverage run -m pytest

coverage: env-dev
	coverage report

run: env-run
	gunicorn -k eventlet -w 1 $(PROJECT).web:server

# environment selection

env-run:
	pyenv local $(PROJECT)-run

env-dev:
	pyenv local $(PROJECT)-dev

# environment creation

envs: create-env-dev create-env-run env-dev

create-env-dev:
	pyenv local --unset
	-pyenv virtualenv $(PYTHON_VERSION) $(PROJECT)-dev  > /dev/null
	pyenv local $(PROJECT)-dev
	pip install -U pip ruff pytest coverage -r requirements.base.txt  > /dev/null

create-env-run:
	pyenv local --unset
	-pyenv virtualenv $(PYTHON_VERSION) $(PROJECT)-run  > /dev/null
	pyenv local $(PROJECT)-run
	pip install -U pip gunicorn eventlet -r requirements.base.txt  > /dev/null

clean:
	rm -rf .ruff_cache .coverage
