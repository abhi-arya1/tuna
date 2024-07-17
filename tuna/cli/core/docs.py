"""

Functional Documentation for Tuna CLI Commands

"""

# pylint: disable=line-too-long
from tuna.cli.core.constants import BLUE, RESET, WARNING_ICON, RED


# Documentation Dictionary
DOCS = {



# INITIALIZE
    "init": f"""
{BLUE}USAGE{RESET}: tuna init
{BLUE}DESCRIPTION{RESET}: Initialize the Tuna configuration in the current directory.

This command sets up the necessary configuration files and folders for using Tuna.
""",




# CLONE
    "clone": f"""
{BLUE}USAGE{RESET}: tuna clone <url>
{BLUE}DESCRIPTION{RESET}: Clone the GitHub repository or Tuna Notebook to the current directory.
""",





# SERVE
    "serve": f"""
{BLUE}USAGE{RESET}: tuna serve [--open | --no-open]
{BLUE}DESCRIPTION{RESET}: Serve the Tuna Jupyter Notebook.

{BLUE}OPTIONS{RESET}:
    --open: Open the Notebook in the browser automatically.
    --no-open: Do not open the Notebook in the browser.

This command starts a Jupyter Notebook server with the Tuna Notebook.
""",



# REFRESH
    "refresh": f"""
{BLUE}USAGE{RESET}: tuna refresh
{BLUE}DESCRIPTION{RESET}: Refresh the Tuna cache in the current directory.

This command updates the cached data used by Tuna from the GitHub repository.
""",



# GITHUB
    "github": f"""
{BLUE}USAGE{RESET}: tuna github
{BLUE}DESCRIPTION{RESET}: Open the Tuna GitHub repository in the default browser.

This command opens the Tuna GitHub repository in the default browser.
""",



# DOCS
    "docs": f"""
{BLUE}USAGE{RESET}: tuna docs
{BLUE}DESCRIPTION{RESET}: Open the Tuna documentation in the default browser.

This command opens the Tuna documentation (README) in the default browser.
""",



# BROWSE
    "browse": f"""
{BLUE}USAGE{RESET}: tuna browse
{BLUE}DESCRIPTION{RESET}: Open the Tuna-initialized GitHub repository in the default browser.

This command opens the GitHub repository associated with the current Tuna configuration.
""",



# TRAIN
    "train": f"""
{BLUE}USAGE{RESET}: tuna train [--local]
{BLUE}DESCRIPTION{RESET}: Set up remote compute training with FluidStack.
{BLUE}OPTIONS{RESET}:
    --local: Train locally instead of using FluidStack.

This command sets up remote compute training with FluidStack, and forwards a powerful Jupyter Instance to your local machine automatically.
""",



# FLUIDSTACK
    "fluidstack": f"""
{BLUE}USAGE{RESET}: tuna fluidstack
{BLUE}DESCRIPTION{RESET}: Fluidstack Configuration Head for Tuna.
{BLUE}OPTIONS{RESET}:
    --manage: Manage Fluidstack Instances on https://dashboard.fluidstack.io

This command allows you to manage your Fluidstack instances, and update/pause/delete instances as needed.
""",


# PURGE
    "purge": f"""
{BLUE}USAGE{RESET}: tuna purge
{BLUE}DESCRIPTION{RESET}: Remove the Tuna configuration from the current directory.

This command deletes the .tuna directory and associated configuration files.
""",



# DEV
    "dev": f"""
{BLUE}USAGE{RESET}: tuna dev
{BLUE}DESCRIPTION{RESET}: Run functions for Tuna that are currently under development.

{RED}[{WARNING_ICON}]{RESET} These functions are not stable and may not work as expected. Do not use in production.
"""

# All commands in `tuna.cli.main.py` MUST be documented here.
# Please follow the format above to add documentation for new commands.
}
