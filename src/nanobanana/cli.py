"""CLI entry point for nanobanana."""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from nanobanana import __version__
from nanobanana.config import load_config, resolve_config
from nanobanana.mime import extension_from_mime


USAGE_TEXT = """\
nanobanana - Generate images using Gemini or OpenRouter API

Usage:
  nanobanana [options] "prompt"

Options:
  -i <file>      Input image file (can be repeated for multi-image composition)
                  Supported formats: PNG, JPEG, WebP, GIF
  -o <file>      Output filename (auto-generated if not specified)
                  Extension auto-corrected to match API response format
  -aspect <ratio> Aspect ratio (default: 1:1)
                  Valid: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  -size <size>   Image size (default: 1K)
                  Valid: 1K, 2K, 4K
  -model <model> OpenRouter model (enables OpenRouter API)
                  Default: google/gemini-3-pro-image-preview
  -h             Show this help
  -version       Show version

Environment:
  GEMINI_API_KEY      Gemini API key
  OPENROUTER_API_KEY  OpenRouter API key

Config File:
  Location: $XDG_CONFIG_HOME/nanobanana/config.json (default: ~/.config/nanobanana/config.json)

  Example config:
    {
      "api": "openrouter",
      "model": "google/gemini-3-pro-image-preview",
      "aspect": "16:9",
      "size": "2K"
    }

  Fields:
    api     - "gemini" or "openrouter" (default: gemini)
    model   - OpenRouter model name (only used with openrouter)
    aspect  - Default aspect ratio
    size    - Default image size

Priority (highest to lowest):
  1. CLI flags
  2. Config file
  3. Environment variables (for API keys only)
  4. Built-in defaults

Examples:
  # Text-to-image generation (Gemini)
  nanobanana "a cute cat"
  nanobanana -o output.jpg "a sunset over mountains"
  nanobanana -aspect 16:9 -size 2K "cinematic landscape"

  # Using OpenRouter
  nanobanana -model google/gemini-3-pro-image-preview "a cute cat"
  nanobanana -model google/gemini-2.5-flash-image-preview "a sunset"

  # Image editing (single input)
  nanobanana -i photo.jpg "transform into watercolor style"
  nanobanana -i portrait.jpg "make it look like a Van Gogh painting"

  # Multi-image composition
  nanobanana -i background.jpg -i subject.jpg "place subject in the scene"
  nanobanana -i dress.jpg -i model.jpg "show the dress on the model"

  # Combined options
  nanobanana -i input.jpg -aspect 16:9 -size 2K -o output.jpg "cinematic edit"
"""


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with single-dash long flags."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-i", action="append", default=[], dest="input_images",
                        help="Input image file (repeatable)")
    parser.add_argument("-o", default="", dest="output",
                        help="Output filename")
    parser.add_argument("-aspect", default="", dest="aspect",
                        help="Aspect ratio")
    parser.add_argument("-size", default="", dest="size",
                        help="Image size")
    parser.add_argument("-model", default="", dest="model",
                        help="OpenRouter model")
    parser.add_argument("-h", action="store_true", dest="show_help",
                        help="Show help")
    parser.add_argument("-version", action="store_true", dest="show_version",
                        help="Show version")
    parser.add_argument("prompt", nargs="*", help="Generation prompt")
    return parser


def print_usage() -> None:
    """Print usage text to stderr."""
    sys.stderr.write(USAGE_TEXT)


def run() -> None:
    """Main CLI logic. Raises RuntimeError on errors."""
    parser = build_parser()
    args = parser.parse_args()

    if args.show_version:
        print(f"nanobanana {__version__}")
        return

    if args.show_help:
        print_usage()
        return

    if not args.prompt:
        print_usage()
        raise RuntimeError("no prompt provided")

    prompt = " ".join(args.prompt)

    # Load config file
    file_config = load_config()

    # Resolve configuration
    aspect, size, api_config = resolve_config(
        aspect_flag=args.aspect,
        size_flag=args.size,
        model_flag=args.model,
        file_config=file_config,
    )

    print("Generating image...")
    print(f"  Prompt: {prompt}")
    if args.input_images:
        print(f"  Inputs: {', '.join(args.input_images)}")
    print(f"  Aspect: {aspect}")
    print(f"  Size:   {size}")
    if api_config.use_openrouter:
        print(f"  API:    OpenRouter ({api_config.model})")
    else:
        print("  API:    Gemini")

    # Generate image
    if api_config.use_openrouter:
        from nanobanana.openrouter import generate_image as gen_openrouter
        image_data, mime_type = gen_openrouter(
            api_key=api_config.api_key,
            model=api_config.model,
            prompt=prompt,
            input_images=args.input_images,
            aspect_ratio=aspect,
            image_size=size,
        )
    else:
        from nanobanana.gemini import generate_image as gen_gemini
        image_data, mime_type = gen_gemini(
            api_key=api_config.api_key,
            prompt=prompt,
            input_images=args.input_images,
            aspect_ratio=aspect,
            image_size=size,
        )

    # Determine output filename
    output_path = args.output
    correct_ext = extension_from_mime(mime_type)

    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"image_{timestamp}{correct_ext}"
    else:
        current_ext = Path(output_path).suffix.lower()
        if current_ext != correct_ext:
            output_path = str(Path(output_path).with_suffix("")) + correct_ext
            print(f"\nInfo: API returned {mime_type} format, adjusted output to: {output_path}")

    # Write file
    try:
        Path(output_path).write_bytes(image_data)
    except OSError as e:
        raise RuntimeError(f"failed to write output file: {e}") from e

    print(f"\nImage saved to: {output_path}")


def main() -> None:
    """Entry point that handles errors."""
    try:
        run()
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
