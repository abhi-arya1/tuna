"""

File Watch Clients for Remote Sync for Tuna CLI 

"""


# from subprocess import run
from watchdog.events import FileSystemEventHandler
from tuna.util.general import log
from tuna.cli.core.constants import INFO_ICON


class LabWatcher(FileSystemEventHandler):
    """
    Watches for changes in the `.tuna` directory to 
    run commands on the remote machine.
    """
    def __init__(self, command: list[str]=None, function: 'function'=None):
        self._command = command
        self._function = function

    def on_any_event(self, event):
        log(INFO_ICON, f"Change detected in {event.src_path}")
        self._function()
