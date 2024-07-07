from tuna.cli.github_fs import fetch, reload
from tuna.cli.datasets import build_dataset
from tuna.cli.jupyter_fs import start_lab, monitor_lab, kill_lab, add_md_cell, add_code_cell
from tuna.cli.fluidstack import select_gpu, spin_instance
from tuna.cli.util import log 
from tuna.cli.constants import TUNA_DIR, CONFIG_FILE, REPO_FILE, HELLO, \
                            INFO_ICON, WARNING_ICON, CHECK_ICON, NOTEBOOK

import json 
import os 
import inquirer
from webbrowser import open as webopen
from sys import argv
from shutil import rmtree


def load_credentials():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            return data.get('username'), data.get('token')
    return None, None


def save_credentials(username, token):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({
            'message': 'DO NOT DELETE -- If this gets deleted, run `tuna init` again.',
            'username': username, 
            'token': token
        }, f, indent=4)


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



def validate_fluidstack(): 
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
        api_key = data.get('fs_api_key', None)
    if not api_key: 
        questions = [
            inquirer.Password('api_key', message="Enter your FluidStack API Key (https://www.fluidstack.io/)")
        ]
        answer = inquirer.prompt(questions)
        api_key = answer['api_key']
        with open(CONFIG_FILE, 'w') as f: 
            data['fs_api_key'] = api_key
            json.dump(data, f, indent=4)
    return api_key

    


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
    add_md_cell(NOTEBOOK, "# Hello, World!")



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
    reload()
    log(CHECK_ICON, "Refreshed successfully!")




def open_repository(): 
    with open(REPO_FILE, 'r') as f: 
        data = json.load(f)
        webopen(data.get('html_url'))



def train(local=False): 
    validate() 
    api_key = validate_fluidstack()
    gpu = select_gpu(api_key)
    spin_instance(api_key, gpu)



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
        refresh()

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

    elif argv[1] == "--dev": 
        if argv[2] == "dataset":
            build_dataset()
        if argv[2] == "train": 
            train()

    else: 
        log(WARNING_ICON, f"Invalid option '{argv[1]}'. Run 'tuna' for help")
    
    exit(0)



if __name__ == '__main__':
    try: 
        main()
    except Exception as e: 
        print(e)
        exit(1)
