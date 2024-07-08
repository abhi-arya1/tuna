"""

Utility functions for the CLI.

"""
import os


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
    print(f"[{icon}] {message}")
