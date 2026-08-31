import torch
from typing import Dict, Any, List

class ModelRegistry:
    """
    Upgraded Model Registry exposing model modes, devices, checkpoints, and task specs.
    """
    @classmethod
    def get_device(cls) -> str:
        if torch.cuda.is_available(): return "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available(): return "mps"
        return "cpu"

    @classmethod
    def list_models(cls) -> List[Dict[str, Any]]:
        device = cls.get_device()
        checkpoint_exists = torch.os.path.exists("checkpoints/rs_vlm_lora/adapter_config.json")
        vlm_mode = "REMOTE_SENSING_ADAPTED" if checkpoint_exists else "DEMO_MODE"

        return [
            {
                "model_id": "rs_vlm_lora",
                "name": "BigEarthNet Fine-Tuned RS-VLM",
                "version": "1.0-lora",
                "task": "vqa",
                "input_modalities": ["single_image"],
                "checkpoint": "checkpoints/rs_vlm_lora",
                "mode": vlm_mode,
                "status": "Ready (REMOTE_SENSING_ADAPTED Checkpoint Loaded)" if checkpoint_exists else "Ready (DEMO_MODE Fallback)",
                "device": device,
                "supports_cpu": True,
                "supports_gpu": True
            },
            {
                "model_id": "rs_grounding_dynamic",
                "name": "RS Dynamic Feature Grounding & Segmentation Engine",
                "version": "2.1-dynamic",
                "task": "grounding",
                "input_modalities": ["single_image"],
                "checkpoint": None,
                "mode": "REAL_MODEL",
                "status": "Ready (Dynamic Contour & Spectral Segmentation Engine)",
                "device": device,
                "supports_cpu": True,
                "supports_gpu": True
            },
            {
                "model_id": "bi_temporal_neural_cd",
                "name": "Bi-Temporal PyTorch Neural Spatial Change Engine",
                "version": "2.0-neural",
                "task": "change_analysis",
                "input_modalities": ["bi_temporal_pair"],
                "checkpoint": None,
                "mode": "REAL_MODEL",
                "status": "Ready (PyTorch Spatial Difference Model)",
                "device": device,
                "supports_cpu": True,
                "supports_gpu": True
            },
            {
                "model_id": "optical_sar_neural_fusion",
                "name": "Optical + SAR PyTorch Cross-Modal Fusion Engine",
                "version": "2.0-fusion",
                "task": "optical_sar_fusion",
                "input_modalities": ["optical_sar_pair"],
                "checkpoint": None,
                "mode": "REAL_MODEL",
                "status": "Ready (PyTorch Feature Alignment & 1x1 Fusion Conv)",
                "device": device,
                "supports_cpu": True,
                "supports_gpu": True
            }
        ]

    @classmethod
    def get_model_info(cls, model_id: str) -> Dict[str, Any]:
        for m in cls.list_models():
            if m["model_id"] == model_id:
                return m
        return {}
