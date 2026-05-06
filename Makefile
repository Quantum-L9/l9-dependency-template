.PHONY: setup dev test test-unit test-integration lint lint-fix security docs mutate clean

setup:
	uv sync --frozen --extra dev
	pre-commit install

dev:
	uv sync --frozen --extra dev

test: lint
	uv run pytest -q --cov=src --cov-report=term-missing --cov-fail-under=90

test-unit:
	uv run pytest tests/unit/ -q --cov=src --cov-report=term-missing

test-integration:
	uv run pytest tests/integration/ -q

lint:
	uv run ruff check src tests
	uv run mypy src

lint-fix:
	uv run ruff check --fix src tests
	uv run ruff format src tests

security:
	uv run pip-audit --strict
	uv run bandit -r src -ll -q

docs:
	uv run mkdocs build --config-file docs/mkdocs.yml

docs-serve:
	uv run mkdocs serve --config-file docs/mkdocs.yml

mutate:
	uv run mutmut run --paths-to-mutate src/constellation_template/

mutate-results:
	uv run mutmut results

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info"  -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -name ".coverage" -delete
	rm -rf dist/ build/ site/
