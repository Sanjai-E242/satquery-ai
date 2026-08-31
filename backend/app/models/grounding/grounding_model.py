import os
import time
from typing import Dict, Any
from app.models.base import BaseVisionLanguageModel
from app.models.grounding.remote_sensing_grounding import RemoteSensingGroundingAdapter

class RemoteSensingGroundingModel(BaseVisionLanguageModel):
    """
    Real Pretrained Florence-2 Vision-Language Grounding & Segmentation Model.
    Delegates inference to RemoteSensingGroundingAdapter.
    """
    def __init__(self):
        self.adapter = RemoteSensingGroundingAdapter()
        self.is_loaded = False

    def load(self) -> bool:
        self.is_loaded = self.adapter.load()
        return self.is_loaded

    def predict(self, inputs: Dict[str, Any], query: str) -> Dict[str, Any]:
        return self.adapter.predict(inputs, query)

    def health_check(self) -> Dict[str, Any]:
        return {"status": "Ready", "loaded": self.is_loaded, "mode": "REAL_MODEL"}
