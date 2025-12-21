# init-python-repo

A composable, best-practice Python repository bootstrapper that creates production-ready project structures with modern tooling.

## Features

- **Modern Tooling**: UV for dependency management, Ruff for linting/formatting, MyPy for type checking
- **Project Types**: Library, API (FastAPI), CLI (Typer), Data (Polars), TUI (Textual)
- **Security**: Bandit and detect-secrets for security scanning
- **CI/CD**: GitHub Actions workflow with multi-Python version testing
- **Docker**: Multi-stage Dockerfile optimized for production
- **Docker Compose**: Ready-to-use compose files for API and Data projects (NEW)
- **License Generation**: MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, or Unlicense (NEW)
- **VS Code Integration**: Settings, extensions, and recommended configurations

## Installation

```bash
# Install with uv
uv tool install git+https://github.com/yourusername/init-python-repo

# Or clone and install locally
git clone https://github.com/yourusername/init-python-repo
cd init-python-repo
uv sync
uv tool install .
```

## Quick Start

```bash
# Create a new library project
init-python-repo -n mylib

# Create a FastAPI project
init-python-repo -n myapi -t api

# Create a CLI project with Apache license
init-python-repo -n mycli -t cli --license Apache-2.0
```

## Usage

```bash
init-python-repo [OPTIONS]
```

### Required Options

| Flag | Short | Description |
|------|-------|-------------|
| `--reponame` | `-n` | Repository name |

### Project Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--repoloc` | `-l` | `~/Repos` | Parent directory for new repo |
| `--python` | `-p` | `3.12` | Python version |
| `--type` | `-t` | `library` | Project type: `library`, `api`, `cli`, `data`, `tui` |
| `--license` | | `MIT` | License: `MIT`, `Apache-2.0`, `GPL-3.0`, `BSD-3-Clause`, `Unlicense`, `None` |
| `--author` | `-a` | (auto) | Author name for license (defaults to git config) |

### Feature Toggles

| Flag | Default | Description |
|------|---------|-------------|
| `--no-vscode` | enabled | Skip VS Code configuration |
| `--no-docker` | enabled | Skip Dockerfile |
| `--no-docker-compose` | enabled | Skip docker-compose.yml (api/data only) |
| `--no-makefile` | enabled | Skip Makefile |
| `--no-changelog` | enabled | Skip CHANGELOG.md |
| `--no-security` | enabled | Skip bandit/detect-secrets |
| `--no-dependabot` | enabled | Skip Dependabot configuration |

### GitHub Options

| Flag | Default | Description |
|------|---------|-------------|
| `--no-github` | enabled | Skip GitHub repo creation |
| `--private/--public` | private | Repository visibility |
| `--no-vscode-open` | opens | Don't open VS Code after creation |

## Examples

### Default Library Project

```bash
init-python-repo -n mylib
```

Creates a minimal Python library with:

- src/mylib/ package structure
- pytest test suite
- Type hints and py.typed marker
- Pre-commit hooks (ruff, mypy)

### FastAPI Project

```bash
init-python-repo -n myapi -t api
```

Includes everything above plus:

- FastAPI with uvicorn
- Health check endpoint
- Async test client (httpx)
- docker-compose.yml with PostgreSQL
- `make run` for development server

### CLI Application

```bash
init-python-repo -n mycli -t cli --license Apache-2.0
```

Includes:

- Typer CLI framework
- Rich for terminal output
- Command structure with tests
- Apache 2.0 license

### Data Pipeline

```bash
init-python-repo -n pipeline -t data
```

Includes:

- Polars for data processing
- DuckDB for analytics
- SQLAlchemy for database access
- docker-compose.yml with PostgreSQL
- Faker for test data generation

### TUI Application

```bash
init-python-repo -n mytui -t tui -p 3.13
```

Includes:

- Textual framework
- CSS styling support
- Hot reload development mode
- Python 3.13

### Minimal Project

```bash
init-python-repo -n minimal --no-docker --no-security --no-changelog --license None
```

### Public Open Source Project

```bash
init-python-repo -n oss-project --public --license MIT
```

### Local Development Only

```bash
init-python-repo -n scratch --no-github --no-vscode-open
```

## Generated Project Structure

```text
myproject/
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   └── dependabot.yml
├── .vscode/
│   ├── settings.json
│   └── extensions.json
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── py.typed
│       └── main.py          # (api/cli only)
├── tests/
│   ├── __init__.py
│   └── test_*.py
├── .editorconfig
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── .secrets.baseline        # (if security enabled)
├── CHANGELOG.md
├── docker-compose.yml       # (api/data only)
├── Dockerfile
├── LICENSE
├── Makefile
├── pyproject.toml
├── README.md
└── uv.lock
```

## Generated Files Explained

### pyproject.toml

- Hatchling build system
- Ruff configuration (line-length: 120, modern rules)
- MyPy strict mode
- pytest with coverage
- No self-referential dependencies (clean structure)

### CI Workflow

Single optimized job that runs:

1. Lint (ruff check + format check)
2. Type check (mypy)
3. Tests (pytest)

Matrix testing across Python 3.12 and 3.13.

### docker-compose.yml (API/Data projects)

- PostgreSQL 16 with health checks
- Automatic database creation
- Volume persistence
- Development-friendly defaults

### Pre-commit Hooks

- ruff (lint + format)
- mypy (type checking)
- bandit (security, if enabled)
- detect-secrets (if enabled)

## Migration from v0.1 (Shell Script)

If you were using the shell script version:

```bash
# Old way (shell script)
PROJECT_TYPE=api ./init-python-repo.sh

# New way (Python CLI)
init-python-repo -n myapi -t api
```

### Key Changes in v0.2

1. **Pure Python**: No more shell script dependencies
2. **License generation**: `--license MIT` (was missing)
3. **docker-compose**: Auto-generated for api/data projects
4. **Cleaner pyproject.toml**: No self-referential dev dependencies
5. **Optimized CI**: Single job instead of redundant test+lint jobs

## Development

```bash
# Clone the repo
git clone https://github.com/yourusername/init-python-repo
cd init-python-repo

# Install dependencies
uv sync

# Run tests
uv run pytest

# Run linting
uv run ruff check .
uv run mypy init_python_repo

# Install locally for testing
uv tool install --editable .
```

## Requirements

- Python 3.12+
- uv (for dependency management)
- git
- gh CLI (optional, for GitHub integration)

## License

MIT License - see [LICENSE](LICENSE) for details.
