"""File templates for generated projects."""

from __future__ import annotations

from datetime import UTC, datetime

from .config import (
    CORE_DEV_DEPS,
    DEV_DEPS,
    RUNTIME_DEPS,
    SECURITY_DEV_DEPS,
    License,
    ProjectConfig,
    ProjectType,
)

# =============================================================================
# License Templates
# =============================================================================

LICENSE_TEMPLATES: dict[License, str] = {
    License.MIT: '''MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''',
    License.APACHE2: '''                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License.

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof.

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      patent license to make, have made, use, offer to sell, sell, import,
      and otherwise transfer the Work.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      shall any Contributor be liable to You for damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations consistent with this License.

   END OF TERMS AND CONDITIONS

   Copyright {year} {author}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
''',
    License.GPL3: '''                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  For the full license text, see: https://www.gnu.org/licenses/gpl-3.0.txt

Copyright {year} {author}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
''',
    License.BSD3: '''BSD 3-Clause License

Copyright (c) {year}, {author}
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
''',
    License.UNLICENSE: '''This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
''',
    License.NONE: "",
}


def get_license_content(license_type: License, author: str) -> str:
    """Generate license content with author and year substitution."""
    if license_type == License.NONE:
        return ""
    template = LICENSE_TEMPLATES.get(license_type, "")
    year = datetime.now(tz=UTC).year
    return template.format(year=year, author=author)


# =============================================================================
# pyproject.toml Template
# =============================================================================


def get_pyproject_toml(config: ProjectConfig) -> str:
    """Generate pyproject.toml content."""
    # Collect runtime dependencies based on project type
    runtime_deps = RUNTIME_DEPS.get(config.project_type, [])

    # Format dependencies list
    if runtime_deps:
        deps_str = ",\n    ".join(f'"{dep}"' for dep in runtime_deps)
        deps_line = f'[\n    {deps_str},\n]'
    else:
        deps_line = "[]"

    # Base section
    content = f'''[project]
name = "{config.package_name}"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">={config.python_version}"
dependencies = {deps_line}
'''

    # Add license if specified
    if config.license_type != License.NONE:
        content += f'license = "{config.license_type.value}"\n'

    # Build system
    content += f'''
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{config.package_name}"]
'''

    # Entry point for CLI/API types
    if config.project_type in (ProjectType.CLI, ProjectType.API):
        content += f'''
[project.scripts]
{config.package_name} = "{config.package_name}.main:app"
'''

    # Dependency groups for dev dependencies
    dev_deps = list(CORE_DEV_DEPS)

    # Add project-type-specific dev deps
    type_dev_deps = DEV_DEPS.get(config.project_type, [])
    dev_deps.extend(type_dev_deps)

    # Add security deps if enabled
    if config.features.security:
        dev_deps.extend(SECURITY_DEV_DEPS)

    # Format dev dependencies
    dev_deps_str = ",\n    ".join(f'"{dep}"' for dep in dev_deps)
    content += f'''
[dependency-groups]
dev = [
    {dev_deps_str},
]
'''

    # Tool configurations
    content += f'''
[tool.ruff]
line-length = 120
target-version = "{config.python_target}"
src = ["src"]

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "RUF"]

[tool.mypy]
strict = true
python_version = "{config.python_version}"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=term-missing"
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
'''

    # Bandit config if security enabled
    if config.features.security:
        content += '''
[tool.bandit]
exclude_dirs = ["tests"]
'''

    return content


# =============================================================================
# .gitignore Template
# =============================================================================

GITIGNORE = '''__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
.mypy_cache/
.pytest_cache/
.ruff_cache/
*.egg-info/
dist/
build/
.coverage
htmlcov/
.env
.secrets.baseline
.DS_Store
'''


# =============================================================================
# .env.example Templates
# =============================================================================


def get_env_example(project_type: ProjectType) -> str:
    """Generate .env.example content based on project type."""
    base = "# Copy to .env and fill in values\nLOG_LEVEL=INFO\n"

    if project_type == ProjectType.API:
        base += """HOST=0.0.0.0
PORT=8000
DATABASE_URL=
"""
    elif project_type == ProjectType.DATA:
        base += """DATABASE_URL=
AWS_PROFILE=
"""
    return base


# =============================================================================
# Pre-commit Config Template
# =============================================================================


def get_precommit_config(include_security: bool) -> str:
    """Generate .pre-commit-config.yaml content."""
    base = '''repos:
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
'''

    if include_security:
        base += '''  - repo: https://github.com/PyCQA/bandit
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
'''
    return base


# =============================================================================
# GitHub Actions CI Template (OPTIMIZED - FIX #5)
# =============================================================================


def get_ci_workflow(python_version: str) -> str:
    """Generate optimized CI workflow (removed redundant lint job)."""
    # Determine Python versions to test
    major, minor = python_version.split(".")
    versions = [python_version]
    if int(minor) < 13:
        versions.append(f"{major}.13")

    versions_str = ", ".join(f'"{v}"' for v in versions)

    return f'''name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: [{versions_str}]
    steps:
      - uses: actions/checkout@v4

      - name: Setup uv
        uses: astral-sh/setup-uv@v4
        with:
          version: "latest"

      - name: Set up Python ${{{{ matrix.python-version }}}}
        run: uv python install ${{{{ matrix.python-version }}}}

      - name: Install dependencies
        run: uv sync --frozen

      - name: Lint
        run: |
          uv run ruff check --output-format=github .
          uv run ruff format --check .

      - name: Type check
        run: uv run mypy src

      - name: Test
        run: uv run pytest
'''


# =============================================================================
# Dependabot Config Template
# =============================================================================

DEPENDABOT_CONFIG = '''version: 2
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
'''


# =============================================================================
# EditorConfig Template
# =============================================================================

EDITORCONFIG = '''root = true

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
'''


# =============================================================================
# VS Code Settings Templates
# =============================================================================

VSCODE_SETTINGS = '''{
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
'''

VSCODE_EXTENSIONS = '''{
  "recommendations": [
    "charliermarsh.ruff",
    "ms-python.python",
    "ms-python.mypy-type-checker",
    "tamasfe.even-better-toml"
  ]
}
'''


# =============================================================================
# Makefile Template
# =============================================================================


def get_makefile(project_type: ProjectType, package_name: str) -> str:
    """Generate Makefile content."""
    base = '''.PHONY: install test lint format typecheck ci clean

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
'''

    if project_type == ProjectType.API:
        base += f'''
run:
	uv run uvicorn {package_name}.main:app --reload

docker-build:
	docker build -t {package_name} .

docker-run:
	docker run -p 8000:8000 {package_name}
'''
    elif project_type == ProjectType.CLI:
        base += f'''
run:
	uv run python -m {package_name}.main
'''
    elif project_type == ProjectType.TUI:
        base += f'''
run:
	uv run python -m {package_name}.app

dev:
	uv run textual run --dev src/{package_name}/app.py
'''

    return base


# =============================================================================
# Dockerfile Template
# =============================================================================


def get_dockerfile(config: ProjectConfig) -> str:
    """Generate Dockerfile content."""
    base = f'''FROM ghcr.io/astral-sh/uv:python{config.python_version}-bookworm-slim AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY src ./src
RUN uv sync --frozen --no-dev

FROM python:{config.python_version}-slim-bookworm
WORKDIR /app
COPY --from=builder /app/.venv .venv
COPY src ./src
ENV PATH="/app/.venv/bin:$PATH"
'''

    if config.project_type == ProjectType.API:
        base += f'CMD ["uvicorn", "{config.package_name}.main:app", "--host", "0.0.0.0", "--port", "8000"]\n'
    elif config.project_type == ProjectType.CLI:
        base += f'ENTRYPOINT ["python", "-m", "{config.package_name}.main"]\n'
    elif config.project_type == ProjectType.TUI:
        base += f'# TUI apps typically not containerized\nCMD ["python", "-m", "{config.package_name}.app"]\n'
    else:
        base += f'CMD ["python", "-m", "{config.package_name}"]\n'

    return base


DOCKERIGNORE = '''.venv/
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
'''


# =============================================================================
# Docker Compose Template (NEW - Feature #4)
# =============================================================================


def get_docker_compose(config: ProjectConfig) -> str:
    """Generate docker-compose.yml for api and data projects."""
    if config.project_type == ProjectType.API:
        return f'''services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=INFO
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/{config.package_name}
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./src:/app/src:ro
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: {config.package_name}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
'''
    elif config.project_type == ProjectType.DATA:
        return f'''services:
  app:
    build: .
    environment:
      - LOG_LEVEL=INFO
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/{config.package_name}
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./src:/app/src:ro
      - ./data:/app/data

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: {config.package_name}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
'''
    return ""


# =============================================================================
# CHANGELOG Template
# =============================================================================

CHANGELOG = '''# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial project structure
'''


# =============================================================================
# Source Code Templates by Project Type
# =============================================================================


def get_main_py(project_type: ProjectType, package_name: str) -> str | None:
    """Get main.py content for project type."""
    if project_type == ProjectType.API:
        return '''from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
'''
    elif project_type == ProjectType.CLI:
        return '''import typer

app = typer.Typer()


@app.command()
def main(name: str = "world") -> None:
    """Greet someone."""
    typer.echo(f"Hello, {name}!")


if __name__ == "__main__":
    app()
'''
    return None


def get_app_py(package_name: str) -> str:
    """Get app.py content for TUI projects."""
    class_name = "".join(word.capitalize() for word in package_name.split("_")) + "App"
    return f'''from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static


class {class_name}(App):
    """A Textual app."""

    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Hello, World!")
        yield Footer()


def main() -> None:
    app = {class_name}()
    app.run()


if __name__ == "__main__":
    main()
'''


def get_pipeline_py() -> str:
    """Get pipeline.py content for data projects."""
    return '''import polars as pl


def transform(df: pl.DataFrame) -> pl.DataFrame:
    """Example transformation."""
    return df
'''


def get_tcss(package_name: str) -> str:
    """Get TCSS content for TUI projects."""
    return '''Screen {
    align: center middle;
}

Static {
    width: auto;
    padding: 1 2;
    background: $surface;
    border: round $primary;
}
'''


# =============================================================================
# Test Templates by Project Type
# =============================================================================


def get_test_file(project_type: ProjectType, package_name: str) -> tuple[str, str]:
    """Get test file name and content for project type."""
    if project_type == ProjectType.API:
        return "test_api.py", f'''from typing import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from {package_name}.main import app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {{"status": "ok"}}
'''
    elif project_type == ProjectType.CLI:
        return "test_cli.py", f'''from typer.testing import CliRunner

from {package_name}.main import app

runner = CliRunner()


def test_main() -> None:
    result = runner.invoke(app, ["--name", "test"])
    assert result.exit_code == 0
    assert "Hello, test!" in result.stdout
'''
    elif project_type == ProjectType.TUI:
        class_name = "".join(word.capitalize() for word in package_name.split("_")) + "App"
        return "test_app.py", f'''import pytest

from {package_name}.app import {class_name}


@pytest.mark.asyncio
async def test_app_runs() -> None:
    app = {class_name}()
    async with app.run_test():
        assert app.is_running
'''
    elif project_type == ProjectType.DATA:
        return "test_pipeline.py", f'''import polars as pl

from {package_name}.pipeline import transform


def test_transform() -> None:
    df = pl.DataFrame({{"a": [1, 2, 3]}})
    result = transform(df)
    assert result.shape == (3, 1)
'''
    else:  # library
        return "test_placeholder.py", '''def test_placeholder() -> None:
    assert True
'''


# =============================================================================
# README Template
# =============================================================================


def get_readme(config: ProjectConfig) -> str:
    """Generate README.md content."""
    tree_lines = [
        "├── .github/",
        "│   ├── workflows/",
        "│   │   └── ci.yml",
    ]
    if config.features.dependabot:
        tree_lines.append("│   └── dependabot.yml")
    tree_lines.extend([
        "├── .pre-commit-config.yaml",
        "├── .python-version",
        "├── .gitignore",
        "├── .env.example",
        "├── .editorconfig",
    ])
    if config.features.vscode:
        tree_lines.append("├── .vscode/")
    if config.features.docker:
        tree_lines.append("├── Dockerfile")
    if config.features.docker_compose and config.project_type in (ProjectType.API, ProjectType.DATA):
        tree_lines.append("├── docker-compose.yml")
    if config.features.makefile:
        tree_lines.append("├── Makefile")
    if config.features.changelog:
        tree_lines.append("├── CHANGELOG.md")
    if config.license_type != License.NONE:
        tree_lines.append("├── LICENSE")
    tree_lines.extend([
        "├── pyproject.toml",
        "├── uv.lock",
        "├── src/",
        f"│   └── {config.package_name}/",
        "│       ├── __init__.py",
        "│       └── py.typed",
    ])

    if config.project_type in (ProjectType.API, ProjectType.CLI):
        tree_lines.append("│       └── main.py")
    elif config.project_type == ProjectType.TUI:
        tree_lines.extend(["│       ├── app.py", "│       └── css/"])
    elif config.project_type == ProjectType.DATA:
        tree_lines.append("│       └── pipeline.py")

    tree_lines.extend([
        "└── tests/",
        "    └── __init__.py",
    ])

    tree = "\n".join(tree_lines)

    content = f'''# {config.package_name}

## Project Structure

```text
{tree}
```

## Setup

```bash
uv sync
source .venv/bin/activate
```

## Development

```bash
'''

    if config.features.makefile:
        content += '''# Run tests
make test

# Lint and format
make format
make lint

# Type check
make typecheck

# Run all CI checks
make ci
'''
    else:
        content += '''# Run tests
uv run pytest

# Lint
uv run ruff check .
uv run ruff format .

# Type check
uv run mypy src
'''

    if config.project_type == ProjectType.API:
        content += f'''
# Run development server
make run
# or: uv run uvicorn {config.package_name}.main:app --reload

# Docker
make docker-build
make docker-run
# or: docker compose up
'''
    elif config.project_type == ProjectType.CLI:
        content += f'''
# Run CLI
make run
# or: uv run python -m {config.package_name}.main --help
'''
    elif config.project_type == ProjectType.TUI:
        content += '''
# Run TUI app
make run

# Run with hot reload (textual dev mode)
make dev
'''

    content += "```\n"

    return content
