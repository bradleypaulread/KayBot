#!/bin/sh

# get script directory path
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

. "${DIR}/venv/bin/activate"

python "${DIR}/main.py"
