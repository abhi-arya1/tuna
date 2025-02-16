# import boto3
# import paramiko
# import time
# from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket
# from pydantic import BaseModel
# from typing import Optional, Dict
# import asyncio
# import nbformat
# from jupyter_client import KernelManager
# import json
# import websockets
# from os import getenv

# class InstanceRequest(BaseModel):
#     instance_type: str
#     volume_size: int = 30
#     notebook_path: Optional[str] = None

# active_kernels: Dict[str, KernelManager] = {}
# connected_clients: Dict[str, set] = {}

# class EC2Manager:
#     def __init__(self):
#         self.ec2 = boto3.resource('ec2',
#             region_name=getenv('AWS_REGION'),
#             aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
#             aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY")
#         )
#         self.ec2 = boto3.client('ec2',
#             region_name=getenv('AWS_REGION'),
#             aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
#             aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY")
#         )
        
#     def create_instance(self, instance_type: str, volume_size: int) -> dict:
#         user_data = """
#         #!/bin/bash
#         sudo apt-get update
#         sudo apt-get install -y python3-pip
#         pip3 install jupyter jupyter_client websockets --break-system-packages
#         jupyter notebook --generate-config
#         echo "c.NotebookApp.ip = '0.0.0.0'" >> ~/.jupyter/jupyter_notebook_config.py
#         echo "c.NotebookApp.allow_root = True" >> ~/.jupyter/jupyter_notebook_config.py
#         echo "c.NotebookApp.open_browser = False" >> ~/.jupyter/jupyter_notebook_config.py
#         echo "c.NotebookApp.port = 8888" >> ~/.jupyter/jupyter_notebook_config.py
#         echo "c.NotebookApp.token = ''" >> ~/.jupyter/jupyter_notebook_config.py
#         """
        
#         instance = self.ec2.create_instances(
#             ImageId='ami-0c55b159cbfafe1f0',
#             InstanceType=instance_type,
#             MinCount=1,
#             MaxCount=1,
#             KeyName='your-key-pair-name',
#             SecurityGroups=['jupyter-security-group'],
#             UserData=user_data,
#             BlockDeviceMappings=[{
#                 'DeviceName': '/dev/xvda',
#                 'Ebs': {
#                     'VolumeSize': volume_size,
#                     'VolumeType': 'gp2'
#                 }
#             }]
#         )[0]
        
#         instance.wait_until_running()
#         instance.reload()
        
#         return {
#             'instance_id': instance.id,
#             'public_ip': instance.public_ip_address
#         }

#     async def execute_notebook(self, instance_ip: str, notebook_path: str, instance_id: str):
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
#         try:
#             ssh.connect(
#                 instance_ip,
#                 username='ubuntu',
#                 key_filename='path/to/your/key.pem'
#             )
            
#             stdin, stdout, stderr = ssh.exec_command('jupyter kernel --kernel=python3')
#             kernel_info = json.loads(stdout.read().decode())
            
#             active_kernels[instance_id] = kernel_info
            
#             # Execute notebook cells and stream output
#             notebook = nbformat.read(notebook_path, as_version=4)
#             for cell in notebook.cells:
#                 if cell.cell_type == "code":
#                     # Execute cell and broadcast output to all connected clients
#                     await self.execute_cell(instance_id, cell.source)
                    
#         finally:
#             ssh.close()

#     async def execute_cell(self, instance_id: str, code: str):
#         kernel_info = active_kernels.get(instance_id)
#         if not kernel_info:
#             return
        
#         # Connect to kernel
#         connection_url = f"ws://{kernel_info['url']}/channels"
#         async with websockets.connect(connection_url) as websocket:
#             # Send code execution request
#             execute_request = {
#                 "header": {"msg_type": "execute_request"},
#                 "content": {"code": code, "silent": False}
#             }
#             await websocket.send(json.dumps(execute_request))
            
#             # Stream output to connected clients
#             while True:
#                 response = json.loads(await websocket.recv())
#                 if response["msg_type"] == "execute_result" or response["msg_type"] == "stream":
#                     output = response["content"]["data"]["text/plain"]
#                     await self.broadcast_output(instance_id, output)
#                 elif response["msg_type"] == "status" and response["content"]["execution_state"] == "idle":
#                     break

#     async def broadcast_output(self, instance_id: str, output: str):
#         if instance_id in connected_clients:
#             for client in connected_clients[instance_id]:
#                 await client.send_text(output)

# ec2_manager = EC2Manager()

# @app.websocket("/ws/{instance_id}")
# async def websocket_endpoint(websocket: WebSocket, instance_id: str):
#     await websocket.accept()
    
#     if instance_id not in connected_clients:
#         connected_clients[instance_id] = set()
#     connected_clients[instance_id].add(websocket)
    
#     try:
#         while True:
#             await websocket.receive_text()
#     except:
#         connected_clients[instance_id].remove(websocket)

# # Previous endpoints remain the same...