"""

Constants used in the Tuna CLI

"""

# pylint: disable=unnecessary-lambda-assignment
from pathlib import Path
from os import getcwd
from enum import Enum


# VERSION
VERSION = "0.1.4 Release 3 (Beta)"


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

# Help Message
HELP = f"{DARK_GRAY}Run 'tuna [-h | --help] <command>' for help{RESET}"

# Tuna Welcome Message
HELLO = f"""
🎣 {PURPLE}Welcome to Tuna CLI v{VERSION}!{RESET}

usage: tuna [-v | --version] <command> [<args>] [-h | --help]

These are common Tuna commands used in various situations:

{BLUE}start a working area{RESET}
   init        Initialize the Tuna configuration in the current directory
   refresh     Refresh the Tuna cache in the current directory

{BLUE}work on the current change{RESET}
   serve       Serve the Tuna Jupyter Notebook
   browse      Open the Tuna-initialized GitHub repository in the default browser
   train       Set up remote compute training with FluidStack

{BLUE}examine the history and state{RESET}
   github      Open the Tuna GitHub repository in the default browser
   docs        Open the Tuna documentation in the default browser

{BLUE}manage your configuration{RESET}
   purge       Remove the Tuna configuration from the current directory
   fluidstack  Fluidstack Configuration Head for Tuna

{BLUE}advanced{RESET}
   dev         Build a dataset for development purposes

See 'tuna [-h | --help] <command>' for more information on a specific command.

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

# FluidStack GPU Machine States
class FluidstackState(Enum):
    """
    FluidStack GPU Machine States
    """
    RUNNING="running"
    PENDING="pending"
    UNHEALTHY="unhealthy"
    SHUTTING_DOWN="shutting_down"
    TERMINATED="terminated"
    STOPPING="stopping"
    STOPPED="stopped"



# FluidStack GPU OS Configuration
STARTUP_SCRIPT_PATH    = lambda username: f'/home/{username}/startup.sh'
PID_FILE_PATH          = lambda username: f'/home/{username}/jupyter_lab.pid'
TOKEN_FILE_PATH        = lambda username: f'/home/{username}/jupyter_token.txt'





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
    HELP_SHORT = "-h"
    VERSION = "--version"
    VERSION_SHORT = "-v"
