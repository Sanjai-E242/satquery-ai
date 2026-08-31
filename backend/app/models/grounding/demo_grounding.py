import os
import time
import uuid
import numpy as np
from PIL import Image, ImageDraw
from typing import Dict, Any
from app.config import settings
from app.models.grounding.base_grounding import BaseGroundingAdapter

class DemoGroundingAdapter(BaseGroundingAdapter):
    """
    Deterministic Demo Fallback Grounding Adapter.
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
        
        w, h = 512, 512
        if img_path and os.path.exists(img_path):
            with Image.open(img_path) as img:
                w, h = img.size

        bbox = [int(w * 0.15), int(h * 0.40), int(w * 0.75), int(h * 0.85)]
        
        overlay_id = str(uuid.uuid4())[:8]
        overlay_filename = f"demo_grounding_mask_{overlay_id}.png"
        overlay_path = settings.GENERATED_DIR / overlay_filename

        if img_path and os.path.exists(img_path):
            with Image.open(img_path).convert("RGBA") as base_img:
                mask = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(mask)
                draw.rectangle(bbox, fill=(0, 150, 255, 120), outline=(0, 150, 255, 255), width=4)
                composite = Image.alpha_composite(base_img, mask)
                composite.save(overlay_path)

        duration_ms = int((time.time() - start_time) * 1000)

        return {
            "answer": f"Demo Grounding: Bounding box `{bbox}`.",
            "boxes": [bbox],
            "scores": [0.85],
            "labels": ["Water Body (Demo)"],
            "bounding_box": bbox,
            "mask_relative_url": f"/storage/generated/{overlay_filename}",
            "mask_path": str(overlay_path),
            "confidence": {"value": 0.85, "type": "estimated"},
            "model": "DemoGroundingHeuristic",
            "mode": "DEMO_MODE",
            "duration_ms": duration_ms
        }

    def get_info(self) -> Dict[str, Any]:
        return {"name": "DemoGroundingHeuristic", "mode": "DEMO_MODE", "status": "Ready (Fallback)"}
