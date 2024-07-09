# pylint: disable=unnecessary-lambda-assignment
"""

Constants used in the Tuna CLI

"""

from pathlib import Path
from os import getcwd
from enum import Enum

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
RED           = '\033[31m'
SPINNER_DOTS  = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

# Tuna Welcome Message
HELLO = f"""
🎣  {BLUE}Welcome to Tuna{RESET}

Commands can be viewed at : https://github.com/abhi-arya1/tuna

Help : Run 'tuna <command> --help', or 'tuna docs'

{BLUE}Happy Tun(a)ing!{RESET}
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

################################################
# CLI Command Tokens

class Token(Enum):
    """
    Tokens for Tuna CLI Commands
    """
    # Command Tokens
    INIT = "init"
    SERVE = "serve"
    REFRESH = "refresh"
    GITHUB, DOCS = "github", "docs"
    BROWSE = "browse"
    TRAIN = "train"
    FLUIDSTACK = "fluidstack"
    PURGE = "purge"
    DEV = "dev"
    DATASET = "dataset"

    # Command Flags
    OPEN = "--open"
    NO_OPEN = "--no-open"
    LOCAL = "--local"
    MANAGE = "--manage"
    HELP = "--help"



# Documentation Dictionary 
COMMANDS_DOCS = {
    "init": f"""
{BLUE}USAGE{RESET}: tuna init
{BLUE}DESCRIPTION{RESET}: Initialize the Tuna configuration in the current directory.

This command sets up the necessary configuration files and folders for using Tuna.
""",

    "serve": f"""
{BLUE}USAGE{RESET}: tuna serve [--open | --no-open]
{BLUE}DESCRIPTION{RESET}: Serve the Tuna Jupyter Notebook.

{BLUE}OPTIONS{RESET}:
    --open: Open the Notebook in the browser automatically.
    --no-open: Do not open the Notebook in the browser.

This command starts a Jupyter Notebook server with the Tuna Notebook.
""",

    "refresh": f"""
{BLUE}USAGE{RESET}: tuna refresh
{BLUE}DESCRIPTION{RESET}: Refresh the Tuna cache in the current directory.

This command updates the cached data used by Tuna from the GitHub repository.
""",

    "github": f"""
{BLUE}USAGE{RESET}: tuna github
{BLUE}DESCRIPTION{RESET}: Open the Tuna GitHub repository in the default browser.

This command opens the Tuna GitHub repository in the default browser.
""",

    "docs": f"""
{BLUE}USAGE{RESET}: tuna docs
{BLUE}DESCRIPTION{RESET}: Open the Tuna documentation in the default browser.

This command opens the Tuna documentation (README) in the default browser.
""",

    "browse": f"""
{BLUE}USAGE{RESET}: tuna browse
{BLUE}DESCRIPTION{RESET}: Open the Tuna-initialized GitHub repository in the default browser.

This command opens the GitHub repository associated with the current Tuna configuration.
""",

    "train": f"""
{BLUE}USAGE{RESET}: tuna train [--local]
{BLUE}DESCRIPTION{RESET}: Set up remote compute training with FluidStack.
{BLUE}OPTIONS{RESET}:
    --local: Train locally instead of using FluidStack.

This command sets up remote compute training with FluidStack, and forwards a powerful Jupyter Instance to your local machine automatically.
""",

    "fluidstack": f"""
{BLUE}USAGE{RESET}: tuna fluidstack
{BLUE}DESCRIPTION{RESET}: Fluidstack Configuration Head for Tuna. 
{BLUE}OPTIONS{RESET}: 
    --manage: Manage Fluidstack Instances on https://dashboard.fluidstack.io

This command allows you to manage your Fluidstack instances, and update/pause/delete instances as needed.
""",

    "purge": f"""
{BLUE}USAGE{RESET}: tuna purge
{BLUE}DESCRIPTION{RESET}: Remove the Tuna configuration from the current directory.

This command deletes the .tuna directory and associated configuration files.
""",

    "dev": f"""
{BLUE}USAGE{RESET}: tuna dev dataset
{BLUE}DESCRIPTION{RESET}: Build a dataset for development purposes.

This command generates a dataset for AI tuning, using the Tuna dataset builder.
"""
}

# Help Message
HELP = f"{DARK_GRAY}Run 'tuna <command> --help' for help{RESET}"
