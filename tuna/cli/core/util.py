"""

Utility functions for the CLI.

"""

import os
import glob
import json
import subprocess
from pathlib import Path
from tuna.cli.core.constants import BLUE, RESET, RED, WARNING_ICON, REMOTE_CFG


def clear_terminal():
    """
    Clears the terminal screen.
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')




def log(icon: str, message: str):
    """
    Logs a message with an icon to the terminal.
    """
    if icon == WARNING_ICON:
        print(f"{RED}[{icon}]{RESET} {message}")
    else:
        print(f"{BLUE}[{icon}]{RESET} {message}")





def write_remote(username: str, hostname: str, ssh_path: str, port: int=22):
    """
    Logs remote configuration 
    """
    with open(REMOTE_CFG, 'w', encoding="utf-8") as j:
        json.dump({
            "username": username,
            "hostname": hostname,
            "ssh_path": ssh_path,
            "port": port
        }, j, indent=4)




# pylint: disable=too-many-arguments
# pylint: disable=line-too-long
def remote_sync(local_path: Path, remote_path: Path, username: str, hostname: str, port: int):
    """
    Copy a directory to a remote machine using SFTP.

    Args:
        local_path (str): The path to the local directory to copy.
        remote_path (str): The path to the destination directory on the remote machine.
        username (str): The username for the remote machine.
        hostname (str): The hostname or IP address of the remote machine.
        port (int): The port to connect to on the remote machine.
        key_filename (str): The path to the private key file for SSH authentication.
    """

    local_files = glob.glob(os.path.join(str(local_path), "*"))
    scp_command = [
        "scp",
        "-r",
        "-v",
        "-P", str(port),
    ] + local_files + [f"{username}@{hostname}:{remote_path}"]

    try:
        print(f"[TUNA] Syncing Files from {str(local_path)}")
        subprocess.run(scp_command, check=True, text=True, capture_output=True)
        print(f"[TUNA] Sync Successful to ~/tunalab from {str(local_path)}")
    except subprocess.CalledProcessError as e:
        print("[TUNA] Sync Error Occurred")
        print(e.stderr)
