"""

GitHub File System Manager for Tuna CLI

This module contains utility functions for managing GitHub repositories and files
for the Tuna CLI.

"""

import json
import mimetypes
import requests
import inquirer
from halo import Halo
from tuna.cli.constants import REPO_FILE, EXCLUDED_EXTENSIONS, \
    EXCLUDED_FILENAMES, CONFIG_FILE, CHECK_ICON
from tuna.cli.util import log



class GitHubFile:
    """
    Class representing a file or directory in a GitHub repository.
    """
    def __init__(self, name: str, path: str, url: str, is_directory: bool=False) -> None:
        self._name = name
        self._path = path
        self._url = url
        self._content = None
        self._is_directory = is_directory
        self._children = []

    def name(self) -> str:
        """Returns the name of the file or directory."""
        return self._name

    def path(self) -> str:
        """Returns the path of the file or directory."""
        return self._path

    def url(self) -> str:
        """Returns the URL of the file."""
        return self._url

    def content(self) -> str:
        """
        Returns the content of the file by requesting the GitHub API, 
        ignoring EXCLUDED_FILENAMES.
        """
        if self._name.lower().endswith(EXCLUDED_EXTENSIONS) or \
                self._name.lower() in EXCLUDED_FILENAMES:
            return mimetypes.guess_type(self._name)[0] or ''
        if self._content is None and not self._is_directory:
            # pylint: disable=missing-timeout
            # pylint: disable=fixme
            # TODO: Fix this hang in the future
            response = requests.get(self._url)
            response.raise_for_status()
            self._content = response.text
        return self._content


    def add_child(self, child: 'GitHubFile') -> None:
        """Adds a child file or directory to the current directory."""
        if self._is_directory:
            self._children.append(child)

    def list_children(self) -> list:
        """Returns a list of children files or directories."""
        return self._children

    def is_directory(self) -> bool:
        """Returns True if the file is a directory."""
        return self._is_directory






class GitHubProject:
    """
    Class representing a GitHub repository in its entirety
    """
    def __init__(self, name: str, url: str) -> None:
        self._url = url
        self._name = name
        self._branches = []
        self.files = []

    def url(self) -> str:
        """Returns the URL of the repository."""
        return self._url

    def name(self) -> str:
        """Returns the name of the repository."""
        return self._name

    def add_branch(self, branch_name) -> None:
        """Adds a branch to the repository"""
        self._branches.append(branch_name)

    def add_file(self, file: GitHubFile) -> None:
        """Adds a file to the repository"""
        self.files.append(file)

    def list_files(self) -> list:
        """Lists all files in the repository"""
        return [file.name() for file in self.files]

    def list_branches(self) -> list:
        """Lists all branches in the repository"""
        return self._branches





def fetch_repos(username, token) -> list:
    """
    Fetches all repositories (public and private) for a given GitHub username.

    Args:
        username (str): The GitHub username.
        token (str): The GitHub personal access token.
    
    Returns:
        list: A list of dictionaries containing repository
    """
    url = f"https://api.github.com/search/repositories?q=user:{username}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    # pylint: disable=missing-timeout
    # pylint: disable=fixme
    # TODO: Fix this hang in the future
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['items']




def fetch_files(username: str, repo: str, token: str, path: str='') -> dict:
    """
    Fetches all files and directories in a GitHub repository.

    Args:
        username (str): The GitHub username.
        repo (str): The GitHub repository name.
        token (str): The GitHub personal access token.
        path (str): The path to the directory. Default=""
    
    Returns:
        dict: A dictionary containing the files and directories in the repository.
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    contents_url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
    # pylint: disable=missing-timeout
    # pylint: disable=fixme
    # TODO: Fix this hang in the future
    response = requests.get(contents_url, headers=headers)

    if not response.ok:
        raise requests.exceptions.RequestException(
            f"Error fetching repo contents: {response.status_text}"
        )

    return response.json()




def fetch_directory(username: str, repo: str, token: str, path: str='') -> list:
    """
    Fetches a directory in a GitHub repository.

    Args:
        username (str): The GitHub username.
        repo (str): The GitHub repository name.
        token (str): The GitHub personal access token.
        path (str): The path to the directory. Default=""
    
    Returns:
        list: A list of GitHubFile objects representing the directory.
    """
    items = fetch_files(username, repo, token, path)
    directory = []

    for item in items:
        if item['type'] == 'file':
            file = GitHubFile(name=item['name'], path=item['path'], url=item['download_url'])
            directory.append(file)
        elif item['type'] == 'dir':
            dir_item = GitHubFile(
                name=item['name'], path=item['path'], url=item['url'], is_directory=True
            )
            children = fetch_directory(username, repo, token, item['path'])
            for child in children:
                dir_item.add_child(child)
            directory.append(dir_item)

    return directory



def reload() -> None:
    """
    Reloads the GitHub configurations for the current `.tuna` project. 
    """
    with open(CONFIG_FILE, 'r', encoding="utf-8") as f:
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
        # pylint: disable=broad-exception-caught
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
                "files": build_structure(project.files)
            }

            with open(REPO_FILE, 'w', encoding="utf-8") as f:
                json.dump(repo_data, f, indent=4)
            spinner.succeed('Built configurations successfully!')
        # pylint: disable=broad-exception-caught
        except Exception as e:
            spinner.fail(f'Configuration load error: {str(e)}')

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch repositories: {e}")




def fetch(username: str, token: str) -> dict:
    """
    Initializes a new `.tuna` GitHub configuration for the user, by 
    prompting for one of their repostiories.

    Args:
        username (str): The GitHub username.
        token (str): The GitHub personal access token.  
    
    Returns:
        dict: A dictionary containing the GitHub configurations to be saved to a Config File
    """
    try:
        repos = fetch_repos(username, token)

        repo_question = [
            inquirer.List(
                'repo', 
                message="Choose a repository",
                choices=[repo['name'] for repo in repos]
            )
        ]
        repo_answer = inquirer.prompt(repo_question)
        selected_repo_name = repo_answer['repo']
        selected_repo_url = \
            [repo['html_url'] for repo in repos if repo['name'] == selected_repo_name][0]

        print(f"\033[92m\u2714 \033[1mSelected Project:\033[0m \033[92m{selected_repo_url}\033[0m")

        with open(CONFIG_FILE, 'w', encoding="utf-8") as f:
            json.dump({
            'message': 'DO NOT DELETE -- If this gets deleted, run `tuna init` again.',
            'username': username, 
            'token': token,
            'repo_url': selected_repo_url
        }, f, indent=4)

        reload()

        log(CHECK_ICON,
            f"Project '{selected_repo_name}' initialized successfully in the '/.tuna' directory!"
        )
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch repositories: {e}")
