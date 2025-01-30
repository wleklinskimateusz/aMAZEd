# Project Setup Guide

Welcome to the project! This guide will walk you through setting up the development environment and getting started.

## Prerequisites

Ensure you have the following installed on your system:

- **Python** (Recommended version: 3.12 or later)
  - Install Pyenv to manage multiple Python versions: https://github.com/pyenv/pyenv for windows you have to you pyenv-win
  - Install Python using Pyenv: `pyenv install 3.13.1`
  - run `pyenv local 3.13.1` to set the Python version for this repository
- **Poetry** (Dependency and virtual environment manager)
  - https://python-poetry.org/docs/

## Project Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/wleklinskimateusz/aMAZEd
    cd aMAZEd
    ```

2. **Install dependencies:**
    
    Install project dependencies with:
    
    ```bash
    poetry sync
    ```

    This will install all required dependencies based on `pyproject.toml` and `poetry.lock`.

## Running the Project

After setting up the environment, you can run the project by executing:

```bash
poetry run python src/maze_solver/main.py
```

## Code Formatting and Linting
### Running Ruff (linting)

```bash
poetry run ruff check .
```

### Fix linting issues automatically

```bash
poetry run ruff check . --fix
```

## Running ruff (formatting)

```bash
poetry run ruff format .
```
If you install a recommended VSCode extension you should have your files formatted automatically on save.

## Running type checker

```bash
poetry run mypy .
```
If you install a recommended VSCode extension you should have your files checked automatically on save.

## Running Tests

We use **pytest** for unit testing. Run tests using:

```bash
poetry run pytest
```

To run tests with coverage:

```bash
poetry run pytest --cov --cov-fail-under=100
```


## Additional Resources

- Poetry Documentation: [https://python-poetry.org/docs/](https://python-poetry.org/docs/)
- Python Documentation: [https://docs.python.org/3/](https://docs.python.org/3/)
- https://mypy-lang.org/


