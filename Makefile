#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = iragca-python
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python dependencies
.PHONY: requirements
requirements:
	uv sync


## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Lint using ruff (use `make format` to do formatting)
.PHONY: lint
lint:
	uv run ruff format --check
	uv run ruff check


## Format source code with ruff
.PHONY: format
format:
	uv run ruff check --fix
	uv run ruff format


## Run tests
.PHONY: test
test:
	uv run pytest tests


## Run mkdocs local server
.PHONY: docs
docs:
	uv run mkdocs serve -f docs/mkdocs.yml -a localhost:7000


## Build patch version
.PHONY: build-patch
build-patch:
	@uv version --bump patch
	@git add .
	@git commit -m "chore: publish patch version"
	@git push origin master


## Build minor version
.PHONY: build-minor
build-minor:
	@uv version --bump minor
	@git add .
	@git commit -m "chore: publish minor version"
	@git push origin master


## Publish
.PHONY: publish
publish:
	@bash -c ' \
		set -a; \
		source .env; \
		set +a; \
		uv build --no-sources; \
		uv publish; \
	'


## Build and publish the patch
.PHONY: publish-patch
publish-patch:
	@make build-patch
	@make publish


## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> New uv virtual environment created. Activate with:"
	@echo ">>> Windows: .\\\\.venv\\\\Scripts\\\\activate"
	@echo ">>> Unix/macOS: source ./.venv/bin/activate"
	



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
