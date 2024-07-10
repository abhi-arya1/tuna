"""

Bash Scripts for running Remote TunaLab instances on FluidStack GPU Machines

Requires: 
    Ubuntu 22.04 LTS Nvidia 

Usage: 
    DO NOT RUN LOCALLY

"""

# pylint: disable=unnecessary-lambda-assignment
from tuna.cli.core.constants import PID_FILE_PATH, TOKEN_FILE_PATH


FLUIDSTACK_CONFIGURATION_SCRIPT = lambda username: f"""
#!/bin/bash

# Exit on any error
set -e

if ! command -v python3.12 &> /dev/null; then
    echo "Configuring for TunaLab"

    sudo apt update 
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install -y python3.12 python3-pip

    pip install jupyterlab
    mkdir tunalab
else
    echo "Tuna Configured, Starting Up..."
fi

# Update PATH
export PATH=$PATH:/home/{username}/.local/bin
echo 'export PATH=$PATH:/home/{username}/.local/bin' >> ~/.bashrc
source ~/.bashrc

# Enter TunaLab 
cd tunalab

# Start JupyterLab in the background and capture the PID
nohup jupyter lab --no-browser --port=8888 > jupyter_lab.log 2>&1 &
echo $! > {PID_FILE_PATH(username)}

# Wait a few seconds to ensure JupyterLab has started
sleep 5

# Retrieve the token from the log file
TOKEN=$(grep -oP 'token=\\K[a-f0-9]+' jupyter_lab.log)

# Print the token
echo $TOKEN > {TOKEN_FILE_PATH(username)}
"""
