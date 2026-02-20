"""Tests for CLI flag parsing and extension auto-correction — ported from Go tests."""

import pytest

from nanobanana.cli import build_parser
from nanobanana.mime import extension_from_mime


def test_parse_basic_prompt() -> None:
    parser = build_parser()
    args = parser.parse_args(["a cute cat"])
    assert args.prompt == ["a cute cat"]
    assert args.input_images == []
    assert args.output == ""
    assert args.aspect == ""
    assert args.size == ""
    assert args.model == ""


def test_parse_all_flags() -> None:
    parser = build_parser()
    args = parser.parse_args([
        "-i", "a.jpg", "-i", "b.png",
        "-o", "out.png",
        "-aspect", "16:9",
        "-size", "2K",
        "-model", "google/gemini-3-pro-image-preview",
        "my prompt",
    ])
    assert args.input_images == ["a.jpg", "b.png"]
    assert args.output == "out.png"
    assert args.aspect == "16:9"
    assert args.size == "2K"
    assert args.model == "google/gemini-3-pro-image-preview"
    assert args.prompt == ["my prompt"]


def test_parse_version_flag() -> None:
    parser = build_parser()
    args = parser.parse_args(["-version"])
    assert args.show_version is True


def test_parse_help_flag() -> None:
    parser = build_parser()
    args = parser.parse_args(["-h"])
    assert args.show_help is True


def test_parse_multi_word_prompt() -> None:
    parser = build_parser()
    args = parser.parse_args(["a", "cute", "cat"])
    assert args.prompt == ["a", "cute", "cat"]


def test_parse_repeatable_input() -> None:
    """Ported from TestStringSlice_Set — verifies -i accumulates."""
    parser = build_parser()
    args = parser.parse_args(["-i", "a.jpg", "-i", "b.png", "-i", "c.webp", "prompt"])
    assert args.input_images == ["a.jpg", "b.png", "c.webp"]


# --- Extension auto-correction (ported from TestExtensionAutoCorrection) ---

@pytest.mark.parametrize(
    "user_output, mime_type, expected_ext",
    [
        ("output.png", "image/jpeg", ".jpg"),
        ("output.jpg", "image/jpeg", ".jpg"),
        ("output.png", "image/png", ".png"),
        ("output.webp", "image/jpeg", ".jpg"),
        ("output", "image/jpeg", ".jpg"),
    ],
)
def test_extension_auto_correction(user_output: str, mime_type: str, expected_ext: str) -> None:
    """Ported from TestExtensionAutoCorrection in Go."""
    from pathlib import Path

    correct_ext = extension_from_mime(mime_type)
    output_path = user_output
    current_ext = Path(output_path).suffix.lower()

    if current_ext != correct_ext:
        # Strip existing extension and add correct one
        stem = Path(output_path).stem if Path(output_path).suffix else output_path
        output_path = stem + correct_ext

    assert output_path.endswith(expected_ext)
