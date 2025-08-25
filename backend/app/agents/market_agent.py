import asyncio
import httpx
from typing import Dict, Any, List
from datetime import datetime
import openai
from .base_agent import BaseResearchAgent
from ..utils.nlp import QueryParser
from config import settings

class MarketResearchAgent(BaseResearchAgent):
    """Specialized agent for market research and analysis with multiple data sources"""
    
    def __init__(self):
        super().__init__()
        self.query_parser = QueryParser()
        
    async def research(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct comprehensive market research using multiple sources"""
        try:
            # Execute multiple research tasks in parallel
            research_tasks = [
                self._web_search_tavily(query, context),
                self._web_search_alternative(query, context),
                self._analyze_trends(query, context),
                self._market_sizing_llm(query, context),
                self._industry_reports(query, context)
            ]
            
            results = await asyncio.gather(*research_tasks, return_exceptions=True)
            
            # Combine and validate results from multiple sources
            combined_data = self._synthesize_results(results, query)
            
            return {
                "web_research": results[0] if not isinstance(results[0], Exception) else {"error": str(results[0])},
                "alternative_search": results[1] if not isinstance(results[1], Exception) else {"error": str(results[1])},
                "trends_analysis": results[2] if not isinstance(results[2], Exception) else {"error": str(results[2])},
                "market_sizing": results[3] if not isinstance(results[3], Exception) else {"error": str(results[3])},
                "industry_reports": results[4] if not isinstance(results[4], Exception) else {"error": str(results[4])},
                "synthesized_data": combined_data,
                "timestamp": datetime.utcnow().isoformat(),
                "confidence": self._calculate_confidence(results),
                "data_sources_count": len([r for r in results if not isinstance(r, Exception)])
            }
            
        except Exception as e:
            return {"error": str(e), "confidence": 0.0}
    
    async def _web_search_tavily(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform web search using Tavily API"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.config.TAVILY_API_KEY,
                        "query": query,
                        "search_depth": "advanced",
                        "include_answer": True,
                        "max_results": 10
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": f"Tavily search failed: {str(e)}", "results": []}
    
    async def _web_search_alternative(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Alternative web search using different approach for redundancy"""
        try:
            # This could be another search API or web scraping approach
            # For now, we'll simulate with a different query variation
            alternative_query = f"{query} market analysis 2024"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.config.TAVILY_API_KEY,
                        "query": alternative_query,
                        "search_depth": "basic",
                        "include_answer": False,
                        "max_results": 5
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": f"Alternative search failed: {str(e)}", "results": []}
    
    async def _analyze_trends(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market trends using multiple approaches"""
        try:
            # Extract keywords for trend analysis
            keywords = await self.query_parser.extract_keywords(query)
            geography = context.get("geography", [""])
            
            # Use Google Trends (simplified for demo)
            trend_data = await self._get_google_trends(keywords[:3], geography)
            
            # Use news API for recent trends
            news_trends = await self._get_news_trends(keywords, geography)
            
            return {
                "google_trends": trend_data,
                "news_trends": news_trends,
                "keywords_analyzed": keywords[:3]
            }
        except Exception as e:
            return {"error": f"Trend analysis failed: {str(e)}"}

    async def _market_sizing_llm(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate market size using LLM with structured output"""
        try:
            client = openai.AsyncOpenAI(api_key=self.config.OPENAI_API_KEY)
            
            sizing_prompt = f"""
            Based on the query '{query}' and context {context}, provide market size estimates.
            Respond in JSON format with keys: 'tam', 'sam', 'som' (in USD), 'cagr' (percentage), 'key_drivers', 'data_sources', and 'confidence_level'.
            """
            
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": sizing_prompt}],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            return self._parse_json_response(response.choices[0].message.content)
        except Exception as e:
            return {"error": f"Market sizing failed: {str(e)}"}

    async def _industry_reports(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search for industry reports and expert analysis"""
        try:
            industry_query = f"industry report {query} market analysis"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.config.TAVILY_API_KEY,
                        "query": industry_query,
                        "search_depth": "advanced",
                        "include_answer": True,
                        "max_results": 5
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": f"Industry reports search failed: {str(e)}", "results": []}

    def _synthesize_results(self, results: List[Any], query: str) -> Dict[str, Any]:
        """Synthesize results from multiple sources for better accuracy"""
        try:
            # Extract successful results
            successful_results = [r for r in results if not isinstance(r, Exception) and not r.get("error")]
            
            if not successful_results:
                return {"error": "No successful research results to synthesize"}
            
            # Combine data from multiple sources
            combined_data = {
                "total_sources": len(successful_results),
                "query": query,
                "synthesis_timestamp": datetime.utcnow().isoformat()
            }
            
            # Merge market sizing data if available
            market_sizing_results = [r for r in successful_results if "tam" in str(r)]
            if market_sizing_results:
                combined_data["market_sizing"] = self._merge_market_sizing(market_sizing_results)
            
            # Merge trend data if available
            trend_results = [r for r in successful_results if "trends" in str(r)]
            if trend_results:
                combined_data["trends"] = self._merge_trend_data(trend_results)
            
            # Calculate overall confidence based on source agreement
            combined_data["overall_confidence"] = self._calculate_source_agreement(successful_results)
            
            return combined_data
            
        except Exception as e:
            return {"error": f"Result synthesis failed: {str(e)}"}

    def _merge_market_sizing(self, sizing_results: List[Dict]) -> Dict[str, Any]:
        """Merge market sizing data from multiple sources"""
        if not sizing_results:
            return {}
        
        # Calculate average values with confidence weighting
        total_tam = 0
        total_sam = 0
        total_som = 0
        total_cagr = 0
        total_confidence = 0
        
        for result in sizing_results:
            if isinstance(result, dict):
                confidence = result.get("confidence_level", 0.5)
                total_confidence += confidence
                
                if "tam" in result:
                    total_tam += result["tam"] * confidence
                if "sam" in result:
                    total_sam += result["sam"] * confidence
                if "som" in result:
                    total_som += result["som"] * confidence
                if "cagr" in result:
                    total_cagr += result["cagr"] * confidence
        
        if total_confidence > 0:
            return {
                "tam": round(total_tam / total_confidence, 2),
                "sam": round(total_sam / total_confidence, 2),
                "som": round(total_som / total_confidence, 2),
                "cagr": round(total_cagr / total_confidence, 2),
                "sources_used": len(sizing_results)
            }
        
        return {}

    def _merge_trend_data(self, trend_results: List[Dict]) -> Dict[str, Any]:
        """Merge trend data from multiple sources"""
        # Implementation for merging trend data
        return {"merged_trends": "Combined trend analysis", "sources": len(trend_results)}

    def _calculate_source_agreement(self, results: List[Dict]) -> float:
        """Calculate confidence based on agreement between sources"""
        if len(results) <= 1:
            return 0.5
        
        # Simple agreement calculation - can be enhanced with more sophisticated logic
        return min(0.9, 0.5 + (len(results) * 0.1))

    async def _get_google_trends(self, keywords: List[str], geography: List[str]) -> Dict[str, Any]:
        """Get Google Trends data (simplified implementation)"""
        # This would use pytrends in a thread pool for production
        return {"trend_data": "Google Trends data", "keywords": keywords}

    async def _get_news_trends(self, keywords: List[str], geography: List[str]) -> Dict[str, Any]:
        """Get recent news trends"""
        # This would use a news API
        return {"news_trends": "Recent news analysis", "keywords": keywords}
