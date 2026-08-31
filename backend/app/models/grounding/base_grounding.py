from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseGroundingAdapter(ABC):
    """
    Abstract Interface for Text-Guided Region Grounding Adapters.
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
