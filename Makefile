.PHONY: help install build test lint format clean

# Default Python interpreter
PYTHON := python3
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
	@echo "Installing dependencies..."
	$(UV) pip install -e .

build:
	@echo "Building package..."
	$(UV) pip install build
	$(PYTHON) -m build

test:
	@echo "Running tests..."
	$(UV) pip install pytest pytest-cov
	$(PYTHON) -m pytest tests/ --cov=$(PROJECT) --cov-report=term-missing

lint:
	@echo "Running linters..."
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .
	$(PYTHON) -m pyright

format:
	@echo "Formatting code..."
	$(PYTHON) -m ruff format .
	$(PYTHON) -m ruff check --fix .

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