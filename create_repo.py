#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "typer>=0.15.0",
#     "rich>=13.0.0",
# ]
# [tool.uv]
# exclude-newer = "2025-06-01T00:00:00Z"
# ///
"""
Create and initialize a new Python repository.

Usage:
    ./create_repo.py --reponame myapi --type api
    ./create_repo.py -n mylib -l ~/Projects
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Annotated

import typer # pyright: ignore[reportMissingImports]
from rich.console import Console # pyright: ignore[reportMissingImports]
from rich.panel import Panel # pyright: ignore[reportMissingImports]

app = typer.Typer(add_completion=False)
console = Console()


def run(
    cmd: list[str],
    cwd: Path | None = None,
    check: bool = True,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Run a command with consistent error handling."""
    return subprocess.run(
        cmd,
        cwd=cwd,
        check=check,
        capture_output=capture,
        text=True,
    )


def check_prerequisites() -> None:
    """Verify required tools are installed."""
    for tool in ["uv", "git", "gh"]:
        result = subprocess.run(["which", tool], capture_output=True)
        if result.returncode != 0:
            console.print(f"[red]ERROR: {tool} not found in PATH[/red]")
            raise typer.Exit(1)


@app.command()
def create(
    reponame: Annotated[str, typer.Option("--reponame", "-n", help="Repository name")],
    repoloc: Annotated[Path, typer.Option("--repoloc", "-l", help="Parent directory")] = Path.home() / "Repos",
    python: Annotated[str, typer.Option("--python", "-p", help="Python version")] = "3.12",
    project_type: Annotated[str, typer.Option("--type", "-t", help="Project type")] = "library",
    no_vscode: Annotated[bool, typer.Option("--no-vscode", help="Skip VS Code")] = False,
    no_github: Annotated[bool, typer.Option("--no-github", help="Skip GitHub repo creation")] = False,
    private: Annotated[bool, typer.Option("--private", help="Make GitHub repo private")] = True,
) -> None:
    """Create and initialize a new Python repository."""
    check_prerequisites()

    repo_path = repoloc / reponame
    script_dir = Path(__file__).parent.resolve()
    init_script = script_dir / "init-python-repo.sh"

    if not init_script.exists():
        console.print(f"[red]ERROR: {init_script} not found[/red]")
        raise typer.Exit(1)

    if repo_path.exists():
        console.print(f"[red]ERROR: {repo_path} already exists[/red]")
        raise typer.Exit(1)

    # Create directory
    console.print(f"[blue]Creating {repo_path}[/blue]")
    repo_path.mkdir(parents=True)

    # Run init script
    console.print(f"[blue]Initializing {project_type} project with Python {python}[/blue]")
    env = {
        **os.environ,
        "PROJECT_TYPE": project_type,
        "PYTHON_VERSION": python,
    }
    result = subprocess.run([str(init_script)], cwd=repo_path, env=env)
    if result.returncode != 0:
        console.print("[red]ERROR: init-python-repo.sh failed[/red]")
        raise typer.Exit(1)

    # Run tests
    console.print("[blue]Running tests[/blue]")
    result = run(["uv", "run", "pytest"], cwd=repo_path, check=False)
    if result.returncode != 0:
        console.print("[yellow]WARNING: Tests failed[/yellow]")

    # GitHub setup
    if not no_github:
        console.print("[blue]Creating GitHub repository[/blue]")
        visibility = "--private" if private else "--public"
        run(
            ["gh", "repo", "create", reponame, visibility, "--source=.", "--remote=origin"],
            cwd=repo_path,
        )
        run(["git", "add", "-A"], cwd=repo_path)
        run(["git", "commit", "-m", "Initial commit"], cwd=repo_path)
        run(["git", "push", "-u", "origin", "main"], cwd=repo_path)
        console.print(f"[green]✓ Pushed to github.com/{get_github_user()}/{reponame}[/green]")

    # Open VS Code
    if not no_vscode:
        run(["code", str(repo_path)])

    console.print(Panel(f"[green]✓ Created {repo_path}[/green]", title="Done"))


def get_github_user() -> str:
    """Get current GitHub username."""
    result = run(["gh", "api", "user", "--jq", ".login"], capture=True)
    return result.stdout.strip()


if __name__ == "__main__":
    app()