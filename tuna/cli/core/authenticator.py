"""

Authenticator and API Key manager for Tuna CLI

"""

import json
import os
import inquirer
from tuna.cli.core.constants import CONFIG_FILE, WARNING_ICON
from tuna.cli.core.util import log


# pylint: disable=line-too-long
def load_credentials() -> tuple[str, str] | tuple[None, None]:
    """
    Loads GitHub Credentials from the Tuna Configuration File.

    Returns:
        tuple[str, str] | tuple[None, None]: The GitHub Username and Token if available, else `tuple[None, None]`
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding="utf-8") as f:
            data = json.load(f)
            return data.get('username'), data.get('token')
    return None, None




def save_credentials(username: str, token: str) -> None:
    """
    Saves GitHub Credentials to the Tuna Configuration File.

    Args:
        username (str): The GitHub Username
        token (str): The GitHub Token
    """
    with open(CONFIG_FILE, 'w', encoding="utf-8") as f:
        json.dump({
            'message': 'DO NOT DELETE -- If this gets deleted, run `tuna init` again.',
            'username': username, 
            'token': token
        }, f, indent=4)




def authenticate() -> tuple[str, str]:
    """
    Authenticates the User with GitHub.

    Returns:
        tuple[str, str]: The GitHub Username and Token
    """
    username, token = load_credentials()
    if not username or not token:
        # pylint: disable=line-too-long
        questions = [
            inquirer.Text('username', message="Enter your GitHub username"),
            inquirer.Password('token', message="Enter your GitHub token (requires username and all repo permissions)")
        ]
        answers = inquirer.prompt(questions)
        username = answers['username']
        token = answers['token']
        save_credentials(username, token)

    return username, token




def validate() -> None:
    """
    Validates the presence of `.tuna` in the directory.
    """
    username, token = load_credentials()
    if not username or not token:
        log(WARNING_ICON, "You haven't initialized Tuna yet. Run `tuna init` to start")
        # pylint: disable=consider-using-sys-exit
        exit(1)




def validate_fluidstack() -> str:
    """
    Validates the presence of the FluidStack API Key in the Configuration File.

    Returns:
        str: The FluidStack API Key
    """
    with open(CONFIG_FILE, 'r', encoding="utf-8") as f:
        data = json.load(f)
        api_key = data.get('fs_api_key', None)
    if not api_key:
        questions = [
            # pylint: disable=line-too-long
            inquirer.Password('api_key', message="Enter your FluidStack API Key (https://www.fluidstack.io/)")
        ]
        answer = inquirer.prompt(questions)
        api_key = answer['api_key']
        with open(CONFIG_FILE, 'w', encoding="utf-8") as f:
            data['fs_api_key'] = api_key
            json.dump(data, f, indent=4)
    return api_key
