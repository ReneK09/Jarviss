#!/usr/bin/env bash
# Stamp a new build id into football/index.html so running apps pick up the update.
set -euo pipefail
cd "$(dirname "$0")/.."
build=$(date -u +%Y-%m-%dT%H:%M)
sed -i -E "s/^const APP_BUILD = '[^']*';/const APP_BUILD = '${build}';/" index.html
grep -n "^const APP_BUILD" index.html
