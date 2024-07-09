"""

SSH Machine Training Setup for Tuna CLI

"""

import inquirer
from tabulate import tabulate
from tuna.cli.core.authenticator import validate, validate_fluidstack
from tuna.cli.core.constants import INFO_ICON, SSH_KEY
from tuna.cli.core.util import log
from tuna.cli.services.fluidstack import get_instances, spin_new_instance, \
    existing_or_new_trainer, select_gpu, spin_existing_instance
from tuna.cli.services.jupyter import connect_lab


def train(local=False) -> None:
    """
    Setup remote compute training with FluidStack.

    Args: 
        local (bool, optional): Whether to train locally. Default=False.
    """
    validate()

    if local:
        log(INFO_ICON, "Local training coming soon...")
        return

    api_key = validate_fluidstack()
    instances = get_instances(api_key)

    if instances and len(instances) != 0:
        use_existing = existing_or_new_trainer()
    else:
        log(INFO_ICON, "No previous instances found. Let's configure a new instance...")
        use_existing = False

    if not instances or len(instances) == 0 or not use_existing:
        gpu = select_gpu(api_key)
        instance = spin_new_instance(api_key, gpu)
        connect_lab(api_key, instance, SSH_KEY)
    else:
        _train_from_existing(api_key, instances)





def _train_from_existing(api_key: str, instances: list[dict]) -> None:
    """
    Prompts the user to select an existing training dataset or create a new one.

    Args:
        api_key (str): The FluidStack API Key provided by the User
        instances (list[dict]): The list of instances running on FluidStack
    """
    instances = get_instances(api_key)
    instances = [instance for instance in instances if "TunaKey" in instance["ssh_keys"]]

    table_data = [
        [
            instance["id"],
            instance["name"],
            instance["configuration"]["gpu_model"]["name"],
            instance["configuration"]["gpu_count"],
            instance["status"]
        ]
        for instance in instances
    ]

    headers = ["ID", "Name", "GPU Type", "# GPUs", "Status"]
    print(tabulate(table_data, headers, tablefmt="pretty"))
    log(INFO_ICON, "Data provided by FluidStack (https://fluidstack.io)")

    # pylint: disable=unnecessary-lambda-assignment
    instance_format = lambda instance: f"{instance['name']} - {instance['id']}"

    questions = [
            inquirer.List('instance',
                        message="Select the instance to use for training",
                        choices=[instance_format(instance) for instance in instances]
            )
        ]
    answers = inquirer.prompt(questions)

    # pylint: disable=line-too-long
    selected_option = \
        next(instance for instance in instances if instance_format(instance) == answers['instance'])

    instance = spin_existing_instance(api_key, selected_option)
    connect_lab(api_key, instance, SSH_KEY)
