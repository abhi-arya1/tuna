from pathlib import Path 
from os import getcwd

CWD = Path(getcwd())

HELLO = """
🎣 Welcome to Tuna

Commands: 
    tuna --init : Initialize Tuna in your current directory
    tuna --serve : Run Tuna in JupyterLab
    tuna --refresh : Refresh GitHub cache in your current directory 
    tuna --edit : Edit the Tuna notebook in your current directory
    tuna : Redisplay this message

Help : Contact support@opennote.me

Happy Tun(a)ing! 🎣
"""

TUNA_DIR = CWD / '.tuna'
NOTEBOOK = TUNA_DIR / 'tuna.ipynb'
CONFIG_FILE = TUNA_DIR / 'tuna.config.json'
AUTH_FILE = TUNA_DIR / 'auth.config.json'


IPYNB_REQUIREMENTS = """
transformers
datasets
peft
trl
python-dotenv
"""