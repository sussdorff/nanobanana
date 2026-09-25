"""Smoke test the installed command rather than a nested package manager invocation."""

import subprocess
import sys
from pathlib import Path


def test_installed_entrypoint_reports_version() -> None:
    cli = Path(sys.executable).with_name("nanobanana")
    result = subprocess.run(
        [str(cli), "-version"], capture_output=True, text=True, check=False, timeout=10,
    )
    assert result.returncode == 0
    assert result.stdout.startswith("nanobanana ")
