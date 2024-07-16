"""

Purge command for Tuna CLI

"""

import os
from shutil import rmtree
import inquirer
from tuna.util.general import log
from tuna.cli.core.constants import INFO_ICON, TUNA_DIR, RED, RESET, WARNING_ICON


def purge() -> None:
    """
    Remove the `.tuna` directory from the current directory.
    """
    # pylint: disable=line-too-long
    if os.path.exists(TUNA_DIR):
        questions = [
            inquirer.Confirm("confirm", message=f"{RED}{WARNING_ICON} Are you sure you want to purge Tuna from this directory?{RESET}")
        ]

        answers = inquirer.prompt(questions)
        if not answers["confirm"]:
            log(INFO_ICON, "Purge aborted")
            return
        rmtree(TUNA_DIR)
        log(INFO_ICON, "Tuna has been purged from your current directory")
    else:
        log(INFO_ICON, "Tuna is not initialized in this directory")
