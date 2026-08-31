from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseChangeAdapter(ABC):
    """
    Abstract Interface for Bi-Temporal Change Detection Adapters.
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
