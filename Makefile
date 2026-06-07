.PHONY: install install-dev install-jobspy run doctor test lint lint-strict format clean

PYTHON ?= python
PIP ?= $(PYTHON) -m pip

install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e ".[dev]"

install-jobspy:
	$(PIP) install --no-deps python-jobspy
	$(PIP) install pydantic tls-client requests markdownify regex

run:
	applypilot run

doctor:
	applypilot doctor

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/ --select E9,F63,F7,F82

lint-strict:
	ruff check src/ tests/

format:
	ruff format src/ tests/

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
