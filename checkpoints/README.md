# Checkpoints Directory

This directory stores trained LoRA/PEFT model adapter checkpoints fine-tuned on the `BigEarthNet.txt` remote-sensing VQA dataset.

- `rs_vlm_lora/adapter_config.json`: Model configuration and training loss metadata.
- `rs_vlm_lora/training_history.json`: Epoch loss progression log.

When a valid fine-tuned checkpoint exists in `checkpoints/rs_vlm_lora`, the backend system automatically transitions from `DEMO_MODE` to `REMOTE_SENSING_ADAPTED`.
