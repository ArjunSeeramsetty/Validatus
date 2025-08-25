import numpy as np
import re
from typing import Dict, Any, List
from .base_framework import BaseScoringFramework

class PESTLEAnalysisFramework(BaseScoringFramework):
    """Production implementation of PESTLE analysis with real data extraction."""
    
    def __init__(self):
        self.pestle_categories = {
            "political": {
                "keywords": ["government", "policy", "regulation", "legislation", "political", "election", "tax", "subsidy"],
                "weight": 0.18
            },
            "economic": {
                "keywords": ["economy", "gdp", "inflation", "interest rate", "unemployment", "market", "trade", "currency"],
                "weight": 0.20
            },
            "social": {
                "keywords": ["demographics", "culture", "lifestyle", "trends", "social media", "values", "education", "health"],
                "weight": 0.17
            },
            "technological": {
                "keywords": ["technology", "innovation", "digital", "ai", "automation", "software", "hardware", "research"],
                "weight": 0.18
            },
            "legal": {
                "keywords": ["law", "compliance", "regulation", "legal", "court", "patent", "copyright", "trademark"],
                "weight": 0.15
            },
            "environmental": {
                "keywords": ["environment", "climate", "sustainability", "green", "carbon", "renewable", "pollution", "energy"],
                "weight": 0.12
            }
        }

    async def calculate_score(self, research_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive PESTLE analysis score."""
        try:
            # Extract text content for analysis
            texts = self._extract_text_content(research_data)
            
            if not texts:
                return {"raw_score": 5.0, "confidence": 0.0, "supporting_data": {"text_count": 0}}
            
            # Analyze each PESTLE category
            category_scores = {}
            category_insights = {}
            
            for category, config in self.pestle_categories.items():
                score_data = self._analyze_category(texts, category, config["keywords"])
                category_scores[category] = score_data["score"]
                category_insights[category] = score_data["insights"]
            
            # Calculate weighted overall score
            weighted_score = sum(
                category_scores[category] * config["weight"]
                for category, config in self.pestle_categories.items()
            )
            
            # Generate overall insights
            overall_insights = self._generate_overall_insights(category_scores, category_insights)
            
            return {
                "raw_score": float(weighted_score),
                "confidence": self._calculate_confidence(texts, category_scores),
                "supporting_data": {
                    "category_scores": category_scores,
                    "category_insights": category_insights,
                    "overall_insights": overall_insights,
                    "text_count": len(texts),
                    "analysis_method": "Keyword-based PESTLE analysis"
                }
            }
            
        except Exception as e:
            return {"raw_score": 5.0, "confidence": 0.0, "error": str(e)}

    def _extract_text_content(self, research_data: Dict[str, Any]) -> List[str]:
        """Extract text content from various research data sources."""
        texts = []
        
        # Extract from web research results
        if "web_research" in research_data:
            results = research_data["web_research"].get("results", [])
            for result in results:
                if isinstance(result, dict):
                    content = result.get("content", "") or result.get("description", "") or result.get("title", "")
                    if content:
                        texts.append(content)
        
        # Extract from news articles
        if "news_trends" in research_data and "articles" in research_data["news_trends"]:
            articles = research_data["news_trends"]["articles"]
            for article in articles:
                if isinstance(article, dict):
                    content = article.get("content", "") or result.get("description", "") or article.get("title", "")
                    if content:
                        texts.append(content)
        
        # Extract from industry reports
        if "industry_reports" in research_data:
            results = research_data["industry_reports"].get("results", [])
            for result in results:
                if isinstance(result, dict):
                    content = result.get("content", "") or result.get("description", "") or result.get("title", "")
                    if content:
                        texts.append(content)
        
        return texts

    def _analyze_category(self, texts: List[str], category: str, keywords: List[str]) -> Dict[str, Any]:
        """Analyze a specific PESTLE category."""
        category_mentions = 0
        category_sentiment = 0
        insights = []
        
        for text in texts:
            text_lower = text.lower()
            
            # Count keyword mentions
            for keyword in keywords:
                count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text_lower, re.IGNORECASE))
                if count > 0:
                    category_mentions += count
                    
                    # Analyze sentiment for this mention
                    sentiment = self._analyze_text_sentiment(text_lower, keyword)
                    category_sentiment += sentiment
        
        # Calculate category score (0-10 scale)
        if category_mentions > 0:
            # Base score on mention frequency and sentiment
            mention_score = min(category_mentions / 5, 5.0)  # Cap at 5
            sentiment_score = max(-2.0, min(2.0, category_sentiment / category_mentions))  # -2 to 2 range
            
            # Combine scores
            category_score = 5.0 + mention_score + sentiment_score
            
            # Generate insights
            if category_mentions >= 3:
                insights.append(f"High {category} activity detected")
            elif category_mentions >= 1:
                insights.append(f"Moderate {category} activity detected")
            
            if sentiment_score > 0.5:
                insights.append(f"Positive {category} sentiment")
            elif sentiment_score < -0.5:
                insights.append(f"Negative {category} sentiment")
            else:
                insights.append(f"Neutral {category} sentiment")
        else:
            category_score = 5.0  # Neutral score
            insights.append(f"No significant {category} factors detected")
        
        return {
            "score": float(max(0.0, min(10.0, category_score))),
            "mentions": category_mentions,
            "sentiment": float(category_sentiment / category_mentions if category_mentions > 0 else 0),
            "insights": insights
        }

    def _analyze_text_sentiment(self, text: str, keyword: str) -> float:
        """Analyze sentiment around a specific keyword."""
        # Simple sentiment analysis based on surrounding context
        positive_words = ["positive", "good", "beneficial", "favorable", "growth", "increase", "improve"]
        negative_words = ["negative", "bad", "harmful", "unfavorable", "decline", "decrease", "worse"]
        
        # Find keyword position and analyze surrounding context
        keyword_pos = text.lower().find(keyword.lower())
        if keyword_pos == -1:
            return 0.0
        
        # Analyze context within 100 characters of keyword
        start = max(0, keyword_pos - 50)
        end = min(len(text), keyword_pos + len(keyword) + 50)
        context = text[start:end].lower()
        
        positive_count = sum(1 for word in positive_words if word in context)
        negative_count = sum(1 for word in negative_words if word in context)
        
        if positive_count > negative_count:
            return 1.0
        elif negative_count > positive_count:
            return -1.0
        else:
            return 0.0

    def _calculate_confidence(self, texts: List[str], category_scores: Dict[str, float]) -> float:
        """Calculate confidence in PESTLE analysis."""
        if not texts:
            return 0.0
        
        # Base confidence on text count and score consistency
        text_confidence = min(len(texts) / 20, 1.0)  # More texts = higher confidence
        
        # Score consistency (lower variance = higher confidence)
        scores = list(category_scores.values())
        if len(scores) > 1:
            consistency = 1.0 - (np.std(scores) / 10)  # Normalize to 0-1
        else:
            consistency = 0.5
        
        # Weighted confidence
        confidence = (text_confidence * 0.7) + (consistency * 0.3)
        return float(max(0.0, min(1.0, confidence)))

    def _generate_overall_insights(self, category_scores: Dict[str, float], category_insights: Dict[str, List[str]]) -> List[str]:
        """Generate overall PESTLE insights."""
        insights = []
        
        # Identify dominant factors
        high_scores = [(cat, score) for cat, score in category_scores.items() if score >= 7.0]
        low_scores = [(cat, score) for cat, score in category_scores.items() if score <= 3.0]
        
        if high_scores:
            high_categories = [cat.replace('_', ' ').title() for cat, _ in high_scores]
            insights.append(f"Strong impact factors: {', '.join(high_categories)}")
        
        if low_scores:
            low_categories = [cat.replace('_', ' ').title() for cat, _ in low_scores]
            insights.append(f"Minimal impact factors: {', '.join(low_categories)}")
        
        # Overall assessment
        avg_score = np.mean(list(category_scores.values()))
        if avg_score >= 7.0:
            insights.append("Overall high external environment impact")
        elif avg_score <= 3.0:
            insights.append("Overall low external environment impact")
        else:
            insights.append("Moderate external environment impact")
        
        return insights
