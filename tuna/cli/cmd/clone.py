"""

Clone Functionality for the Tuna CLI

"""

import json
import requests
from tuna.services.github import reload
from tuna.cli.cmd.init import make_dir
from tuna.cli.core.authenticator import load_credentials, save_credentials, authenticate
from tuna.cli.core.constants import AUTH_FILE, INFO_ICON, NOTEBOOK, WARNING_ICON
from tuna.cli.core.learn import NOTEBOOK_CONSTANTS
from tuna.util.general import log

# pylint: disable=consider-using-sys-exit, C0201
# pylint: disable=line-too-long

def clone(url: str) -> None:
    """
    Clone the GitHub repository or Tuna Notebook to the current directory.
    """
    if not url:
        log(WARNING_ICON, "'clone' requires a valid GitHub/Notebook URL or Tuna Notebook name, such as 'tuna clone <url>'")
        exit(1)

    if url.endswith('.ipynb') or url in NOTEBOOK_CONSTANTS.keys():
        if url in NOTEBOOK_CONSTANTS.keys():
            url = NOTEBOOK_CONSTANTS[url]
        log(INFO_ICON, f"Cloning Notebook '{url.split('/')[-1]}'...")
        url = _convert_to_rawgithubusercontent_url(url)
        content = _fetch_notebook(url)
        with open(NOTEBOOK, 'w', encoding="utf-8") as f:
            f.write(content)
    else:
        make_dir()
        username, gh_token = load_credentials()
        if not username or not gh_token:
            username, gh_token = authenticate()
            save_credentials(username, gh_token)

        username = _parse_username_from_github_url(url)

        with open(AUTH_FILE, 'w', encoding="utf-8") as f:
            json.dump({
            'message': 'DO NOT DELETE -- If this gets deleted, run `tuna init` again.',
            'username': username, 
            'token': gh_token,
            'repo_url': url
        }, f, indent=4)

        reload()




def _convert_to_rawgithubusercontent_url(github_url):
    """
    Converts a GitHub URL to a raw.githubusercontent.com URL.
    
    Parameters:
        github_url (str): The GitHub URL to convert.
        
    Returns:
        str: The converted raw.githubusercontent.com URL.
    """
    if not github_url.startswith("https://github.com/"):
        raise ValueError("Invalid GitHub URL")

    url_parts = github_url[len("https://github.com/"):].split('/')

    if len(url_parts) < 5 or url_parts[2] != "blob":
        raise ValueError("Invalid GitHub URL format")

    raw_url_parts = ["https://raw.githubusercontent.com"] + url_parts[:2] + url_parts[3:]

    raw_url = '/'.join(raw_url_parts)

    return raw_url





def _parse_username_from_github_url(github_url):
    """
    Parses the username from a GitHub repository URL and removes the .git suffix if it exists.

    Parameters:
        github_url (str): The GitHub repository URL.

    Returns:
        str: The parsed username.
    """
    if not github_url.startswith("https://github.com/"):
        raise ValueError("Invalid GitHub URL")

    url_parts = github_url[len("https://github.com/"):].split('/')

    if len(url_parts) < 2:
        raise ValueError("Invalid GitHub URL format")

    return url_parts[0].replace(".git", "")




def _fetch_notebook(url):
    """
    Gets the content of a Jupyter Notebook from a GitHub URL.
    """
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.text
