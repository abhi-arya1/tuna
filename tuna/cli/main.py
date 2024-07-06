from .github_fs import fetch
from .jupyter_fs import start_lab, monitor_lab, kill_lab
from .constants import TUNA_DIR, AUTH_FILE, HELLO
import json 
import os 
import inquirer
from sys import argv


def load_credentials():
        if os.path.exists(AUTH_FILE):
            with open(AUTH_FILE, 'r') as f:
                data = json.load(f)
                return data.get('username'), data.get('token')
        return None, None


def save_credentials(username, token):
    with open(AUTH_FILE, 'w') as f:
        json.dump({
            'message': 'This file contains your GitHub credentials. Do not share this file with anyone! If you think your credentials have been compromised, delete this file and run `tuna --init` again.',
            'data_usage': 'We do not store this file. You can delete it whenever you want to revoke the Tuna CLI\'s access, and run `tuna --init` again to reauthenticate.',
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


def main(): 
    if len(argv) == 1: 
        print(HELLO)
        exit(0)

    if argv[1] == "--init": 
        print("Let's get started...")
        TUNA_DIR.mkdir(exist_ok=True)
        username, token = load_credentials()
        if not username or not token:
            username, token = authenticate()
            save_credentials(username, token)
        repo = fetch(username, token)
        print(repo)

    elif argv[1] == "--serve":
        lab = start_lab()
        try:
            monitor_lab(lab)
        except KeyboardInterrupt:
            kill_lab(lab)

    elif argv[1] == "--refresh": 
        print("Refreshing GitHub cache in your current directory")
    elif argv[1] == "--edit": 
        print("Editing the Tuna notebook in your current directory")
    else: 
        print("Invalid flag. Run 'tuna' for help")
    
    exit(0)



if __name__ == '__main__':
    try: 
        main()
    except Exception as e: 
        print(e)
        exit(1)
