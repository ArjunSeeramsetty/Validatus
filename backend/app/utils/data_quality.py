import asyncio
import re
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timedelta
import numpy as np
from urllib.parse import urlparse
import aiohttp
from textstat import flesch_reading_ease, flesch_kincaid_grade
import spacy
from transformers import pipeline

class AdvancedDataQualityAssessment:
    """Production-grade data quality assessment with comprehensive metrics"""
    
    def __init__(self):
        # Load NLP models
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback for development environments
            self.nlp = None
            
        # Initialize quality assessment models
        try:
            self.quality_classifier = pipeline(
                "text-classification",
                model="microsoft/DialoGPT-medium",
                device=-1  # CPU
            )
        except Exception:
            self.quality_classifier = None
        
        # Domain authority mapping
        self.domain_authority = {
            'bloomberg.com': 0.95, 'reuters.com': 0.95, 'wsj.com': 0.95,
            'economist.com': 0.90, 'ft.com': 0.90, 'forbes.com': 0.85,
            'mckinsey.com': 0.90, 'bcg.com': 0.90, 'deloitte.com': 0.85,
            'harvard.edu': 0.95, 'mit.edu': 0.95, 'stanford.edu': 0.95,
            'who.int': 0.90, 'worldbank.org': 0.90, 'imf.org': 0.90
        }
        
        # Quality thresholds
        self.thresholds = {
            'min_content_length': 100,
            'max_content_length': 10000,
            'min_sources': 3,
            'recency_days': 90,
            'min_domain_authority': 0.5,
            'min_readability_score': 30
        }

    async def comprehensive_quality_assessment(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct comprehensive quality assessment across all dimensions"""
        try:
            assessment_tasks = [
                self._assess_content_quality(research_data),
                self._assess_source_credibility(research_data),
                self._assess_temporal_relevance(research_data),
                self._assess_information_completeness(research_data),
                self._assess_factual_consistency(research_data),
                self._assess_linguistic_quality(research_data)
            ]
            
            results = await asyncio.gather(*assessment_tasks, return_exceptions=True)
            
            # Process results
            quality_dimensions = {
                'content_quality': results[0] if not isinstance(results[0], Exception) else 0.0,
                'source_credibility': results[1] if not isinstance(results[1], Exception) else 0.0,
                'temporal_relevance': results[2] if not isinstance(results[2], Exception) else 0.0,
                'information_completeness': results[3] if not isinstance(results[3], Exception) else 0.0,
                'factual_consistency': results[4] if not isinstance(results[4], Exception) else 0.0,
                'linguistic_quality': results[5] if not isinstance(results[5], Exception) else 0.0
            }
            
            # Calculate weighted overall score
            weights = {
                'content_quality': 0.25,
                'source_credibility': 0.20,
                'temporal_relevance': 0.15,
                'information_completeness': 0.15,
                'factual_consistency': 0.15,
                'linguistic_quality': 0.10
            }
            
            overall_score = sum(
                quality_dimensions[dimension] * weights[dimension]
                for dimension in quality_dimensions
            )
            
            return {
                'overall_quality_score': overall_score,
                'quality_grade': self._assign_quality_grade(overall_score),
                'detailed_assessment': quality_dimensions,
                'improvement_recommendations': self._generate_improvement_recommendations(quality_dimensions),
                'data_reliability_index': self._calculate_reliability_index(quality_dimensions),
                'assessment_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'overall_quality_score': 0.0,
                'error': str(e),
                'quality_grade': 'F',
                'assessment_timestamp': datetime.utcnow().isoformat()
            }

    async def _assess_content_quality(self, research_data: Dict[str, Any]) -> float:
        """Assess content quality using multiple linguistic and semantic metrics"""
        try:
            content_texts = self._extract_content_texts(research_data)
            
            if not content_texts:
                return 0.0
            
            quality_scores = []
            
            for text in content_texts:
                if len(text) < self.thresholds['min_content_length']:
                    continue
                    
                score = 0.0
                
                # Length appropriateness (0.2 weight)
                length_score = self._score_content_length(text)
                score += length_score * 0.2
                
                # Readability assessment (0.3 weight)
                readability_score = self._score_readability(text)
                score += readability_score * 0.3
                
                # Information density (0.2 weight)
                density_score = self._score_information_density(text)
                score += density_score * 0.2
                
                # Structural quality (0.15 weight)
                structure_score = self._score_text_structure(text)
                score += structure_score * 0.15
                
                # Factual content presence (0.15 weight)
                factual_score = self._score_factual_content(text)
                score += factual_score * 0.15
                
                quality_scores.append(min(score, 1.0))
            
            return float(np.mean(quality_scores)) if quality_scores else 0.0
            
        except Exception as e:
            return 0.0

    def _extract_content_texts(self, research_data: Dict[str, Any]) -> List[str]:
        """Extract all text content from research data"""
        texts = []
        
        def extract_text_recursive(obj):
            if isinstance(obj, str):
                texts.append(obj)
            elif isinstance(obj, dict):
                for value in obj.values():
                    extract_text_recursive(value)
            elif isinstance(obj, list):
                for item in obj:
                    extract_text_recursive(item)
        
        extract_text_recursive(research_data)
        return texts

    def _score_content_length(self, text: str) -> float:
        """Score content length appropriateness"""
        length = len(text)
        
        if length < self.thresholds['min_content_length']:
            return 0.0
        elif length > self.thresholds['max_content_length']:
            return 0.5
        elif self.thresholds['min_content_length'] <= length <= 2000:
            return 1.0
        else:
            # Gradual decrease for very long content
            return max(0.5, 1.0 - (length - 2000) / 8000)

    def _score_readability(self, text: str) -> float:
        """Score text readability using multiple metrics"""
        try:
            # Flesch Reading Ease (0-100 scale)
            ease_score = flesch_reading_ease(text)
            # Normalize to 0-1 scale (30-70 is good range)
            normalized_ease = max(0, min(1, (ease_score - 30) / 40))
            
            # Flesch-Kincaid Grade Level
            grade_level = flesch_kincaid_grade(text)
            # Normalize (8-12 grade level is ideal for business content)
            normalized_grade = max(0, min(1, 1 - abs(grade_level - 10) / 10))
            
            return (normalized_ease + normalized_grade) / 2
            
        except Exception:
            return 0.5  # Default moderate score

    def _score_information_density(self, text: str) -> float:
        """Score information density using entity recognition and keyword analysis"""
        try:
            if not self.nlp:
                return 0.5  # Default score if NLP model unavailable
                
            doc = self.nlp(text)
            
            # Count entities (organizations, people, locations, etc.)
            entities = len([ent for ent in doc.ents if ent.label_ in 
                          ['ORG', 'PERSON', 'GPE', 'MONEY', 'PERCENT', 'DATE']])
            
            # Count numerical data
            numbers = len(re.findall(r'\b\d+(?:\.\d+)?\b', text))
            
            # Calculate density score
            text_length = len(text.split())
            if text_length == 0:
                return 0.0
                
            entity_density = entities / text_length * 100
            number_density = numbers / text_length * 100
            
            # Normalize (good density is 2-8 entities per 100 words)
            normalized_entity = min(1.0, entity_density / 8)
            normalized_number = min(1.0, number_density / 5)
            
            return (normalized_entity + normalized_number) / 2
            
        except Exception:
            return 0.5

    def _score_text_structure(self, text: str) -> float:
        """Score text structural quality"""
        try:
            score = 0.0
            
            # Check for paragraphs
            paragraphs = text.split('\n\n')
            if len(paragraphs) > 1:
                score += 0.3
            
            # Check for bullet points or lists
            if any(char in text for char in ['•', '-', '*', '1.', '2.']):
                score += 0.2
            
            # Check for headers
            if any(line.strip().endswith(':') for line in text.split('\n')):
                score += 0.2
            
            # Check for balanced sentence lengths
            sentences = text.split('. ')
            if sentences:
                avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
                if 10 <= avg_sentence_length <= 25:
                    score += 0.3
            
            return min(1.0, score)
            
        except Exception:
            return 0.5

    def _score_factual_content(self, text: str) -> float:
        """Score presence of factual content"""
        try:
            score = 0.0
            
            # Check for specific data points
            if re.search(r'\d+%', text):
                score += 0.3
            
            if re.search(r'\$\d+', text):
                score += 0.2
            
            if re.search(r'\d{4}', text):  # Years
                score += 0.2
            
            # Check for citations or references
            if any(term in text.lower() for term in ['according to', 'study shows', 'research indicates']):
                score += 0.3
            
            return min(1.0, score)
            
        except Exception:
            return 0.5

    async def _assess_source_credibility(self, research_data: Dict[str, Any]) -> float:
        """Assess credibility of sources using domain authority and verification"""
        try:
            sources = self._extract_sources(research_data)
            
            if not sources:
                return 0.0
            
            credibility_scores = []
            
            for source in sources:
                try:
                    domain = urlparse(source).netloc.lower()
                    
                    # Domain authority score
                    authority_score = self.domain_authority.get(domain, 0.3)
                    
                    # Additional credibility factors
                    https_score = 0.1 if source.startswith('https://') else 0.0
                    
                    # Check for academic/government domains
                    academic_score = 0.2 if any(tld in domain for tld in ['.edu', '.gov', '.org']) else 0.0
                    
                    total_score = min(1.0, authority_score + https_score + academic_score)
                    credibility_scores.append(total_score)
                    
                except Exception:
                    credibility_scores.append(0.3)  # Default low score for problematic URLs
            
            return float(np.mean(credibility_scores))
            
        except Exception:
            return 0.0

    def _extract_sources(self, research_data: Dict[str, Any]) -> List[str]:
        """Extract all source URLs from research data"""
        sources = []
        
        def extract_sources_recursive(obj):
            if isinstance(obj, str) and obj.startswith('http'):
                sources.append(obj)
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    if key in ['url', 'source', 'citation', 'reference']:
                        if isinstance(value, str) and value.startswith('http'):
                            sources.append(value)
                    else:
                        extract_sources_recursive(value)
            elif isinstance(obj, list):
                for item in obj:
                    extract_sources_recursive(item)
        
        extract_sources_recursive(research_data)
        return sources

    async def _assess_temporal_relevance(self, research_data: Dict[str, Any]) -> float:
        """Assess temporal relevance of research data"""
        try:
            # Extract dates from research data
            dates = self._extract_dates(research_data)
            
            if not dates:
                return 0.5  # Default moderate score if no dates found
            
            current_date = datetime.utcnow()
            relevance_scores = []
            
            for date_str in dates:
                try:
                    # Parse date (handle multiple formats)
                    parsed_date = self._parse_date(date_str)
                    if parsed_date:
                        days_old = (current_date - parsed_date).days
                        
                        if days_old <= 30:
                            relevance_scores.append(1.0)
                        elif days_old <= 90:
                            relevance_scores.append(0.8)
                        elif days_old <= 180:
                            relevance_scores.append(0.6)
                        elif days_old <= 365:
                            relevance_scores.append(0.4)
                        else:
                            relevance_scores.append(0.2)
                            
                except Exception:
                    continue
            
            return float(np.mean(relevance_scores)) if relevance_scores else 0.5
            
        except Exception:
            return 0.5

    def _extract_dates(self, research_data: Dict[str, Any]) -> List[str]:
        """Extract date strings from research data"""
        dates = []
        
        def extract_dates_recursive(obj):
            if isinstance(obj, str):
                # Look for date patterns
                date_patterns = [
                    r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
                    r'\d{2}/\d{2}/\d{4}',   # MM/DD/YYYY
                    r'\d{4}',               # Year only
                ]
                
                for pattern in date_patterns:
                    matches = re.findall(pattern, obj)
                    dates.extend(matches)
                    
            elif isinstance(obj, dict):
                for value in obj.values():
                    extract_dates_recursive(value)
            elif isinstance(obj, list):
                for item in obj:
                    extract_dates_recursive(item)
        
        extract_dates_recursive(research_data)
        return list(set(dates))  # Remove duplicates

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string in multiple formats"""
        try:
            # Try different date formats
            formats = [
                '%Y-%m-%d',
                '%m/%d/%Y',
                '%Y',
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            return None
            
        except Exception:
            return None

    async def _assess_information_completeness(self, research_data: Dict[str, Any]) -> float:
        """Assess completeness of information provided"""
        try:
            completeness_scores = []
            
            # Check for different types of information
            info_types = {
                'quantitative_data': ['market_size', 'growth_rate', 'revenue', 'percentage'],
                'qualitative_insights': ['trends', 'analysis', 'insights', 'recommendations'],
                'competitive_info': ['competitors', 'market_share', 'competitive_advantage'],
                'market_context': ['industry', 'geography', 'regulations', 'risks']
            }
            
            for info_type, keywords in info_types.items():
                score = self._check_info_type_presence(research_data, keywords)
                completeness_scores.append(score)
            
            return float(np.mean(completeness_scores))
            
        except Exception:
            return 0.5

    def _check_info_type_presence(self, data: Dict[str, Any], keywords: List[str]) -> float:
        """Check presence of specific information type"""
        try:
            data_str = str(data).lower()
            matches = sum(1 for keyword in keywords if keyword in data_str)
            return min(1.0, matches / len(keywords))
            
        except Exception:
            return 0.0

    async def _assess_factual_consistency(self, research_data: Dict[str, Any]) -> float:
        """Assess factual consistency across different sources"""
        try:
            # Extract numerical data points
            numerical_data = self._extract_numerical_data(research_data)
            
            if len(numerical_data) < 2:
                return 0.5  # Need at least 2 data points to assess consistency
            
            # Check for consistency in similar metrics
            consistency_scores = []
            
            # Group by metric type
            metric_groups = self._group_numerical_metrics(numerical_data)
            
            for metric_type, values in metric_groups.items():
                if len(values) > 1:
                    consistency = self._calculate_metric_consistency(values)
                    consistency_scores.append(consistency)
            
            return float(np.mean(consistency_scores)) if consistency_scores else 0.5
            
        except Exception:
            return 0.5

    def _extract_numerical_data(self, research_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract numerical data points from research data"""
        numerical_data = []
        
        def extract_numbers_recursive(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    extract_numbers_recursive(value, current_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    current_path = f"{path}[{i}]"
                    extract_numbers_recursive(item, current_path)
            elif isinstance(obj, (int, float)):
                numerical_data.append({
                    'value': obj,
                    'path': path,
                    'type': 'number'
                })
            elif isinstance(obj, str):
                # Look for percentage patterns
                percentage_match = re.search(r'(\d+(?:\.\d+)?)%', obj)
                if percentage_match:
                    numerical_data.append({
                        'value': float(percentage_match.group(1)),
                        'path': path,
                        'type': 'percentage'
                    })
                
                # Look for currency patterns
                currency_match = re.search(r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)', obj)
                if currency_match:
                    value_str = currency_match.group(1).replace(',', '')
                    numerical_data.append({
                        'value': float(value_str),
                        'path': path,
                        'type': 'currency'
                    })
        
        extract_numbers_recursive(research_data)
        return numerical_data

    def _group_numerical_metrics(self, numerical_data: List[Dict[str, Any]]) -> Dict[str, List[float]]:
        """Group numerical data by metric type"""
        groups = {}
        
        for item in numerical_data:
            metric_type = self._categorize_metric(item['path'])
            if metric_type not in groups:
                groups[metric_type] = []
            groups[metric_type].append(item['value'])
        
        return groups

    def _categorize_metric(self, path: str) -> str:
        """Categorize metric based on path"""
        path_lower = path.lower()
        
        if any(term in path_lower for term in ['market', 'size', 'value']):
            return 'market_size'
        elif any(term in path_lower for term in ['growth', 'rate', 'cagr']):
            return 'growth_rate'
        elif any(term in path_lower for term in ['revenue', 'sales', 'income']):
            return 'revenue'
        elif any(term in path_lower for term in ['percentage', 'percent', '%']):
            return 'percentage'
        else:
            return 'other'

    def _calculate_metric_consistency(self, values: List[float]) -> float:
        """Calculate consistency score for a group of values"""
        try:
            if len(values) < 2:
                return 1.0
            
            mean_value = np.mean(values)
            std_dev = np.std(values)
            
            if mean_value == 0:
                return 1.0 if std_dev == 0 else 0.0
            
            # Coefficient of variation (lower is more consistent)
            cv = std_dev / abs(mean_value)
            
            # Convert to consistency score (0-1, higher is more consistent)
            consistency = max(0, 1 - cv)
            
            return min(1.0, consistency)
            
        except Exception:
            return 0.5

    async def _assess_linguistic_quality(self, research_data: Dict[str, Any]) -> float:
        """Assess linguistic quality of research data"""
        try:
            content_texts = self._extract_content_texts(research_data)
            
            if not content_texts:
                return 0.5
            
            linguistic_scores = []
            
            for text in content_texts:
                if len(text) < 50:  # Skip very short texts
                    continue
                
                score = 0.0
                
                # Grammar and spelling (basic check)
                grammar_score = self._assess_basic_grammar(text)
                score += grammar_score * 0.4
                
                # Professional language
                professional_score = self._assess_professional_language(text)
                score += professional_score * 0.3
                
                # Clarity and coherence
                clarity_score = self._assess_text_clarity(text)
                score += clarity_score * 0.3
                
                linguistic_scores.append(score)
            
            return float(np.mean(linguistic_scores)) if linguistic_scores else 0.5
            
        except Exception:
            return 0.5

    def _assess_basic_grammar(self, text: str) -> float:
        """Basic grammar assessment"""
        try:
            score = 1.0
            
            # Check for common issues
            sentences = text.split('. ')
            
            for sentence in sentences:
                if sentence and not sentence[0].isupper():
                    score -= 0.1
                
                if sentence and not sentence.endswith(('.', '!', '?')):
                    score -= 0.1
            
            return max(0.0, score)
            
        except Exception:
            return 0.5

    def _assess_professional_language(self, text: str) -> float:
        """Assess use of professional business language"""
        try:
            professional_terms = [
                'analysis', 'strategy', 'market', 'business', 'industry',
                'competitive', 'strategic', 'opportunity', 'challenge',
                'growth', 'development', 'innovation', 'leadership'
            ]
            
            text_lower = text.lower()
            professional_count = sum(1 for term in professional_terms if term in text_lower)
            
            # Normalize score
            max_expected = min(len(professional_terms), len(text.split()) // 20)
            if max_expected == 0:
                return 0.5
            
            score = min(1.0, professional_count / max_expected)
            return score
            
        except Exception:
            return 0.5

    def _assess_text_clarity(self, text: str) -> float:
        """Assess text clarity and coherence"""
        try:
            score = 1.0
            
            # Check sentence length variety
            sentences = text.split('. ')
            if sentences:
                sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
                if sentence_lengths:
                    avg_length = np.mean(sentence_lengths)
                    if avg_length > 30:  # Very long sentences
                        score -= 0.3
                    elif avg_length < 5:  # Very short sentences
                        score -= 0.2
            
            # Check for repetitive words
            words = text.lower().split()
            if len(words) > 10:
                word_freq = {}
                for word in words:
                    if len(word) > 3:  # Skip short words
                        word_freq[word] = word_freq.get(word, 0) + 1
                
                max_freq = max(word_freq.values()) if word_freq else 0
                if max_freq > len(words) * 0.1:  # More than 10% repetition
                    score -= 0.2
            
            return max(0.0, score)
            
        except Exception:
            return 0.5

    def _assign_quality_grade(self, score: float) -> str:
        """Assign letter grade based on quality score"""
        if score >= 0.9:
            return 'A+'
        elif score >= 0.85:
            return 'A'
        elif score >= 0.8:
            return 'A-'
        elif score >= 0.75:
            return 'B+'
        elif score >= 0.7:
            return 'B'
        elif score >= 0.65:
            return 'B-'
        elif score >= 0.6:
            return 'C+'
        elif score >= 0.55:
            return 'C'
        elif score >= 0.5:
            return 'C-'
        elif score >= 0.4:
            return 'D'
        else:
            return 'F'

    def _generate_improvement_recommendations(self, quality_dimensions: Dict[str, float]) -> List[str]:
        """Generate specific recommendations based on quality assessment"""
        recommendations = []
        
        if quality_dimensions['content_quality'] < 0.6:
            recommendations.append("Improve content quality by seeking more detailed, well-structured sources")
        
        if quality_dimensions['source_credibility'] < 0.7:
            recommendations.append("Include more authoritative sources from recognized industry publications")
        
        if quality_dimensions['temporal_relevance'] < 0.6:
            recommendations.append("Focus on more recent sources to ensure current market conditions")
        
        if quality_dimensions['information_completeness'] < 0.7:
            recommendations.append("Gather additional data points to provide more comprehensive analysis")
        
        if quality_dimensions['factual_consistency'] < 0.6:
            recommendations.append("Verify data consistency across multiple sources")
        
        if quality_dimensions['linguistic_quality'] < 0.6:
            recommendations.append("Improve language quality and professional terminology usage")
        
        return recommendations

    def _calculate_reliability_index(self, quality_dimensions: Dict[str, float]) -> float:
        """Calculate overall data reliability index"""
        try:
            # Weight factors for reliability calculation
            reliability_weights = {
                'source_credibility': 0.35,
                'factual_consistency': 0.25,
                'temporal_relevance': 0.20,
                'content_quality': 0.20
            }
            
            reliability_score = sum(
                quality_dimensions[dimension] * reliability_weights[dimension]
                for dimension in reliability_weights
                if dimension in quality_dimensions
            )
            
            return min(1.0, reliability_score)
            
        except Exception:
            return 0.5
