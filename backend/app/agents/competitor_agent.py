from .base_agent import BaseResearchAgent
from typing import Dict, Any
import httpx
import openai
from config import settings

class CompetitorAnalysisAgent(BaseResearchAgent):
    """Agent for analyzing competitors and competitive landscape."""
    
    async def research(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct comprehensive competitor analysis"""
        try:
            # This would involve deep dives into competitor websites, financial reports, and news.
            competitor_query = f"competitive analysis {query} key competitors market positioning"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.config.TAVILY_API_KEY,
                        "query": competitor_query,
                        "search_depth": "advanced",
                        "include_answer": True,
                        "max_results": 10
                    }
                )
                response.raise_for_status()
                
                data = response.json()
                
                # Analyze competitive landscape using LLM
                competitive_analysis = await self._analyze_competitive_landscape(data.get("results", []), query)
                
                return {
                    "competitor_data": data,
                    "competitive_analysis": competitive_analysis,
                    "timestamp": "2024-01-01T00:00:00Z"
                }
                
        except Exception as e:
            return {"error": f"Competitor analysis failed: {str(e)}"}
    
    async def _analyze_competitive_landscape(self, results: list, query: str) -> Dict[str, Any]:
        """Analyze competitive landscape from research results"""
        try:
            if not results:
                return {"error": "No competitor data available"}
            
            # Extract competitor information
            competitor_info = []
            for result in results[:5]:  # Limit to first 5 results
                if result.get("content"):
                    competitor_info.append(result["content"][:500])  # Limit content length
            
            if not competitor_info:
                return {"error": "No competitor content found"}
            
            # Use LLM for competitive analysis
            client = openai.AsyncOpenAI(api_key=self.config.OPENAI_API_KEY)
            
            combined_info = " ".join(competitor_info)
            
            prompt = f"""
            Analyze the competitive landscape for: {query}
            
            Competitor Information:
            {combined_info[:3000]}
            
            Provide a JSON response with:
            - key_competitors: list of main competitors identified
            - market_positions: brief description of each competitor's position
            - competitive_advantages: list of competitive advantages mentioned
            - market_share_estimate: rough estimate of market concentration
            - threat_level: 1-10 scale of competitive threat
            """
            
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            return self._parse_json_response(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"Competitive landscape analysis failed: {str(e)}"}
