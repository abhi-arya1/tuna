import inquirer
from tabulate import tabulate
import requests
from tuna.cli.util import log 
from tuna.cli.constants import CHECK_ICON, CROSS_ICON, INFO_ICON
from subprocess import run
from pathlib import Path

SSH_KEY = Path.home() / '.ssh' / 'id_rsa.pub'

def select_gpu(api_key: str): 
    res = requests.get("https://platform.fluidstack.io/list_available_configurations", headers={"api-key": api_key})
    gpu_options = res.json()

    table_data = [
        [gpu["gpu_type"].replace('_', ' '), f"${gpu['price_per_gpu_hr']}", gpu["estimated_provisioning_time_minutes"], gpu["gpu_counts"]]
        for gpu in gpu_options
    ]

    headers = ["GPU Type", "$ per GPU/hr (USD)", "Load Time (min)", "# Simultaenous GPUs Available"]
    print(tabulate(table_data, headers, tablefmt="pretty"))
    log(INFO_ICON, "Data provided by FluidStack (https://fluidstack.io)")

    choices = [
        f"{gpu['gpu_type'].replace('_', ' ')} - ${gpu['price_per_gpu_hr']} per GPU/hr"
        for gpu in gpu_options
    ]

    questions = [
        inquirer.List('gpu',
                    message="Select an available GPU option",
                    choices=choices)
    ]

    answers = inquirer.prompt(questions)

    selected_option = next(gpu for gpu in gpu_options if f"{gpu['gpu_type'].replace('_', ' ')} - ${gpu['price_per_gpu_hr']} per GPU/hr" == answers['gpu'])
    log(CHECK_ICON, f"Selected GPU: {selected_option['gpu_type'].replace('_', ' ')}")
    return selected_option



def check_ssh_key(): 
    if not SSH_KEY.exists():
        log(CROSS_ICON, "No SSH key found. Please make an RSA PublicKey at `~/.ssh/id_rsa.pub` and put it in your FluidStack account.")
        exit(1)
    else: 
        with open(SSH_KEY, 'r') as f:
            ssh_key = f.read()
            return ssh_key


def spin_instance(api_key: str, selected_gpu: dict):
    questions = [
        inquirer.Text('instance_name', message="Enter an instance name")
    ]
    answers = inquirer.prompt(questions)
    name = answers['instance_name']

    key = check_ssh_key()

    res = requests.post("https://platform.fluidstack.io/instances", 
            headers={
                "api-key": api_key,
                "Content-Type": "application/json"
            },
            json={
                "gpu_type": selected_gpu['gpu_type'],
                "name": name,
                "ssh_key": key
            }
        )
    instance = res.json()
    
    try: 
        _ = instance["id"]
    except KeyError:
        try: 
            log(CROSS_ICON, f"Failed to spin up instance: {instance['message']} | Details: {instance["details"]}")
        except KeyError: 
            log(CROSS_ICON, f"Failed to spin up instance: {instance['message']} | Data: {instance["data"]}")
        exit(1)

    log(INFO_ICON, f"Spinning up instance '{name}' with {selected_gpu['gpu_type'].replace('_', ' ')} GPU...")
    table_data = [
        [instance["id"], instance["name"], instance["gpu_type"], instance["operating_system_label"]]
        for instance in [instance]
    ]

    headers = ["ID", "Name", "GPU", "OS"]
    print(tabulate(table_data, headers, tablefmt="pretty"))
