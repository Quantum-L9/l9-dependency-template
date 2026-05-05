.PHONY: setup dev test test-unit test-integration lint lint-fix clean

setup:
	pip install -e ".[dev]"
	pre-commit install

dev:
	pip install -e ".[dev]"

test: lint
	pytest -q

test-unit:
	pytest tests/unit/ -q

test-integration:
	pytest tests/integration/ -q

lint:
	ruff check src tests
	mypy src

lint-fix:
	ruff check --fix src tests
	ruff format src tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
