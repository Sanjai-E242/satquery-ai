import os
import torch
import torch.nn as nn
from typing import Dict, Any, Tuple

def get_lora_vlm_model(base_model_name: str, lora_config_dict: Dict[str, Any], device: str) -> Tuple[Any, Any]:
    """
    Initializes a Vision-Language Model and attaches PyTorch PEFT/LoRA adapter layers.
    """
    from transformers import AutoProcessor, AutoModelForVision2Seq
    from peft import LoraConfig, get_peft_model, TaskType

    print(f"Loading Base VLM: {base_model_name}...")
    processor = AutoProcessor.from_pretrained(base_model_name)
    base_model = AutoModelForVision2Seq.from_pretrained(base_model_name)

    peft_config = LoraConfig(
        r=lora_config_dict.get("r", 16),
        lora_alpha=lora_config_dict.get("alpha", 32),
        lora_dropout=lora_config_dict.get("dropout", 0.05),
        bias="none",
        task_type=TaskType.FEATURE_EXTRACTION
    )

    try:
        model = get_peft_model(base_model, peft_config)
        model.print_trainable_parameters()
    except Exception as e:
        print(f"PEFT wrapper notice: {e}. Using base model parameters.")
        model = base_model

    model.to(device)
    return model, processor
