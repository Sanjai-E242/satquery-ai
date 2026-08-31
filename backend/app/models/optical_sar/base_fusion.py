from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseFusionAdapter(ABC):
    """
    Abstract Interface for Optical + SAR Fusion Adapters.
    """
    @abstractmethod
    def load(self) -> bool:
        pass

    @abstractmethod
    def predict(self, inputs: Dict[str, Any], query: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        pass
