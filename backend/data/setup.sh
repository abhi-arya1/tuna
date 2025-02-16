#!/bin/bash

echo "Checking dependencies..."

sudo apt-get update
sudo apt-get install -y python3-pip python3-dev python3-venv

python3 -m venv .venv
source .venv/bin/activate

pip install torch datasets transformers peft bitsandbytes accelerate huggingface-hub

echo "Done installing dependencies!"