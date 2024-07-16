"""

JupyterLab Instance Utilities for Tuna

This module contains utility functions for managing JupyterLab instances
for the Tuna CLI.

"""

# pylint: disable=line-too-long

import sys
import time
import curses
import subprocess
import threading
import itertools
from threading import Thread
from pathlib import Path
import paramiko
import psutil
from watchdog.observers import Observer
from tuna.util.general import log, sync_to_remote
from tuna.cli.core.watchfiles import LabWatcher

# pylint: disable=unused-import
from tuna.services.clouds.fluidstack import stop_instance
from tuna.cli.core.authenticator import validate_ip

from tuna.cli.core.scripts import FLUIDSTACK_CONFIGURATION_SCRIPT, SYNC_WITH_LOCAL_SCRIPT
from tuna.cli.core.constants import TUNA_DIR, INFO_ICON, CHECK_ICON, \
    CURSOR_UP_ONE, ERASE_LINE, DARK_GRAY, PURPLE, RESET, SPINNER_DOTS, BLUE, \
    STARTUP_SCRIPT_PATH, JUPYTER_PID_PATH, TOKEN_FILE_PATH, R_TUNA_DIR, LOCAL_DAEMON_TAG, \
    REMOTE_DAEMON_TAG, SYNC_SCRIPT_PATH, WATCHFILES_PID_PATH



def start_lab(browser: bool) -> subprocess.Popen:
    """
    Start JupyterLab in the `.tuna` parent directory. 

    Args: 
        browser (bool): Whether to open the lab in the default browser.

    Returns: 
        subprocess.Popen: The process object for the JupyterLab instance.
    """
    print(">>> Starting TunaLab...")
    time.sleep(1.5)
    command = ['jupyter', 'lab', "--LabApp.token=''"] if browser else ['jupyter', 'lab', "--LabApp.token=''", '--no-browser']
    # pylint: disable=consider-using-with
    process = subprocess.Popen(
            command,
            cwd=(TUNA_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    return process



# pylint: disable=too-many-arguments
def monitor_lab(process: subprocess.Popen, token: str="", username: str="", hostname: str="", port: int=22) -> None:
    """
    Monitor the CPU and Memory usage of the JupyterLab instance on the local machine.

    Args:
        process (subprocess.Popen): The process object for the JupyterLab instance.
        token (str): The token for the JupyterLab instance. Defaults to "" for Local Runs 
        watch_directory (str): The directory to watch for file changes.
        watch_command (str): The command to run when a file change is detected.
    """
    def watch_files():
        def on_change():
            sync_to_remote(TUNA_DIR, R_TUNA_DIR, username, hostname, port)

        event_handler = LabWatcher(function=on_change)
        observer = Observer()
        observer.schedule(event_handler, TUNA_DIR, recursive=True)
        observer.start()
        observer.join()

    def draw_screen(stdscr):
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(True)  # Make getch() non-blocking
        stdscr.clear()

        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

        bold = curses.A_BOLD
        pl = " " * 3
        if token == "":
            log_message = f"{pl}Running TunaLab on http://localhost:8888/lab"
        else:
            log_message = f"{pl}Running TunaLab on http://localhost:8888/lab?token={token}"

        stdscr.addstr(0, 0, "")
        stdscr.addstr(1, 0, log_message, bold)
        stdscr.addstr(2, 0, f"{pl}Type CTRL+C to end lab. Monitoring CPU and Memory usage...", bold)

        p = psutil.Process(process.pid)

        if token:
            watch_thread = threading.Thread(target=watch_files)
            watch_thread.daemon = True
            log(INFO_ICON, f"[{LOCAL_DAEMON_TAG}] Starting to watch for changes in {TUNA_DIR}")
            watch_thread.start()

        while True:
            stdscr.refresh()
            if p.is_running():
                cpu_usage = p.cpu_percent(interval=1)
                memory_usage = p.memory_info().rss / (1024 * 1024)

                cpu_color = curses.color_pair(1) if cpu_usage > 50 else curses.color_pair(3)
                mem_color = curses.color_pair(1) if memory_usage > 50 * 1024 else curses.color_pair(3)

                stdscr.addstr(4, 0, f"{pl}>>> CPU Usage: {cpu_usage}% ", cpu_color)
                stdscr.addstr(5, 0, f"{pl}>>> Memory Usage: {memory_usage} MB\n\n", mem_color)
                stdscr.clrtoeol()

                if stdscr.getch() == ord('q'):
                    break
            time.sleep(5)


    curses.wrapper(draw_screen)



def kill_lab(process: subprocess.Popen) -> None:
    """
    Kills the JupyterLab instance on the local machine and ends the TunaLab session.

    Args:
        process (subprocess.Popen): The process object for the JupyterLab instance
    """
    log(CHECK_ICON, "Ended Local TunaLab Server, Goodbye...")
    process.terminate()
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        process.kill()




def _tunalab_spinner_thread(stop: 'any') -> None:
    """
    UI Spinner Function for TunaLab Configuration 
    
    - Do not call outside of `jupyter.py`   
    """
    spinner = itertools.cycle(SPINNER_DOTS)
    while not stop():
        sys.stdout.write(f'\r{PURPLE}{next(spinner)}{RESET} Configuring TunaLab for Training...')
        sys.stdout.flush()
        time.sleep(0.1)





def connect_local_lab() -> None:
    """
    Connects a Local JupyterLab Instance for seamless remote development with 
    the dataset and files generated with Tuna, in `.tuna`

    Keeps the lab running for compute until it is manually stopped by the user.
    """
    process = start_lab(browser=False)
    monitor_lab(process)
    kill_lab(process)




# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=unused-argument
def connect_lab(api_key: str, instance: dict, ssh_file: Path) -> None:
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

    local_hostname, local_ip = validate_ip()

    # Connect and set up remote machine configuration
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, key_filename=str(ssh_file))
    client.exec_command(f"touch {STARTUP_SCRIPT_PATH(username)}")
    client.exec_command(f"touch {JUPYTER_PID_PATH(username)}")
    client.exec_command(f"touch {SYNC_SCRIPT_PATH(username)}")

    # Configure Remote Scripts
    sftp = client.open_sftp()
    with sftp.file(STARTUP_SCRIPT_PATH(username), 'w') as f:
        f.write(FLUIDSTACK_CONFIGURATION_SCRIPT(username))
    sftp.chmod(STARTUP_SCRIPT_PATH(username), 0o755)

    with sftp.file(SYNC_SCRIPT_PATH(username), 'w') as f:
        f.write(SYNC_WITH_LOCAL_SCRIPT(username, local_hostname, local_ip))
    sftp.chmod(SYNC_SCRIPT_PATH(username), 0o755)

    sftp.close()


    # Execute setup scripts on remote machine and log output to command line
    print(f"{BLUE}[{INFO_ICON} Tuna Builder] Log via {username}@{hostname}:{port} --> {RESET}")

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
    with sftp.file(JUPYTER_PID_PATH(username), 'r') as f, \
            sftp.file(TOKEN_FILE_PATH(username), 'r') as g:
        remote_pid = f.read().strip().decode('utf-8')
        remote_token = g.read().strip().decode('utf-8').split(" ")[0]

    sftp.close()


    # Tunnel Remote Compute to Local Machine
    tunnel_command = [
        'ssh',
        '-N',
        '-L', 'localhost:8888:localhost:8888',
        f'{username}@{hostname}'
    ]

    # JupyterLab Local Instance forwarded to Remote Compute
    # pylint: disable=consider-using-with
    local_process = subprocess.Popen(tunnel_command)

    try:
        # Run initial sync, start monitoring lab instance
        sync_to_remote(TUNA_DIR, R_TUNA_DIR, username, hostname, port)
        monitor_lab(local_process,
                    token=remote_token,
                    username=username,
                    hostname=hostname,
                    port=port
                )
    except KeyboardInterrupt:
        _, stdout, _ = client.exec_command(f"sudo kill -9 {remote_pid}")
        log(REMOTE_DAEMON_TAG, "Remote Tuna Server ended.")

        _, stdout, _ = client.exec_command(f"python3 {SYNC_SCRIPT_PATH(username)}")
        log(REMOTE_DAEMON_TAG, "Files synced back to local. All remote processes complete.")

        log(LOCAL_DAEMON_TAG, f"Daemon processes ended. No longer watching files in {TUNA_DIR}.")
        log(INFO_ICON, "Your GPU instance has not been ended on Fluidstack. Visit https://dashboard.fluidstack.io/ or run 'tuna fluidstack --manage' to manage instances.")
        kill_lab(local_process)
        client.close()
