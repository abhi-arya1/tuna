"""

Authenticator and API Key manager for Tuna CLI

"""

import os
import json
import socket
import inquirer
from tuna.cli.core.constants import AUTH_FILE, WARNING_ICON, BOLD, RESET, ITALIC, INFO_ICON
from tuna.util.general import log


# pylint: disable=line-too-long
def load_credentials() -> tuple[str, str] | tuple[None, None]:
    """
    Loads GitHub Credentials from the Tuna Configuration File.

    Returns:
        tuple[str, str] | tuple[None, None]: The GitHub Username and Token if available, else `tuple[None, None]`
    """
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, 'r', encoding="utf-8") as f:
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
    with open(AUTH_FILE, 'w', encoding="utf-8") as f:
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




def validate_fs() -> str:
    """
    Validates the presence of the FluidStack API Key in the Configuration File.

    Returns:
        str: The FluidStack API Key
    """
    with open(AUTH_FILE, 'r', encoding="utf-8") as f:
        data = json.load(f)
        api_key = data.get('fs_api_key', None)
    if not api_key:
        try:
            questions = [
                # pylint: disable=line-too-long
                inquirer.Password('api_key', message="Enter your FluidStack API Key (https://www.fluidstack.io/)")
            ]
            answer = inquirer.prompt(questions)
            api_key = answer['api_key']
            with open(AUTH_FILE, 'w', encoding="utf-8") as f:
                data['fs_api_key'] = api_key
                json.dump(data, f, indent=4)
        except TypeError: 
            log(WARNING_ICON, "Cloud tuna training requires a FluidStack API Key, but more services are coming soon!")
            exit(1)
    return api_key




def validate_hf() -> str:
    """
    Validates the presence of the Hugging Face API Key in the Configuration File.

    Returns:
        str: The Hugging Face API Key
    """
    with open(AUTH_FILE, 'r', encoding="utf-8") as f:
        data = json.load(f)
        api_key = data.get('hf_api_key', None)
    if not api_key:
        try: 
            log(INFO_ICON, "Training requires a HuggingFace API Key (https://huggingface.co/settings/tokens).")
            questions = [
                inquirer.Password('api_key', message=f"Enter ^^^^ here, with {BOLD}{ITALIC}Write{RESET} access enabled")
            ]
            answer = inquirer.prompt(questions)
            api_key = answer['api_key']
            with open(AUTH_FILE, 'w', encoding="utf-8") as f:
                data['hf_api_key'] = api_key
                json.dump(data, f, indent=4)
        except TypeError:
            log(WARNING_ICON, "Rerun `tuna train` once you make your API key")
            exit(1)
    return api_key




def validate_ip() -> tuple[str, str]:
    """
    Gets the user's IP address and hostname for SSH connections, 
    and allows reverse sync with remote machines. 

    Returns:
        tuple[str, str]: The User's IP Address and Hostname in the format "hostname", "ip_address"
    """
    hostname = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('1.1.1.1', 1))
        ip_address = s.getsockname()[0]
        # pylint: disable=all
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    with open(AUTH_FILE, 'r', encoding='utf-8') as f: 
        data = json.load(f) 
    with open(AUTH_FILE, 'w', encoding='utf-8') as f:
        data['user__ip_addr'] = ip_address
        data['user_hostname'] = hostname
        json.dump(data, f, indent=4)

    return hostname, ip_address
