#!/bin/bash
if [[ -z "$VIRTUAL_ENV" ]]; then
  echo "Activating the virtual environment and rerunning..."
  uv run "$SHELL" "$0" "$@"
  exit $?
fi

set -e

yapf -ir -vv src
pytype src
