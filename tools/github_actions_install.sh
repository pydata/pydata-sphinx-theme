#!/bin/bash

# First arg ($1) is the extras_require to install, optional second arg
# ($2) is an extra dependency (currently just nox on one run)
set -eo pipefail
export PYTHONUTF8=1
if [[ "$SPHINX_VERSION" == "rls" ]]; then
    SPHINX_INSTALL="sphinx[test]"
elif [[ "$SPHINX_VERSION" == "dev" ]]; then
    SPHINX_INSTALL="sphinx[test]@https://codeload.github.com/sphinx-doc/sphinx/zip/refs/heads/master"
elif [[ "$SPHINX_VERSION" == "old" ]]; then
    SPHINX_INSTALL="sphinx[test]==6.1.0"
else  # for the "build site" jobs
    SPHINX_INSTALL="sphinx<7.3"
fi
set -x  # print commands
python -m pip install --upgrade pip wheel setuptools
python -m pip install -e .["$1"] ${SPHINX_INSTALL} $2
