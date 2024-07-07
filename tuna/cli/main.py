from tuna.cli.github_fs import fetch
from tuna.cli.datasets import build_dataset
from tuna.cli.jupyter_fs import start_lab, monitor_lab, kill_lab
from tuna.cli.constants import TUNA_DIR, AUTH_FILE, CONFIG_FILE, HELLO, INFO_ICON, WARNING_ICON
from tuna.cli.util import log 
import json 
import os 
import inquirer
from webbrowser import open as webopen
from sys import argv
from shutil import rmtree
from halo import Halo


def load_credentials():
        if os.path.exists(AUTH_FILE):
            with open(AUTH_FILE, 'r') as f:
                data = json.load(f)
                return data.get('username'), data.get('token')
        return None, None


def save_credentials(username, token):
    with open(AUTH_FILE, 'w') as f:
        json.dump({
            'message': 'This file contains your GitHub credentials. Do not share this file with anyone! If you think your credentials have been compromised, delete this file and run `tuna init` again.',
            'data_usage': 'We do not store this file. You can delete it whenever you want to revoke the Tuna CLI\'s access, and run `tuna init` again to reauthenticate.',
            'username': username, 
            'token': token
        }, f)


def authenticate(): 
    username, token = load_credentials()
    if not username or not token:
        questions = [
            inquirer.Text('username', message="Enter your GitHub username"),
            inquirer.Password('token', message="Enter your GitHub token (requires username and all repo permissions)")
        ]
        answers = inquirer.prompt(questions)
        username = answers['username']
        token = answers['token']
        save_credentials(username, token)
    
    return username, token


def validate(): 
    username, token = load_credentials()
    if not username or not token: 
        log(WARNING_ICON, "You haven't initialized Tuna yet. Run `tuna init` to start")
        exit(1)



def init(): 
    if os.path.exists(TUNA_DIR):
        log(INFO_ICON, "You've already initialized Tuna in this directory! Run `tuna purge` to start fresh.")
        exit(1)
    print(f"[{INFO_ICON}] Let's get started...")
    TUNA_DIR.mkdir(exist_ok=True)
    username, token = load_credentials()
    if not username or not token:
        username, token = authenticate()
        save_credentials(username, token)
    fetch(username, token)



def serve(browser: bool=False): 
    validate()
    lab = start_lab(browser)
    try:
        monitor_lab(lab)
    except KeyboardInterrupt:
        kill_lab(lab)



def refresh(): 
    validate()
    log(INFO_ICON, "Refreshing the Tuna Cache in your current directory")



def open_repository(): 
    with open(CONFIG_FILE, 'r') as f: 
        data = json.load(f)
        webopen(data.get('html_url'))



def purge():
    if os.path.exists(TUNA_DIR):
        rmtree(TUNA_DIR)
        log(INFO_ICON, "Tuna has been purged from your current directory")
    else: 
        log(INFO_ICON, "Tuna is not initialized in this directory")



def main(): 
    if len(argv) == 1: 
        print(HELLO)
        exit(0)

    if argv[1] == "init": 
        init()

    elif argv[1] == "serve":
        if(len(argv)) > 2: 
            if argv[2] == "--open":
                serve(browser=True)
            elif argv[2] == "--no-open":
                serve()
            else: 
                log(WARNING_ICON, f"Invalid flag for 'serve': '{argv[2]}'. Run 'tuna' for help")
        else: 
            serve()

    elif argv[1] == "refresh": 
        validate() 

    elif argv[1] in ["github", "docs", "help"]:
        log(INFO_ICON, "Opening 'https://github.com/abhi-arya1/tuna' in your default browser.")
        webopen("https://github.com/abhi-arya1/tuna")

    elif argv[1] == "browse": 
        validate()
        log(INFO_ICON, "Opening your repository in your default browser.")
        open_repository()

    elif argv[1] == "train":
        if(len(argv)) > 2: 
            if argv[2] == "--local":
                log(INFO_ICON, "Local training coming soon...")
                # train(local=True)
            else: 
                log(WARNING_ICON, f"Invalid flag for 'train': '{argv[2]}'. Run 'tuna' for help")
        else: 
            log(INFO_ICON, "Remote training coming soon...")
            # train(local=False)

    elif argv[1] == "purge":
        purge()

    elif argv[1] == "dev": 
        if argv[2] == "--datasets":
            build_dataset()

    else: 
        log(WARNING_ICON, f"Invalid option '{argv[1]}'. Run 'tuna' for help")
    
    exit(0)



if __name__ == '__main__':
    try: 
        main()
    except Exception as e: 
        print(e)
        exit(1)
