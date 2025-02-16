import paramiko
from typing import Callable, Literal
from util.dtypes import WSRequest
from util.helpers import get_log_format

from os import getenv 
SSH_USERNAME = "ubuntu"
SSH_HOST = getenv("SSH_HOST_H100")


async def run_command(ssh: paramiko.SSHClient, command: str, send_handler: Callable[[dict, Literal["text"]], None]) -> None:
    stdin, stdout, stderr = ssh.exec_command(command)

    for line in iter(stdout.readline, ""):
        await send_handler({
            "type": "train_details",
            "text": "",
            "log": get_log_format(f"{line}\n"),
            "complete": False
        })

    for line in iter(stderr.readline, ""):
        await send_handler({
            "type": "train_details",
            "text": "",
            "log": get_log_format(f"[ERROR] {line}\n"),
            "complete": False
        })




async def transfer_file(ssh: paramiko.SSHClient, source: str, destination: str, send_handler: Callable[[dict, Literal["text"]], None]) -> None:
    sftp = ssh.open_sftp()
    sftp.put(source, destination)

    await send_handler({
        "type": "train_details",
        "text": "",
        "log": get_log_format(f"Transferred {source} to {destination}\n"),
        "complete": False
    })



# class TrainDetails(BaseModel):
#     type: str
#     text: str 
#     log: str 
#     complete: bool = False



async def train_model_response(data: WSRequest, send_handler: Callable[[dict, Literal["text"]], None]) -> None:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(SSH_HOST, username=SSH_USERNAME)

        await transfer_file(ssh, "data/dataset.jsonl", "/home/ubuntu/runway/dataset.jsonl", send_handler)
        await transfer_file(ssh, "data/setup.sh", "/home/ubuntu/runway/setup.sh", send_handler)
        await transfer_file(ssh, "data/run.sh", "/home/ubuntu/runway/run.sh", send_handler)
        await transfer_file(ssh, "data/secrets.txt", "/home/ubuntu/runway/secrets.txt", send_handler)
        await run_command(ssh, "cd /home/ubuntu/runway && chmod +x ./setup.sh", send_handler)
        await run_command(ssh, "cd /home/ubuntu/runway && chmod +x ./run.sh", send_handler)
        await transfer_file(ssh, "data/train_script.py", "/home/ubuntu/runway/train_script.py", send_handler)
        await transfer_file(ssh, "data/config.json", "/home/ubuntu/runway/config.json", send_handler)

        await send_handler({
            "type": "train_details",
            "text": "Setting up instance...",
            "log": get_log_format("Beginning training pipeline", tuna_msg=True),
            "complete": False
        })

        await run_command(ssh, "cd /home/ubuntu/runway && ./setup.sh", send_handler)
        await send_handler({
            "type": "train_details",
            "text": "Training model...",
            "log": get_log_format("Setup complete. Beginning training", tuna_msg=True),
            "complete": False
        })
        await run_command(ssh, "cd /home/ubuntu/runway && ./run.sh", send_handler)

        await send_handler({
            "type": "train_details",
            "text": "Completed training. Saving weights!",
            "log": get_log_format(f"Completed model training", tuna_msg=True),
            "complete": True
        })

    except Exception as e:
        print(f"[ERROR] {e}")
        await send_handler({
            "type": "train_details",
            "text": "We ran into an error with model training...",
            "log": get_log_format(f"[ERROR] {e}\n"),
            "complete": False
        })

    finally:
        ssh.close()

