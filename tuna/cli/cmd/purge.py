"""

Purge command for Tuna CLI

"""

import os
from shutil import rmtree
from tuna.cli.core.util import log
from tuna.cli.core.constants import INFO_ICON, TUNA_DIR


def purge() -> None:
    """
    Remove the `.tuna` directory from the current directory.
    """
    if os.path.exists(TUNA_DIR):
        rmtree(TUNA_DIR)
        log(INFO_ICON, "Tuna has been purged from your current directory")
    else:
        log(INFO_ICON, "Tuna is not initialized in this directory")
