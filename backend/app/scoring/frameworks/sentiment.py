from .base_framework import BaseScoringFramework
from typing import Dict, Any, List

class SentimentAnalysisFramework(BaseScoringFramework):
    def __init__(self):
        # In a production environment, you might load a more sophisticated model.
        # For now, we'll use a simple keyword-based approach.
        self.positive_words = ["good", "great", "excellent", "love", "best", "amazing", "satisfied", "happy"]
        self.negative_words = ["bad", "terrible", "awful", "hate", "worst", "poor", "disappointed", "frustrated"]

    async def calculate_score(self, research_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate sentiment score from text data."""
        texts: List[str] = [result.get("content", "") for result in research_data.get("results", [])]
        
        if not texts:
            return {"raw_score": 0, "confidence": 0, "supporting_data": {"mentions": 0}}

        total_score = 0
        mentions = 0
        for text in texts:
            if not text: continue
            text_lower = text.lower()
            pos_count = sum(1 for word in self.positive_words if word in text_lower)
            neg_count = sum(1 for word in self.negative_words if word in text_lower)
            
            if pos_count > 0 or neg_count > 0:
                mentions += 1
                total_score += (pos_count - neg_count) / (pos_count + neg_count)
        
        avg_sentiment = total_score / mentions if mentions > 0 else 0
        
        return {
            "raw_score": avg_sentiment, # Ranges from -1 to 1
            "confidence": min(mentions / 10, 1.0), # Confidence increases with more mentions
            "supporting_data": {"mentions": mentions, "positive_keywords": len(self.positive_words)}
        }
