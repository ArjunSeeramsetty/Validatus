import asyncio
import httpx
from typing import Dict, Any, List
from datetime import datetime, timedelta
import openai
import pandas as pd
import numpy as np
from .base_agent import BaseResearchAgent
from ..utils.nlp import QueryParser
from config import settings

# Enhanced imports for production features
try:
    from pytrends.request import TrendReq
    PYTENDS_AVAILABLE = True
except ImportError:
    PYTENDS_AVAILABLE = False

try:
    from newsapi import NewsApiClient
    NEWSAPI_AVAILABLE = True
except ImportError:
    NEWSAPI_AVAILABLE = False

class MarketResearchAgent(BaseResearchAgent):
    """Specialized agent for market research and analysis with multiple data sources"""
    
    def __init__(self):
        super().__init__()
        self.query_parser = QueryParser()
        
        # Initialize enhanced data sources
        if PYTENDS_AVAILABLE:
            self.pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)
        else:
            self.pytrends = None
            
        if NEWSAPI_AVAILABLE and hasattr(settings, 'NEWS_API_KEY'):
            self.news_client = NewsApiClient(api_key=settings.NEWS_API_KEY)
        else:
            self.news_client = None
        
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
        """Analyze market trends using multiple approaches with real data"""
        try:
            # Extract keywords for trend analysis
            keywords = await self.query_parser.extract_keywords(query)
            geography = context.get("geography", ["US"])
            
            # Enhanced Google Trends analysis
            trend_data = await self._get_enhanced_google_trends(keywords[:3], geography)
            
            # Enhanced news trends analysis
            news_trends = await self._get_enhanced_news_trends(keywords, geography)
            
            # Calculate trend momentum and insights
            trend_insights = self._calculate_trend_insights(trend_data, news_trends)
            
            return {
                "google_trends": trend_data,
                "news_trends": news_trends,
                "trend_insights": trend_insights,
                "keywords_analyzed": keywords[:3],
                "overall_momentum": trend_insights.get("overall_momentum", 0),
                "trend_confidence": self._calculate_trend_confidence(trend_data, news_trends)
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
        """Enhanced Google Trends analysis with real data"""
        if not self.pytrends or not PYTENDS_AVAILABLE:
            return {"trend_data": "Google Trends not available", "keywords": keywords}
        
        try:
            # Map geography to Google Trends format
            geo_code = self._map_geography_to_trends_code(geography)
            
            # Multiple timeframes for comprehensive analysis
            timeframes = ['today 12-m', 'today 3-m', 'today 1-m']
            trend_data = {}
            
            for timeframe in timeframes:
                try:
                    self.pytrends.build_payload(
                        keywords[:5],  # Google Trends limit
                        cat=0,
                        timeframe=timeframe,
                        geo=geo_code,
                        gprop=''
                    )
                    
                    # Interest over time
                    interest_data = self.pytrends.interest_over_time()
                    if not interest_data.empty:
                        trend_data[timeframe] = {
                            "interest_over_time": interest_data.to_dict(),
                            "momentum": self._calculate_trend_momentum(interest_data),
                            "data_points": len(interest_data)
                        }
                    
                    # Related queries
                    try:
                        related_queries = self.pytrends.related_queries()
                        trend_data[timeframe]["related_queries"] = related_queries
                    except:
                        trend_data[timeframe]["related_queries"] = {}
                    
                    await asyncio.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    trend_data[timeframe] = {"error": str(e)}
            
            return {
                "trend_data": trend_data,
                "keywords_analyzed": keywords,
                "geography": geo_code
            }
            
        except Exception as e:
            return {"error": f"Google Trends analysis failed: {str(e)}"}

    async def _get_news_trends(self, keywords: List[str], geography: List[str]) -> Dict[str, Any]:
        """Enhanced news analysis using NewsAPI"""
        if not self.news_client or not NEWSAPI_AVAILABLE:
            return {"news_trends": "News API not available", "keywords": keywords}
        
        try:
            # Multiple news searches for comprehensive coverage
            news_searches = [
                {"q": " OR ".join(keywords[:3]), "language": "en", "sort_by": "relevancy"},
                {"q": " OR ".join(keywords[:3]), "language": "en", "sort_by": "publishedAt"},
                {"domains": "reuters.com,bloomberg.com,wsj.com", "q": keywords[0], "language": "en"}
            ]
            
            all_articles = []
            for search_params in news_searches:
                try:
                    response = self.news_client.get_everything(
                        **search_params,
                        from_param=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                        to=datetime.now().strftime('%Y-%m-%d'),
                        page_size=20
                    )
                    
                    if response['status'] == 'ok':
                        all_articles.extend(response['articles'])
                        
                except Exception as e:
                    continue
            
            # Process articles for insights
            processed_articles = self._process_news_articles(all_articles)
            
            return {
                "articles": processed_articles,
                "article_count": len(processed_articles),
                "sources": list(set([article.get('source', {}).get('name', '') for article in processed_articles])),
                "confidence": min(len(processed_articles) / 50, 1.0)  # Confidence based on article count
            }
            
        except Exception as e:
            return {"error": f"News analysis failed: {str(e)}"}

    def _map_geography_to_trends_code(self, geography: List[str]) -> str:
        """Map geography to Google Trends country codes"""
        if not geography:
            return "US"
        
        # Simple mapping - can be expanded
        geo_mapping = {
            "US": "US", "United States": "US", "USA": "US",
            "UK": "GB", "United Kingdom": "GB", "Great Britain": "GB",
            "CA": "CA", "Canada": "CA",
            "AU": "AU", "Australia": "AU",
            "DE": "DE", "Germany": "DE",
            "FR": "FR", "France": "FR"
        }
        
        for geo in geography:
            if geo in geo_mapping:
                return geo_mapping[geo]
        
        return "US"  # Default to US

    def _calculate_trend_momentum(self, interest_data: pd.DataFrame) -> Dict[str, float]:
        """Calculate trend momentum with statistical rigor"""
        if interest_data.empty:
            return {"momentum": 0, "direction": "neutral"}
        
        try:
            # Calculate momentum using linear regression
            for column in interest_data.columns:
                if column != 'isPartial':
                    values = interest_data[column].dropna().values
                    if len(values) > 1:
                        x = np.arange(len(values))
                        slope, _ = np.polyfit(x, values, 1)
                        
                        # Normalize slope to momentum score
                        momentum = np.tanh(slope / 10)  # Sigmoid normalization
                        direction = "positive" if slope > 0 else "negative" if slope < 0 else "neutral"
                        
                        return {
                            "momentum": float(momentum),
                            "direction": direction,
                            "slope": float(slope),
                            "data_points": len(values)
                        }
        except Exception:
            pass
        
        return {"momentum": 0, "direction": "neutral"}

    def _process_news_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process news articles for analysis"""
        processed = []
        for article in articles[:50]:  # Limit to 50 articles
            processed.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "content": article.get("content", ""),
                "source": article.get("source", {}).get("name", ""),
                "published_at": article.get("publishedAt", ""),
                "url": article.get("url", "")
            })
        return processed

    def _calculate_trend_insights(self, trend_data: Dict[str, Any], news_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive trend insights"""
        insights = {
            "overall_momentum": 0,
            "trend_strength": "weak",
            "key_insights": []
        }
        
        # Analyze Google Trends momentum
        if "trend_data" in trend_data and not "error" in trend_data:
            momentums = []
            for timeframe, data in trend_data["trend_data"].items():
                if "momentum" in data and "momentum" in data["momentum"]:
                    momentums.append(data["momentum"]["momentum"])
            
            if momentums:
                insights["overall_momentum"] = float(np.mean(momentums))
                
                # Determine trend strength
                avg_momentum = abs(insights["overall_momentum"])
                if avg_momentum > 0.7:
                    insights["trend_strength"] = "strong"
                elif avg_momentum > 0.4:
                    insights["trend_strength"] = "moderate"
                else:
                    insights["trend_strength"] = "weak"
        
        # Analyze news volume
        if "article_count" in news_data:
            article_count = news_data["article_count"]
            if article_count > 30:
                insights["key_insights"].append("High media coverage indicates strong market interest")
            elif article_count > 15:
                insights["key_insights"].append("Moderate media coverage suggests growing market awareness")
            else:
                insights["key_insights"].append("Limited media coverage may indicate early market stage")
        
        return insights

    def _calculate_trend_confidence(self, trend_data: Dict[str, Any], news_data: Dict[str, Any]) -> float:
        """Calculate confidence in trend analysis"""
        confidence_factors = []
        
        # Google Trends confidence
        if "trend_data" in trend_data and not "error" in trend_data:
            valid_timeframes = sum(1 for data in trend_data["trend_data"].values() if "error" not in data)
            total_timeframes = len(trend_data["trend_data"])
            if total_timeframes > 0:
                confidence_factors.append(valid_timeframes / total_timeframes)
        
        # News confidence
        if "article_count" in news_data:
            article_count = news_data["article_count"]
            confidence_factors.append(min(article_count / 30, 1.0))
        
        return float(np.mean(confidence_factors)) if confidence_factors else 0.5
