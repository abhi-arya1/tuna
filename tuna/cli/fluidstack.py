# pylint: disable=consider-using-sys-exit
# pylint: disable=missing-timeout
"""

FluidStack API Utilities for Tuna

This module contains utility functions for managing FluidStack instances and GPUs
for the Tuna CLI.

"""

import time
import inquirer
import requests
from tabulate import tabulate
from halo import Halo
from tuna.cli.util import log
from tuna.cli.constants import CHECK_ICON, CROSS_ICON, INFO_ICON, SSH_KEY
from tuna.cli.jupyter_fs import connect_lab


def select_gpu(api_key: str) -> dict:
    """
    Selects a GPU from the available options on FluidStack.

    Args:
        api_key (str): The FluidStack API Key provided by the User
    
    Returns:
        dict: The selected GPU configuration via FluidStack API
    """
    # pylint: disable=missing-timeout
    # Get available GPUs on FluidStack
    res = requests.get(
        "https://platform.fluidstack.io/list_available_configurations", 
        headers={"api-key": api_key}
        )
    gpu_options = res.json()

    table_data = [
        [
            gpu["gpu_type"].replace('_', ' '),
            f"${gpu['price_per_gpu_hr']}",
            gpu["estimated_provisioning_time_minutes"],
            gpu["gpu_counts"]
        ]
        for gpu in gpu_options
    ]

    headers = ["GPU Type", "$ per GPU/hr (USD)", "Load Time (min)", "# Simultaenous GPUs Available"]
    print(tabulate(table_data, headers, tablefmt="pretty"))
    log(INFO_ICON, "Data provided by FluidStack (https://fluidstack.io)")


    # Prompt GPU Selection
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
    # pylint: disable=line-too-long
    selected_option = \
        next(gpu for gpu in gpu_options if f"{gpu['gpu_type'].replace('_', ' ')} - ${gpu['price_per_gpu_hr']} per GPU/hr" == answers['gpu'])


    # Get GPU Selection Specifics
    questions = [
        inquirer.List('#gpus',
            message="How many GPUs would you like to use?",
            choices=[str(i) for i in selected_option['gpu_counts']]
        )
    ]

    answers = inquirer.prompt(questions)
    selected_option['gpu_count'] = int(answers['#gpus'])

    # Log and Return Configured GPU Option
    log(CHECK_ICON, f"Selected GPU: {selected_option['gpu_type'].replace('_', ' ')}")
    return selected_option




# pylint: disable=inconsistent-return-statements
def check_ssh_key(api_key) -> str:
    """
    Check if the SSH Key is present in the FluidStack account, and make one if not. 

    Args:
        api_key (str): The FluidStack API Key provided by the User

    Returns:
        str: The name of the SSH Key in the FluidStack account
    """
    spinner = Halo(text="Creating SSH Link", spinner="dots")
    spinner.start()
    try:
        if not SSH_KEY.exists():
            # pylint: disable=line-too-long
            log(CROSS_ICON, "No SSH key found. Please make an RSA PublicKey at `~/.ssh/id_rsa.pub` and put it in your FluidStack account.")
            exit(1)
        else:
            with open(SSH_KEY, 'r', encoding="utf-8") as f:
                ssh_key = f.read()

        res = requests.get('https://platform.fluidstack.io/ssh_keys', headers={
            "api-key": api_key
        })
        keys = res.json()
        if "TunaKey" in [key['name'] for key in keys]:
            spinner.succeed("SSH Key Verified")
            return "TunaKey"

        res = requests.post('https://platform.fluidstack.io/ssh_keys', headers={
            "api-key": api_key,
            "Content-Type": "application/json"
        }, json={
            "name": "TunaKey",
            "public_key": ssh_key
        })
        spinner.succeed("SSH Key 'TunaKey' created successfully in your FluidStack account")
        return "TunaKey"
    except requests.exceptions.RequestException as e:
        spinner.fail(f"Failed to create SSH key: {e}")
        exit(1)




# pylint: disable=too-many-locals
def spin_instance(api_key: str, selected_gpu: dict) -> None:
    """
    Spins up a FluidStack instance with the selected GPU configuration.

    Args:
        api_key (str): The FluidStack API Key provided by the User
        selected_gpu (dict): The selected GPU configuration via FluidStack API

    Connects and runs the Remote Instance for tuning immediately after provisioning.
    """
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
            # pylint: disable=line-too-long
            log(CROSS_ICON,
                f"Failed to spin up instance: {instance['message']} | Details: {instance["details"]}")
        except KeyError:
            log(CROSS_ICON,
                f"Failed to spin up instance: {instance['message']} | Data: {instance["data"]}")
        exit(1)

    estimated_time = selected_gpu.get('estimated_provisioning_time_minutes', 5)
    # pylint: disable=line-too-long
    spinner = Halo(text=f"Spinning up instance '{name}' with {selected_gpu['gpu_type'].replace('_', ' ')} GPU...", spinner='dots')
    spinner.start()

    estimated_time_seconds = estimated_time * 60

    for remaining_seconds in range(estimated_time_seconds, 0, -15):
        remaining_minutes = remaining_seconds // 60
        spinner.text = f'Allocating instance... ({remaining_minutes} minutes remaining)'

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

        time.sleep(15)
    else:
        spinner.fail(f"Instance failed to start within {estimated_time} minutes. Details: {this_instance}")

    table_data = [
        [instance["id"], instance["name"], selected_gpu["gpu_type"], "Ubuntu 22.04 LTS Nvidia"]
        for instance in [instance]
    ]

    headers = ["ID", "Name", "GPU", "OS"]
    print(tabulate(table_data, headers, tablefmt="pretty"))

    connect_lab(instance, SSH_KEY)
