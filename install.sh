#!/bin/sh

set -x

pip install --upgrade pip

pip uninstall --yes antlr4-tools
pip install antlr4-tools

pip uninstall --yes antlr4-python3-runtime
pip install antlr4-python3-runtime
