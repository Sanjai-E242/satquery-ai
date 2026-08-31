from typing import Dict, Any
from app.models.change_detection.base_change import BaseChangeAdapter
from app.models.change_detection.classical_change import ClassicalChangeDetector
from app.models.change_detection.neural_change import NeuralChangeDetector

class BiTemporalChangeModel(BaseChangeAdapter):
    """
    Unified Bi-Temporal Change Detection Engine.
    Exposes NeuralChangeDetector (Real Model) with ClassicalChangeDetector fallback.
    """
    def __init__(self, use_neural: bool = True):
        self.use_neural = use_neural
        self.neural_detector = NeuralChangeDetector()
        self.classical_detector = ClassicalChangeDetector()
        self.neural_detector.load()
        self.classical_detector.load()

    def load(self) -> bool:
        return True

    def predict(self, inputs: Dict[str, Any], query: str) -> Dict[str, Any]:
        if self.use_neural:
            return self.neural_detector.predict(inputs, query)
        return self.classical_detector.predict(inputs, query)

    def get_info(self) -> Dict[str, Any]:
        if self.use_neural:
            return self.neural_detector.get_info()
        return self.classical_detector.get_info()

    def health_check(self) -> Dict[str, Any]:
        return self.get_info()
