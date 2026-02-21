"""Check PyPI for newer versions of nanobanana-cli."""

import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from nanobanana.config import get_config_path

_PYPI_URL = "https://pypi.org/pypi/nanobanana-cli/json"
_CHECK_INTERVAL = 86400  # 24 hours


def _cache_path() -> Path:
    """Return path to the update check cache file."""
    config_path = get_config_path()
    if config_path is None:
        return Path.home() / ".cache" / "nanobanana" / "update_check.json"
    return config_path.parent / "update_check.json"


def _read_cache() -> dict:
    path = _cache_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _write_cache(data: dict) -> None:
    path = _cache_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data))
    except OSError:
        pass


def _fetch_latest_version() -> str | None:
    """Fetch latest version from PyPI. Returns None on any failure."""
    try:
        req = urllib.request.Request(_PYPI_URL, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read())
            return data.get("info", {}).get("version")
    except Exception:
        return None


def _run_upgrade() -> bool:
    """Run uv tool upgrade. Returns True on success."""
    try:
        result = subprocess.run(
            ["uv", "tool", "upgrade", "nanobanana-cli"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        return result.returncode == 0
    except Exception:
        return False


def check_for_update(current_version: str, *, auto_update: bool = False) -> str | None:
    """Check if a newer version is available on PyPI.

    If auto_update is True, automatically runs uv tool upgrade.
    Otherwise returns an update hint string.
    Returns None if up to date / check skipped. Never raises.
    """
    if current_version == "dev":
        return None

    try:
        cache = _read_cache()
        last_check = cache.get("last_check", 0)

        if time.time() - last_check < _CHECK_INTERVAL:
            # Use cached result
            latest = cache.get("latest_version")
        else:
            latest = _fetch_latest_version()
            _write_cache({
                "last_check": time.time(),
                "latest_version": latest,
            })

        if latest and latest != current_version:
            if auto_update:
                print(
                    f"Updating nanobanana-cli: {current_version} \u2192 {latest}...",
                    file=sys.stderr,
                )
                if _run_upgrade():
                    return f"Updated to {latest}. Restart to use the new version."
                else:
                    return (
                        f"Auto-update failed. Run manually:\n"
                        f"  uv tool upgrade nanobanana-cli"
                    )
            return (
                f"Update available: {current_version} \u2192 {latest}\n"
                f"Run: uv tool upgrade nanobanana-cli"
            )
    except Exception:
        pass

    return None
