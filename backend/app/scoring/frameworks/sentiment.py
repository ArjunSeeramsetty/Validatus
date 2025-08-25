from .base_framework import BaseScoringFramework
from typing import Dict, Any, List
import re
import numpy as np

class SentimentAnalysisFramework(BaseScoringFramework):
    def __init__(self):
        # Enhanced positive and negative keywords with weights
        self.positive_keywords = {
            "excellent": 2.0, "outstanding": 2.0, "superior": 1.8, "premium": 1.5,
            "high-quality": 1.5, "best-in-class": 2.0, "amazing": 1.8, "fantastic": 1.8,
            "great": 1.5, "good": 1.0, "positive": 1.0, "satisfied": 1.2,
            "love": 1.8, "enjoy": 1.3, "recommend": 1.5, "exceeded": 1.8,
            "innovative": 1.5, "revolutionary": 1.8, "breakthrough": 1.8, "cutting-edge": 1.5,
            "reliable": 1.3, "trustworthy": 1.3, "professional": 1.2, "efficient": 1.3,
            "user-friendly": 1.2, "intuitive": 1.3, "seamless": 1.5, "smooth": 1.2
        }
        
        self.negative_keywords = {
            "poor": -2.0, "terrible": -2.0, "awful": -2.0, "horrible": -2.0,
            "bad": -1.5, "disappointing": -1.8, "frustrating": -1.5, "annoying": -1.3,
            "hate": -2.0, "dislike": -1.5, "problem": -1.0, "issue": -1.0,
            "broken": -1.8, "defective": -1.8, "faulty": -1.8, "useless": -2.0,
            "outdated": -1.5, "slow": -1.3, "buggy": -1.8, "unreliable": -1.8,
            "difficult": -1.2, "confusing": -1.3, "complicated": -1.2, "clunky": -1.5,
            "expensive": -1.0, "overpriced": -1.5, "waste": -1.8, "regret": -1.5
        }
        
        # Context-specific sentiment indicators
        self.context_keywords = {
            "quality": {
                "positive": ["excellent", "outstanding", "superior", "premium", "high-quality"],
                "negative": ["poor", "inferior", "low-quality", "substandard", "defective"]
            },
            "usability": {
                "positive": ["easy", "intuitive", "user-friendly", "seamless", "smooth"],
                "negative": ["difficult", "confusing", "complicated", "frustrating", "clunky"]
            },
            "value": {
                "positive": ["worth", "valuable", "affordable", "reasonable", "great-value"],
                "negative": ["expensive", "overpriced", "waste", "not-worth", "costly"]
            }
        }

    async def calculate_score(self, research_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced sentiment score calculation with weighted keywords and context analysis."""
        texts = self._extract_all_text_content(research_data)
        
        if not texts:
            return {"raw_score": 0, "confidence": 0, "supporting_data": {"text_count": 0}}

        # Calculate weighted sentiment scores
        sentiment_scores = []
        context_scores = {}
        mentions = 0
        
        for text in texts:
            if not text:
                continue
                
            text_lower = text.lower()
            text_score = self._calculate_text_sentiment(text_lower)
            
            if text_score != 0:
                sentiment_scores.append(text_score)
                mentions += 1
                
                # Analyze context-specific sentiment
                context_analysis = self._analyze_context_sentiment(text_lower, context)
                for context_type, score in context_analysis.items():
                    if context_type not in context_scores:
                        context_scores[context_type] = []
                    context_scores[context_type].append(score)
        
        if not sentiment_scores:
            return {"raw_score": 0, "confidence": 0, "supporting_data": {"mentions": 0}}
        
        # Calculate overall sentiment
        avg_sentiment = np.mean(sentiment_scores)
        
        # Normalize to -1 to 1 range
        normalized_sentiment = np.tanh(avg_sentiment / 2)
        
        # Calculate confidence based on data quality
        confidence = self._calculate_confidence(mentions, len(texts), sentiment_scores)
        
        # Prepare supporting data
        supporting_data = {
            "mentions": mentions,
            "text_count": len(texts),
            "context_scores": {k: np.mean(v) for k, v in context_scores.items() if v},
            "sentiment_distribution": self._analyze_sentiment_distribution(sentiment_scores),
            "keyword_analysis": self._analyze_keyword_usage(texts)
        }
        
        return {
            "raw_score": float(normalized_sentiment),  # Ranges from -1 to 1
            "confidence": float(confidence),
            "supporting_data": supporting_data
        }

    def _extract_all_text_content(self, research_data: Dict[str, Any]) -> List[str]:
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
        
        # Extract from alternative search results
        if "alternative_search" in research_data:
            results = research_data["alternative_search"].get("results", [])
            for result in results:
                if isinstance(result, dict):
                    content = result.get("content", "") or result.get("description", "") or result.get("title", "")
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
        
        # Extract from news articles
        if "news_trends" in research_data and "articles" in research_data["news_trends"]:
            articles = research_data["news_trends"]["articles"]
            for article in articles:
                if isinstance(article, dict):
                    content = article.get("content", "") or article.get("description", "") or article.get("title", "")
                    if content:
                        texts.append(content)
        
        return texts

    def _calculate_text_sentiment(self, text: str) -> float:
        """Calculate sentiment score for a single text using weighted keywords."""
        positive_score = 0
        negative_score = 0
        
        # Calculate positive sentiment
        for keyword, weight in self.positive_keywords.items():
            count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE))
            positive_score += count * weight
        
        # Calculate negative sentiment
        for keyword, weight in self.negative_keywords.items():
            count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE))
            negative_score += abs(count * weight)
        
        # Return net sentiment score
        return positive_score - negative_score

    def _analyze_context_sentiment(self, text: str, context: Dict[str, Any]) -> Dict[str, float]:
        """Analyze sentiment for specific contexts."""
        context_scores = {}
        
        for context_type, keywords in self.context_keywords.items():
            positive_count = sum(1 for word in keywords["positive"] if word in text)
            negative_count = sum(1 for word in keywords["negative"] if word in text)
            
            if positive_count > 0 or negative_count > 0:
                context_scores[context_type] = (positive_count - negative_count) / (positive_count + negative_count)
        
        return context_scores

    def _calculate_confidence(self, mentions: int, total_texts: int, scores: List[float]) -> float:
        """Calculate confidence in sentiment analysis."""
        if mentions == 0:
            return 0.0
        
        # Base confidence on mention ratio
        mention_ratio = mentions / total_texts if total_texts > 0 else 0
        
        # Confidence increases with more mentions and consistent scores
        consistency = 1.0 - np.std(scores) if len(scores) > 1 else 0.5
        
        # Weighted confidence calculation
        confidence = (mention_ratio * 0.6) + (consistency * 0.4)
        
        return min(confidence, 1.0)

    def _analyze_sentiment_distribution(self, scores: List[float]) -> Dict[str, Any]:
        """Analyze the distribution of sentiment scores."""
        if not scores:
            return {}
        
        return {
            "mean": float(np.mean(scores)),
            "std": float(np.std(scores)),
            "min": float(np.min(scores)),
            "max": float(np.max(scores)),
            "positive_count": sum(1 for s in scores if s > 0),
            "negative_count": sum(1 for s in scores if s < 0),
            "neutral_count": sum(1 for s in scores if s == 0)
        }

    def _analyze_keyword_usage(self, texts: List[str]) -> Dict[str, Any]:
        """Analyze keyword usage patterns."""
        keyword_counts = {"positive": {}, "negative": {}}
        
        # Count positive keywords
        for keyword in self.positive_keywords:
            count = sum(len(re.findall(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE)) for text in texts)
            if count > 0:
                keyword_counts["positive"][keyword] = count
        
        # Count negative keywords
        for keyword in self.negative_keywords:
            count = sum(len(re.findall(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE)) for text in texts)
            if count > 0:
                keyword_counts["negative"][keyword] = count
        
        return keyword_counts
