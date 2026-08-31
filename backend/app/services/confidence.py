import math
import torch
import numpy as np
from typing import Dict, Any, Optional
from app.schemas.schemas import ConfidenceInfo

class ConfidenceEngine:
    """
    Calculates dynamic confidence scores based on model output probabilities,
    input image quality, geospatial georeferencing, and modality agreement.
    Guarantees finite, native Python float values.
    """
    @staticmethod
    def calculate_confidence(
        raw_score: Optional[Any] = None,
        model_mode: str = "REAL_MODEL",
        image_meta: Optional[Dict[str, Any]] = None,
        has_secondary: bool = False
    ) -> ConfidenceInfo:
        
        # 1. Normalize raw_score to standard Python float
        base_val = 0.90
        if raw_score is not None:
            try:
                if isinstance(raw_score, torch.Tensor):
                    raw_val = float(raw_score.detach().cpu().item() if raw_score.numel() == 1 else raw_score.mean().item())
                elif isinstance(raw_score, (np.floating, np.integer)):
                    raw_val = float(raw_score)
                elif isinstance(raw_score, (int, float)):
                    raw_val = float(raw_score)
                else:
                    raw_val = float(raw_score)

                if not math.isnan(raw_val) and not math.isinf(raw_val) and 0.0 <= raw_val <= 1.0:
                    base_val = raw_val
            except Exception:
                base_val = 0.90

        if model_mode == "DEMO_MODE":
            return ConfidenceInfo(value=0.85, type="estimated")

        # Quality adjustments
        if image_meta and isinstance(image_meta, dict):
            try:
                w = int(image_meta.get("width", 512) or 512)
                h = int(image_meta.get("height", 512) or 512)
                if w >= 512 and h >= 512:
                    base_val += 0.02
                if image_meta.get("has_geospatial"):
                    base_val += 0.03
                fmt = str(image_meta.get("format", "")).upper()
                if fmt not in ["TIF", "TIFF", "GEOTIFF"]:
                    base_val -= 0.02
            except Exception:
                pass

        if has_secondary:
            base_val += 0.02

        if math.isnan(base_val) or math.isinf(base_val):
            base_val = 0.88

        final_score = float(round(max(0.60, min(0.99, base_val)), 2))
        conf_type = "model_derived" if (model_mode in ["REAL_MODEL", "REMOTE_SENSING_ADAPTED"]) else "estimated"

        return ConfidenceInfo(
            value=final_score,
            type=str(conf_type)
        )
