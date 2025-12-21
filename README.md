# How to create_repo.py

## Make executable
```sh
chmod +x create_repo.py
```

## Run directly (uv handles deps automatically)
```sh
./create_repo.py --reponame myapi --type api
```

## Or generate lockfile for full reproducibility
```sh
uv lock --script create_repo.py
```

## Install to ~/.local/bin via uv
```sh
uv tool install --from . create-repo
```

## Then use anywhere
```sh
create-repo --reponame myapi --type api
```

## Usage
```sh
./create_repo.py --reponame NAME [OPTIONS]
```

### Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--reponame` | `-n` | (required) | Repository name |
| `--repoloc` | `-l` | `~/Repos` | Parent directory |
| `--python` | `-p` | `3.12` | Python version |
| `--type` | `-t` | `library` | Project type: `library`, `api`, `cli`, `data`, `tui` |
| `--no-vscode` | | `false` | Skip opening VS Code |
| `--no-github` | | `false` | Skip GitHub repo creation |
| `--private` | | `true` | Make GitHub repo private |

## Examples

### Default library project (Python 3.12, all features)

```sh
./create_repo.py -n mylib
```

### FastAPI project

```sh
./create_repo.py -n myapi -t api
```

### TUI project with Python 3.13
```sh
./create_repo.py -n mytui -t tui -p 3.13
```

### CLI project without Docker
```sh
INCLUDE_DOCKER=false ./create_repo.py -n mycli -t cli
```

### Data pipeline project
```sh
./create_repo.py -n pipeline -t data
```

### Custom location
```sh
./create_repo.py -n myproject -l ~/Projects
```

### Local development only (no GitHub)
```sh
./create_repo.py -n scratch -t library --no-github --no-vscode
```

### Public GitHub repository
```sh
./create_repo.py -n oss-tool -t cli --no-private
```

## Feature Flags (Environment Variables)

These control what the underlying `init-python-repo.sh` generates:
```sh
INCLUDE_VSCODE=false \
INCLUDE_DOCKER=false \
INCLUDE_MAKEFILE=false \
INCLUDE_CHANGELOG=false \
INCLUDE_SECURITY=false \
INCLUDE_DEPENDABOT=false \
./create_repo.py -n minimal
```

## Reproducibility

Generate a lockfile for exact dependency versions:
```sh
uv lock --script create_repo.py
```

Subsequent runs use `create_repo.py.lock` automatically.
