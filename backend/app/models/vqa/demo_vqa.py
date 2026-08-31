import os
import time
import numpy as np
from PIL import Image
from typing import Dict, Any
from app.models.vqa.base_vqa import BaseVQAAdapter

class DemoVQAAdapter(BaseVQAAdapter):
    """
    Deterministic Demo Fallback VQA Adapter.
    Calculates RGB spectral index heuristics when real AI model weights are offline.
    """
    def __init__(self):
        self.is_loaded = False
        self.mode = "DEMO_MODE"

    def load(self) -> bool:
        self.is_loaded = True
        return True

    def predict(self, inputs: Dict[str, Any], query: str) -> Dict[str, Any]:
        start_time = time.time()
        img_path = inputs.get("primary_image_path")
        
        brightness = 128.0
        greenness = 0.0
        blueness = 0.0
        
        if img_path and os.path.exists(img_path):
            try:
                with Image.open(img_path) as img:
                    arr = np.array(img.convert("RGB"))
                    mean_rgb = arr.mean(axis=(0, 1)).tolist()
                    brightness = float(np.mean(mean_rgb))
                    r, g, b = mean_rgb[0], mean_rgb[1], mean_rgb[2]
                    total = r + g + b + 1e-5
                    greenness = g / total
                    blueness = b / total
            except Exception as e:
                print(f"Demo VQA process error: {e}")

        q_lower = query.lower()
        if "dominant" in q_lower or "land cover" in q_lower:
            if greenness > 0.38:
                answer = "The dominant land cover is dense vegetation / agricultural cropland."
            elif blueness > 0.38:
                answer = "The dominant feature is an aquatic water body."
            elif brightness > 140:
                answer = "The dominant land cover consists of built-up urban structures."
            else:
                answer = "The scene contains a mixed land-cover landscape featuring sparse vegetation and soil."
        else:
            answer = f"Spectral analysis shows average intensity {brightness:.1f} with balanced reflectance."

        duration_ms = int((time.time() - start_time) * 1000)

        return {
            "answer": answer,
            "confidence": {
                "value": 0.85,
                "type": "estimated"
            },
            "model": "DemoHeuristicVQA",
            "mode": "DEMO_MODE",
            "duration_ms": duration_ms
        }

    def get_info(self) -> Dict[str, Any]:
        return {
            "name": "DemoHeuristicVQA",
            "mode": "DEMO_MODE",
            "status": "Ready (Fallback)"
        }
