from typing import Dict, Any
from app.models.optical_sar.base_fusion import BaseFusionAdapter
from app.models.optical_sar.classical_fusion import ClassicalOpticalSARBaseline
from app.models.optical_sar.neural_fusion import NeuralOpticalSARFusion

class OpticalSARFusionModel(BaseFusionAdapter):
    """
    Unified Optical + SAR Cross-Modal Fusion Engine.
    Exposes NeuralOpticalSARFusion (Real Model) with ClassicalOpticalSARBaseline fallback.
    """
    def __init__(self, use_neural: bool = True):
        self.use_neural = use_neural
        self.neural_fusion = NeuralOpticalSARFusion()
        self.classical_baseline = ClassicalOpticalSARBaseline()
        self.neural_fusion.load()
        self.classical_baseline.load()

    def load(self) -> bool:
        return True

    def predict(self, inputs: Dict[str, Any], query: str) -> Dict[str, Any]:
        if self.use_neural:
            return self.neural_fusion.predict(inputs, query)
        return self.classical_baseline.predict(inputs, query)

    def get_info(self) -> Dict[str, Any]:
        if self.use_neural:
            return self.neural_fusion.get_info()
        return self.classical_baseline.get_info()

    def health_check(self) -> Dict[str, Any]:
        return self.get_info()
