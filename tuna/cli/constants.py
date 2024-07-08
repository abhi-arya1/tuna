# pylint: disable=unnecessary-lambda-assignment
"""

Constants used in the Tuna CLI

"""

from pathlib import Path
from os import getcwd


################################################
# Tuna-Generated Directory Constants

CWD = Path(getcwd())

TUNA_DIR    = CWD / '.tuna'
NOTEBOOK    = TUNA_DIR / 'tuna.ipynb'
REPO_FILE   = TUNA_DIR / 'tuna.config.json'
CONFIG_FILE = TUNA_DIR / 'auth.config.json'
TRAIN_DATA  = TUNA_DIR / 'train_dataset.jsonl'
EVAL_DATA   = TUNA_DIR / 'eval_dataset.txt'
TEST_DATA   = TUNA_DIR / 'test_dataset.txt'

TUNA_GITIGNORE = """
ipynb_checkpoints/
auth.config.json
"""

IPYNB_REQUIREMENTS = """
transformers
datasets
peft
trl
python-dotenv
"""

################################################
# CLI-Related Constants

# ANSI and UNICODE Constants
CHECK_ICON    = "\u2714"
CROSS_ICON    = "\u2716"
WARNING_ICON  = "\u26A0"
LOADING_ICON  = "\u27F3"
INFO_ICON     = "\u24D8"
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE    = '\x1b[2K'
DARK_GRAY     = '\x1b[90m'
PURPLE        = '\x1b[95m'
BLUE          = '\x1b[34m'
RESET         = '\x1b[0m'
SPINNER_DOTS  = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

# Tuna Welcome Message
HELLO = """
🎣  Welcome to Tuna

Commands can be viewed at : https://github.com/abhi-arya1/tuna

Help : Contact support@opennote.me

Happy Tun(a)ing!  🎣
"""

# Files Ignored by Tuna Trainer
EXCLUDED_EXTENSIONS = (
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', 
    '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', 
    '.csv', '.ico', '.pickle', '.pkl'
)

EXCLUDED_FILENAMES = (
    'license.md', 'license.txt', 'license', 'pipfile', 
    'pipfile.lock', 'package-lock.json', 'outfile'
)

# SSH Configurations
SSH_KEY = Path.home() / '.ssh' / 'id_rsa.pub'

################################################
# Trainer and Remote Development Constants

# FluidStack GPU OS Configuration
STARTUP_SCRIPT_PATH    = lambda username: f'/home/{username}/startup.sh'
PID_FILE_PATH          = lambda username: f'/home/{username}/jupyter_lab.pid'
TOKEN_FILE_PATH        = lambda username: f'/home/{username}/jupyter_token.txt'
STARTUP_SCRIPT_CONTENT = lambda username: f"""
#!/bin/bash

# Exit on any error
set -e

if ! command -v python3.12 &> /dev/null; then
    echo "Configuring for TunaLab"

    sudo apt update 
    sudo apt upgrade -y
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
