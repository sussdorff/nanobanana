"""Interactive setup wizard for first-time configuration."""

import sys

from nanobanana.config import VALID_ASPECT_RATIOS, VALID_SIZES, write_config


def _prompt_choice(prompt: str, options: list[str], default: str) -> str:
    """Ask user to pick from a list. Returns the chosen value."""
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        marker = " (default)" if opt == default else ""
        print(f"  {i}. {opt}{marker}")

    while True:
        raw = input(f"Choice [default: {default}]: ").strip()
        if not raw:
            return default
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        if raw in options:
            return raw
        print(f"  Invalid choice. Enter 1-{len(options)} or one of: {', '.join(options)}")


def _prompt_string(prompt: str, default: str = "") -> str:
    """Ask for a free-text string with an optional default."""
    suffix = f" [default: {default}]" if default else ""
    raw = input(f"\n{prompt}{suffix}: ").strip()
    return raw or default


def run_setup() -> None:
    """Run the interactive setup wizard."""
    if not sys.stdin.isatty():
        raise RuntimeError(
            "setup requires an interactive terminal\n"
            "Run: nanobanana setup"
        )

    print("nanobanana setup")
    print("=" * 40)
    print("This will create a configuration file so you can start generating images.")

    # 1. API backend
    api = _prompt_choice(
        "Which API backend?",
        ["gemini", "openrouter"],
        default="gemini",
    )

    # 2. API key source
    key_source = _prompt_choice(
        "How do you want to provide your API key?",
        ["paste", "key_command", "env"],
        default="paste",
    )

    config: dict = {"api": api}
    api_key_value = ""

    if key_source == "paste":
        env_name = "GEMINI_API_KEY" if api == "gemini" else "OPENROUTER_API_KEY"
        api_key_value = _prompt_string(
            f"Paste your {env_name.replace('_', ' ').title()}"
        )
        if not api_key_value:
            print("\n  Warning: No API key provided. You can add it later by editing the config file.")
        else:
            config["api_key"] = api_key_value

    elif key_source == "key_command":
        key_cmd = _prompt_string(
            "Shell command that returns your API key (e.g. op read 'op://vault/item/field')"
        )
        if key_cmd:
            config["key_command"] = key_cmd
        else:
            print("\n  Warning: No key command provided. You can add it later.")

    elif key_source == "env":
        env_name = "GEMINI_API_KEY" if api == "gemini" else "OPENROUTER_API_KEY"
        print(f"\n  Set the {env_name} environment variable before running nanobanana.")
        print(f"  Example: export {env_name}='your-key-here'")

    # 3. Default aspect ratio
    sorted_ratios = sorted(VALID_ASPECT_RATIOS)
    aspect = _prompt_choice(
        "Default aspect ratio?",
        sorted_ratios,
        default="1:1",
    )
    if aspect != "1:1":
        config["aspect"] = aspect

    # 4. Default size
    sorted_sizes = sorted(VALID_SIZES)
    size = _prompt_choice(
        "Default image size?",
        sorted_sizes,
        default="1K",
    )
    if size != "1K":
        config["size"] = size

    # Write config
    import json
    config_path = write_config(config)

    print(f"\nConfig written to: {config_path}")
    print(f"\n{json.dumps(config, indent=2)}")

    print("\nNext steps:")
    if key_source == "env":
        env_name = "GEMINI_API_KEY" if api == "gemini" else "OPENROUTER_API_KEY"
        print(f"  1. export {env_name}='your-key-here'")
        print(f'  2. nanobanana "a cute cat"')
    else:
        print(f'  nanobanana "a cute cat"')
