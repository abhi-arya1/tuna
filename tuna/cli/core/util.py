"""

Utility functions for the CLI.

"""
import os
from tuna.cli.core.constants import BLUE, RESET, RED, WARNING_ICON


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
