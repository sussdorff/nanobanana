"""Tests for CLI flag parsing and extension auto-correction — ported from Go tests."""

import pytest

from nanobanana.cli import build_parser, _extract_subcommand
from nanobanana.mime import extension_from_mime
from nanobanana.templates import COMMANDS, get_command, format_help_overview, format_command_help


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


# --- Subcommand routing tests ---

class TestSubcommandExtraction:
    """Tests for _extract_subcommand — command detection from argv."""

    def test_known_command_extracted(self) -> None:
        cmd, rest = _extract_subcommand(["dashboard", "my metrics"])
        assert cmd == "dashboard"
        assert rest == ["my metrics"]

    def test_known_command_with_flags(self) -> None:
        cmd, rest = _extract_subcommand(["-o", "out.png", "slide", "my slide"])
        assert cmd == "slide"
        assert rest == ["-o", "out.png", "my slide"]

    def test_unknown_first_arg_is_free_prompt(self) -> None:
        cmd, rest = _extract_subcommand(["a cute cat"])
        assert cmd == ""
        assert rest == ["a cute cat"]

    def test_flags_only_no_command(self) -> None:
        cmd, rest = _extract_subcommand(["-aspect", "16:9", "-size", "2K", "a prompt"])
        assert cmd == ""
        assert rest == ["-aspect", "16:9", "-size", "2K", "a prompt"]

    def test_empty_argv(self) -> None:
        cmd, rest = _extract_subcommand([])
        assert cmd == ""
        assert rest == []

    def test_help_command(self) -> None:
        cmd, rest = _extract_subcommand(["help"])
        assert cmd == "help"
        assert rest == []

    def test_help_with_topic(self) -> None:
        cmd, rest = _extract_subcommand(["help", "dashboard"])
        assert cmd == "help"
        assert rest == ["dashboard"]

    def test_version_command(self) -> None:
        cmd, rest = _extract_subcommand(["version"])
        assert cmd == "version"
        assert rest == []

    def test_generate_command(self) -> None:
        cmd, rest = _extract_subcommand(["generate", "a cute cat"])
        assert cmd == "generate"
        assert rest == ["a cute cat"]

    def test_all_registered_commands(self) -> None:
        """Every command in COMMANDS should be recognized."""
        for name in COMMANDS:
            cmd, rest = _extract_subcommand([name, "some prompt"])
            assert cmd == name, f"Command {name!r} not recognized"
            assert rest == ["some prompt"]


class TestTemplateApplication:
    """Tests that templates correctly wrap user prompts."""

    def test_dashboard_template_contains_user_prompt(self) -> None:
        cmd = get_command("dashboard")
        assert cmd is not None
        result = cmd.apply("revenue metrics for Q4", aspect="16:9", size="2K")
        assert "revenue metrics for Q4" in result
        assert "TASK" in result
        assert "SOURCE MATERIAL" in result

    def test_generate_passes_through(self) -> None:
        cmd = get_command("generate")
        assert cmd is not None
        result = cmd.apply("a cute cat", aspect="1:1", size="1K")
        assert result == "a cute cat"

    def test_aspect_and_size_injected(self) -> None:
        cmd = get_command("slide")
        assert cmd is not None
        result = cmd.apply("test", aspect="16:9", size="2K")
        assert "16:9" in result
        assert "2K" in result

    @pytest.mark.parametrize("command_name", list(COMMANDS.keys()))
    def test_all_templates_accept_format_args(self, command_name: str) -> None:
        """Every template must format without errors."""
        cmd = get_command(command_name)
        assert cmd is not None
        result = cmd.apply("test prompt", aspect="1:1", size="1K")
        assert isinstance(result, str)
        assert len(result) > 0


class TestCommandDefaults:
    """Tests that commands have appropriate default aspect/size."""

    def test_dashboard_defaults(self) -> None:
        cmd = get_command("dashboard")
        assert cmd is not None
        assert cmd.default_aspect == "16:9"
        assert cmd.default_size == "2K"

    def test_moodboard_defaults(self) -> None:
        cmd = get_command("moodboard")
        assert cmd is not None
        assert cmd.default_aspect == "1:1"
        assert cmd.default_size == "2K"

    def test_explore_defaults(self) -> None:
        cmd = get_command("explore")
        assert cmd is not None
        assert cmd.default_aspect == "1:1"
        assert cmd.default_size == "2K"

    def test_icon_defaults(self) -> None:
        cmd = get_command("icon")
        assert cmd is not None
        assert cmd.default_aspect == "1:1"
        assert cmd.default_size == "1K"

    def test_slide_defaults(self) -> None:
        cmd = get_command("slide")
        assert cmd is not None
        assert cmd.default_aspect == "16:9"
        assert cmd.default_size == "2K"

    def test_generate_defaults(self) -> None:
        cmd = get_command("generate")
        assert cmd is not None
        assert cmd.default_aspect == "1:1"
        assert cmd.default_size == "1K"


class TestHelpFormatting:
    """Tests for help text generation."""

    def test_help_overview_lists_all_commands(self) -> None:
        overview = format_help_overview()
        for name in COMMANDS:
            assert name in overview

    def test_help_overview_includes_help_and_version(self) -> None:
        overview = format_help_overview()
        assert "help" in overview
        assert "version" in overview

    def test_command_help_shows_defaults(self) -> None:
        cmd = get_command("dashboard")
        assert cmd is not None
        help_text = format_command_help(cmd)
        assert "16:9" in help_text
        assert "2K" in help_text
        assert "dashboard" in help_text

    def test_command_help_shows_template(self) -> None:
        cmd = get_command("slide")
        assert cmd is not None
        help_text = format_command_help(cmd)
        assert "TASK" in help_text

    def test_unknown_command_returns_none(self) -> None:
        assert get_command("nonexistent") is None


class TestBackwardsCompatibility:
    """Tests that existing usage patterns still work after subcommand addition."""

    def test_free_prompt_no_command(self) -> None:
        """nanobanana 'a cute cat' should still work."""
        cmd, rest = _extract_subcommand(["a cute cat"])
        assert cmd == ""
        parser = build_parser()
        args = parser.parse_args(rest)
        assert args.prompt == ["a cute cat"]

    def test_flags_with_free_prompt(self) -> None:
        """nanobanana -i img.jpg 'prompt' should still work."""
        cmd, rest = _extract_subcommand(["-i", "img.jpg", "a prompt"])
        assert cmd == ""
        parser = build_parser()
        args = parser.parse_args(rest)
        assert args.input_images == ["img.jpg"]
        assert args.prompt == ["a prompt"]

    def test_all_flags_with_free_prompt(self) -> None:
        """nanobanana -i a.jpg -o out.png -aspect 16:9 -size 2K 'prompt'"""
        argv = ["-i", "a.jpg", "-o", "out.png", "-aspect", "16:9", "-size", "2K", "my prompt"]
        cmd, rest = _extract_subcommand(argv)
        assert cmd == ""
        parser = build_parser()
        args = parser.parse_args(rest)
        assert args.input_images == ["a.jpg"]
        assert args.output == "out.png"
        assert args.aspect == "16:9"
        assert args.size == "2K"
        assert args.prompt == ["my prompt"]

    def test_version_flag_still_works(self) -> None:
        cmd, rest = _extract_subcommand(["-version"])
        assert cmd == ""
        parser = build_parser()
        args = parser.parse_args(rest)
        assert args.show_version is True

    def test_help_flag_still_works(self) -> None:
        cmd, rest = _extract_subcommand(["-h"])
        assert cmd == ""
        parser = build_parser()
        args = parser.parse_args(rest)
        assert args.show_help is True
