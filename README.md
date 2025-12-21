# How to init-python-repo.sh

## Default library project (Python 3.12, all features)

mkdir mylib && cd mylib
~/scripts/init-python-repo.sh

## FastAPI project

mkdir myapi && cd myapi
PROJECT_TYPE=api ~/scripts/init-python-repo.sh

## TUI project with Python 3.13

mkdir mytui && cd mytui
PROJECT_TYPE=tui PYTHON_VERSION=3.13 ~/scripts/init-python-repo.sh

## CLI project without Docker

mkdir mycli && cd mycli
PROJECT_TYPE=cli INCLUDE_DOCKER=false ~/scripts/init-python-repo.sh

## Data pipeline project

mkdir pipeline && cd pipeline
PROJECT_TYPE=data ~/scripts/init-python-repo.sh

## Minimal setup (no optional features)

mkdir minimal && cd minimal
INCLUDE_VSCODE=false \
INCLUDE_DOCKER=false \
INCLUDE_MAKEFILE=false \
INCLUDE_CHANGELOG=false \
INCLUDE_SECURITY=false \
INCLUDE_DEPENDABOT=false \
~/scripts/init-python-repo.sh
