from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json
from config import settings

class BaseResearchAgent(ABC):
    def __init__(self):
        self.config = settings

    @abstractmethod
    async def research(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def _calculate_confidence(self, results: List[Any]) -> float:
        """Calculate a confidence score based on the success of research tasks."""
        successful_tasks = sum(1 for r in results if not isinstance(r, Exception) and not r.get("error"))
        return successful_tasks / len(results) if results else 0.0

    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Safely parse a JSON string from an LLM response."""
        try:
            # Clean up potential markdown code fences
            if response_text.strip().startswith("```json"):
                response_text = response_text.strip()[7:-3].strip()
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON response", "raw_text": response_text}
