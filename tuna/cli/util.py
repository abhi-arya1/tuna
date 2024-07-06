import os

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def log(icon: str, message: str): 
    print(f"[{icon}] {message}")