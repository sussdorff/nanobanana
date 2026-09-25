"""Tests for the setup wizard and config writing."""

import json

from nanobanana.cli import _extract_subcommand
from nanobanana.config import FileConfig, load_config, resolve_config, write_config


def test_setup_subcommand_extracted() -> None:
    cmd, rest = _extract_subcommand(["setup", "extra"])
    assert cmd == "setup"
    assert rest == ["extra"]


class TestWriteConfig:
    """Tests for write_config()."""

    def test_write_creates_file(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        data = {"api": "gemini", "api_key": "test-key"}
        path = write_config(data)

        assert path.exists()
        written = json.loads(path.read_text())
        assert written == data

    def test_write_creates_directories(self, tmp_path, monkeypatch) -> None:
        config_home = tmp_path / "deep" / "nested"
        monkeypatch.setenv("XDG_CONFIG_HOME", str(config_home))
        path = write_config({"api": "gemini"})

        assert path.exists()
        assert "nanobanana" in str(path)

    def test_write_then_load_roundtrip(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        data = {
            "api": "openrouter",
            "api_key": "or-key-123",
            "aspect": "16:9",
            "size": "2K",
        }
        write_config(data)

        fc = load_config()
        assert fc is not None
        assert fc.api == "openrouter"
        assert fc.api_key == "or-key-123"
        assert fc.aspect == "16:9"
        assert fc.size == "2K"


class TestApiKeyFromConfig:
    """Tests that api_key in config file is used as fallback."""

    def test_api_key_from_config_gemini(self, monkeypatch) -> None:
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

        fc = FileConfig(api_key="config-gemini-key")
        _, _, config = resolve_config(
            aspect_flag="", size_flag="", model_flag="", file_config=fc,
        )
        assert config.api_key == "config-gemini-key"
        assert config.use_openrouter is False

    def test_api_key_from_config_openrouter(self, monkeypatch) -> None:
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

        fc = FileConfig(api="openrouter", api_key="config-or-key")
        _, _, config = resolve_config(
            aspect_flag="", size_flag="", model_flag="", file_config=fc,
        )
        assert config.api_key == "config-or-key"
        assert config.use_openrouter is True

    def test_env_var_overrides_config_api_key(self, monkeypatch) -> None:
        monkeypatch.setenv("GEMINI_API_KEY", "env-key")
        monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

        fc = FileConfig(api_key="config-key")
        _, _, config = resolve_config(
            aspect_flag="", size_flag="", model_flag="", file_config=fc,
        )
        assert config.api_key == "env-key"

    def test_config_api_key_priority_over_key_command(self, monkeypatch) -> None:
        """api_key from config takes priority over key_command."""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

        fc = FileConfig(api_key="direct-key", key_command="echo should-not-run")
        _, _, config = resolve_config(
            aspect_flag="", size_flag="", model_flag="", file_config=fc,
        )
        assert config.api_key == "direct-key"

class TestHelpText:
    """Tests that setup appears in help text."""

    def test_setup_in_help_overview(self) -> None:
        from nanobanana.templates import format_help_overview
        overview = format_help_overview()
        assert "setup" in overview
