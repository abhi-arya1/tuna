"""

Initialize command for Tuna CLI

"""

import os
from tuna.cli.core.constants import INFO_ICON, TUNA_DIR
from tuna.util.general import log
from tuna.cli.core.authenticator import load_credentials, save_credentials, authenticate
from tuna.services.github import fetch


def make_dir():
    """
    Make the `.tuna` directory in the current directory.
    """
    if os.path.exists(TUNA_DIR):
        # pylint: disable=line-too-long
        # pylint: disable=consider-using-sys-exit
        log(INFO_ICON, "You've already initialized Tuna in this directory! Run `tuna purge` to start fresh.")
        exit(1)
    print(f"[{INFO_ICON}] Let's get started...")
    TUNA_DIR.mkdir(exist_ok=True)




def init() -> None:
    """
    Initialize `.tuna` in the current directory.
    """
    make_dir()
    username, token = load_credentials()
    if not username or not token:
        username, token = authenticate()
        save_credentials(username, token)
    fetch(username, token)
