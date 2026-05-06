.PHONY: setup dev test test-unit test-integration lint lint-fix security clean

setup:
	pip install -e ".[dev]"
	pre-commit install

dev:
	pip install -e ".[dev]"

test: lint
	pytest -q --cov=src --cov-report=term-missing --cov-fail-under=90

test-unit:
	pytest tests/unit/ -q --cov=src --cov-report=term-missing

test-integration:
	pytest tests/integration/ -q

lint:
	ruff check src tests
	mypy src

lint-fix:
	ruff check --fix src tests
	ruff format src tests

security:
	pip-audit --strict
	bandit -r src -ll -q

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
