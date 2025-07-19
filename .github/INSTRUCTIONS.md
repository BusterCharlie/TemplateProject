# Project Instructions

This document provides instructions for maintaining code quality using Ruff.

## Code Formatting and Linting with Ruff

This project uses [Ruff](https://docs.astral.sh/ruff/) for extremely fast Python linting and code formatting. It is a replacement for tools like Flake8, isort, and Black.

### Setup

The required dependency (`ruff`) is listed in `pyproject.toml` and will be installed automatically by the `run.sh` or `run.bat` script into the project's virtual environment.

### Usage

1.  **Activate the virtual environment:**
    -   On macOS/Linux: `source .venv/bin/activate`
    -   On Windows: `.venv\Scripts\activate`

2.  **Check for linting errors:**
    ```bash
    ruff check .
    ```

3.  **Automatically fix linting errors:**
    Many errors can be fixed automatically.
    ```bash
    ruff check . --fix
    ```

4.  **Format your code:**
    This ensures a consistent code style across the entire project.
    ```bash
    ruff format .
    ```

### Configuration

Ruff's behavior is configured in the `pyproject.toml` file under the `[tool.ruff]` section. You can customize rules and settings there.
