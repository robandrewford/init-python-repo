#!/bin/bash
set -euo pipefail

#==============================================================================
# Configuration
#==============================================================================
# Unset VIRTUAL_ENV to avoid uv warnings when running inside a venv
unset VIRTUAL_ENV

PYTHON_VERSION="${PYTHON_VERSION:-3.12}"
# Original directory name from the path
PROJECT_DIR_NAME="$(basename "$PWD")"
# Sanitized name for Python package/module usage (using underscores)
PROJECT_NAME="$(echo "$PROJECT_DIR_NAME" | tr '-' '_' | tr '.' '_')"

# Feature flags (override via environment)
INCLUDE_VSCODE="${INCLUDE_VSCODE:-true}"
INCLUDE_DOCKER="${INCLUDE_DOCKER:-true}"
INCLUDE_MAKEFILE="${INCLUDE_MAKEFILE:-true}"
INCLUDE_CHANGELOG="${INCLUDE_CHANGELOG:-true}"
INCLUDE_SECURITY="${INCLUDE_SECURITY:-true}"
INCLUDE_DEPENDABOT="${INCLUDE_DEPENDABOT:-true}"

# Project type: library | api | cli | data | tui
PROJECT_TYPE="${PROJECT_TYPE:-library}"

#==============================================================================
# Validation
#==============================================================================
# Prevent project name that shadowing dev dependency
if [[ "$PROJECT_NAME" == "test-repo" ]]; then
    echo "ERROR: Project name 'test-repo' is invalid due to shadowing." >&2
    exit 1
fi

if [[ -f "pyproject.toml" ]]; then
    echo "ERROR: pyproject.toml already exists" >&2
    exit 1
fi

if [[ -n "$(ls -A 2>/dev/null)" ]]; then
    echo "ERROR: Directory not empty. Run from empty project directory." >&2
    exit 1
fi

echo "Initializing ${PROJECT_NAME} (Python ${PYTHON_VERSION}, type: ${PROJECT_TYPE})"

#==============================================================================
# Base initialization
#==============================================================================
# We force the name to PROJECT_NAME to ensures it's a valid Python identifier
# and to avoid uv's automatic dash-conversion for the package structure it might infer.
uv init . --python "$PYTHON_VERSION" --no-workspace --name "$PROJECT_NAME"
# Remove default hello.py/main.py created by uv init to avoid mypy errors
rm -f hello.py main.py
# Some uv versions might still use the directory name for the project name field in pyproject.toml
sed -i '' "s/name = \".*\"/name = \"$PROJECT_NAME\"/" pyproject.toml
echo "$PYTHON_VERSION" > .python-version

# Configure uv to treat the project as a package for local discovery
cat >> pyproject.toml << EOF

[tool.uv]
package = true
EOF

#==============================================================================
# Dependencies by project type
#==============================================================================
# Core dev dependencies (all project types)
uv add --dev ruff pytest pytest-cov mypy pre-commit pytest-asyncio

case "$PROJECT_TYPE" in
    api)
        uv add fastapi uvicorn httpx pydantic pydantic-settings python-dotenv structlog
        uv add --dev httpx  # async test client
        ;;
    cli)
        uv add typer rich python-dotenv
        ;;
    data)
        uv add polars pyarrow duckdb sqlalchemy httpx pydantic python-dotenv structlog
        uv add --dev faker  # test data generation
        ;;
    tui)
        uv add textual rich python-dotenv
        uv add --dev textual-dev pytest-asyncio
        ;;
    library)
        # Minimal — no runtime dependencies by default
        ;;
    *)
        echo "ERROR: Unknown PROJECT_TYPE: ${PROJECT_TYPE}" >&2
        echo "Valid options: library, api, cli, data, tui" >&2
        exit 1
        ;;
esac

if [[ "$INCLUDE_SECURITY" == "true" ]]; then
    uv add --dev bandit detect-secrets
fi

uv lock
uv sync

#==============================================================================
# pyproject.toml extensions
#==============================================================================
cat >> pyproject.toml << EOF

[project.scripts]
${PROJECT_NAME} = "${PROJECT_NAME}.main:app"

[tool.ruff]
line-length = 120
target-version = "py${PYTHON_VERSION//./}"
src = ["src"]

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "RUF"]

[tool.mypy]
strict = true
python_version = "${PYTHON_VERSION}"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=term-missing"
asyncio_mode = "auto"
EOF

# Force editable install of the current project to ensure source is discoverable
uv add --dev --editable .

if [[ "$PROJECT_TYPE" == "tui" ]]; then
    cat >> pyproject.toml << 'EOF'
asyncio_mode = "auto"
EOF
fi

if [[ "$INCLUDE_SECURITY" == "true" ]]; then
    cat >> pyproject.toml << 'EOF'

[tool.bandit]
exclude_dirs = ["tests"]
EOF
fi

#==============================================================================
# .gitignore
#==============================================================================
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
.venv/
.mypy_cache/
.pytest_cache/
.ruff_cache/
*.egg-info/
dist/
.coverage
htmlcov/
.env
.secrets.baseline
EOF

#==============================================================================
# .env handling
#==============================================================================
cat > .env.example << 'EOF'
# Copy to .env and fill in values
LOG_LEVEL=INFO
EOF

case "$PROJECT_TYPE" in
    api)
        cat >> .env.example << 'EOF'
HOST=0.0.0.0
PORT=8000
DATABASE_URL=
EOF
        ;;
    data)
        cat >> .env.example << 'EOF'
DATABASE_URL=
AWS_PROFILE=
EOF
        ;;
esac

#==============================================================================
# Final project registration
#==============================================================================
# Run a final sync to ensures the project itself is installed and discoverable
# We do this at the end to avoid uv thinking the project is a dependency before its config is written
uv sync

#==============================================================================
# Pre-commit config
#==============================================================================
if [[ "$INCLUDE_SECURITY" == "true" ]]; then
    cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: uv run mypy
        language: system
        types: [python]
  - repo: https://github.com/PyCQA/bandit
    rev: 1.8.0
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
        additional_dependencies: ["bandit[toml]"]
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ["--baseline", ".secrets.baseline"]
EOF
else
    cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: uv run mypy
        language: system
        types: [python]
EOF
fi

#==============================================================================
# GitHub Actions
#==============================================================================
mkdir -p .github/workflows
cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - name: Setup uv
        uses: astral-sh/setup-uv@v7
        with:
          python-version: ${{ matrix.python-version }}
          enable-cache: true
      - name: Install dependencies
        run: uv sync --frozen
      - name: Lint
        run: uv run ruff check .
      - name: Type check
        run: uv run mypy src
      - name: Test
        run: uv run pytest

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v7
        with:
          enable-cache: true
      - run: uv sync --frozen
      - run: uv run ruff check --output-format=github .
      - run: uv run ruff format --check .
EOF

#==============================================================================
# Dependabot (conditional)
#==============================================================================
if [[ "$INCLUDE_DEPENDABOT" == "true" ]]; then
    cat > .github/dependabot.yml << 'EOF'
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      dev-dependencies:
        patterns:
          - "ruff"
          - "pytest*"
          - "mypy"
          - "pre-commit"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
EOF
fi

#==============================================================================
# Project structure
#==============================================================================
mkdir -p "src/${PROJECT_NAME}" tests
touch "src/${PROJECT_NAME}/__init__.py"
touch "src/${PROJECT_NAME}/py.typed"
touch tests/__init__.py

# Starter files by project type
case "$PROJECT_TYPE" in
    api)
        cat > "src/${PROJECT_NAME}/main.py" << 'EOF'
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
EOF
        cat > "tests/test_api.py" << EOF
from typing import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from ${PROJECT_NAME}.main import app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
EOF
        ;;
    cli)
        cat > "src/${PROJECT_NAME}/main.py" << EOF
import typer

app = typer.Typer()


@app.command()
def main(name: str = "world") -> None:
    """Greet someone."""
    typer.echo(f"Hello, {name}!")


if __name__ == "__main__":
    app()
EOF
        cat > "tests/test_cli.py" << EOF
from typer.testing import CliRunner

from ${PROJECT_NAME}.main import app

runner = CliRunner()


def test_main() -> None:
    result = runner.invoke(app, ["--name", "test"])
    assert result.exit_code == 0
    assert "Hello, test!" in result.stdout
EOF
        ;;
    tui)
        cat > "src/${PROJECT_NAME}/app.py" << EOF
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static


class ${PROJECT_NAME^}App(App):
    """A Textual app."""

    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Hello, World!")
        yield Footer()


def main() -> None:
    app = ${PROJECT_NAME^}App()
    app.run()


if __name__ == "__main__":
    main()
EOF
        cat > "tests/test_app.py" << EOF
import pytest

from ${PROJECT_NAME}.app import ${PROJECT_NAME^}App


@pytest.mark.asyncio
async def test_app_runs() -> None:
    app = ${PROJECT_NAME^}App()
    async with app.run_test():
        assert app.is_running
EOF
        mkdir -p "src/${PROJECT_NAME}/css"
        cat > "src/${PROJECT_NAME}/css/${PROJECT_NAME}.tcss" << 'EOF'
Screen {
    align: center middle;
}

Static {
    width: auto;
    padding: 1 2;
    background: $surface;
    border: round $primary;
}
EOF
        ;;
    data)
        cat > "src/${PROJECT_NAME}/pipeline.py" << 'EOF'
import polars as pl


def transform(df: pl.DataFrame) -> pl.DataFrame:
    """Example transformation."""
    return df
EOF
        cat > "tests/test_pipeline.py" << EOF
import polars as pl

from ${PROJECT_NAME}.pipeline import transform


def test_transform() -> None:
    df = pl.DataFrame({"a": [1, 2, 3]})
    result = transform(df)
    assert result.shape == (3, 1)
EOF
        ;;
    library)
        cat > "tests/test_placeholder.py" << 'EOF'
def test_placeholder() -> None:
    assert True
EOF
        ;;
esac

#==============================================================================
# direnv configuration
#==============================================================================
cat > .envrc << 'EOF'
source .venv/bin/activate
EOF

#==============================================================================
# EditorConfig
#==============================================================================
cat > .editorconfig << 'EOF'
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.{yml,yaml,json,toml}]
indent_size = 2

[*.tcss]
indent_size = 2

[Makefile]
indent_style = tab
EOF

#==============================================================================
# VS Code (conditional)
#==============================================================================
if [[ "$INCLUDE_VSCODE" == "true" ]]; then
    mkdir -p .vscode
    cat > .vscode/settings.json << 'EOF'
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "python.analysis.typeCheckingMode": "strict"
}
EOF
    cat > .vscode/extensions.json << 'EOF'
{
  "recommendations": [
    "charliermarsh.ruff",
    "ms-python.python",
    "ms-python.mypy-type-checker",
    "tamasfe.even-better-toml"
  ]
}
EOF
fi

#==============================================================================
# Makefile (conditional)
#==============================================================================
if [[ "$INCLUDE_MAKEFILE" == "true" ]]; then
    cat > Makefile << 'EOF'
.PHONY: install test lint format typecheck ci clean

install:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .
	uv run ruff check --fix .

typecheck:
	uv run mypy src

ci: lint typecheck test

clean:
	rm -rf .venv .mypy_cache .pytest_cache .ruff_cache .coverage htmlcov dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
EOF

    # Add project-type-specific targets
    case "$PROJECT_TYPE" in
        api)
            cat >> Makefile << 'EOF'

run:
	uv run uvicorn src.$(shell basename $(CURDIR)).main:app --reload
EOF
            ;;
        cli)
            cat >> Makefile << 'EOF'

run:
	uv run python -m $(shell basename $(CURDIR)).main
EOF
            ;;
        tui)
            cat >> Makefile << 'EOF'

run:
	uv run python -m $(shell basename $(CURDIR)).app

dev:
	uv run textual run --dev src/$(shell basename $(CURDIR))/app.py
EOF
            ;;
    esac
fi

#==============================================================================
# Docker (conditional)
#==============================================================================
if [[ "$INCLUDE_DOCKER" == "true" ]]; then
    cat > Dockerfile << EOF
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY src ./src
RUN uv sync --frozen --no-dev

FROM python:${PYTHON_VERSION}-slim-bookworm
WORKDIR /app
COPY --from=builder /app/.venv .venv
COPY src ./src
ENV PATH="/app/.venv/bin:\$PATH"
EOF

    # Entrypoint by project type
    case "$PROJECT_TYPE" in
        api)
            echo 'CMD ["uvicorn", "'${PROJECT_NAME}'.main:app", "--host", "0.0.0.0", "--port", "8000"]' >> Dockerfile
            ;;
        cli)
            echo 'ENTRYPOINT ["python", "-m", "'${PROJECT_NAME}'.main"]' >> Dockerfile
            ;;
        tui)
            echo '# TUI apps typically not containerized' >> Dockerfile
            echo 'CMD ["python", "-m", "'${PROJECT_NAME}'.app"]' >> Dockerfile
            ;;
        *)
            echo 'CMD ["python", "-m", "'${PROJECT_NAME}'"]' >> Dockerfile
            ;;
    esac

    cat > .dockerignore << 'EOF'
.venv/
.git/
.github/
.vscode/
.mypy_cache/
.pytest_cache/
.ruff_cache/
__pycache__/
*.pyc
.coverage
htmlcov/
.env
.secrets.baseline
EOF
fi

#==============================================================================
# CHANGELOG (conditional)
#==============================================================================
if [[ "$INCLUDE_CHANGELOG" == "true" ]]; then
    cat > CHANGELOG.md << 'EOF'
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
EOF
fi

#==============================================================================
# Security baseline (conditional)
#==============================================================================
if [[ "$INCLUDE_SECURITY" == "true" ]]; then
    uv run detect-secrets scan > .secrets.baseline 2>/dev/null || echo "{}" > .secrets.baseline
fi

#==============================================================================
# README with tree
#==============================================================================
generate_tree() {
    echo "├── .github/"
    echo "│   └── workflows/"
    echo "│       └── ci.yml"
    [[ "$INCLUDE_DEPENDABOT" == "true" ]] && echo "│   └── dependabot.yml"
    echo "├── .pre-commit-config.yaml"
    echo "├── .python-version"
    echo "├── .gitignore"
    echo "├── .envrc"
    echo "├── .env.example"
    echo "├── .editorconfig"
    [[ "$INCLUDE_VSCODE" == "true" ]] && echo "├── .vscode/"
    [[ "$INCLUDE_DOCKER" == "true" ]] && echo "├── Dockerfile"
    [[ "$INCLUDE_MAKEFILE" == "true" ]] && echo "├── Makefile"
    [[ "$INCLUDE_CHANGELOG" == "true" ]] && echo "├── CHANGELOG.md"
    echo "├── pyproject.toml"
    echo "├── uv.lock"
    echo "├── src/"
    echo "│   └── ${PROJECT_NAME}/"
    echo "│       ├── __init__.py"
    echo "│       └── py.typed"
    case "$PROJECT_TYPE" in
        api|cli) echo "│       └── main.py" ;;
        tui)
            echo "│       ├── app.py"
            echo "│       └── css/"
            ;;
        data) echo "│       └── pipeline.py" ;;
    esac
    echo "└── tests/"
    echo "    └── __init__.py"
}

cat > README.md << EOF
# ${PROJECT_NAME}

## Project Structure

\`\`\`
$(generate_tree)
\`\`\`

## Setup

\`\`\`bash
uv sync
\`\`\`

**Note:** This project uses [direnv](https://direnv.net/) for automatic virtual environment activation.
When you \`cd\` into the project directory, direnv will automatically activate the \`.venv\`.
On first use, you'll need to run \`direnv allow\` to approve the \`.envrc\` file.

Alternatively, you can manually activate the virtual environment:
\`\`\`bash
source .venv/bin/activate
\`\`\`

## Development

\`\`\`bash
EOF

if [[ "$INCLUDE_MAKEFILE" == "true" ]]; then
    cat >> README.md << 'EOF'
# Run tests
make test

# Lint and format
make format
make lint

# Type check
make typecheck

# Run all CI checks
make ci
EOF
else
    cat >> README.md << 'EOF'
# Run tests
uv run pytest

# Lint
uv run ruff check .
uv run ruff format .

# Type check
uv run mypy src
EOF
fi

case "$PROJECT_TYPE" in
    api)
        cat >> README.md << 'EOF'

# Run development server
make run
# or: uv run uvicorn src.${PROJECT_NAME}.main:app --reload
EOF
        ;;
    cli)
        cat >> README.md << 'EOF'

# Run CLI
make run
# or: uv run python -m ${PROJECT_NAME}.main --help
EOF
        ;;
    tui)
        cat >> README.md << 'EOF'

# Run TUI app
make run

# Run with hot reload (textual dev mode)
make dev
EOF
        ;;
esac

cat >> README.md << 'EOF'
```
EOF

#==============================================================================
# Git init + pre-commit install
#==============================================================================
git init --quiet
uv run pre-commit install

#==============================================================================
# Summary
#==============================================================================
echo ""
echo "✓ ${PROJECT_NAME} initialized"
echo "  Python:  ${PYTHON_VERSION}"
echo "  Type:    ${PROJECT_TYPE}"
echo "  Features:"
[[ "$INCLUDE_VSCODE" == "true" ]]     && echo "    - VS Code config"
[[ "$INCLUDE_DOCKER" == "true" ]]     && echo "    - Dockerfile"
[[ "$INCLUDE_MAKEFILE" == "true" ]]   && echo "    - Makefile"
[[ "$INCLUDE_CHANGELOG" == "true" ]]  && echo "    - CHANGELOG.md"
[[ "$INCLUDE_SECURITY" == "true" ]]   && echo "    - Security scanning (bandit, detect-secrets)"
[[ "$INCLUDE_DEPENDABOT" == "true" ]] && echo "    - Dependabot"
echo ""
echo "Next steps:"
echo "  cd ${PROJECT_NAME}"
echo "  source .venv/bin/activate"
[[ "$INCLUDE_MAKEFILE" == "true" ]] && echo "  make test"

# Usage examples:
#
# Default library project
# mkdir mylib && cd mylib
# ~/scripts/init-python-repo.sh
#
# TUI project with Python 3.13
# mkdir mytui && cd mytui
# PROJECT_TYPE=tui PYTHON_VERSION=3.13 ~/scripts/init-python-repo.sh
#
# API without Docker
# mkdir myapi && cd myapi
# PROJECT_TYPE=api INCLUDE_DOCKER=false ~/scripts/init-python-repo.sh
#
# Minimal library (no optional features)
# mkdir minimal && cd minimal
# INCLUDE_VSCODE=false INCLUDE_DOCKER=false INCLUDE_SECURITY=false ~/scripts/init-python-repo.sh
