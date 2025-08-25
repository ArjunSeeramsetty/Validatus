from .base_agent import BaseResearchAgent
from typing import Dict, Any
import httpx
import openai
from config import settings

class PricingResearchAgent(BaseResearchAgent):
    """Agent for researching pricing strategies and models."""
    
    async def research(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Research pricing strategies and market pricing"""
        try:
            # This would involve scraping competitor pricing pages and analyzing market data.
            pricing_query = f"pricing strategies {query} pricing models market pricing analysis"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.config.TAVILY_API_KEY,
                        "query": pricing_query,
                        "search_depth": "advanced",
                        "include_answer": True,
                        "max_results": 8
                    }
                )
                response.raise_for_status()
                
                data = response.json()
                
                # Analyze pricing using LLM
                pricing_analysis = await self._analyze_pricing_strategies(data.get("results", []), query)
                
                return {
                    "pricing_data": data,
                    "pricing_analysis": pricing_analysis,
                    "timestamp": "2024-01-01T00:00:00Z"
                }
                
        except Exception as e:
            return {"error": f"Pricing research failed: {str(e)}"}
    
    async def _analyze_pricing_strategies(self, results: list, query: str) -> Dict[str, Any]:
        """Analyze pricing strategies from research results"""
        try:
            if not results:
                return {"error": "No pricing data available"}
            
            # Extract pricing information
            pricing_info = []
            for result in results[:5]:  # Limit to first 5 results
                if result.get("content"):
                    pricing_info.append(result["content"][:500])  # Limit content length
            
            if not pricing_info:
                return {"error": "No pricing content found"}
            
            # Use LLM for pricing analysis
            client = openai.AsyncOpenAI(api_key=self.config.OPENAI_API_KEY)
            
            combined_info = " ".join(pricing_info)
            
            prompt = f"""
            Analyze the pricing strategies for: {query}
            
            Pricing Information:
            {combined_info[:3000]}
            
            Provide a JSON response with:
            - pricing_models: list of pricing models identified
            - price_ranges: estimated price ranges mentioned
            - pricing_strategies: different pricing strategies used
            - competitive_pricing: how pricing compares to competitors
            - pricing_trends: any pricing trends or changes mentioned
            """
            
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            return self._parse_json_response(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"Pricing strategy analysis failed: {str(e)}"}
