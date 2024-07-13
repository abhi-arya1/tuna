"""

Bash Scripts for running Remote TunaLab instances on FluidStack GPU Machines

Requires: 
    Ubuntu 22.04 LTS Nvidia 

Usage: 
    DO NOT RUN LOCALLY

"""

# pylint: disable=unnecessary-lambda-assignment
from tuna.cli.core.constants import PID_FILE_PATH, TOKEN_FILE_PATH, TUNA_LAB_LOC

# sudo add-apt-repository -y ppa:deadsnakes/ppa
# sudo apt update
# sudo apt install -y python3.12 python3-pip

FLUIDSTACK_CONFIGURATION_SCRIPT = lambda username: f"""
#!/bin/bash

# Exit on any error
set -e

echo "TUNA: Connected to Remote Machine: {username}"

if [ ! -d "tunalab" ]; then
    echo "TUNA: Configuring for TunaLab"

    echo "TUNA: Configuring Python Interpreter"
    sudo apt install -y python3-pip

    echo "TUNA: Installing JupyterLab"
    pip install jupyterlab
    
    mkdir {TUNA_LAB_LOC}
    echo "TUNA: TunaLab Workspace created." 
else
    echo "TUNA: TunaLab Workspace instance exists."
fi

echo "TUNA: Starting TunaLab..."

# Update PATH
export PATH=$PATH:/home/{username}/.local/bin
echo 'export PATH=$PATH:/home/{username}/.local/bin' >> ~/.bashrc
source ~/.bashrc
echo "TUNA: PATH updated."

# Enter TunaLab 
cd tunalab

if [ -e "tuna_remote.log" ]; then
    rm tuna_remote.log
fi
echo "TUNA: Remote logs configured"

# Start JupyterLab in the background and capture the PID
echo "TUNA: Starting JupyterLab..."
nohup jupyter lab --no-browser --port=8888 > tuna_remote.log 2>&1 &
echo $! > {PID_FILE_PATH(username)}

# Wait a few seconds to ensure JupyterLab has started
sleep 5

# Retrieve the token from the log file
TOKEN=$(grep -oP 'token=\\K[a-f0-9]+' tuna_remote.log)

# Print the token
echo $TOKEN > {TOKEN_FILE_PATH(username)}
"""
