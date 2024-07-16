"""

Bash and Python Scripts for running Remote TunaLab instances on FluidStack GPU Machines

Requires: 
    Ubuntu 22.04 LTS Nvidia 

Usage: 
    DO NOT RUN LOCALLY

"""

# pylint: disable=unnecessary-lambda-assignment
from tuna.cli.core.constants import JUPYTER_PID_PATH, TOKEN_FILE_PATH, R_TUNA_DIR, \
    TUNA_DIR, REMOTE_DAEMON_TAG


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
    
    mkdir {R_TUNA_DIR}
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
echo $! > {JUPYTER_PID_PATH(username)}

# Wait a few seconds to ensure JupyterLab has started
sleep 5

# Retrieve the token from the log file
TOKEN=$(grep -oP 'token=\\K[a-f0-9]+' tuna_remote.log)

# Print the token
echo $TOKEN > {TOKEN_FILE_PATH(username)}
"""





# pylint: disable=line-too-long
SYNC_WITH_LOCAL_SCRIPT = lambda remote_username, local_username, ip: f"""

import os
import glob 
import subprocess

def sync_to_remote():
    remote_files = glob.glob(os.path.join('{R_TUNA_DIR}, "*"))
    scp_command = [
        "scp",
        "-r",
        "-v",
    ] + remote_files + [f"{local_username}@{ip}:{TUNA_DIR}"]

    try:
        print("[{REMOTE_DAEMON_TAG}] Syncing edits back from {R_TUNA_DIR}")
        subprocess.run(scp_command, check=True, text=True, capture_output=True)
        print("[{REMOTE_DAEMON_TAG}] Sync Successful to {local_username}@{ip}:{TUNA_DIR} from {R_TUNA_DIR}")
    except subprocess.CalledProcessError as e:
        print("[{REMOTE_DAEMON_TAG}] Sync Error Occurred")
        print(e.stderr)

sync_to_remote()
"""
