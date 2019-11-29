#!/usr/bin/env bash
set -e
python -m pip install --upgrade twine cibuildwheel
CIBW_BEFORE_BUILD='python -m pip install -r requirements.txt'
CIBW_BUILD=$(python -c 'import sys; print("cp" + "".join(map(str, sys.version_info[:2])) + "-*")')
cibuildwheel --output-dir dist
