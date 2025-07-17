.PHONY: help install build test lint format clean

# UV executable
UV := uv
# Project name
PROJECT := sql-composer

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies using uv"
	@echo "  make build        - Build the package"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters (ruff, pyright)"
	@echo "  make format       - Format code using ruff"
	@echo "  make clean        - Remove Python cache files and build artifacts"

install:
	@echo "Creating virtual environment if it doesn't exist..."
	$(UV) venv
	@echo "Installing dependencies..."
	$(UV) pip install -e ".[dev]"

build:
	@echo "Building package..."
	$(UV) run python -m build

test:
	@echo "Running tests..."
	$(UV) run python -m pytest tests/ --cov=$(PROJECT) --cov-report=term-missing

lint:
	@echo "Running linters..."
	$(UV) run python -m ruff check .
	$(UV) run python -m ruff format --check .
	$(UV) run python -m pyright

format:
	@echo "Formatting code..."
	$(UV) run python -m ruff format .
	$(UV) run python -m ruff check --fix .

clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/ 