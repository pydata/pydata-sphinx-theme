#!/bin/bash

# First arg ($1) is the extras_require to install, optional second arg
# ($2) is an extra dependency (currently just nox on one run)
set -eo pipefail
export PYTHONUTF8=1
if [[ "$SPHINX_VERSION" == "" ]]; then
    SPHINX_INSTALL=""
elif [[ "$SPHINX_VERSION" == "dev" ]]; then
    SPHINX_INSTALL="https://github.com/sphinx-doc/sphinx"
else
    SPHINX_INSTALL="sphinx==$SPHINX_VERSION"
fi
set -x  # print commands
python -m pip install --upgrade pip wheel setuptools
python -m pip install -e .["$1"] ${SPHINX_INSTALL} $2
