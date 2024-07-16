"""

Refresh command for Tuna CLI

"""

from tuna.cli.core.authenticator import validate
from tuna.services.github import reload
from tuna.util.general import log
from tuna.cli.core.constants import INFO_ICON, CHECK_ICON


def refresh() -> None:
    """
    Refresh the Tuna Cache in the current directory.
    """
    validate()
    log(INFO_ICON, "Refreshing the Tuna Cache in your current directory")
    reload()
    log(CHECK_ICON, "Refreshed successfully!")
