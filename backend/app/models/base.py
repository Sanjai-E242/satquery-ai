from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseVisionLanguageModel(ABC):
    """
    Abstract interface for Remote-Sensing Vision-Language Models & Specialist Adapters.
    """
    @abstractmethod
    def load(self) -> bool:
        """Load model weights into memory/device."""
        pass

    @abstractmethod
    def predict(self, inputs: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Run model inference."""
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Check model status."""
        pass
