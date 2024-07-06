import nbformat as nbf
import subprocess
import time 
import psutil 
import sys 
from .util import clear_terminal, log
from .constants import TUNA_DIR, CROSS_ICON, WARNING_ICON, LOADING_ICON, INFO_ICON


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

