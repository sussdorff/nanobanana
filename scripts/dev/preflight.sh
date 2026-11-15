#!/usr/bin/env bash
# Pre-push preflight. The fleet-global pre-push hook runs this script when the
# repository ships it. It fails the push when a declared toolchain version is
# outdated against the latest upstream release.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

status=0
report="$(ccore toolchains check)" || status=$?
if [ "$status" -ne 0 ]; then
  printf '%s\n' "$report" >&2
  exit "$status"
fi
