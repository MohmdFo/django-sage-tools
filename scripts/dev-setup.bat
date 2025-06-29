@echo off
REM Django Sage Tools - Development Setup Script (Windows)

echo 🚀 Setting up Django Sage Tools development environment...

REM Install dependencies
echo 📦 Installing dependencies...
poetry install

REM Install pre-commit hooks
echo 🔧 Installing pre-commit hooks...
poetry run pre-commit install

REM Run code quality checks
echo ✨ Running code quality checks...
poetry run black .
poetry run isort .
poetry run ruff check . --fix

REM Run tests if they exist
if exist "sage_tools\tests" (
    echo 🧪 Running tests...
    poetry run pytest
)

REM Validate package can be built
echo 📦 Validating package build...
poetry build

REM Success message
echo ✅ Development environment setup complete!
echo.
echo Available commands:
echo   poetry run black .                    # Format code
echo   poetry run isort .                    # Sort imports
echo   poetry run ruff check .               # Lint code
echo   poetry run pre-commit run --all-files # Run all checks
echo   poetry run pytest                     # Run tests
echo   poetry build                          # Build package
echo   poetry publish                        # Publish to PyPI
echo.
echo 🎉 Happy coding! 