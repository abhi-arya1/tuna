"""

Initialize command for Tuna CLI

"""

import os
from tuna.cli.core.constants import INFO_ICON, TUNA_DIR, NOTEBOOK
from tuna.cli.core.util import log
from tuna.cli.core.authenticator import load_credentials, save_credentials, authenticate
from tuna.cli.services.github import fetch
from tuna.cli.services.jupyter import add_md_cell


def init() -> None:
    """
    Initialize `.tuna` in the current directory.
    """
    if os.path.exists(TUNA_DIR):
        # pylint: disable=line-too-long
        # pylint: disable=consider-using-sys-exit
        log(INFO_ICON, "You've already initialized Tuna in this directory! Run `tuna purge` to start fresh.")
        exit(1)
    print(f"[{INFO_ICON}] Let's get started...")
    TUNA_DIR.mkdir(exist_ok=True)
    username, token = load_credentials()
    if not username or not token:
        username, token = authenticate()
        save_credentials(username, token)
    fetch(username, token)
    add_md_cell(NOTEBOOK, "# Hello, World!")
