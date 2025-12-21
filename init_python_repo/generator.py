"""Project generator - creates and initializes Python repositories."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from .config import (
    License,
    ProjectConfig,
    ProjectType,
)
from .templates import (
    CHANGELOG,
    DEPENDABOT_CONFIG,
    DOCKERIGNORE,
    EDITORCONFIG,
    GITIGNORE,
    VSCODE_EXTENSIONS,
    VSCODE_SETTINGS,
    get_app_py,
    get_ci_workflow,
    get_docker_compose,
    get_dockerfile,
    get_env_example,
    get_license_content,
    get_main_py,
    get_makefile,
    get_pipeline_py,
    get_precommit_config,
    get_pyproject_toml,
    get_readme,
    get_tcss,
    get_test_file,
)


class ProjectGenerator:
    """Generates Python project repositories."""

    def __init__(self, config: ProjectConfig, author: str = ""):
        """Initialize the generator with project configuration.

        Args:
            config: Project configuration.
            author: Author name for license (defaults to git user.name or GitHub username).
        """
        self.config = config
        self.author = author or self._get_author()
        self.path = config.path

    def _get_author(self) -> str:
        """Get author name from git config or GitHub."""
        try:
            result = subprocess.run(
                ["git", "config", "user.name"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            pass

        try:
            result = subprocess.run(
                ["gh", "api", "user", "--jq", ".name"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "Your Name"

    def _run(
        self,
        cmd: list[str],
        cwd: Path | None = None,
        check: bool = True,
        capture: bool = False,
        clean_env: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        """Run a command with consistent error handling.

        Args:
            cmd: Command and arguments to run.
            cwd: Working directory for the command.
            check: Raise exception on non-zero exit code.
            capture: Capture stdout/stderr instead of displaying.
            clean_env: Remove VIRTUAL_ENV from environment.
        """
        env = None
        if clean_env:
            env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
        return subprocess.run(
            cmd,
            cwd=cwd or self.path,
            check=check,
            capture_output=capture,
            text=True,
            env=env,
        )

    def _write_file(self, relative_path: str, content: str) -> None:
        """Write content to a file within the project."""
        file_path = self.path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)

    def generate(self) -> None:
        """Generate the complete project structure."""
        # Create project directory
        self.path.mkdir(parents=True, exist_ok=True)

        # Initialize with uv
        self._init_uv()

        # Generate config files (including pyproject.toml with all dependencies)
        # This also runs uv lock and uv sync to install everything
        self._generate_config_files()

        # Generate source and test files
        self._generate_source_files()
        self._generate_test_files()
        self._generate_github_files()

        if self.config.features.vscode:
            self._generate_vscode_files()

        if self.config.features.docker:
            self._generate_docker_files()

        if self.config.features.makefile:
            self._write_file(
                "Makefile",
                get_makefile(self.config.project_type, self.config.package_name),
            )

        if self.config.features.changelog:
            self._write_file("CHANGELOG.md", CHANGELOG)

        if self.config.license_type != License.NONE:
            self._write_file(
                "LICENSE", get_license_content(self.config.license_type, self.author)
            )

        # Generate docker-compose for api/data projects (NEW Feature #4)
        if self.config.features.docker_compose and self.config.project_type in (
            ProjectType.API,
            ProjectType.DATA,
        ):
            compose_content = get_docker_compose(self.config)
            if compose_content:
                self._write_file("docker-compose.yml", compose_content)

        # Generate README
        self._write_file("README.md", get_readme(self.config))

        # Security baseline
        if self.config.features.security:
            self._generate_security_baseline()

        # Final sync and git init
        self._finalize()

    def _init_uv(self) -> None:
        """Initialize project with uv."""
        # Initialize with uv - NO editable self-install (FIX #1)
        self._run(
            [
                "uv",
                "init",
                ".",
                "--python",
                self.config.python_version,
                "--no-workspace",
                "--name",
                self.config.package_name,
            ],
            clean_env=True,
        )

        # Remove default files created by uv init
        for f in ["hello.py", "main.py"]:
            path = self.path / f
            if path.exists():
                path.unlink()

        # Write .python-version
        self._write_file(".python-version", f"{self.config.python_version}\n")

    def _generate_config_files(self) -> None:
        """Generate configuration files."""
        # pyproject.toml (completely rewrite with our template)
        self._write_file("pyproject.toml", get_pyproject_toml(self.config))

        # Re-sync after pyproject.toml changes
        self._run(["uv", "lock"], clean_env=True)
        self._run(["uv", "sync"], clean_env=True)

        # Other config files
        self._write_file(".gitignore", GITIGNORE)
        self._write_file(".env.example", get_env_example(self.config.project_type))
        self._write_file(".editorconfig", EDITORCONFIG)
        self._write_file(
            ".pre-commit-config.yaml",
            get_precommit_config(self.config.features.security),
        )

    def _generate_source_files(self) -> None:
        """Generate source code files."""
        src_dir = f"src/{self.config.package_name}"

        # Create package structure
        self._write_file(f"{src_dir}/__init__.py", "")
        self._write_file(f"{src_dir}/py.typed", "")

        # Project-type-specific files
        if self.config.project_type == ProjectType.API:
            main_content = get_main_py(ProjectType.API, self.config.package_name)
            if main_content:
                self._write_file(f"{src_dir}/main.py", main_content)

        elif self.config.project_type == ProjectType.CLI:
            main_content = get_main_py(ProjectType.CLI, self.config.package_name)
            if main_content:
                self._write_file(f"{src_dir}/main.py", main_content)

        elif self.config.project_type == ProjectType.TUI:
            self._write_file(f"{src_dir}/app.py", get_app_py(self.config.package_name))
            self._write_file(
                f"{src_dir}/css/{self.config.package_name}.tcss",
                get_tcss(self.config.package_name),
            )

        elif self.config.project_type == ProjectType.DATA:
            self._write_file(f"{src_dir}/pipeline.py", get_pipeline_py())

    def _generate_test_files(self) -> None:
        """Generate test files."""
        self._write_file("tests/__init__.py", "")

        test_name, test_content = get_test_file(
            self.config.project_type, self.config.package_name
        )
        self._write_file(f"tests/{test_name}", test_content)

    def _generate_github_files(self) -> None:
        """Generate GitHub-related files."""
        # CI workflow (OPTIMIZED - FIX #5)
        self._write_file(
            ".github/workflows/ci.yml", get_ci_workflow(self.config.python_version)
        )

        # Dependabot
        if self.config.features.dependabot:
            self._write_file(".github/dependabot.yml", DEPENDABOT_CONFIG)

    def _generate_vscode_files(self) -> None:
        """Generate VS Code configuration files."""
        self._write_file(".vscode/settings.json", VSCODE_SETTINGS)
        self._write_file(".vscode/extensions.json", VSCODE_EXTENSIONS)

    def _generate_docker_files(self) -> None:
        """Generate Docker-related files."""
        self._write_file("Dockerfile", get_dockerfile(self.config))
        self._write_file(".dockerignore", DOCKERIGNORE)

    def _generate_security_baseline(self) -> None:
        """Generate security baseline for detect-secrets."""
        result = self._run(
            ["uv", "run", "detect-secrets", "scan"],
            capture=True,
            check=False,
            clean_env=True,
        )
        baseline = result.stdout if result.returncode == 0 else "{}"
        self._write_file(".secrets.baseline", baseline)

    def _finalize(self) -> None:
        """Final steps: git init and pre-commit install."""
        # Initialize git
        self._run(["git", "init", "--quiet"])

        # Install pre-commit hooks
        self._run(["uv", "run", "pre-commit", "install"], clean_env=True)


def create_project(config: ProjectConfig, author: str = "") -> Path:
    """Create a new Python project.

    Args:
        config: Project configuration.
        author: Author name for license.

    Returns:
        Path to the created project.
    """
    generator = ProjectGenerator(config, author)
    generator.generate()
    return config.path
