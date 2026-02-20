"""Configuration loading and validation."""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

GEMINI_MODEL = "gemini-3-pro-image-preview"
OPENROUTER_DEFAULT_MODEL = "google/gemini-3-pro-image-preview"
HTTP_TIMEOUT = 120

VALID_ASPECT_RATIOS = frozenset({
    "1:1", "2:3", "3:2", "3:4", "4:3",
    "4:5", "5:4", "9:16", "16:9", "21:9",
})

VALID_SIZES = frozenset({"1K", "2K", "4K"})


@dataclass
class FileConfig:
    api: str = ""
    model: str = ""
    aspect: str = ""
    size: str = ""


@dataclass
class APIConfig:
    use_openrouter: bool = False
    api_key: str = ""
    model: str = ""


def get_config_path() -> Path | None:
    """Return the XDG config file path, or None if home dir unavailable."""
    config_home = os.environ.get("XDG_CONFIG_HOME")
    if not config_home:
        home = Path.home()
        config_home = str(home / ".config")
    return Path(config_home) / "nanobanana" / "config.json"


def load_config() -> FileConfig | None:
    """Load configuration from the XDG config file. Returns None if not found."""
    config_path = get_config_path()
    if config_path is None or not config_path.exists():
        return None

    try:
        data = json.loads(config_path.read_text())
    except json.JSONDecodeError as e:
        raise RuntimeError(f"failed to parse config file: {e}") from e
    except OSError as e:
        raise RuntimeError(f"failed to read config file: {e}") from e

    return FileConfig(
        api=data.get("api", ""),
        model=data.get("model", ""),
        aspect=data.get("aspect", ""),
        size=data.get("size", ""),
    )


def resolve_config(
    *,
    aspect_flag: str,
    size_flag: str,
    model_flag: str,
    file_config: FileConfig | None,
) -> tuple[str, str, APIConfig]:
    """Resolve final aspect, size, and API config from flags + file config + env.

    Returns (aspect, size, api_config).
    Raises RuntimeError on validation errors.
    """
    # Defaults
    aspect = "1:1"
    size = "1K"
    model = ""
    use_openrouter = False

    # Apply config file values
    if file_config is not None:
        if file_config.aspect:
            aspect = file_config.aspect
        if file_config.size:
            size = file_config.size
        if file_config.model:
            model = file_config.model
        if file_config.api == "openrouter":
            use_openrouter = True

    # Apply CLI flags (override config)
    if aspect_flag:
        aspect = aspect_flag
    if size_flag:
        size = size_flag
    if model_flag:
        model = model_flag
        use_openrouter = True  # -model flag implies OpenRouter

    # Determine which API to use and validate API key
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
    gemini_key = os.environ.get("GEMINI_API_KEY", "")

    config = APIConfig()

    if use_openrouter or model or (openrouter_key and not gemini_key):
        if not openrouter_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY environment variable not set "
                "(required for OpenRouter API)"
            )
        config.use_openrouter = True
        config.api_key = openrouter_key
        config.model = model if model else OPENROUTER_DEFAULT_MODEL
    else:
        if not gemini_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable not set "
                "(or use OPENROUTER_API_KEY)"
            )
        config.use_openrouter = False
        config.api_key = gemini_key

    # Validate aspect ratio
    if aspect not in VALID_ASPECT_RATIOS:
        raise RuntimeError(
            f"invalid aspect ratio: {aspect} "
            f"(valid: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9)"
        )

    # Validate size
    if size not in VALID_SIZES:
        raise RuntimeError(f"invalid size: {size} (valid: 1K, 2K, 4K)")

    return aspect, size, config
