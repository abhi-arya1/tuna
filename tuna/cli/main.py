"""

Tuna CLI Entry-Point 

This file manages all functionality for the Tuna CLI.

"""


from webbrowser import open as webopen
from sys import argv, exit
from tuna.cli.core.util import log
from tuna.cli.core.constants import HELLO, INFO_ICON, WARNING_ICON, \
    Token, HELP, VERSION
from tuna.cli.core.docs import DOCS
from tuna.cli.generators.dataset import build_dataset
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




def _handle_serve_command(arg: str) -> None:
    """
    Handles the 'serve' command with the provided argument.
    """
    if arg == Token.OPEN.value:
        serve(browser=True)
    elif arg == Token.NO_OPEN.value:
        serve()
    elif arg:
        log(WARNING_ICON, f"Invalid flag for 'serve': '{arg}'. {HELP}")
    else:
        serve()




def _handle_train_command(arg: str, args: list[str]) -> None:
    """
    Handles the 'train' command with the provided argument.
    """
    if arg == Token.LOCAL.value:
        if len(args) == 4 and args[3] == Token.FORCE.value:
            train(local=True, force=True)
        else: 
            train(local=True)
    elif arg == Token.FORCE.value:
        train(force=True)
    elif arg:
        log(WARNING_ICON, f"Invalid flag for 'train': '{arg}'. {HELP}")
    else:
        train()




def _handle_fluidstack_command(arg: str) -> None:
    """
    Handles the 'fluidstack' command with the provided argument.
    """
    if arg == Token.MANAGE.value:
        log(INFO_ICON, "Opening FluidStack Dashboard in your default browser.")
        webopen("https://dashboard.fluidstack.io/")
    elif arg:
        log(WARNING_ICON, f"Invalid option '{arg}'. {HELP}")
    else:
        log(WARNING_ICON, f"Invalid options '{argv}'. {HELP}")




def _handle_make_command(arg: str) -> None:
    """
    Handles the 'make' command with the provided argument.
    """
    if arg == Token.DATASET.value:
        build_dataset()
    elif arg == Token.NOTEBOOK.value:
        log(WARNING_ICON, "This feature is not yet implemented. Please check back later.")
    elif arg:
        log(WARNING_ICON, f"Invalid option '{arg}'. {HELP}")
    else:
        log(WARNING_ICON, f"`tuna make` requires a command, such as `tuna make [notebook | dataset]`. {HELP}")




def _open_url(url: str) -> None:
    """
    Opens the provided URL in the default browser.
    """
    log(INFO_ICON, f"Opening '{url}' in your default browser.")
    webopen(url)




def _handle_dev(arg: str) -> None:
    """
    Handles development mode commands for Tuna CLI
    """
    log(INFO_ICON, f"No commands under development. Build 'v{VERSION}' is stable.")




# pylint: disable=all
def main() -> None:
    """
    Runs the `tuna` CLI with any provided arguments.
    """
    if len(argv) == 1:
        print(HELLO)
        exit(0)

    command = argv[1]
    arg = argv[2] if len(argv) > 2 else None

    match command:        
        case Token.HELP.value | Token.HELP_SHORT.value:
            if arg:
                _help(arg)
            else:
                log(WARNING_ICON, f"No argument provided for '{command}'. {HELP}")

        case Token.VERSION.value | Token.VERSION_SHORT.value:
            _version()
        
        case Token.INIT.value:
            init()

        case Token.SERVE.value:
            _handle_serve_command(arg)

        case Token.REFRESH.value:
            refresh()

        case Token.GITHUB.value | Token.DOCS.value:
            _open_url("https://github.com/abhi-arya1/tuna")

        case Token.BROWSE.value:
            open_repository()

        case Token.TRAIN.value:
            _handle_train_command(arg, argv)

        case Token.FLUIDSTACK.value:
            _handle_fluidstack_command(arg)

        case Token.PURGE.value:
            purge()

        case Token.MAKE.value:
            _handle_make_command(arg)

        case Token.DEV.value:
            _handle_dev(arg)

        case _:
            log(WARNING_ICON, f"Invalid option '{command}'. {HELP}")

    exit(0)



if __name__ == '__main__':
    try:
        main()
    # pylint: disable=broad-exception-caught
    except Exception as e:
        log(WARNING_ICON, f"Tuna encountered an error: {e}")
        exit(1)
