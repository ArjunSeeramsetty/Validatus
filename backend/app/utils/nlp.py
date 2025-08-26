import asyncio
import openai
import spacy
from typing import Dict, Any, List, Optional, Tuple
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    pipeline, AutoModelForTokenClassification
)
import torch
import re
from datetime import datetime
import json
from config import settings

class ProductionNLPProcessor:
    """Advanced NLP processing for strategic analysis with production-grade models"""
    
    def __init__(self):
        # Initialize models
        self._initialize_models()
        
        # OpenAI client
        self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Strategic keywords for different domains
        self.strategic_keywords = {
            'market_size': ['market size', 'tam', 'sam', 'som', 'addressable market', 'market value'],
            'competition': ['competitor', 'competitive', 'market share', 'rivalry', 'competitive advantage'],
            'growth': ['growth', 'cagr', 'expansion', 'scaling', 'increase', 'growing'],
            'risk': ['risk', 'threat', 'challenge', 'barrier', 'obstacle', 'difficulty'],
            'opportunity': ['opportunity', 'potential', 'untapped', 'emerging', 'new market']
        }

    def _initialize_models(self):
        """Initialize all NLP models with error handling"""
        try:
            # Sentiment analysis
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Named Entity Recognition
            self.ner_pipeline = pipeline(
                "ner",
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                aggregation_strategy="simple",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Question Answering
            self.qa_pipeline = pipeline(
                "question-answering",
                model="deepset/roberta-base-squad2",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Text Summarization
            self.summarization_pipeline = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # SpaCy for linguistic analysis
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                self.nlp = None
                
        except Exception as e:
            # Fallback initialization
            self.sentiment_pipeline = None
            self.ner_pipeline = None
            self.qa_pipeline = None
            self.summarization_pipeline = None
            self.nlp = None
            print(f"Warning: NLP models initialization failed: {e}")

    async def advanced_query_parsing(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced query parsing with intent recognition and entity extraction"""
        try:
            parsing_tasks = [
                self._extract_entities(query),
                self._identify_intent(query, context),
                self._extract_strategic_keywords(query),
                self._analyze_query_complexity(query),
                self._generate_search_variations(query, context)
            ]
            
            results = await asyncio.gather(*parsing_tasks, return_exceptions=True)
            
            return {
                'entities': results[0] if not isinstance(results[0], Exception) else {},
                'intent': results[1] if not isinstance(results[1], Exception) else 'general_analysis',
                'strategic_keywords': results[2] if not isinstance(results[2], Exception) else [],
                'complexity_analysis': results[3] if not isinstance(results[3], Exception) else {},
                'search_variations': results[4] if not isinstance(results[4], Exception) else [],
                'parsed_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {'error': str(e), 'parsed_timestamp': datetime.utcnow().isoformat()}

    async def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities using BERT-based NER"""
        try:
            if not self.ner_pipeline:
                return self._fallback_entity_extraction(text)
            
            # Use transformer model for NER
            entities = self.ner_pipeline(text)
            
            # Organize entities by type
            entity_dict = {}
            for entity in entities:
                entity_type = entity['entity_group']
                entity_text = entity['word']
                
                if entity_type not in entity_dict:
                    entity_dict[entity_type] = []
                
                if entity_text not in entity_dict[entity_type]:
                    entity_dict[entity_type].append(entity_text)
            
            # Add business-specific entity extraction
            business_entities = await self._extract_business_entities(text)
            entity_dict.update(business_entities)
            
            return entity_dict
            
        except Exception as e:
            return self._fallback_entity_extraction(text)

    def _fallback_entity_extraction(self, text: str) -> Dict[str, List[str]]:
        """Fallback entity extraction using regex patterns"""
        try:
            entities = {}
            
            # Extract company names (capitalized words)
            companies = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
            if companies:
                entities['ORG'] = companies[:10]  # Limit to top 10
            
            # Extract monetary values
            money_values = re.findall(r'\$\d+(?:,\d{3})*(?:\.\d{2})?', text)
            if money_values:
                entities['MONEY'] = money_values
            
            # Extract percentages
            percentages = re.findall(r'\d+(?:\.\d+)?%', text)
            if percentages:
                entities['PERCENT'] = percentages
            
            # Extract years
            years = re.findall(r'\b(?:19|20)\d{2}\b', text)
            if years:
                entities['DATE'] = years
            
            return entities
            
        except Exception:
            return {}

    async def _extract_business_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract business-specific entities"""
        try:
            business_entities = {}
            
            # Industry terms
            industry_patterns = [
                r'\b(?:tech|technology|healthcare|finance|retail|automotive|manufacturing)\b',
                r'\b(?:SaaS|B2B|B2C|e-commerce|fintech|edtech|healthtech)\b'
            ]
            
            industries = []
            for pattern in industry_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                industries.extend(matches)
            
            if industries:
                business_entities['INDUSTRY'] = list(set(industries))
            
            # Market terms
            market_patterns = [
                r'\b(?:market|industry|sector|vertical|segment)\b',
                r'\b(?:TAM|SAM|SOM|addressable market|target market)\b'
            ]
            
            markets = []
            for pattern in market_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                markets.extend(matches)
            
            if markets:
                business_entities['MARKET_TERM'] = list(set(markets))
            
            return business_entities
            
        except Exception:
            return {}

    async def _identify_intent(self, query: str, context: Dict[str, Any]) -> str:
        """Identify strategic intent using context and query analysis"""
        try:
            # Use OpenAI for intent classification
            intent_prompt = f"""
            Analyze the following business query and classify the strategic intent.
            
            Query: "{query}"
            Context: {context}
            
            Classify into one of these intents:
            - market_analysis: Understanding market size, trends, competition
            - product_validation: Validating product-market fit, features
            - competitive_intelligence: Analyzing competitors, positioning
            - growth_strategy: Expansion, scaling, new markets
            - risk_assessment: Identifying risks, threats, challenges
            - opportunity_identification: Finding new opportunities
            - consumer_insights: Understanding customer behavior, preferences
            - brand_positioning: Brand strategy, messaging, positioning
            
            Respond with just the intent category.
            """
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o-mini",  # Cost-effective for classification
                messages=[{"role": "user", "content": intent_prompt}],
                temperature=0.1,
                max_tokens=50
            )
            
            intent = response.choices[0].message.content.strip().lower()
            
            # Validate intent
            valid_intents = [
                'market_analysis', 'product_validation', 'competitive_intelligence',
                'growth_strategy', 'risk_assessment', 'opportunity_identification',
                'consumer_insights', 'brand_positioning'
            ]
            
            return intent if intent in valid_intents else 'general_analysis'
            
        except Exception:
            return 'general_analysis'

    async def _extract_strategic_keywords(self, text: str) -> List[Dict[str, Any]]:
        """Extract strategic keywords with relevance scoring"""
        try:
            extracted_keywords = []
            
            for category, keywords in self.strategic_keywords.items():
                for keyword in keywords:
                    # Case-insensitive search
                    matches = len(re.findall(keyword, text, re.IGNORECASE))
                    if matches > 0:
                        extracted_keywords.append({
                            'keyword': keyword,
                            'category': category,
                            'frequency': matches,
                            'relevance_score': self._calculate_keyword_relevance(keyword, text)
                        })
            
            # Sort by relevance
            extracted_keywords.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            return extracted_keywords[:20]  # Top 20 most relevant
            
        except Exception:
            return []

    def _calculate_keyword_relevance(self, keyword: str, text: str) -> float:
        """Calculate keyword relevance based on context and position"""
        try:
            text_lower = text.lower()
            keyword_lower = keyword.lower()
            
            # Base frequency score
            frequency = text_lower.count(keyword_lower)
            if frequency == 0:
                return 0.0
            
            # Position scoring (keywords at the beginning are more important)
            first_occurrence = text_lower.find(keyword_lower)
            position_score = 1.0 - (first_occurrence / len(text)) if len(text) > 0 else 0.5
            
            # Context scoring (keywords near other strategic terms)
            context_score = self._calculate_context_score(keyword_lower, text_lower)
            
            # Combined relevance score
            relevance = (frequency * 0.4) + (position_score * 0.3) + (context_score * 0.3)
            
            return min(1.0, relevance)
            
        except Exception:
            return 0.0

    def _calculate_context_score(self, keyword: str, text: str) -> float:
        """Calculate context score based on proximity to other strategic terms"""
        try:
            # Find all strategic terms in text
            all_strategic_terms = []
            for category_keywords in self.strategic_keywords.values():
                all_strategic_terms.extend(category_keywords)
            
            # Find positions of keyword and other strategic terms
            keyword_pos = text.find(keyword)
            if keyword_pos == -1:
                return 0.0
            
            strategic_positions = []
            for term in all_strategic_terms:
                if term != keyword:
                    pos = text.find(term)
                    if pos != -1:
                        strategic_positions.append(pos)
            
            if not strategic_positions:
                return 0.5  # No other strategic terms found
            
            # Calculate average distance to other strategic terms
            distances = [abs(keyword_pos - pos) for pos in strategic_positions]
            avg_distance = sum(distances) / len(distances)
            
            # Convert distance to score (closer = higher score)
            max_distance = len(text)
            context_score = max(0, 1 - (avg_distance / max_distance))
            
            return context_score
            
        except Exception:
            return 0.5

    async def _analyze_query_complexity(self, query: str) -> Dict[str, Any]:
        """Analyze query complexity for research planning"""
        try:
            complexity_metrics = {}
            
            # Word count
            word_count = len(query.split())
            complexity_metrics['word_count'] = word_count
            
            # Complexity score based on word count
            if word_count <= 5:
                complexity_metrics['complexity_level'] = 'simple'
                complexity_metrics['complexity_score'] = 0.3
            elif word_count <= 15:
                complexity_metrics['complexity_level'] = 'moderate'
                complexity_metrics['complexity_score'] = 0.6
            else:
                complexity_metrics['complexity_level'] = 'complex'
                complexity_metrics['complexity_score'] = 0.9
            
            # Check for specific complexity indicators
            complexity_indicators = {
                'comparison': ['vs', 'versus', 'compare', 'difference'],
                'temporal': ['trend', 'growth', 'forecast', 'prediction'],
                'analytical': ['analysis', 'research', 'study', 'investigation'],
                'quantitative': ['percentage', 'growth rate', 'market size', 'revenue']
            }
            
            indicator_scores = {}
            for indicator_type, terms in complexity_indicators.items():
                score = sum(1 for term in terms if term.lower() in query.lower())
                indicator_scores[indicator_type] = min(1.0, score / len(terms))
            
            complexity_metrics['indicator_scores'] = indicator_scores
            
            # Overall complexity adjustment
            indicator_avg = sum(indicator_scores.values()) / len(indicator_scores)
            complexity_metrics['complexity_score'] = min(1.0, 
                complexity_metrics['complexity_score'] + (indicator_avg * 0.3))
            
            return complexity_metrics
            
        except Exception:
            return {
                'complexity_level': 'unknown',
                'complexity_score': 0.5,
                'word_count': 0,
                'indicator_scores': {}
            }

    async def _generate_search_variations(self, query: str, context: Dict[str, Any]) -> List[str]:
        """Generate search variations for comprehensive research"""
        try:
            variations = []
            
            # Basic variations
            variations.append(query)
            
            # Add industry context if available
            industry = context.get('industry', '')
            if industry:
                variations.append(f"{industry} industry: {query}")
                variations.append(f"{query} in {industry} sector")
            
            # Add geography context if available
            geography = context.get('geography', [])
            if geography:
                geo_str = ', '.join(geography)
                variations.append(f"{query} in {geo_str}")
                variations.append(f"{geo_str} market: {query}")
            
            # Add company stage context if available
            company_stage = context.get('company_stage', '')
            if company_stage:
                variations.append(f"{company_stage} company: {query}")
                variations.append(f"{query} for {company_stage} businesses")
            
            # Add strategic variations
            strategic_variations = [
                f"market analysis: {query}",
                f"competitive landscape: {query}",
                f"growth opportunities: {query}",
                f"risk assessment: {query}",
                f"trend analysis: {query}"
            ]
            variations.extend(strategic_variations)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_variations = []
            for variation in variations:
                if variation not in seen:
                    seen.add(variation)
                    unique_variations.append(variation)
            
            return unique_variations[:15]  # Limit to top 15 variations
            
        except Exception:
            return [query]

    async def advanced_text_summarization(self, texts: List[str], max_length: int = 150) -> Dict[str, Any]:
        """Advanced text summarization with key insights extraction"""
        try:
            if not texts:
                return {'summary': '', 'key_insights': [], 'confidence': 0.0}
            
            # Combine texts for summarization
            combined_text = ' '.join(texts)
            
            # Truncate if too long (BART has token limits)
            if len(combined_text) > 8000:  # Conservative limit
                combined_text = combined_text[:8000] + "..."
            
            # Generate summary
            if self.summarization_pipeline:
                summary_result = self.summarization_pipeline(
                    combined_text,
                    max_length=max_length,
                    min_length=30,
                    do_sample=False
                )
                summary = summary_result[0]['summary_text']
            else:
                # Fallback summarization
                summary = await self._llm_summarization(combined_text, max_length)
            
            # Extract key insights
            key_insights = await self._extract_key_insights(combined_text)
            
            # Calculate confidence
            confidence = self._calculate_summary_confidence(summary, combined_text)
            
            return {
                'summary': summary,
                'key_insights': key_insights,
                'confidence': confidence,
                'word_count': len(summary.split()),
                'compression_ratio': len(summary) / len(combined_text) if combined_text else 0
            }
            
        except Exception as e:
            return {
                'summary': '',
                'key_insights': [],
                'confidence': 0.0,
                'error': str(e)
            }

    async def _extract_key_insights(self, text: str) -> List[str]:
        """Extract key insights from text"""
        try:
            insights = []
            
            # Split into sentences
            sentences = text.split('. ')
            
            # Score sentences based on insight indicators
            scored_sentences = []
            for sentence in sentences:
                if len(sentence.strip()) < 20:  # Skip very short sentences
                    continue
                
                score = 0
                
                # Check for insight indicators
                insight_indicators = [
                    'market size', 'growth rate', 'key player', 'trend', 'opportunity', 
                    'challenge', 'risk', 'competitive', 'innovation', 'disruption',
                    'customer', 'user', 'adoption', 'penetration', 'forecast'
                ]
                
                for indicator in insight_indicators:
                    if indicator.lower() in sentence.lower():
                        score += 1
                
                # Check for numerical data
                if re.search(r'\d+%|\$\d+|\d+\.\d+', sentence):
                    score += 2
                
                # Check for comparative terms
                if re.search(r'\b(?:vs|versus|compared|higher|lower|increase|decrease)\b', sentence, re.IGNORECASE):
                    score += 1
                
                scored_sentences.append((sentence, score))
            
            # Sort by score and take top insights
            scored_sentences.sort(key=lambda x: x[1], reverse=True)
            top_insights = [sentence for sentence, score in scored_sentences[:10] if score > 0]
            
            return top_insights
            
        except Exception:
            return []

    def _calculate_summary_confidence(self, summary: str, original_text: str) -> float:
        """Calculate confidence in summary quality"""
        try:
            if not summary or not original_text:
                return 0.0
            
            # Length appropriateness
            summary_length = len(summary.split())
            original_length = len(original_text.split())
            
            if original_length == 0:
                return 0.0
            
            compression_ratio = summary_length / original_length
            
            # Ideal compression ratio is between 0.1 and 0.3
            if 0.1 <= compression_ratio <= 0.3:
                length_score = 1.0
            elif compression_ratio < 0.1:
                length_score = compression_ratio / 0.1
            else:
                length_score = max(0, 1 - (compression_ratio - 0.3) / 0.7)
            
            # Content coverage (check if key terms from original are in summary)
            original_terms = set(original_text.lower().split())
            summary_terms = set(summary.lower().split())
            
            # Focus on important terms (longer words)
            important_terms = [term for term in original_terms if len(term) > 4]
            if important_terms:
                coverage_score = len(set(important_terms) & summary_terms) / len(important_terms)
            else:
                coverage_score = 0.5
            
            # Combined confidence
            confidence = (length_score * 0.4) + (coverage_score * 0.6)
            
            return min(1.0, confidence)
            
        except Exception:
            return 0.5

    async def _llm_summarization(self, text: str, max_length: int) -> str:
        """Fallback LLM-based summarization"""
        try:
            summarization_prompt = f"""
            Summarize the following business research text in {max_length} words or less.
            Focus on key strategic insights, market data, and actionable information.
            
            Text: {text}
            
            Summary:
            """
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": summarization_prompt}],
                temperature=0.2,
                max_tokens=max_length * 2  # Account for token vs word difference
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception:
            # Final fallback - extract first few sentences
            sentences = text.split('. ')
            return '. '.join(sentences[:3]) + '.' if sentences else text[:500]

    async def sentiment_analysis(self, texts: List[str]) -> Dict[str, Any]:
        """Perform sentiment analysis on multiple texts"""
        try:
            if not texts:
                return {'sentiment': 'neutral', 'confidence': 0.0, 'scores': []}
            
            if not self.sentiment_pipeline:
                return await self._llm_sentiment_analysis(texts)
            
            # Process texts in batches
            batch_size = 10
            all_scores = []
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                batch_results = self.sentiment_pipeline(batch)
                all_scores.extend(batch_results)
            
            # Aggregate results
            sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
            confidence_scores = []
            
            for result in all_scores:
                label = result['label'].lower()
                confidence = result['score']
                
                if 'positive' in label:
                    sentiment_counts['positive'] += 1
                elif 'negative' in label:
                    sentiment_counts['negative'] += 1
                else:
                    sentiment_counts['neutral'] += 1
                
                confidence_scores.append(confidence)
            
            # Determine overall sentiment
            total_texts = len(texts)
            if sentiment_counts['positive'] > sentiment_counts['negative']:
                overall_sentiment = 'positive'
            elif sentiment_counts['negative'] > sentiment_counts['positive']:
                overall_sentiment = 'negative'
            else:
                overall_sentiment = 'neutral'
            
            # Calculate overall confidence
            overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
            
            return {
                'sentiment': overall_sentiment,
                'confidence': overall_confidence,
                'scores': all_scores,
                'distribution': sentiment_counts,
                'total_texts': total_texts
            }
            
        except Exception as e:
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'error': str(e)
            }

    async def _llm_sentiment_analysis(self, texts: List[str]) -> Dict[str, Any]:
        """LLM-based sentiment analysis fallback"""
        try:
            # Combine texts for analysis
            combined_text = ' '.join(texts[:5])  # Limit to first 5 texts
            
            sentiment_prompt = f"""
            Analyze the sentiment of the following business text. 
            Respond with only: positive, negative, or neutral.
            
            Text: {combined_text}
            """
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": sentiment_prompt}],
                temperature=0.1,
                max_tokens=10
            )
            
            sentiment = response.choices[0].message.content.strip().lower()
            
            # Validate sentiment
            if sentiment not in ['positive', 'negative', 'neutral']:
                sentiment = 'neutral'
            
            return {
                'sentiment': sentiment,
                'confidence': 0.7,  # Lower confidence for LLM-based analysis
                'scores': [],
                'distribution': {sentiment: len(texts)},
                'total_texts': len(texts)
            }
            
        except Exception:
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'error': 'LLM sentiment analysis failed'
            }

class QueryParser:
    """Simple query parser for backward compatibility with existing code"""
    
    def __init__(self):
        self.nlp_processor = ProductionNLPProcessor()
    
    async def extract_keywords(self, query: str) -> List[str]:
        """Extract keywords from a query"""
        try:
            # Use the ProductionNLPProcessor to extract strategic keywords
            context = {}
            result = await self.nlp_processor.advanced_query_parsing(query, context)
            return result.get('strategic_keywords', [])
        except Exception:
            # Fallback: simple keyword extraction
            words = query.lower().split()
            # Filter out common stop words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            keywords = [word for word in words if word not in stop_words and len(word) > 2]
            return keywords[:10]  # Limit to 10 keywords
    
    async def parse(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Parse a query and return structured information"""
        try:
            if context is None:
                context = {}
            
            # Use the ProductionNLPProcessor for advanced parsing
            result = await self.nlp_processor.advanced_query_parsing(query, context)
            return result
        except Exception:
            # Fallback: basic parsing
            return {
                'entities': [],
                'intent': 'general_analysis',
                'strategic_keywords': await self.extract_keywords(query),
                'complexity_analysis': {'complexity': 'medium'},
                'search_variations': [query],
                'parsed_timestamp': datetime.utcnow().isoformat()
            }
