#!/bin/bash
set -ex
python3 src/auto-spacing.py "$@" > auto-spacing.txt
