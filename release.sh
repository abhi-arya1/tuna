#!/bin/bash

# This script builds and uploads the package to PyPI
# It assumes that ~/.pypirc is configured with the PyPI credentials, 
# and will do nothing but build the project to `dist/` if it is not.

# Do not attempt to use unless you are an authorized maintainer.

# All Pull Requests that change the `dist` folder will be rejected.

python3 -m build

python3 -m twine upload --repository pypi dist/*