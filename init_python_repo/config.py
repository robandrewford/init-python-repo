"""Configuration models and defaults for init-python-repo."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class ProjectType(str, Enum):
    """Supported project types."""

    LIBRARY = "library"
    API = "api"
    CLI = "cli"
    DATA = "data"
    TUI = "tui"


class License(str, Enum):
    """Supported license types."""

    MIT = "MIT"
    APACHE2 = "Apache-2.0"
    GPL3 = "GPL-3.0"
    BSD3 = "BSD-3-Clause"
    UNLICENSE = "Unlicense"
    NONE = "None"


@dataclass
class FeatureFlags:
    """Feature toggles for generated project."""

    vscode: bool = True
    docker: bool = True
    makefile: bool = True
    changelog: bool = True
    security: bool = True
    dependabot: bool = True
    docker_compose: bool = True  # NEW: docker-compose for api/data


@dataclass
class ProjectConfig:
    """Complete project configuration."""

    name: str
    location: Path = field(default_factory=lambda: Path.home() / "Repos")
    python_version: str = "3.12"
    project_type: ProjectType = ProjectType.LIBRARY
    license_type: License = License.MIT
    features: FeatureFlags = field(default_factory=FeatureFlags)
    private_repo: bool = True
    skip_github: bool = False
    skip_vscode_open: bool = False

    @property
    def path(self) -> Path:
        """Full path to the project directory."""
        return self.location / self.name

    @property
    def package_name(self) -> str:
        """Python-safe package name (underscores instead of dashes)."""
        return self.name.replace("-", "_").replace(".", "_")

    @property
    def python_target(self) -> str:
        """Python target version for ruff (e.g., 'py312')."""
        return f"py{self.python_version.replace('.', '')}"


# Dependency mappings by project type
RUNTIME_DEPS: dict[ProjectType, list[str]] = {
    ProjectType.LIBRARY: [],
    ProjectType.API: [
        "fastapi",
        "uvicorn",
        "httpx",
        "pydantic",
        "pydantic-settings",
        "python-dotenv",
        "structlog",
    ],
    ProjectType.CLI: ["typer", "rich", "python-dotenv"],
    ProjectType.DATA: [
        "polars",
        "pyarrow",
        "duckdb",
        "sqlalchemy",
        "httpx",
        "pydantic",
        "python-dotenv",
        "structlog",
    ],
    ProjectType.TUI: ["textual", "rich", "python-dotenv"],
}

DEV_DEPS: dict[ProjectType, list[str]] = {
    ProjectType.LIBRARY: [],
    ProjectType.API: ["httpx"],  # async test client
    ProjectType.CLI: [],
    ProjectType.DATA: ["faker"],  # test data generation
    ProjectType.TUI: ["textual-dev"],
}

# Core dev dependencies (all project types)
CORE_DEV_DEPS: list[str] = [
    "ruff",
    "pytest",
    "pytest-cov",
    "mypy",
    "pre-commit",
    "pytest-asyncio",
]

SECURITY_DEV_DEPS: list[str] = ["bandit", "detect-secrets"]
