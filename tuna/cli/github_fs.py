"""

GitHub File System Manager for Tuna CLI

"""


import requests
import inquirer
import json
import mimetypes
from halo import Halo
from tuna.cli.constants import REPO_FILE, EXCLUDED_EXTENSIONS, EXCLUDED_FILENAMES, CONFIG_FILE, CHECK_ICON
from tuna.cli.util import log


class GitHubFile:
    def __init__(self, name, path, url, is_directory=False): 
        self._name: str = name
        self._path = path
        self._url = url
        self._content = None
        self._is_directory = is_directory
        self._children = []

    def name(self): 
        return self._name

    def path(self):
        return self._path

    def url(self): 
        return self._url
    
    def content(self):
        if self._name.lower().endswith(EXCLUDED_EXTENSIONS) or self._name.lower() in EXCLUDED_FILENAMES:
            return mimetypes.guess_type(self._name)[0] or ''
        if self._content is None and not self._is_directory:
            response = requests.get(self._url)
            response.raise_for_status()
            self._content = response.text
        return self._content
    
    def add_child(self, child):
        if self._is_directory:
            self._children.append(child)

    def list_children(self):
        return self._children

    def is_directory(self):
        return self._is_directory
    





class GitHubProject: 
    def __init__(self, name, url): 
        self._url = url
        self._name = name 
        self._branches = []
        self._files = []

    def url(self): 
        return self._url
    
    def name(self):
        return self._name
    
    def add_branch(self, branch_name):
        self._branches.append(branch_name)

    def add_file(self, file: GitHubFile):
        self._files.append(file)

    def list_files(self):
        return [file.name() for file in self._files]

    def list_branches(self):
        return self._branches






def fetch_repos(username, token):
    url = f"https://api.github.com/search/repositories?q=user:{username}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['items']




def fetch_files(username, repo, token, path=''):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    contents_url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
    response = requests.get(contents_url, headers=headers)
    
    if not response.ok:
        raise Exception(f"Error fetching repo contents: {response.status_text}")

    return response.json()




def fetch_directory(username, repo, token, path=''):
    items = fetch_files(username, repo, token, path)
    directory = []

    for item in items:
        if item['type'] == 'file':
            file = GitHubFile(name=item['name'], path=item['path'], url=item['download_url'])
            directory.append(file)
        elif item['type'] == 'dir':
            dir_item = GitHubFile(name=item['name'], path=item['path'], url=item['url'], is_directory=True)
            children = fetch_directory(username, repo, token, item['path'])
            for child in children:
                dir_item.add_child(child)
            directory.append(dir_item)

    return directory



def reload():
    with open(CONFIG_FILE, 'r') as f:
        auth_data = json.load(f)
        username = auth_data['username']
        token = auth_data['token']
        repo_url = auth_data['repo_url']
        repo_name = repo_url.split('/')[-1]

    project = GitHubProject(name=repo_name, url=repo_url)
    
    spinner = Halo(text='Fetching files', spinner='dots')
    spinner.start()
    try: 
        try:
            directory = fetch_directory(username, repo_name, token)
            for item in directory:
                project.add_file(item)
            spinner.succeed('Files fetched successfully!')
        except Exception as e:
            spinner.fail(f'File load error: {str(e)}')

        spinner = Halo(text='Building configurations', spinner='dots')
        spinner.start()

        try:
            def build_structure(files):
                structure = []
                for file in files:
                    if file.is_directory():
                        structure.append({
                            "filename": file.name(),
                            "filepath": file.path(),
                            "file_url": file.url(),
                            "directory": True,
                            "children": build_structure(file.list_children())
                        })
                    else:
                        structure.append({
                            "filename": file.name(),
                            "filepath": file.path(),
                            "file_url": file.url(),
                            "directory": False,
                            "content": file.content()
                        })
                return structure

            repo_data: dict = {
                "repository_name": repo_name,
                "html_url": repo_url,
                "files": build_structure(project._files)
            }

            with open(REPO_FILE, 'w') as f: 
                json.dump(repo_data, f, indent=4)
            spinner.succeed('Built configurations successfully!')
        except Exception as e:
            spinner.fail(f'Configuration load error: {str(e)}')
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch repositories: {e}")




def fetch(username, token) -> dict:
    try:
        repos = fetch_repos(username, token)

        repo_question = [
            inquirer.List('repo', message="Choose a repository", choices=[repo['name'] for repo in repos])
        ]
        repo_answer = inquirer.prompt(repo_question)
        selected_repo_name = repo_answer['repo']
        selected_repo_url = [repo['html_url'] for repo in repos if repo['name'] == selected_repo_name][0]

        print(f"\033[92m\u2714 \033[1mSelected Project:\033[0m \033[92m{selected_repo_url}\033[0m")
        
        with open(CONFIG_FILE, 'w') as f: 
            json.dump({
            'message': 'DO NOT DELETE -- If this gets deleted, run `tuna init` again.',
            'username': username, 
            'token': token,
            'repo_url': selected_repo_url
        }, f, indent=4)

        reload()

        log(CHECK_ICON, f"Project '{selected_repo_name}' initialized successfully in the '/.tuna' directory!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch repositories: {e}")


