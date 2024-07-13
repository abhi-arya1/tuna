#!/bin/bash

###################################

# This script builds and uploads the package to PyPI
# It assumes that ~/.pypirc is configured with the PyPI credentials, 
# and will do nothing but build the project to `dist/` if it is not.

# Do not attempt to use unless you are an authorized maintainer.

# All Pull Requests that change the `dist` folder will be rejected.

###################################

set -e # Exit on error

rm dist/* # Clean up the dist folder

python3 -m build # Build the package

python3 -m twine upload --repository pypi dist/* # Upload the package to PyPI (https://pypi.org/project/tuna-cli/)