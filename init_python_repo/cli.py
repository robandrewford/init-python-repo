"""Command-line interface for init-python-repo."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

from .config import FeatureFlags, License, ProjectConfig, ProjectType
from .generator import create_project

# Module-level default path to avoid B008
DEFAULT_REPO_LOCATION = Path.home() / "Repos"

app = typer.Typer(
    name="init-python-repo",
    help="Create and initialize Python repositories with best practices.",
    add_completion=False,
)
console = Console()


def check_prerequisites() -> None:
    """Verify required tools are installed."""
    for tool in ["uv", "git"]:
        result = subprocess.run(["which", tool], capture_output=True)
        if result.returncode != 0:
            console.print(f"[red]ERROR: {tool} not found in PATH[/red]")
            raise typer.Exit(1)


def get_github_user() -> str:
    """Get current GitHub username."""
    try:
        result = subprocess.run(
            ["gh", "api", "user", "--jq", ".login"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def github_repo_exists(reponame: str) -> bool:
    """Check if a GitHub repository already exists for the current user."""
    result = subprocess.run(
        ["gh", "repo", "view", reponame],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


@app.command()
def create(
    reponame: Annotated[
        str,
        typer.Option(
            "--reponame", "-n", help="Repository name (required)", prompt=True
        ),
    ],
    repoloc: Annotated[
        Path,
        typer.Option("--repoloc", "-l", help="Parent directory for the new repo"),
    ] = DEFAULT_REPO_LOCATION,
    python: Annotated[
        str,
        typer.Option("--python", "-p", help="Python version"),
    ] = "3.12",
    project_type: Annotated[
        ProjectType,
        typer.Option("--type", "-t", help="Project type"),
    ] = ProjectType.LIBRARY,
    license_type: Annotated[
        License,
        typer.Option("--license", help="License type"),
    ] = License.MIT,
    no_vscode: Annotated[
        bool,
        typer.Option("--no-vscode", help="Skip VS Code configuration"),
    ] = False,
    no_docker: Annotated[
        bool,
        typer.Option("--no-docker", help="Skip Docker configuration"),
    ] = False,
    no_makefile: Annotated[
        bool,
        typer.Option("--no-makefile", help="Skip Makefile generation"),
    ] = False,
    no_changelog: Annotated[
        bool,
        typer.Option("--no-changelog", help="Skip CHANGELOG.md generation"),
    ] = False,
    no_security: Annotated[
        bool,
        typer.Option("--no-security", help="Skip security tools (bandit, detect-secrets)"),
    ] = False,
    no_dependabot: Annotated[
        bool,
        typer.Option("--no-dependabot", help="Skip Dependabot configuration"),
    ] = False,
    no_docker_compose: Annotated[
        bool,
        typer.Option("--no-docker-compose", help="Skip docker-compose.yml for api/data projects"),
    ] = False,
    no_github: Annotated[
        bool,
        typer.Option("--no-github", help="Skip GitHub repo creation"),
    ] = False,
    private: Annotated[
        bool,
        typer.Option("--private/--public", help="Make GitHub repo private or public"),
    ] = True,
    no_vscode_open: Annotated[
        bool,
        typer.Option("--no-vscode-open", help="Don't open VS Code after creation"),
    ] = False,
    author: Annotated[
        str,
        typer.Option("--author", "-a", help="Author name for license"),
    ] = "",
) -> None:
    """Create and initialize a new Python repository.

    Examples:

        # Default library project (Python 3.12, MIT license, all features)
        init-python-repo -n mylib

        # FastAPI project
        init-python-repo -n myapi -t api

        # CLI project with Apache license
        init-python-repo -n mycli -t cli --license Apache-2.0

        # TUI project with Python 3.13
        init-python-repo -n mytui -t tui -p 3.13

        # Minimal project (no docker, no security)
        init-python-repo -n minimal --no-docker --no-security

        # Public GitHub repository
        init-python-repo -n oss-tool --public
    """
    check_prerequisites()

    repo_path = repoloc / reponame

    # Validation
    if repo_path.exists():
        console.print(f"[red]ERROR: {repo_path} already exists[/red]")
        raise typer.Exit(1)

    # Check for invalid project names
    invalid_names = {"test-repo", "test_repo", "tests", "test"}
    if reponame.lower() in invalid_names:
        console.print(
            f"[red]ERROR: Project name '{reponame}' is reserved or invalid[/red]"
        )
        raise typer.Exit(1)

    # Build configuration
    features = FeatureFlags(
        vscode=not no_vscode,
        docker=not no_docker,
        makefile=not no_makefile,
        changelog=not no_changelog,
        security=not no_security,
        dependabot=not no_dependabot,
        docker_compose=not no_docker_compose,
    )

    config = ProjectConfig(
        name=reponame,
        location=repoloc,
        python_version=python,
        project_type=project_type,
        license_type=license_type,
        features=features,
        private_repo=private,
        skip_github=no_github,
        skip_vscode_open=no_vscode_open,
    )

    # Show what we're doing
    console.print(
        f"[blue]Creating {config.package_name} ({project_type.value}, Python {python})[/blue]"
    )

    # Generate the project
    try:
        create_project(config, author)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]ERROR: Command failed: {e.cmd}[/red]")
        raise typer.Exit(1) from None
    except Exception as e:
        console.print(f"[red]ERROR: {e}[/red]")
        raise typer.Exit(1) from None

    # Run tests
    console.print("[blue]Running tests...[/blue]")
    result = subprocess.run(
        ["uv", "run", "pytest"],
        cwd=repo_path,
        env={k: v for k, v in __import__("os").environ.items() if k != "VIRTUAL_ENV"},
    )
    if result.returncode != 0:
        console.print("[yellow]WARNING: Tests failed[/yellow]")

    # GitHub setup
    if not no_github:
        # Check for gh CLI
        gh_check = subprocess.run(["which", "gh"], capture_output=True)
        if gh_check.returncode != 0:
            console.print(
                "[yellow]WARNING: gh CLI not found, skipping GitHub setup[/yellow]"
            )
        else:
            # Check if repo exists
            if github_repo_exists(reponame):
                console.print(
                    f"[red]ERROR: GitHub repository '{reponame}' already exists.[/red]"
                )
                console.print(
                    f"[yellow]To delete: gh repo delete {reponame} --yes[/yellow]"
                )
                console.print(f"[yellow]To clean up: rm -rf {repo_path}[/yellow]")
                raise typer.Exit(1)

            console.print("[blue]Creating GitHub repository...[/blue]")
            visibility = "--private" if private else "--public"
            subprocess.run(
                [
                    "gh",
                    "repo",
                    "create",
                    reponame,
                    visibility,
                    "--source=.",
                    "--remote=origin",
                ],
                cwd=repo_path,
                check=True,
            )

            # Stage, commit, push
            subprocess.run(["git", "add", "-A"], cwd=repo_path, check=True)

            # Run pre-commit to fix any issues
            console.print("[blue]Running pre-commit hooks...[/blue]")
            subprocess.run(
                ["uv", "run", "pre-commit", "run", "--all-files"],
                cwd=repo_path,
                env={
                    k: v
                    for k, v in __import__("os").environ.items()
                    if k != "VIRTUAL_ENV"
                },
            )

            # Re-stage after pre-commit fixes
            subprocess.run(["git", "add", "-A"], cwd=repo_path, check=True)

            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=repo_path,
                check=True,
            )
            subprocess.run(
                ["git", "push", "-u", "origin", "main"],
                cwd=repo_path,
                check=True,
            )

            gh_user = get_github_user()
            if gh_user:
                console.print(
                    f"[green]✓ Pushed to github.com/{gh_user}/{reponame}[/green]"
                )

    # Open VS Code
    if not no_vscode_open:
        try:
            subprocess.run(["code", str(repo_path)], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run(
                    ["open", "-a", "Visual Studio Code", str(repo_path)],
                    check=True,
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                console.print(
                    "[dim]Note: VS Code not opened (install shell command via ⌘⇧P → 'Shell Command: Install')[/dim]"
                )

    # Summary
    console.print(Panel(f"[green]✓ Created {repo_path}[/green]", title="Done"))

    # Print enabled features
    console.print("\n[bold]Features enabled:[/bold]")
    if features.vscode:
        console.print("  • VS Code configuration")
    if features.docker:
        console.print("  • Dockerfile")
    if features.docker_compose and project_type in (ProjectType.API, ProjectType.DATA):
        console.print("  • docker-compose.yml")
    if features.makefile:
        console.print("  • Makefile")
    if features.changelog:
        console.print("  • CHANGELOG.md")
    if features.security:
        console.print("  • Security scanning (bandit, detect-secrets)")
    if features.dependabot:
        console.print("  • Dependabot")
    if config.license_type != License.NONE:
        console.print(f"  • License: {config.license_type.value}")

    console.print("\n[bold]Next steps:[/bold]")
    console.print(f"  cd {repo_path}")
    console.print("  source .venv/bin/activate")
    if features.makefile:
        console.print("  make test")


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    sys.exit(main() or 0)
