import asyncio
import httpx
from typing import Dict, Any, List
from datetime import datetime
import openai
from .base_agent import BaseResearchAgent
from ..utils.nlp import QueryParser
from config import settings

class ConsumerInsightsAgent(BaseResearchAgent):
    """Agent for gathering consumer insights, sentiment, and behavior data"""
    
    def __init__(self):
        super().__init__()
        self.query_parser = QueryParser()
        
    async def research(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct comprehensive consumer research using multiple sources"""
        try:
            # Execute multiple research tasks in parallel
            research_tasks = [
                self._social_media_analysis(query, context),
                self._review_analysis(query, context),
                self._consumer_surveys(query, context),
                self._behavioral_data(query, context),
                self._sentiment_analysis(query, context)
            ]
            
            results = await asyncio.gather(*research_tasks, return_exceptions=True)
            
            # Combine and synthesize results
            combined_data = self._synthesize_consumer_data(results, query)
            
            return {
                "social_media": results[0] if not isinstance(results[0], Exception) else {"error": str(results[0])},
                "reviews": results[1] if not isinstance(results[1], Exception) else {"error": str(results[1])},
                "surveys": results[2] if not isinstance(results[2], Exception) else {"error": str(results[2])},
                "behavioral": results[3] if not isinstance(results[3], Exception) else {"error": str(results[3])},
                "sentiment": results[4] if not isinstance(results[4], Exception) else {"error": str(results[4])},
                "synthesized_data": combined_data,
                "timestamp": datetime.utcnow().isoformat(),
                "confidence": self._calculate_confidence(results),
                "data_sources_count": len([r for r in results if not isinstance(r, Exception)])
            }
            
        except Exception as e:
            return {"error": str(e), "confidence": 0.0}
    
    async def _social_media_analysis(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze social media sentiment and engagement"""
        try:
            # Extract relevant keywords
            keywords = await self.query_parser.extract_keywords(query)
            
            # Search for social media discussions
            social_query = f"social media discussions about {' '.join(keywords[:3])}"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.config.TAVILY_API_KEY,
                        "query": social_query,
                        "search_depth": "advanced",
                        "include_answer": True,
                        "max_results": 5
                    }
                )
                response.raise_for_status()
                
                data = response.json()
                
                # Analyze sentiment using LLM
                sentiment_analysis = await self._analyze_social_sentiment(data.get("results", []))
                
                return {
                    "social_data": data,
                    "sentiment_analysis": sentiment_analysis,
                    "keywords_analyzed": keywords[:3]
                }
                
        except Exception as e:
            return {"error": f"Social media analysis failed: {str(e)}"}
    
    async def _review_analysis(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze product reviews and ratings"""
        try:
            keywords = await self.query_parser.extract_keywords(query)
            review_query = f"product reviews {' '.join(keywords[:3])} customer feedback"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.config.TAVILY_API_KEY,
                        "query": review_query,
                        "search_depth": "advanced",
                        "include_answer": True,
                        "max_results": 7
                    }
                )
                response.raise_for_status()
                
                data = response.json()
                
                # Extract review insights
                review_insights = await self._extract_review_insights(data.get("results", []))
                
                return {
                    "review_data": data,
                    "review_insights": review_insights,
                    "review_count": len(data.get("results", []))
                }
                
        except Exception as e:
            return {"error": f"Review analysis failed: {str(e)}"}
    
    async def _consumer_surveys(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search for consumer survey data and market research"""
        try:
            survey_query = f"consumer survey {' '.join(await self.query_parser.extract_keywords(query)[:3])} market research"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.config.TAVILY_API_KEY,
                        "query": survey_query,
                        "search_depth": "basic",
                        "include_answer": False,
                        "max_results": 5
                    }
                )
                response.raise_for_status()
                
                return response.json()
                
        except Exception as e:
            return {"error": f"Consumer survey search failed: {str(e)}"}
    
    async def _behavioral_data(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze consumer behavior patterns"""
        try:
            # This would typically involve analyzing user behavior data
            # For now, we'll search for behavioral insights
            behavior_query = f"consumer behavior patterns {' '.join(await self.query_parser.extract_keywords(query)[:3])}"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.config.TAVILY_API_KEY,
                        "query": behavior_query,
                        "search_depth": "advanced",
                        "include_answer": True,
                        "max_results": 5
                    }
                )
                response.raise_for_status()
                
                return response.json()
                
        except Exception as e:
            return {"error": f"Behavioral data analysis failed: {str(e)}"}
    
    async def _sentiment_analysis(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive sentiment analysis"""
        try:
            client = openai.AsyncOpenAI(api_key=self.config.OPENAI_API_KEY)
            
            # Get all available data for sentiment analysis
            all_data = []
            keywords = await self.query_parser.extract_keywords(query)
            
            # Create a comprehensive sentiment analysis prompt
            prompt = f"""
            Analyze the sentiment and consumer perception for: {query}
            
            Keywords: {', '.join(keywords[:5])}
            Context: {context}
            
            Provide a JSON response with:
            - overall_sentiment: -1 to 1 scale
            - consumer_confidence: 0 to 1 scale
            - key_positive_themes: list of positive aspects
            - key_negative_themes: list of negative aspects
            - purchase_intent_signals: 0 to 1 scale
            - brand_perception: 0 to 1 scale
            """
            
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            return self._parse_json_response(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"Sentiment analysis failed: {str(e)}"}
    
    async def _analyze_social_sentiment(self, social_results: List[Dict]) -> Dict[str, Any]:
        """Analyze sentiment from social media results"""
        try:
            if not social_results:
                return {"error": "No social media data available"}
            
            # Extract text content for sentiment analysis
            texts = [result.get("content", "") for result in social_results if result.get("content")]
            
            if not texts:
                return {"error": "No text content found in social media data"}
            
            # Use LLM for sentiment analysis
            client = openai.AsyncOpenAI(api_key=self.config.OPENAI_API_KEY)
            
            combined_text = " ".join(texts[:5])  # Limit to first 5 for analysis
            
            prompt = f"""
            Analyze the sentiment of the following social media content:
            
            {combined_text[:2000]}  # Limit text length
            
            Provide a JSON response with:
            - sentiment_score: -1 to 1 scale
            - engagement_level: 0 to 1 scale
            - key_topics: list of main topics discussed
            - consumer_mood: description of overall consumer sentiment
            """
            
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            return self._parse_json_response(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"Social sentiment analysis failed: {str(e)}"}
    
    async def _extract_review_insights(self, review_results: List[Dict]) -> Dict[str, Any]:
        """Extract insights from product reviews"""
        try:
            if not review_results:
                return {"error": "No review data available"}
            
            # Extract review content
            reviews = [result.get("content", "") for result in review_results if result.get("content")]
            
            if not reviews:
                return {"error": "No review content found"}
            
            # Use LLM to extract review insights
            client = openai.AsyncOpenAI(api_key=self.config.OPENAI_API_KEY)
            
            combined_reviews = " ".join(reviews[:10])  # Limit to first 10 reviews
            
            prompt = f"""
            Analyze the following product reviews and extract key insights:
            
            {combined_reviews[:3000]}  # Limit text length
            
            Provide a JSON response with:
            - average_rating: estimated rating out of 5
            - common_complaints: list of negative feedback
            - common_praises: list of positive feedback
            - improvement_areas: list of areas for improvement
            - overall_satisfaction: 0 to 1 scale
            """
            
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            return self._parse_json_response(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"Review insights extraction failed: {str(e)}"}
    
    def _synthesize_consumer_data(self, results: List[Any], query: str) -> Dict[str, Any]:
        """Synthesize consumer data from multiple sources"""
        try:
            successful_results = [r for r in results if not isinstance(r, Exception) and not r.get("error")]
            
            if not successful_results:
                return {"error": "No successful consumer research results to synthesize"}
            
            # Combine insights from different sources
            combined_insights = {
                "total_sources": len(successful_results),
                "query": query,
                "synthesis_timestamp": datetime.utcnow().isoformat(),
                "data_quality": "high" if len(successful_results) >= 3 else "medium"
            }
            
            # Merge sentiment data
            sentiment_results = [r for r in successful_results if "sentiment" in str(r)]
            if sentiment_results:
                combined_insights["sentiment_analysis"] = self._merge_sentiment_data(sentiment_results)
            
            # Merge review insights
            review_results = [r for r in successful_results if "review" in str(r)]
            if review_results:
                combined_insights["review_insights"] = self._merge_review_data(review_results)
            
            return combined_insights
            
        except Exception as e:
            return {"error": f"Consumer data synthesis failed: {str(e)}"}
    
    def _merge_sentiment_data(self, sentiment_results: List[Dict]) -> Dict[str, Any]:
        """Merge sentiment data from multiple sources"""
        # Implementation for merging sentiment data
        return {"merged_sentiment": "Combined sentiment analysis", "sources": len(sentiment_results)}
    
    def _merge_review_data(self, review_results: List[Dict]) -> Dict[str, Any]:
        """Merge review data from multiple sources"""
        # Implementation for merging review data
        return {"merged_reviews": "Combined review analysis", "sources": len(review_results)}
