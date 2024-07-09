"""

Tuna CLI Entry-Point 

This file manages all functionality for the Tuna CLI.

"""


from webbrowser import open as webopen
from sys import argv
from tuna.cli.services.datasets import build_dataset
from tuna.cli.core.util import log
from tuna.cli.core.constants import HELLO, INFO_ICON, WARNING_ICON, \
    Token, HELP, VERSION
from tuna.cli.core.docs import DOCS
from tuna.cli.cmd.init import init
from tuna.cli.cmd.serve import serve
from tuna.cli.cmd.refresh import refresh
from tuna.cli.cmd.open_repo import open_repository
from tuna.cli.cmd.purge import purge
from tuna.cli.cmd.train import train




def _help(token: str) -> None:
    """
    Helper function to display information for a specific Tuna command.
    """
    doc = DOCS.get(token, False) 
    if not doc: 
        log(WARNING_ICON, f"Invalid help command '{argv[2]}'. \n- [-h | --help] only works with valid commands. \n- Run 'tuna' for some valid commands.")
        exit(1)
    print(DOCS[token])
    exit(0)




def _version() -> None: 
    """
    Display the current version of Tuna.
    """
    print(f"Tuna v{VERSION}")
    exit(0)



# pylint: disable=all
def main() -> None:
    """
    Runs the `tuna` CLI with any provided arguments.
    """
    if len(argv) == 1:
        print(HELLO)
        exit(0)

    if len(argv) == 3:
        if argv[1] in [Token.HELP.value, Token.HELP_SHORT.value]:
            _help(argv[2])

    if argv[1] in [Token.VERSION.value, Token.VERSION_SHORT.value]:
        _version()

    elif argv[1] == Token.INIT.value:
        init()

    elif argv[1] == Token.SERVE.value:
        if(len(argv)) > 2:
            if argv[2] ==Token.OPEN.value:
                serve(browser=True)
            elif argv[2] == Token.NO_OPEN.value:
                serve()
            else:
                log(WARNING_ICON, f"Invalid flag for 'serve': '{argv[2]}'. {HELP}")
        else:
            serve()

    elif argv[1] == Token.REFRESH.value:
        refresh()

    elif argv[1] in [Token.GITHUB.value, Token.DOCS.value]:
        log(INFO_ICON, "Opening 'https://github.com/abhi-arya1/tuna' in your default browser.")
        webopen("https://github.com/abhi-arya1/tuna")

    elif argv[1] == Token.BROWSE.value:
        open_repository()

    elif argv[1] == Token.TRAIN.value:
        if(len(argv)) > 2:
            if argv[2] == Token.LOCAL.value:
                train(local=True)
            else:
                log(WARNING_ICON, f"Invalid flag for 'train': '{argv[2]}'. {HELP}")
        else:
            train()

    elif argv[1] == Token.FLUIDSTACK.value:
        if len(argv) == 3 and argv[2] == Token.MANAGE.value:
            log(INFO_ICON, "Opening FluidStack Dashboard in your default browser.")
            webopen("https://dashboard.fluidstack.io/")
        elif len(argv) == 3:
            log(WARNING_ICON, f"Invalid option '{argv[2]}'. {HELP}")
        else:
            log(WARNING_ICON, f"Invalid options '{argv}'. {HELP}")

    elif argv[1] == Token.PURGE.value:
        purge()

    elif argv[1] == Token.DATASET.value:
        if argv[2] == "dataset":
            build_dataset()

    else:
        log(WARNING_ICON, f"Invalid option '{argv[1]}'. {HELP}")

    exit(0)



if __name__ == '__main__':
    try:
        main()
    # pylint: disable=broad-exception-caught
    except Exception as e:
        log(WARNING_ICON, f"Tuna encountered an error: {e}")
        exit(1)
