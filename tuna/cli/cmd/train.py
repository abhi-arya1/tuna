"""

SSH Machine Training Setup for Tuna CLI

"""

from tuna.cli.core.authenticator import validate, validate_fluidstack
from tuna.cli.core.constants import INFO_ICON
from tuna.cli.core.util import log
from tuna.cli.services.fluidstack import get_instances, spin_instance, \
    existing_or_new_trainer, select_gpu

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
        use_existing = False

    if not instances or len(instances) == 0 or not use_existing:
        gpu = select_gpu(api_key)
        spin_instance(api_key, gpu)
    else:
        pass