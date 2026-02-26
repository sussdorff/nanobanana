# Changelog

All notable changes to nanobanana will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [CalVer](https://calver.org/) versioning (YYYY.0M.MICRO).

## [Unreleased]

### Added

- Add OpenRouter API support
- Add XDG config file support
- Rewrite nanobanana from Go to Python
- Add key_command config for shell-based API key retrieval
- Add subcommands with structured prompt templates
- Add 20 slide subtemplates and refactor skill for progressive disclosure
- Add install.sh for CLI + skill installation
- Rename PyPI package to nanobanana-cli, use trusted publishing
- Add install-skill subcommand for PyPI-based skill distribution
- Add interactive setup wizard for first-time configuration
- Add -open flag to open image after saving
- Add update checker with optional auto_update config
- Add auto_update prompt to setup wizard

### Fixed

- Auto-launch setup wizard on TTY when config is missing
- Use %APPDATA% for config path on Windows
- Use uv tool install --force --refresh for updates (upgrade ignores cache)

