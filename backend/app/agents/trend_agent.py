from .base_agent import BaseResearchAgent
from typing import Dict, Any
import httpx
import openai
from config import settings

class TrendAnalysisAgent(BaseResearchAgent):
    """Agent for identifying and analyzing market and technology trends."""
    
    async def research(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market and technology trends"""
        try:
            # This would use tools like Google Trends, industry reports, and news analysis.
            trend_query = f"emerging trends {query} market technology innovation 2024"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.config.TAVILY_API_KEY,
                        "query": trend_query,
                        "search_depth": "advanced",
                        "include_answer": True,
                        "max_results": 8
                    }
                )
                response.raise_for_status()
                
                data = response.json()
                
                # Analyze trends using LLM
                trend_analysis = await self._analyze_trends(data.get("results", []), query)
                
                return {
                    "trend_data": data,
                    "trend_analysis": trend_analysis,
                    "timestamp": "2024-01-01T00:00:00Z"
                }
                
        except Exception as e:
            return {"error": f"Trend analysis failed: {str(e)}"}
    
    async def _analyze_trends(self, results: list, query: str) -> Dict[str, Any]:
        """Analyze trends from research results"""
        try:
            if not results:
                return {"error": "No trend data available"}
            
            # Extract trend information
            trend_info = []
            for result in results[:5]:  # Limit to first 5 results
                if result.get("content"):
                    trend_info.append(result["content"][:500])  # Limit content length
            
            if not trend_info:
                return {"error": "No trend content found"}
            
            # Use LLM for trend analysis
            client = openai.AsyncOpenAI(api_key=self.config.OPENAI_API_KEY)
            
            combined_info = " ".join(trend_info)
            
            prompt = f"""
            Analyze the emerging trends for: {query}
            
            Trend Information:
            {combined_info[:3000]}
            
            Provide a JSON response with:
            - key_trends: list of main trends identified
            - trend_categories: categorize trends (technology, market, social, etc.)
            - impact_level: 1-10 scale of potential impact
            - adoption_timeline: estimated timeline for adoption
            - opportunity_areas: areas where these trends create opportunities
            """
            
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            return self._parse_json_response(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"Trend analysis failed: {str(e)}"}
