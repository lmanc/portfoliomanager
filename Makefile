PYTHON_FILES := $(shell find . -maxdepth 1 -name '*.py') $(shell find ./tests -name '*.py')

.PHONY: black
black:
	black -S $(PYTHON_FILES)

.PHONY: isort
isort:
	isort $(PYTHON_FILES)

.PHONY: autopep8
autopep8:
	autopep8 -aaa --in-place $(PYTHON_FILES)

.PHONY: lint
lint: isort autopep8 black


