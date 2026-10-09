#!/usr/bin/env bash
# Pre-push preflight. The fleet-global pre-push hook runs this script when the
# repository ships it. It is the toolchains-standard gate: it fails the push when
# a declared toolchain version is outdated against the latest upstream release.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

status=0
report="$(python3 .agents/standards/toolchains/scripts/check_toolchain_versions.py)" || status=$?
if [ "$status" -ne 0 ]; then
  printf '%s\n' "$report" >&2
  exit "$status"
fi
