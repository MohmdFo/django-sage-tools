.PHONY: help install test lint format clean build publish dev-setup

help: ## Show this help message
	@echo 'Django Sage Tools - Available Make Commands:'
	@echo ''
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies
	poetry install

dev-setup: install ## Complete development environment setup
	poetry run pre-commit install
	@echo "✅ Development environment ready!"

test: ## Run tests
	poetry run pytest

test-cov: ## Run tests with coverage
	poetry run pytest --cov=sage_tools --cov-report=html --cov-report=term

lint: ## Run linting
	poetry run ruff check .
	poetry run mypy sage_tools

format: ## Format code
	poetry run black .
	poetry run isort .
	poetry run ruff check . --fix

format-check: ## Check formatting without making changes
	poetry run black --check .
	poetry run isort --check-only .
	poetry run ruff check .

pre-commit: ## Run pre-commit hooks
	poetry run pre-commit run --all-files

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean ## Build package
	poetry build

check-build: build ## Check built package
	poetry run twine check dist/*

setup-testpypi: ## Setup TestPyPI repository
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	@echo "⚠️  Now set your TestPyPI token: poetry config pypi-token.testpypi YOUR_TEST_TOKEN"

publish-test: build setup-testpypi ## Publish to Test PyPI
	@echo "🚀 Publishing to Test PyPI..."
	poetry publish -r testpypi
	@echo "✅ Check your package at: https://test.pypi.org/project/django-sage-tools/"

publish-check: ## Check if ready to publish
	@echo "📋 Pre-publish checklist:"
	@echo "  - PyPI token configured: poetry config pypi-token.pypi YOUR_TOKEN"
	@echo "  - Version updated in pyproject.toml"
	@echo "  - CHANGELOG.md updated"
	@echo "  - All tests passing"
	@echo "  - Code quality checks pass"
	poetry check
	poetry build
	poetry run twine check dist/*
	@echo "✅ Package is ready for publishing!"

publish: build ## Publish to PyPI
	@echo "🚀 Publishing to PyPI..."
	poetry publish
	@echo "✅ Published! Check: https://pypi.org/project/django-sage-tools/"

version-patch: ## Bump patch version
	poetry run cz bump --increment PATCH

version-minor: ## Bump minor version
	poetry run cz bump --increment MINOR

version-major: ## Bump major version
	poetry run cz bump --increment MAJOR

changelog: ## Update changelog
	poetry run cz changelog

docs: ## Build documentation
	cd docs && make html

all: format lint test build ## Run full quality pipeline 