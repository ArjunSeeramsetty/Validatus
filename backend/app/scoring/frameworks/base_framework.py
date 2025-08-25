from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseScoringFramework(ABC):
    @abstractmethod
    async def calculate_score(self, research_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        pass
