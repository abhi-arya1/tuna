"""

Serve command for Tuna CLI

"""

from tuna.cli.core.authenticator import validate
from tuna.services.jupyter import start_lab, monitor_lab, kill_lab


def serve(browser: bool=False) -> None:
    """
    Serve the Tuna Jupyter Notebook in the Browser.

    Args:
        browser (bool, optional): Whether to open the Notebook in the Browser. Default=False.
    """
    validate()
    lab = start_lab(browser)
    try:
        monitor_lab(lab)
    except KeyboardInterrupt:
        kill_lab(lab)
