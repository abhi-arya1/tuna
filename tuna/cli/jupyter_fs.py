import nbformat as nbf
import paramiko
import subprocess
import time 
import psutil 
import sys 
from tuna.cli.util import clear_terminal, log
from tuna.cli.constants import TUNA_DIR, CROSS_ICON, WARNING_ICON, LOADING_ICON, INFO_ICON
from pathlib import Path 


STARTUP_SCRIPT_PATH = Path.home() / 'startup.sh'
PID_FILE_PATH = Path.home() / 'jupyter_lab.pid'
def get_startup_script(username):
    return f"""
#!/bin/bash

# Exit on any error
set -e

# Update and install Python 3.12 and JupyterLab
sudo apt update 
sudo apt upgrade -y
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.12 python3-pip
pip install jupyterlab

# Update PATH
echo 'export PATH=$PATH:/home/{username}/.local/bin' >> ~/.bashrc
source ~/.bashrc

# Start JupyterLab in the background and capture the PID
nohup jupyter lab > jupyter_lab.log 2>&1 &
echo $! > {PID_FILE_PATH}

# Wait a few seconds to ensure JupyterLab has started
sleep 5

# Retrieve the token from the log file
TOKEN=$(grep -oP 'token=\\K\\S+' jupyter_lab.log)

# Print the token
echo $TOKEN
"""


def start_lab(browser: bool): 
    print(f"[{LOADING_ICON} Starting TunaLab...")
    command = ['jupyter', 'lab'] if browser else ['jupyter', 'lab', '--no-browser']
    process = subprocess.Popen(command, cwd=(TUNA_DIR), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process


def monitor_lab(process): 
    clear_terminal()
    log(INFO_ICON, "Running TunaLab on \033[1mhttp://localhost:8888/lab/tree/tuna.ipynb\033[0m")
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
    log(CROSS_ICON, "Ended TunaLab") 
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()




token, pid = get_jupyter_token_and_pid()
if not token:
    print("Failed to retrieve Jupyter token.")
else:
    # Set up the SSH tunnel
    tunnel_process = setup_ssh_tunnel()
    
    # Wait a bit to ensure the tunnel is established
    time.sleep(5)
    
    # Print the connection URL and PID
    print(f'http://localhost:{LOCAL_PORT}/lab?token={token}')
    print(f'JupyterLab PID: {pid}')

    # Keep the script running to maintain the tunnel
    try:
        tunnel_process.wait()
    except KeyboardInterrupt:
        tunnel_process.terminate()
        print("\nSSH tunnel closed.")




def connect_lab(instance, api_key, ssh_file): 
    username = instance["username"]
    port = instance["ssh_port"]
    hostname = instance["ip_address"]

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, key_filename=str(ssh_file))

    sftp = client.open_sftp()
    with sftp.file(STARTUP_SCRIPT_PATH, 'w') as f:
        f.write(get_startup_script(username))
    sftp.chmod(STARTUP_SCRIPT_PATH, 0o755)
    sftp.close()

    stdin, stdout, stderr = client.exec_command(f'bash {STARTUP_SCRIPT_PATH}')
    token = stdout.read().decode().strip()

    print(token)
    
    sftp = client.open_sftp()
    with sftp.file(PID_FILE_PATH, 'r') as f:
        remote_pid = f.read().strip()
    sftp.close()
    
    client.close()

    tunnel_command = [
        'ssh',
        '-N',
        '-L', f'localhost:8888:localhost:8888',
        f'{username}@{hostname}'
    ]
    local_process = subprocess.Popen(tunnel_command)








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

