"""

Constants used in the Tuna CLI

"""

# pylint: disable=unnecessary-lambda-assignment
from pathlib import Path
from os import getcwd
from enum import Enum
from tuna.version import LATEST_VERSION

# VERSION
VERSION = LATEST_VERSION

################################################
# Tuna-Generated Directory Constants

CWD = Path(getcwd())

TUNA_DIR       = CWD / '.tuna'
NOTEBOOK       = TUNA_DIR / 'tuna.ipynb'
REPO_FILE      = TUNA_DIR / 'tuna.config.json'
AUTH_FILE      = TUNA_DIR / 'auth.config.json'
TRAIN_DATA     = TUNA_DIR / 'train_dataset.jsonl'
EVAL_DATA      = TUNA_DIR / 'eval_dataset.jsonl'
OUTPUT_MODEL   = TUNA_DIR / 'trained_model'
MODEL_ADAPTERS = TUNA_DIR / 'adapters_lora'


# Remote JupyterLab Items
R_TUNA_DIR       = '/home/ubuntu/tunalab'
R_NOTEBOOK       = '/home/ubuntu/tunalab/tuna_remote.ipynb'
R_TUNA_LOG       = '/home/ubuntu/tunalab/tuna_remote.log'
R_REPO_FILE      = '/home/ubuntu/tunalab/tuna.config.json'
R_AUTH_FILE      = '/home/ubuntu/tunalab/auth.config.json'
R_OUTPUT_MODEL   = '/home/ubuntu/tunalab/trained_model'
R_MODEL_ADAPTERS = '/home/ubuntu/tunalab/adapters_lora'
R_TRAIN_DATA     = '/home/ubuntu/tunalab/train_dataset.jsonl'
R_EVAL_DATA      = '/home/ubuntu/tunalab/eval_dataset.jsonl'



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
BOLD          = '\033[1m'
ITALIC        = '\033[3m'
SPINNER_DOTS  = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
CDOT          = "•"


# Daemon Constants
LOCAL_DAEMON_TAG  = "TUNA_LOCAL_D"
REMOTE_DAEMON_TAG = "TUNA_REMOTE_D"


# Daemon Messages
UNDEFINED_BEHV    = f"{RED}[{WARNING_ICON}{BOLD} UNDEFINED BEHAVIOR]{RESET}"
NO_NOTEBOOK       = f"{RED}[{WARNING_ICON}{BOLD} NO NOTEBOOK]{RESET}"
CANCELLED_CMD     = f"{RED}[{WARNING_ICON}{BOLD} CANCELLED CMD]{RESET}"
NOT_IMPLEMENTED   = f"{RED}[{WARNING_ICON}{BOLD} NOT IMPLEMENTED]{RESET}"


# Help Message
HELP  = f"{DARK_GRAY}Run 'tuna [-h | --help] <command>' for help{RESET}"
LEARN = lambda word: f"{DARK_GRAY}Run \'tuna learn {word}\' for more information{RESET}"


# Tuna Welcome Message
HELLO = f"""
🎣 {PURPLE}Welcome to Tuna CLI v{VERSION}!{RESET}

usage:   tuna [-h | --help] <command> [<args>]
version: tuna [-v | --version]

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
# Remote Development Constants

class RemotePlatform(Enum):
    """
    Remote Development Platforms supported by Tuna
    """
    FLUIDSTACK    = "fluidstack"
    AWS           = "aws"           # COMING SOON
    GCP           = "gcp"           # COMING SOON
    AZURE         = "azure"         # COMING SOON
    AKASH         = "akash"         # COMING SOON
    DIGITAL_OCEAN = "digital_ocean" # COMING SOON
    INTEL_CLOUD   = "intel_cloud"   # COMING SOON


# FluidStack GPU Machine States
class FluidstackState(Enum):
    """
    FluidStack GPU Machine States
    """
    RUNNING       = "running"
    PENDING       = "pending"
    UNHEALTHY     = "unhealthy"
    SHUTTING_DOWN = "shutting_down"
    TERMINATED    = "terminated"
    STOPPING      = "stopping"
    STOPPED       = "stopped"



# FluidStack GPU OS Configuration
STARTUP_SCRIPT_PATH    = lambda username: f'/home/{username}/startup.sh'
SYNC_SCRIPT_PATH       = lambda username: f'/home/{username}/watchfiles.py'
JUPYTER_PID_PATH       = lambda username: f'/home/{username}/jupyter_lab.pid'
WATCHFILES_PID_PATH    = lambda username: f'/home/{username}/tuna_daemon.pid'
TOKEN_FILE_PATH        = lambda username: f'/home/{username}/jupyter_token.txt'


################################################
# CLI Command Tokens

class Token(Enum):
    """
    Tokens for Tuna CLI Commands
    """
    # Command Tokens
    INIT           = "init"
    SERVE          = "serve"
    REFRESH        = "refresh"
    GITHUB, DOCS   = "github", "docs"
    BROWSE         = "browse"
    TRAIN          = "train"
    FLUIDSTACK     = "fluidstack"
    PURGE          = "purge"
    DEV            = "dev"
    MAKE           = "make"
    DATASET        = "dataset"
    NOTEBOOK       = "notebook"
    NOTEBOOK_SHORT = "nb"
    DATASET_SHORT  = "ds"
    LEARN          = "learn"
    REPORT_BUG     = "bug"
    CLONE          = "clone"

    # Command Flags
    OPEN           = "--open"
    NO_OPEN        = "--no-open"
    LOCAL          = "--local"
    MANAGE         = "--manage"
    HELP           = "--help"
    HELP_SHORT     = "-h"
    VERSION        = "--version"
    VERSION_SHORT  = "-v"
    FORCE          = "--force"



class TopicTokens(Enum):
    """
    Every technical term mentioned in Tuna can be 
    defined with `tuna learn [word]`. All of those 
    technical terms are shown here.
    """
    # pylint: disable=all
    pass
