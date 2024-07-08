import nbformat as nbf
import paramiko
import subprocess
import time 
import psutil 
import sys 
from tuna.cli.util import clear_terminal, log
from tuna.cli.constants import TUNA_DIR, WARNING_ICON, LOADING_ICON, INFO_ICON, CHECK_ICON
from halo import Halo
from rich.console import Console
from rich.live import Live
from rich.text import Text

console = Console()

STARTUP_SCRIPT_PATH = lambda username: f'/home/{username}/startup.sh'
PID_FILE_PATH = lambda username: f'/home/{username}/jupyter_lab.pid'
TOKEN_FILE_PATH = lambda username: f'/home/{username}/jupyter_token.txt'  
STARTUP_SCRIPT_CONTENT = lambda username: f"""
#!/bin/bash

# Exit on any error
set -e

if ! command -v python3.12 &> /dev/null; then
    echo "Configuring for TunaLab"

    sudo apt update 
    sudo apt upgrade -y
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install -y python3.12 python3-pip

    pip install jupyterlab
    mkdir tunalab
else
    echo "Tuna Configured, Starting Up..."
fi

# Update PATH
export PATH=$PATH:/home/{username}/.local/bin
echo 'export PATH=$PATH:/home/{username}/.local/bin' >> ~/.bashrc
source ~/.bashrc

# Enter TunaLab 
cd tunalab

# Start JupyterLab in the background and capture the PID
nohup jupyter lab --no-browser --port=8888 > jupyter_lab.log 2>&1 &
echo $! > {PID_FILE_PATH(username)}

# Wait a few seconds to ensure JupyterLab has started
sleep 5

# Retrieve the token from the log file
TOKEN=$(grep -oP 'token=\\K[a-f0-9]+' jupyter_lab.log)

# Print the token
echo $TOKEN > {TOKEN_FILE_PATH(username)}
"""


def start_lab(browser: bool): 
    print(f"[{LOADING_ICON} Starting TunaLab...")
    command = ['jupyter', 'lab'] if browser else ['jupyter', 'lab', '--no-browser']
    process = subprocess.Popen(command, cwd=(TUNA_DIR), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process


def monitor_lab(process, token=""): 
    # clear_terminal()
    if token == "": 
        log(INFO_ICON, f"Running TunaLab on \033[1mhttp://localhost:8888/lab\033[0m")
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
                
                sys.stdout.write(f"[{cpu_icon}] CPU Usage: {cpu_color}{cpu_usage}%\033[0m\n[{mem_icon}] Memory Usage: {mem_color}{memory_usage} MB\033[0m\n\n")
                sys.stdout.flush()
                sys.stdout.flush()

            time.sleep(5)
    except psutil.NoSuchProcess:
        pass


def kill_lab(process):
    log(CHECK_ICON, "Ended TunaLab, Goodbye") 
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()



def connect_lab(instance, ssh_file): 
    spinner = Halo(text="Configuring instance for Tuna", spinner="dots")
    spinner.start()

    username = instance["username"]
    port = instance["ssh_port"]
    hostname =  instance["ip_address"]

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

    _, stdout, _ = client.exec_command(f'bash {STARTUP_SCRIPT_PATH(username)}')
    lines = []
    with Live(Text("", style="grey"), refresh_per_second=4) as live:
        for line in iter(stdout.readline, ""):
            lines.append(line.strip())
            if len(lines) > 5:
                lines.pop(0)
            live.update(Text("\n".join(lines), style="grey"))
    
    sftp = client.open_sftp()
    with sftp.file(PID_FILE_PATH(username), 'r') as f, sftp.file(TOKEN_FILE_PATH(username), 'r') as g:
        remote_pid = f.read().strip().decode('utf-8')
        remote_token = g.read().strip().decode('utf-8').split(" ")[0]
        print(remote_pid, remote_token)
    sftp.close()

    tunnel_command = [
        'ssh',
        '-N',
        '-L', f'localhost:8888:localhost:8888',
        f'{username}@{hostname}'
    ]

    spinner.succeed(f"Connected to instance: '{username}@{hostname}' Starting Lab now...")

    local_process = subprocess.Popen(tunnel_command)

    try:
        monitor_lab(local_process, token=remote_token)
    except KeyboardInterrupt:
        _, stdout, _ = client.exec_command(f"sudo kill -9 {remote_pid}")
        print(stdout)
        kill_lab(local_process)
        client.close()

    



def add_md_cell(notebook_path, content):
    if notebook_path.exists():
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbf.read(f, as_version=4)
    else:
        nb = nbf.v4.new_notebook()

    new_cell = nbf.v4.new_markdown_cell(content)

    nb.cells.append(new_cell)

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)


        

def add_code_cell(notebook_path, content):
    if notebook_path.exists():
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbf.read(f, as_version=4)
    else:
        nb = nbf.v4.new_notebook()

    new_cell = nbf.v4.new_code_cell(content)

    nb.cells.append(new_cell)

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)