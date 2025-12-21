"""Tests for configuration module."""

from pathlib import Path

from init_python_repo.config import (
    CORE_DEV_DEPS,
    DEV_DEPS,
    RUNTIME_DEPS,
    FeatureFlags,
    License,
    ProjectConfig,
    ProjectType,
)


class TestProjectType:
    """Tests for ProjectType enum."""

    def test_all_types_defined(self) -> None:
        """Ensure all project types are defined."""
        assert ProjectType.LIBRARY.value == "library"
        assert ProjectType.API.value == "api"
        assert ProjectType.CLI.value == "cli"
        assert ProjectType.DATA.value == "data"
        assert ProjectType.TUI.value == "tui"

    def test_project_type_is_string(self) -> None:
        """Verify ProjectType is a string enum."""
        assert isinstance(ProjectType.LIBRARY.value, str)


class TestLicense:
    """Tests for License enum."""

    def test_all_licenses_defined(self) -> None:
        """Ensure all license types are defined."""
        assert License.MIT.value == "MIT"
        assert License.APACHE2.value == "Apache-2.0"
        assert License.GPL3.value == "GPL-3.0"
        assert License.BSD3.value == "BSD-3-Clause"
        assert License.UNLICENSE.value == "Unlicense"
        assert License.NONE.value == "None"


class TestFeatureFlags:
    """Tests for FeatureFlags dataclass."""

    def test_default_values(self) -> None:
        """Test default feature flags."""
        flags = FeatureFlags()
        assert flags.vscode is True
        assert flags.docker is True
        assert flags.makefile is True
        assert flags.changelog is True
        assert flags.security is True
        assert flags.dependabot is True
        assert flags.docker_compose is True

    def test_custom_values(self) -> None:
        """Test custom feature flag values."""
        flags = FeatureFlags(vscode=False, docker=False, security=False)
        assert flags.vscode is False
        assert flags.docker is False
        assert flags.security is False
        assert flags.makefile is True  # unchanged default


class TestProjectConfig:
    """Tests for ProjectConfig dataclass."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = ProjectConfig(name="test-project")
        assert config.name == "test-project"
        assert config.python_version == "3.12"
        assert config.project_type == ProjectType.LIBRARY
        assert config.license_type == License.MIT
        assert config.private_repo is True

    def test_path_property(self) -> None:
        """Test path property combines location and name."""
        config = ProjectConfig(name="myproject", location=Path("/tmp"))
        assert config.path == Path("/tmp/myproject")

    def test_package_name_converts_dashes(self) -> None:
        """Test package_name converts dashes to underscores."""
        config = ProjectConfig(name="my-cool-project")
        assert config.package_name == "my_cool_project"

    def test_package_name_converts_dots(self) -> None:
        """Test package_name converts dots to underscores."""
        config = ProjectConfig(name="my.project")
        assert config.package_name == "my_project"

    def test_python_target_property(self) -> None:
        """Test python_target generates correct format."""
        config = ProjectConfig(name="test", python_version="3.12")
        assert config.python_target == "py312"

        config2 = ProjectConfig(name="test", python_version="3.13")
        assert config2.python_target == "py313"


class TestDependencyMappings:
    """Tests for dependency mappings."""

    def test_all_project_types_have_runtime_deps(self) -> None:
        """Ensure all project types have runtime deps defined."""
        for project_type in ProjectType:
            assert project_type in RUNTIME_DEPS

    def test_all_project_types_have_dev_deps(self) -> None:
        """Ensure all project types have dev deps defined."""
        for project_type in ProjectType:
            assert project_type in DEV_DEPS

    def test_library_has_no_runtime_deps(self) -> None:
        """Library should have no runtime dependencies."""
        assert RUNTIME_DEPS[ProjectType.LIBRARY] == []

    def test_api_has_fastapi(self) -> None:
        """API projects should include FastAPI."""
        assert "fastapi" in RUNTIME_DEPS[ProjectType.API]

    def test_cli_has_typer(self) -> None:
        """CLI projects should include Typer."""
        assert "typer" in RUNTIME_DEPS[ProjectType.CLI]

    def test_data_has_polars(self) -> None:
        """Data projects should include Polars."""
        assert "polars" in RUNTIME_DEPS[ProjectType.DATA]

    def test_tui_has_textual(self) -> None:
        """TUI projects should include Textual."""
        assert "textual" in RUNTIME_DEPS[ProjectType.TUI]

    def test_core_dev_deps_includes_essentials(self) -> None:
        """Core dev deps should include essential tools."""
        assert "ruff" in CORE_DEV_DEPS
        assert "pytest" in CORE_DEV_DEPS
        assert "mypy" in CORE_DEV_DEPS
        assert "pre-commit" in CORE_DEV_DEPS
