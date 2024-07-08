import inquirer
import requests
import time
import paramiko
from tabulate import tabulate
from halo import Halo
from tuna.cli.util import log 
from tuna.cli.constants import CHECK_ICON, CROSS_ICON, INFO_ICON
from tuna.cli.jupyter_fs import connect_lab
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

    questions = [
        inquirer.List('#gpus', 
            message="How many GPUs would you like to use?",
            choices=[str(i) for i in selected_option['gpu_counts']]
        )
    ]

    answers = inquirer.prompt(questions)
    selected_option['gpu_count'] = int(answers['#gpus'])

    log(CHECK_ICON, f"Selected GPU: {selected_option['gpu_type'].replace('_', ' ')}")
    return selected_option



def check_ssh_key(api_key): 
    spinner = Halo(text="Creating SSH Link", spinner="dots")
    spinner.start()
    try: 
        if not SSH_KEY.exists():
            log(CROSS_ICON, "No SSH key found. Please make an RSA PublicKey at `~/.ssh/id_rsa.pub` and put it in your FluidStack account.")
            exit(1)
        else: 
            with open(SSH_KEY, 'r') as f:
                ssh_key = f.read()
        
        res = requests.get('https://platform.fluidstack.io/ssh_keys', headers={
            "api-key": api_key
        })
        keys = res.json()
        if "TunaKey" in [key['name'] for key in keys]:
            spinner.succeed("SSH Key Verified")
            return "TunaKey"
        else: 
            res = requests.post('https://platform.fluidstack.io/ssh_keys', headers={
                "api-key": api_key,
                "Content-Type": "application/json"
            }, json={
                "name": "TunaKey",
                "public_key": ssh_key
            })
            key = res.json()
            spinner.succeed("SSH Key 'TunaKey' created successfully in your FluidStack account")
            return key['name']
    except requests.exceptions.RequestException as e:
        spinner.fail(f"Failed to create SSH key: {e}")
        exit(1)



def spin_instance(api_key: str, selected_gpu: dict):
    questions = [
        inquirer.Text('instance_name', message="Enter an instance name")
    ]
    answers = inquirer.prompt(questions)
    name = answers['instance_name']

    key = check_ssh_key(api_key)

    res = requests.post("https://platform.fluidstack.io/instances", 
            headers={
                "api-key": api_key,
                "Content-Type": "application/json"
            },
            json={
                "gpu_type": selected_gpu['gpu_type'],
                "name": name,
                "ssh_key": key, 
                "operating_system_label": "ubuntu_22_04_lts_nvidia",
                "gpu_count": selected_gpu['gpu_count'],
            }
        )
    instance = res.json()
    
    try: 
        instance_id = instance["id"]
    except KeyError:
        try: 
            log(CROSS_ICON, f"Failed to spin up instance: {instance['message']} | Details: {instance["details"]}")
        except KeyError: 
            log(CROSS_ICON, f"Failed to spin up instance: {instance['message']} | Data: {instance["data"]}")
        exit(1)

    estimated_time = selected_gpu.get('estimated_provisioning_time_minutes', 5) 
    spinner = Halo(text=f"Spinning up instance '{name}' with {selected_gpu['gpu_type'].replace('_', ' ')} GPU...", spinner='dots')
    spinner.start()

    # Convert estimated time to seconds for the loop
    estimated_time_seconds = estimated_time * 60

    for remaining_seconds in range(estimated_time_seconds, 0, -20):
        remaining_minutes = remaining_seconds // 60
        spinner.text = f'Provisioning instance... ({remaining_minutes} minutes remaining)'

        status_response = requests.get("https://platform.fluidstack.io/instances",
                                    headers={"api-key": api_key})
        instances = status_response.json()

        this_instance = None 
        instance_status = None
        for inst in instances:
            if inst["id"] == instance_id:
                this_instance = inst
                instance_status = inst["status"]
                break

        if instance_status == "running":
            spinner.succeed('Instance is running!')
            instance = this_instance
            break

        time.sleep(20)
    else:
        spinner.fail(f"Instance failed to start within {estimated_time} minutes. Details: {this_instance}")

    table_data = [
        [instance["id"], instance["name"], selected_gpu["gpu_type"], "Ubuntu 22.04 LTS Nvidia"]
        for instance in [instance]
    ]

    headers = ["ID", "Name", "GPU", "OS"]
    print(tabulate(table_data, headers, tablefmt="pretty"))

    connect_lab(instance, api_key, SSH_KEY)

    
