#!/bin/bash
set -e

yapf -ir -vv src
pytype src
