"""Tests for the update checker."""

import json
import time

import pytest

from nanobanana.update_check import (
    _cache_path,
    _read_cache,
    _write_cache,
    check_for_update,
)


class TestUpdateCheckCache:
    """Tests for cache read/write."""

    def test_write_and_read_cache(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        data = {"last_check": 12345, "latest_version": "20260101.120000"}
        _write_cache(data)
        assert _read_cache() == data

    def test_read_missing_cache(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        assert _read_cache() == {}

    def test_read_corrupt_cache(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        path = _cache_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("not json")
        assert _read_cache() == {}


class TestCheckForUpdate:
    """Tests for the update check logic."""

    def test_dev_version_skips_check(self) -> None:
        assert check_for_update("dev") is None

    def test_same_version_returns_none(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        # Seed cache with same version
        _write_cache({
            "last_check": time.time(),
            "latest_version": "20260221.120000",
        })
        assert check_for_update("20260221.120000") is None

    def test_newer_version_returns_hint(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        # Seed cache with newer version
        _write_cache({
            "last_check": time.time(),
            "latest_version": "20260222.120000",
        })
        hint = check_for_update("20260221.120000")
        assert hint is not None
        assert "20260222.120000" in hint
        assert "uv tool install" in hint

    def test_stale_cache_triggers_fetch(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        # Seed cache with old timestamp
        _write_cache({
            "last_check": time.time() - 100000,
            "latest_version": "20260220.120000",
        })
        # Mock the fetch to return a known version
        monkeypatch.setattr(
            "nanobanana.update_check._fetch_latest_version",
            lambda: "20260222.120000",
        )
        hint = check_for_update("20260221.120000")
        assert hint is not None
        assert "20260222.120000" in hint

    def test_fetch_failure_returns_none(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        # Stale cache so it tries to fetch
        _write_cache({"last_check": 0})
        monkeypatch.setattr(
            "nanobanana.update_check._fetch_latest_version",
            lambda: None,
        )
        assert check_for_update("20260221.120000") is None

    def test_auto_update_success(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        _write_cache({
            "last_check": time.time(),
            "latest_version": "20260222.120000",
        })
        monkeypatch.setattr(
            "nanobanana.update_check._run_upgrade",
            lambda: True,
        )
        hint = check_for_update("20260221.120000", auto_update=True)
        assert hint is not None
        assert "Updated to" in hint

    def test_auto_update_failure(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        _write_cache({
            "last_check": time.time(),
            "latest_version": "20260222.120000",
        })
        monkeypatch.setattr(
            "nanobanana.update_check._run_upgrade",
            lambda: False,
        )
        hint = check_for_update("20260221.120000", auto_update=True)
        assert hint is not None
        assert "Auto-update failed" in hint


class TestAutoUpdateConfig:
    """Tests that auto_update is loaded from config."""

    def test_load_auto_update_true(self, tmp_path, monkeypatch) -> None:
        from nanobanana.config import load_config
        config_dir = tmp_path / "nanobanana"
        config_dir.mkdir()
        (config_dir / "config.json").write_text(json.dumps({
            "api": "gemini",
            "auto_update": True,
        }))
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        fc = load_config()
        assert fc is not None
        assert fc.auto_update is True

    def test_load_auto_update_default_false(self, tmp_path, monkeypatch) -> None:
        from nanobanana.config import load_config
        config_dir = tmp_path / "nanobanana"
        config_dir.mkdir()
        (config_dir / "config.json").write_text(json.dumps({"api": "gemini"}))
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        fc = load_config()
        assert fc is not None
        assert fc.auto_update is False
