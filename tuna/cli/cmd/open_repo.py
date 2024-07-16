"""

Open a repository in the browser for Tuna CLI

"""

import json
from webbrowser import open as webopen
from tuna.cli.core.constants import REPO_FILE, INFO_ICON
from tuna.cli.core.authenticator import validate
from tuna.util.general import log


def open_repository() -> None:
    """
    Opens the Tuna-initialized GitHub Repository in the default browser.
    """
    validate()
    log(INFO_ICON, "Opening your repository in your default browser.")
    with open(REPO_FILE, 'r', encoding="utf-8") as f:
        data = json.load(f)
        webopen(data.get('html_url'))
