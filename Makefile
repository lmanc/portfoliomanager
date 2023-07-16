PYTHON_FILES := $(shell find . -maxdepth 1 -name '*.py') $(shell find ./tests -name '*.py')

.PHONY: black
black:
	black -Sl 79 $(PYTHON_FILES)

.PHONY: isort
isort:
	isort $(PYTHON_FILES)


.PHONY: lint
lint: isort black


