"""

SSH Machine Training Setup for Tuna CLI

"""

# pylint: disable=consider-using-sys-exit

import GPUtil as gputil
import inquirer
from tabulate import tabulate
from tuna.util.nbutil import validate_nb
from tuna.cli.core.authenticator import validate, validate_fs, validate_hf
from tuna.cli.core.constants import INFO_ICON, SSH_KEY, WARNING_ICON, UNDEFINED_BEHV, \
    NO_NOTEBOOK, NOTEBOOK, RemotePlatform, NOT_IMPLEMENTED
from tuna.util.general import log, warn
from tuna.services.clouds.fluidstack import get_instances, spin_new_instance, \
    existing_or_new_trainer, select_gpu, spin_existing_instance
from tuna.services.jupyter import connect_lab, connect_local_lab
from tuna.cli.core.authenticator import validate_ip



def train(local=False, force=False) -> None:
    """
    Setup remote compute training with FluidStack.

    Args: 
        local (bool, optional): Whether to train locally. Default=False.
    """
    validate()
    validate_ip()

    if local:
        if not force:
            _check_gpu()
        else:
            warn(UNDEFINED_BEHV, "Forcing local training without GPU check...")
        connect_local_lab()
        return

    if not force:
        validate_nb(NOTEBOOK)
    else:
        warn(NO_NOTEBOOK, "Forcing remote training without notebook check...")

    platform = _get_platform()

    # pylint: disable=line-too-long
    if platform != RemotePlatform.FLUIDSTACK:
        warn(NOT_IMPLEMENTED, f"Only FluidStack is currently supported for remote training, {platform} coming soon!")
        exit(1)

    fs_api_key = validate_fs()
    validate_hf()

    instances = get_instances(fs_api_key)

    if instances and len(instances) != 0:
        use_existing = existing_or_new_trainer()
    else:
        log(INFO_ICON, "No previous instances found. Let's configure a new instance...")
        use_existing = False

    if not instances or len(instances) == 0 or not use_existing:
        gpu = select_gpu(fs_api_key)
        instance = spin_new_instance(fs_api_key, gpu)
        connect_lab(fs_api_key, instance, SSH_KEY)
    else:
        _train_from_existing(fs_api_key, instances)




def _get_platform() -> RemotePlatform:
    """
    Gets the user's preferred training platform.
    """
    questions = [
        inquirer.List('platform',
                    message="Select the cloud platform for remote training",
                    choices=RemotePlatform.__members__.keys()
        )
    ]
    answers = inquirer.prompt(questions)

    return RemotePlatform.__members__[answers['platform'].upper()]




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




# pylint: disable=consider-using-sys-exit
# pylint: disable=line-too-long
def _check_gpu():
    """
    Validate existence of NVIDIA GPU for local training
    """
    gpus = gputil.getGPUs()
    if len(gpus) == 0:
        log(WARNING_ICON, "Tuna '--local' training requires an NVIDIA GPU, which wasn't found on your system. Use 'tuna train --local --force' to bypass this check.")
        exit(1)
