from .base_framework import BaseScoringFramework
from typing import Dict, Any, List
import re

class MarketSizingFramework(BaseScoringFramework):
    """Framework for analyzing market size, growth, and scalability metrics"""
    
    async def calculate_score(self, research_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate market sizing score from research data"""
        try:
            # Extract market size information from research data
            market_info = self._extract_market_data(research_data)
            
            if not market_info:
                return {
                    "raw_score": 0,
                    "confidence": 0.1,
                    "supporting_data": {"error": "No market size data found"}
                }
            
            # Calculate score based on market size and growth
            score = self._calculate_market_score(market_info)
            confidence = self._calculate_confidence(market_info)
            
            return {
                "raw_score": score,
                "confidence": confidence,
                "supporting_data": market_info,
                "calculation_method": "market_sizing_framework"
            }
            
        except Exception as e:
            return {
                "raw_score": 0,
                "confidence": 0.0,
                "supporting_data": {"error": f"Market sizing calculation failed: {str(e)}"}
            }
    
    def _extract_market_data(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract market size and growth data from research results"""
        market_info = {}
        
        # Look for market size data in various formats
        if "market_sizing" in research_data:
            market_info.update(research_data["market_sizing"])
        
        # Extract from web search results
        if "web_research" in research_data and "results" in research_data["web_research"]:
            for result in research_data["web_research"]["results"]:
                content = result.get("content", "")
                self._extract_market_metrics(content, market_info)
        
        # Extract from alternative search
        if "alternative_search" in research_data and "results" in research_data["alternative_search"]:
            for result in research_data["alternative_search"]["results"]:
                content = result.get("content", "")
                self._extract_market_metrics(content, market_info)
        
        return market_info
    
    def _extract_market_metrics(self, content: str, market_info: Dict[str, Any]):
        """Extract market metrics from text content"""
        if not content:
            return
        
        # Extract TAM, SAM, SOM values
        tam_match = re.search(r'(\$?\d+(?:\.\d+)?\s*(?:billion|million|trillion|B|M|T))', content, re.IGNORECASE)
        if tam_match and "tam" not in market_info:
            market_info["tam"] = self._normalize_currency(tam_match.group(1))
        
        # Extract CAGR
        cagr_match = re.search(r'(\d+(?:\.\d+)?)\s*%?\s*(?:CAGR|growth rate|annual growth)', content, re.IGNORECASE)
        if cagr_match and "cagr" not in market_info:
            market_info["cagr"] = float(cagr_match.group(1))
        
        # Extract market size in USD
        usd_match = re.search(r'\$(\d+(?:\.\d+)?)\s*(?:billion|million|trillion|B|M|T)', content, re.IGNORECASE)
        if usd_match and "market_size_usd" not in market_info:
            market_info["market_size_usd"] = self._normalize_currency(f"${usd_match.group(1)}")
    
    def _normalize_currency(self, currency_str: str) -> float:
        """Normalize currency strings to USD values"""
        try:
            currency_str = currency_str.upper().replace('$', '').replace(',', '')
            
            if 'TRILLION' in currency_str or 'T' in currency_str:
                multiplier = 1_000_000_000_000
            elif 'BILLION' in currency_str or 'B' in currency_str:
                multiplier = 1_000_000_000
            elif 'MILLION' in currency_str or 'M' in currency_str:
                multiplier = 1_000_000
            else:
                multiplier = 1
            
            # Extract numeric value
            numeric_value = re.search(r'(\d+(?:\.\d+)?)', currency_str)
            if numeric_value:
                return float(numeric_value.group(1)) * multiplier
            
            return 0
        except:
            return 0
    
    def _calculate_market_score(self, market_info: Dict[str, Any]) -> float:
        """Calculate market score based on size and growth"""
        score = 0
        
        # Market size scoring (0-50 points)
        market_size = market_info.get("market_size_usd", 0)
        if market_size > 100_000_000_000:  # >$100B
            score += 50
        elif market_size > 10_000_000_000:  # >$10B
            score += 40
        elif market_size > 1_000_000_000:   # >$1B
            score += 30
        elif market_size > 100_000_000:     # >$100M
            score += 20
        elif market_size > 10_000_000:      # >$10M
            score += 10
        
        # Growth rate scoring (0-50 points)
        cagr = market_info.get("cagr", 0)
        if cagr > 20:
            score += 50
        elif cagr > 15:
            score += 40
        elif cagr > 10:
            score += 30
        elif cagr > 5:
            score += 20
        elif cagr > 0:
            score += 10
        
        return min(score, 100)
    
    def _calculate_confidence(self, market_info: Dict[str, Any]) -> float:
        """Calculate confidence level based on data quality"""
        confidence = 0.0
        
        # Base confidence from data availability
        if "tam" in market_info:
            confidence += 0.3
        if "cagr" in market_info:
            confidence += 0.3
        if "market_size_usd" in market_info:
            confidence += 0.2
        
        # Additional confidence from multiple sources
        source_count = len([k for k in market_info.keys() if k not in ["error"]])
        if source_count >= 3:
            confidence += 0.2
        elif source_count >= 2:
            confidence += 0.1
        
        return min(confidence, 1.0)
