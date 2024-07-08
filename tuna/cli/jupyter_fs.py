"""

JupyterLab File System Utilities for Tuna

This module contains utility functions for managing Jupyter Notebooks and JupyterLab instances
for the Tuna CLI.

"""

import subprocess
import sys
import time
import itertools
from threading import Thread
from pathlib import Path
import nbformat as nbf
import paramiko
import psutil
from tuna.cli.util import clear_terminal, log
from tuna.cli.constants import TUNA_DIR, WARNING_ICON, LOADING_ICON, INFO_ICON, CHECK_ICON, \
    CURSOR_UP_ONE, ERASE_LINE, DARK_GRAY, PURPLE, RESET, SPINNER_DOTS, BLUE, \
    STARTUP_SCRIPT_PATH, PID_FILE_PATH, TOKEN_FILE_PATH, STARTUP_SCRIPT_CONTENT



def _get_notebook(notebook_path: Path) -> nbf.notebooknode.NotebookNode:
    """
    Reads a Jupyter Notebook File and returns the NotebookNode object.

    Args:
        notebook_path (pathlib.Path): The path to the Jupyter Notebook file.

    Returns:
        nbf.notebooknode.NotebookNode: The NotebookNode object for the Jupyter Notebook file.
    """
    if notebook_path.exists():
        with open(notebook_path, 'r', encoding='utf-8') as f:
            return nbf.read(f, as_version=4)
    else:
        return nbf.v4.new_notebook()



def add_md_cell(notebook_path: Path, content: str) -> None:
    """
    Adds a Markdown Cell to a Jupyter Notebook File.

    Args:
        notebook_path (pathlib.Path): The path to the Jupyter Notebook file.
        content (str): The content to be added to the Markdown Cell.
    """
    nb = _get_notebook(notebook_path)
    new_cell = nbf.v4.new_markdown_cell(content)
    nb.cells.append(new_cell)

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)




def add_code_cell(notebook_path: Path, content: str) -> None:
    """
    Adds a Code Cell to a Jupyter Notebook File.

    Args:
        notebook_path (pathlib.Path): The path to the Jupyter Notebook file.
        content (str): The content to be added to the Code Cell.
    """
    nb = _get_notebook(notebook_path)
    new_cell = nbf.v4.new_code_cell(content)
    nb.cells.append(new_cell)

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)



def start_lab(browser: bool) -> subprocess.Popen:
    """
    Start JupyterLab in the `.tuna` parent directory. 

    Args: 
        browser (bool): Whether to open the lab in the default browser.

    Returns: 
        subprocess.Popen: The process object for the JupyterLab instance.
    """
    print(f"[{LOADING_ICON}] Starting TunaLab...")
    command = ['jupyter', 'lab'] if browser else ['jupyter', 'lab', '--no-browser']
    # pylint: disable=consider-using-with
    process = subprocess.Popen(
            command,
            cwd=(TUNA_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    return process




def monitor_lab(process: subprocess.Popen, token: str="") -> None:
    """
    Monitor the CPU and Memory usage of the JupyterLab instance on the local machine.

    Args:
        process (subprocess.Popen): The process object for the JupyterLab instance.
        token (str): The token for the JupyterLab instance. Defaults to "" for Local Runs 
    """
    clear_terminal()
    if token == "":
        log(INFO_ICON, "Running TunaLab on \033[1mhttp://localhost:8888/lab\033[0m")
    else:
        log(INFO_ICON, f"Running TunaLab on \033[1mhttp://localhost:8888/lab?token={token}\033[0m")
    log(INFO_ICON, "Type CTRL+C to end lab. Monitoring CPU and Memory usage...\n\n\n\n")

    try:
        p = psutil.Process(process.pid)

        while True:
            if p.is_running():
                cpu_usage = p.cpu_percent(interval=1)
                memory_usage = p.memory_info().rss / (1024 * 1024)

                sys.stdout.write("\033[F\033[F\033[F")
                cpu_color = "\033[91m" if cpu_usage > 50 else "\033[0m"
                mem_color = "\033[91m" if memory_usage > 50 * 1024 else "\033[0m"
                cpu_icon = WARNING_ICON if cpu_usage > 50 else INFO_ICON
                mem_icon = WARNING_ICON if memory_usage > 50 * 1024 else INFO_ICON

                sys.stdout.write(
                    # pylint: disable=line-too-long
                    f"[{cpu_icon}] CPU Usage: {cpu_color}{cpu_usage}%\033[0m\n[{mem_icon}] Memory Usage: {mem_color}{memory_usage} MB\033[0m\n\n")
                sys.stdout.flush()

            time.sleep(5)
    except psutil.NoSuchProcess:
        pass




def kill_lab(process: subprocess.Popen) -> None:
    """
    Kills the JupyterLab instance on the local machine and ends the TunaLab session.

    Args:
        process (subprocess.Popen): The process object for the JupyterLab instance
    """
    log(CHECK_ICON, "Ended TunaLab, Goodbye")
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()




def _tunalab_spinner_thread(stop: 'any') -> None:
    """
    UI Spinner Function for TunaLab Configuration 
    
    - Do not call outside of `jupyter_fs.py`   
    """
    spinner = itertools.cycle(SPINNER_DOTS)
    while not stop():
        sys.stdout.write(f'\r{PURPLE}{next(spinner)}{RESET} Configuring TunaLab for Training...')
        sys.stdout.flush()
        time.sleep(0.1)


# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
def connect_lab(instance: dict, ssh_file: Path) -> None:
    """
    Connects a FluidStack GPU Instance using the User's Local 
    SSH Configuration to a JupyterLab Instance for seamless remote development with 
    the dataset and files generated with Tuna, in `.tuna`

    Args:
        instance (dict): The FluidStack GPU Instance details.
        ssh_file (pathlib.Path): The path to the SSH Key file

    Keeps the lab running for compute until it is manually stopped by the user.
    """
    # Get SSH configuration details
    username = instance["username"]
    port = instance["ssh_port"]
    hostname =  instance["ip_address"]

    print(f"{BLUE}[{INFO_ICON} Tuna Build] Log via {username}@{hostname}:{port} --> {RESET}")


    # Connect and set up remote machine configuration
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, key_filename=str(ssh_file))
    client.exec_command(f"touch {STARTUP_SCRIPT_PATH(username)}")
    client.exec_command(f"touch {PID_FILE_PATH(username)}")

    sftp = client.open_sftp()
    with sftp.file(STARTUP_SCRIPT_PATH(username), 'w') as f:
        f.write(STARTUP_SCRIPT_CONTENT(username))
    sftp.chmod(STARTUP_SCRIPT_PATH(username), 0o755)
    sftp.close()


    # Execute setup scripts on remote machine and log output to command line
    _, stdout, _ = client.exec_command(f'bash {STARTUP_SCRIPT_PATH(username)}')
    stop_spinner = False
    spinner = Thread(target=_tunalab_spinner_thread, args=(lambda: stop_spinner,))
    spinner.start()
    print('\n' * 4)

    lines = []
    try:
        for line in iter(stdout.readline, ""):
            line = line.strip()
            lines.append(line)
            if len(lines) > 5:
                lines.pop(0)

            sys.stdout.write(CURSOR_UP_ONE * 5)

            for _, output_line in enumerate(lines):
                sys.stdout.write(ERASE_LINE)
                sys.stdout.flush()
                print(f"\r{DARK_GRAY}>>> {output_line}{RESET}")
                sys.stdout.flush()

            sys.stdout.write('\n' * (5 - len(lines)))
            sys.stdout.flush()

            time.sleep(0.5)
    finally:
        stop_spinner = True
        spinner.join()

    sys.stdout.write(ERASE_LINE)
    print(f'\r{PURPLE}✔︎{RESET} Configuration Complete! Starting Lab Now...')


    # Get Process and Token for Remote Jupyter Instance
    sftp = client.open_sftp()
    with sftp.file(PID_FILE_PATH(username), 'r') as f, \
            sftp.file(TOKEN_FILE_PATH(username), 'r') as g:
        remote_pid = f.read().strip().decode('utf-8')
        remote_token = g.read().strip().decode('utf-8').split(" ")[0]
        print(remote_pid, remote_token)
    sftp.close()


    # Tunnel Remote Compute to Local Machine
    tunnel_command = [
        'ssh',
        '-N',
        '-L', 'localhost:8888:localhost:8888',
        f'{username}@{hostname}'
    ]


    # Run Local JupyterLab Instance on Remote Compute, and monitor **LOCAL** CPU and Memory Usage
    # until process is ended by the user
    # pylint: disable=consider-using-with
    local_process = subprocess.Popen(tunnel_command)

    try:
        monitor_lab(local_process, token=remote_token)
    except KeyboardInterrupt:
        _, stdout, _ = client.exec_command(f"sudo kill -9 {remote_pid}")
        print(stdout)
        kill_lab(local_process)
        client.close()
