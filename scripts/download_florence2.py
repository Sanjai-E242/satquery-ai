import os
import sys
import torch
from huggingface_hub import snapshot_download

print("Downloading Florence-2-base checkpoint from Hugging Face...")
repo_id = "microsoft/Florence-2-base"
local_dir = os.path.expanduser("~/.cache/huggingface/hub/models--microsoft--Florence-2-base")

path = snapshot_download(
    repo_id=repo_id,
    allow_patterns=["*.json", "*.py", "*.bin", "*.safetensors", "*.model", "*.txt"]
)

print(f"Successfully downloaded {repo_id} to {path}!")
