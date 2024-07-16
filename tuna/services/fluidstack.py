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
from tuna.util.general import log
from tuna.cli.core.constants import WARNING_ICON, CHECK_ICON, CROSS_ICON, \
    INFO_ICON, SSH_KEY, FluidstackState



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




def existing_or_new_trainer() -> bool:
    """
    Prompts the user to select an existing training dataset or create a new one.

    Returns:
        bool: True if the user selects an existing training dataset, False otherwise
    """
    # pylint: disable=line-too-long
    questions = [
        inquirer.List('trainer',
                    message="Would you like to use an existing FluidStack instance, or run a new one?",
                    choices=["Existing", "New"]
                    )
    ]
    answers = inquirer.prompt(questions)
    return answers['trainer'] == "Existing"




def stop_instance(api_key: str, instance_id: str):
    """
    Stops the FluidStack instance with the specified ID.

    Args:
        api_key (str): The FluidStack API Key provided by the User
        instance_id (str): The ID of the instance to stop
    """
    res = requests.put(f"https://platform.fluidstack.io/instances/{instance_id}/stop",
        headers={"api-key": api_key}
    )
    if res.status_code == 200:
        log(CHECK_ICON,
            f"Instance with ID {instance_id} stopping on https://dashboard.fluidstack.io")
    else:
        log(CROSS_ICON, f"Failed to stop Fluidstack instance with ID {instance_id} | {res.json()}")




def get_instances(api_key: str) -> list[dict]:
    """
    Fetches the list of instances running on FluidStack.

    Args:
        api_key (str): The FluidStack API Key provided by the User

    Returns:
        list[dict]: The list of instances running on FluidStack
    """
    res = requests.get("https://platform.fluidstack.io/instances",
        headers={"api-key": api_key}
    )
    instances = res.json()
    return instances




def get_instance_by_id(instance_id: str, instances: list[dict]) -> dict:
    """
    Fetches the instance by ID from the list of instances.

    Args:
        api_key (str): The FluidStack API Key provided by the User
        instance_id (str): The ID of the instance to fetch
        instances (list[dict]): The list of instances running on FluidStack

    Returns:
        dict: The instance with the specified ID
    """
    for instance in instances:
        if instance["id"] == instance_id:
            return instance
    raise ValueError(f"Instance with ID {instance_id} not found")





# pylint: disable=too-many-locals
# pylint: disable=line-too-long
def spin_new_instance(api_key: str, selected_gpu: dict) -> dict:
    """
    Spins up a FluidStack instance with the selected GPU configuration.

    Args:
        api_key (str): The FluidStack API Key provided by the User
        selected_gpu (dict): The selected GPU configuration via FluidStack API

    Returns: 
        dict: The instance that was spun up
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

    est_time = selected_gpu.get('estimated_provisioning_time_minutes', 5)
    est_time_secs = est_time * 60
    tickspeed = 20
    # pylint: disable=line-too-long
    spinner = Halo(text=f"Spinning up instance '{name}' with {selected_gpu['gpu_type'].replace('_', ' ')} GPU...", spinner='dots')
    spinner.start()

    for remaining_seconds in range(est_time_secs, 0, -tickspeed):
        spinner.text = f'Allocating instance {name} with {selected_gpu['gpu_type'].replace('_', ' ')}... ({round(remaining_seconds / 60, 2)} minutes remaining)'
        instances = get_instances(api_key)
        instance = get_instance_by_id(instance_id, instances)

        if instance["status"] == FluidstackState.RUNNING.value:
            spinner.succeed(f'Spun up instance {name} with {selected_gpu["gpu_type"].replace("_", " ")} GPU successfully!')
            break

        time.sleep(tickspeed)
    else:
        spinner.fail(f"Instance failed to start within {est_time} minutes. Details: {instance}")

    table_data = [
        [instance["name"], selected_gpu["gpu_type"], "Ubuntu 22.04 LTS Nvidia"]
        for instance in [instance]
    ]

    headers = ["Name", "GPU", "OS"]
    print(tabulate(table_data, headers, tablefmt="pretty"))

    return instance




def spin_existing_instance(api_key: str, instance: dict) -> dict:
    """
    Spins up an instance that's in the user's FluidStack account. 

    Args:
        api_key (str): The FluidStack API Key provided by the User
        instance (dict): The instance to load up

    Returns: 
        dict: The instance that was spun up
    """
    status = instance["status"]

    if status == FluidstackState.RUNNING.value:
        log(CHECK_ICON, f"Instance '{instance['name']}' is running!")
        return instance

    if status == FluidstackState.PENDING.value:
        instance_id = instance["id"]
        est_time = instance["configuration"]["estimated_provisioning_time_minutes"]
        est_time_secs = est_time * 60
        tickspeed = 15

        spinner = Halo(text=f"Waiting for '{instance['name']} to start up...", spinner='dots')
        spinner.start()

        for remaining_seconds in range(est_time_secs, 0, -tickspeed):
            spinner.text = f"Waiting for '{instance['name']}' to start up... ({round(remaining_seconds / 60, 2)} minutes remaining)"
            instances = get_instances(api_key)
            instance = get_instance_by_id(instance_id, instances)

            if instance["status"] == FluidstackState.RUNNING.value:
                spinner.succeed(f'Spun up instance \'{instance['name']}\' successfully!')
                break

            time.sleep(tickspeed)
        else:
            spinner.fail(f"Instance failed to start within {est_time} minutes. Details: {instance}")
            exit(1)

        return instance

    if status == FluidstackState.STOPPED.value:
        res = requests.put(f"https://platform.fluidstack.io/instances/{instance['id']}/start",
            headers={"api-key": api_key}
        )
        if res.status_code == 200:
            log(CHECK_ICON, f"Started instance '{instance['name']}' successfully!")
            return instance

        message = res.json()
        log(WARNING_ICON, f"Failed to start instance '{instance['name']}': {message}. Run 'tuna fluidstack --manage' to fix this.")
        exit(0)


    log(CROSS_ICON, f"Instance '{instance['name']}' is in an invalid 'tuna' state: {status}. Run 'tuna fluidstack --manage' to fix this.")
    exit(0)
