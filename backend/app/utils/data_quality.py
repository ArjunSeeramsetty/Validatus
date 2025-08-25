from typing import Dict, Any, List, Tuple
import re
from datetime import datetime, timedelta
import numpy as np
from urllib.parse import urlparse
import asyncio

class DataQualityAssessment:
    """Advanced data quality assessment for research results"""
    
    def __init__(self):
        self.trusted_domains = {
            "news": ["reuters.com", "bloomberg.com", "wsj.com", "ft.com", "economist.com"],
            "research": ["statista.com", "mckinsey.com", "deloitte.com", "pwc.com", "bcg.com"],
            "government": [".gov", "worldbank.org", "imf.org", "oecd.org"],
            "academic": [".edu", "scholar.google.com", "jstor.org", "pubmed.ncbi.nlm.nih.gov"]
        }
        
        self.quality_thresholds = {
            "minimum_sources": 3,
            "recency_days": 90,
            "source_diversity": 0.6,
            "content_length_min": 50,
            "domain_trust_weight": 0.3
        }

    async def assess_research_quality(self, research_data: Dict[str, Any]) -> Dict[str, float]:
        """Comprehensive quality assessment of research data"""
        try:
            quality_metrics = {}
            
            # Parallel quality checks
            quality_tasks = [
                self._assess_source_quality(research_data),
                self._assess_content_quality(research_data),
                self._assess_temporal_quality(research_data),
                self._assess_diversity_quality(research_data),
                self._assess_consistency_quality(research_data)
            ]
            
            results = await asyncio.gather(*quality_tasks, return_exceptions=True)
            
            quality_metrics["source_quality"] = results[0] if not isinstance(results[0], Exception) else 0.0
            quality_metrics["content_quality"] = results[1] if not isinstance(results[1], Exception) else 0.0
            quality_metrics["temporal_quality"] = results[2] if not isinstance(results[2], Exception) else 0.0
            quality_metrics["diversity_quality"] = results[3] if not isinstance(results[3], Exception) else 0.0
            quality_metrics["consistency_quality"] = results[4] if not isinstance(results[4], Exception) else 0.0
            
            # Calculate overall quality score
            weights = {
                "source_quality": 0.25,
                "content_quality": 0.20,
                "temporal_quality": 0.20,
                "diversity_quality": 0.20,
                "consistency_quality": 0.15
            }
            
            overall_quality = sum(
                quality_metrics[metric] * weights[metric] 
                for metric in quality_metrics
            )
            
            return {
                "overall_quality": overall_quality,
                "detailed_metrics": quality_metrics,
                "quality_grade": self._assign_quality_grade(overall_quality),
                "improvement_recommendations": self._generate_quality_recommendations(quality_metrics)
            }
            
        except Exception as e:
            return {
                "overall_quality": 0.0,
                "error": str(e),
                "quality_grade": "F",
                "detailed_metrics": {}
            }

    async def _assess_source_quality(self, research_data: Dict[str, Any]) -> float:
        """Assess quality based on source credibility"""
        sources = self._extract_sources(research_data)
        
        if not sources:
            return 0.0
        
        source_scores = []
        
        for source in sources:
            score = 0.0
            
            # Domain trust assessment
            domain = urlparse(source).netloc.lower()
            
            for category, domains in self.trusted_domains.items():
                if any(trusted_domain in domain for trusted_domain in domains):
                    category_scores = {
                        "government": 1.0,
                        "academic": 0.9,
                        "research": 0.8,
                        "news": 0.7
                    }
                    score = category_scores.get(category, 0.5)
                    break
            else:
                # Unknown domain - assess based on TLD and other factors
                if domain.endswith('.org'):
                    score = 0.6
                elif domain.endswith('.com'):
                    score = 0.4
                else:
                    score = 0.3
            
            source_scores.append(score)
        
        return float(np.mean(source_scores)) if source_scores else 0.0

    async def _assess_content_quality(self, research_data: Dict[str, Any]) -> float:
        """Assess quality based on content characteristics"""
        contents = self._extract_content(research_data)
        
        if not contents:
            return 0.0
        
        quality_scores = []
        
        for content in contents:
            score = 0.0
            
            # Length assessment
            if len(content) >= 500:
                score += 0.3
            elif len(content) >= 200:
                score += 0.2
            elif len(content) >= 50:
                score += 0.1
            
            # Structure assessment
            if self._has_structured_content(content):
                score += 0.2
            
            # Data presence assessment
            if self._contains_numerical_data(content):
                score += 0.2
            
            # Citation assessment
            if self._contains_citations(content):
                score += 0.15
            
            # Language quality assessment
            score += self._assess_language_quality(content) * 0.15
            
            quality_scores.append(min(score, 1.0))
        
        return float(np.mean(quality_scores)) if quality_scores else 0.0

    def _has_structured_content(self, content: str) -> bool:
        """Check if content has structured elements"""
        structure_indicators = [
            r'\d+\.',  # Numbered lists
            r'•|\*',   # Bullet points
            r'\n\s*-', # Dashed lists
            r'[A-Z][a-z]+:',  # Section headers
            r'Table \d+|Figure \d+',  # Tables/figures
        ]
        
        return any(re.search(pattern, content) for pattern in structure_indicators)

    def _contains_numerical_data(self, content: str) -> bool:
        """Check if content contains quantitative data"""
        number_patterns = [
            r'\$[\d,]+(?:\.\d{2})?[MmBbKk]?',  # Monetary values
            r'\d+(?:\.\d+)?%',  # Percentages
            r'\d{1,3}(?:,\d{3})*(?:\.\d+)?',  # Large numbers
            r'\d+(?:\.\d+)?\s*(?:million|billion|thousand)',  # Spelled out numbers
        ]
        
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in number_patterns)

    def _contains_citations(self, content: str) -> bool:
        """Check if content contains citations or references"""
        citation_patterns = [
            r'\[[\d\]]+\]',  # Numbered citations
            r'\([^)]*\d{4}[^)]*\)',  # Parenthetical citations with years
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',  # URLs
        ]
        
        return any(re.search(pattern, content) for pattern in citation_patterns)

    def _assess_language_quality(self, content: str) -> float:
        """Assess language quality of content"""
        # Simple language quality assessment
        sentences = content.split('.')
        if len(sentences) < 2:
            return 0.3
        
        # Check for proper sentence structure
        proper_sentences = 0
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence[0].isupper() and len(sentence.split()) > 3:
                proper_sentences += 1
        
        return min(proper_sentences / len(sentences), 1.0)

    async def _assess_temporal_quality(self, research_data: Dict[str, Any]) -> float:
        """Assess quality based on data recency"""
        timestamps = self._extract_timestamps(research_data)
        
        if not timestamps:
            return 0.5  # Default to medium quality if no timestamps
        
        recent_count = 0
        total_count = 0
        
        for timestamp in timestamps:
            try:
                if isinstance(timestamp, str):
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    dt = timestamp
                
                age_days = (datetime.now(dt.tzinfo) - dt).days
                if age_days <= self.quality_thresholds["recency_days"]:
                    recent_count += 1
                total_count += 1
                
            except Exception:
                continue
        
        return recent_count / total_count if total_count > 0 else 0.5

    async def _assess_diversity_quality(self, research_data: Dict[str, Any]) -> float:
        """Assess quality based on source diversity"""
        sources = self._extract_sources(research_data)
        
        if not sources:
            return 0.0
        
        # Calculate domain diversity
        domains = set()
        for source in sources:
            try:
                domain = urlparse(source).netloc.lower()
                if domain:
                    domains.add(domain)
            except Exception:
                continue
        
        # Calculate diversity score
        if len(sources) >= self.quality_thresholds["minimum_sources"]:
            diversity_score = len(domains) / len(sources)
            return min(diversity_score, 1.0)
        else:
            return 0.0

    async def _assess_consistency_quality(self, research_data: Dict[str, Any]) -> float:
        """Assess quality based on data consistency"""
        # This is a simplified consistency check
        # In production, you might implement more sophisticated consistency validation
        
        # Check for conflicting information
        conflicts = 0
        total_checks = 0
        
        # Example: Check for conflicting market size estimates
        if "market_sizing" in research_data:
            sizing_data = research_data["market_sizing"]
            if "tam" in sizing_data and "sam" in sizing_data:
                tam = sizing_data["tam"]
                sam = sizing_data["sam"]
                if tam < sam:  # TAM should be larger than SAM
                    conflicts += 1
                total_checks += 1
        
        # Calculate consistency score
        if total_checks > 0:
            consistency_score = 1.0 - (conflicts / total_checks)
            return max(consistency_score, 0.0)
        else:
            return 0.5  # Default to medium consistency

    def _extract_sources(self, research_data: Dict[str, Any]) -> List[str]:
        """Extract all source URLs from research data"""
        sources = []
        
        # From web research results
        if "web_research" in research_data:
            results = research_data["web_research"].get("results", [])
            for result in results:
                if isinstance(result, dict) and "url" in result:
                    sources.append(result["url"])
        
        # From alternative sources
        if "alternative_search" in research_data:
            results = research_data["alternative_search"].get("results", [])
            for result in results:
                if isinstance(result, dict) and "url" in result:
                    sources.append(result["url"])
        
        # From industry reports
        if "industry_reports" in research_data:
            results = research_data["industry_reports"].get("results", [])
            for result in results:
                if isinstance(result, dict) and "url" in result:
                    sources.append(result["url"])
        
        return list(set(sources))  # Remove duplicates

    def _extract_content(self, research_data: Dict[str, Any]) -> List[str]:
        """Extract content from research data"""
        contents = []
        
        # From web research results
        if "web_research" in research_data:
            results = research_data["web_research"].get("results", [])
            for result in results:
                if isinstance(result, dict):
                    content = result.get("content", "") or result.get("description", "") or result.get("title", "")
                    if content:
                        contents.append(content)
        
        # From news articles
        if "news_trends" in research_data and "articles" in research_data["news_trends"]:
            articles = research_data["news_trends"]["articles"]
            for article in articles:
                if isinstance(article, dict):
                    content = article.get("content", "") or article.get("description", "") or article.get("title", "")
                    if content:
                        contents.append(content)
        
        return contents

    def _extract_timestamps(self, research_data: Dict[str, Any]) -> List[Any]:
        """Extract timestamps from research data"""
        timestamps = []
        
        # From research results
        if "timestamp" in research_data:
            timestamps.append(research_data["timestamp"])
        
        # From news articles
        if "news_trends" in research_data and "articles" in research_data["news_trends"]:
            articles = research_data["news_trends"]["articles"]
            for article in articles:
                if isinstance(article, dict) and "published_at" in article:
                    timestamps.append(article["published_at"])
        
        return timestamps

    def _assign_quality_grade(self, quality_score: float) -> str:
        """Assign a letter grade based on quality score"""
        if quality_score >= 0.9:
            return "A+"
        elif quality_score >= 0.8:
            return "A"
        elif quality_score >= 0.7:
            return "B+"
        elif quality_score >= 0.6:
            return "B"
        elif quality_score >= 0.5:
            return "C"
        elif quality_score >= 0.4:
            return "D"
        else:
            return "F"

    def _generate_quality_recommendations(self, quality_metrics: Dict[str, float]) -> List[str]:
        """Generate recommendations for improving data quality"""
        recommendations = []
        
        if quality_metrics.get("source_quality", 0) < 0.6:
            recommendations.append("Increase use of authoritative sources (government, academic, research institutions)")
        
        if quality_metrics.get("content_quality", 0) < 0.6:
            recommendations.append("Ensure content includes structured data, numerical information, and proper citations")
        
        if quality_metrics.get("temporal_quality", 0) < 0.6:
            recommendations.append("Focus on more recent data sources (within 90 days)")
        
        if quality_metrics.get("diversity_quality", 0) < 0.6:
            recommendations.append("Increase source diversity by using multiple domains and providers")
        
        if quality_metrics.get("consistency_quality", 0) < 0.6:
            recommendations.append("Validate data consistency across multiple sources")
        
        if not recommendations:
            recommendations.append("Data quality is good. Continue current research practices.")
        
        return recommendations


class AdvancedValidation:
    """Advanced validation for scoring results"""
    
    @staticmethod
    def validate_score_consistency(layer_scores: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate consistency across related scores"""
        validation_results = {
            "consistency_score": 1.0,
            "inconsistencies": [],
            "recommendations": []
        }
        
        try:
            # Check for logical inconsistencies
            inconsistencies = []
            
            # Example: High sentiment but low purchase intent
            if "sentiment" in layer_scores and "purchase_intent" in layer_scores:
                sentiment_score = layer_scores["sentiment"].get("score", 50)
                intent_score = layer_scores["purchase_intent"].get("score", 50)
                
                if sentiment_score > 80 and intent_score < 30:
                    inconsistencies.append({
                        "type": "sentiment_intent_mismatch",
                        "description": "High sentiment but low purchase intent may indicate awareness without conversion",
                        "severity": "medium"
                    })
            
            # Calculate consistency score
            consistency_penalty = len(inconsistencies) * 0.1
            validation_results["consistency_score"] = max(0, 1.0 - consistency_penalty)
            validation_results["inconsistencies"] = inconsistencies
            
        except Exception as e:
            validation_results["error"] = str(e)
        
        return validation_results
