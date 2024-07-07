from pathlib import Path 
from os import getcwd


################################################ 
# Tuna-Generated Directory Constants

CWD = Path(getcwd())

TUNA_DIR = CWD / '.tuna'
NOTEBOOK = TUNA_DIR / 'tuna.ipynb'
REPO_FILE = TUNA_DIR / 'tuna.config.json'
CONFIG_FILE = TUNA_DIR / 'auth.config.json'
TRAIN_DATA = TUNA_DIR / 'train_dataset.jsonl'
EVAL_DATA = TUNA_DIR / 'eval_dataset.txt' 
TEST_DATA = TUNA_DIR / 'test_dataset.txt'

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

CHECK_ICON = "\u2714"  # Check mark
CROSS_ICON = "\u2716"  # Cross mark
WARNING_ICON = "\u26A0"  # Warning sign
LOADING_ICON = "\u27F3" # Loading sign
INFO_ICON = "\u24D8" # Information sign

HELLO = """
🎣  Welcome to Tuna

Commands: 
    ⋅ tuna init : Initialize Tuna in your current directory

    ⋅ tuna serve : Run Tuna in JupyterLab, no automatic browser opening
        ⋅ tuna serve --open : Same as above with automatic browser opening
        ⋅ tuna serve --no-open : Same as "tuna serve"

    ⋅ tuna refresh : Refresh GitHub cache in your current directory

    ⋅ tuna train : Begin training your model on the code with a powerful rented GPU
        ⋅ tuna train --local : Begin training your model on local hardware (Requires an NVIDIA GPU)

    ⋅ tuna github (or) tuna help (or) tuna docs : Open the Tuna GitHub Repository in the browser

    ⋅ tuna purge : (USE WITH CAUTION) Purge the '.tuna' folder from your current directory

    ⋅ tuna : Redisplay this message

Help : Contact support@opennote.me

Happy Tun(a)ing!  🎣
"""


EXCLUDED_EXTENSIONS = (
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', 
    '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', 
    '.csv', '.ico', '.pickle', '.pkl'
)

EXCLUDED_FILENAMES = (
    'license.md', 'license.txt', 'license', 'pipfile', 
    'pipfile.lock', 'package-lock.json', 'outfile'
)