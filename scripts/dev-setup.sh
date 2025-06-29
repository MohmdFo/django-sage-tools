#!/bin/bash

# Django Sage Tools - Development Setup Script
set -e

echo "🚀 Setting up Django Sage Tools development environment..."

# Install dependencies
echo "📦 Installing dependencies..."
poetry install

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
poetry run pre-commit install

# Run code quality checks
echo "✨ Running code quality checks..."
poetry run black .
poetry run isort .
poetry run ruff check . --fix

# Run tests if they exist
if [ -d "sage_tools/tests" ]; then
    echo "🧪 Running tests..."
    poetry run pytest
fi

# Validate package can be built
echo "📦 Validating package build..."
poetry build

# Success message
echo "✅ Development environment setup complete!"
echo ""
echo "Available commands:"
echo "  poetry run black .                    # Format code"
echo "  poetry run isort .                    # Sort imports"
echo "  poetry run ruff check .               # Lint code"
echo "  poetry run pre-commit run --all-files # Run all checks"
echo "  poetry run pytest                     # Run tests"
echo "  poetry build                          # Build package"
echo "  poetry publish                        # Publish to PyPI"
echo ""
echo "🎉 Happy coding!" 