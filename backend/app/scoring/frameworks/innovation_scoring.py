from .base_framework import BaseScoringFramework
from typing import Dict, Any

class InnovationScoringFramework(BaseScoringFramework):
    """Framework for analyzing innovation and differentiation metrics"""
    
    async def calculate_score(self, research_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate innovation score from research data"""
        try:
            # Extract innovation information
            innovation_info = self._extract_innovation_data(research_data)
            
            if not innovation_info:
                return {
                    "raw_score": 5,  # Default middle score
                    "confidence": 0.1,
                    "supporting_data": {"error": "No innovation data found"}
                }
            
            # Calculate score based on innovation indicators
            score = self._calculate_innovation_score(innovation_info)
            confidence = self._calculate_confidence(innovation_info)
            
            return {
                "raw_score": score,
                "confidence": confidence,
                "supporting_data": innovation_info,
                "calculation_method": "innovation_scoring_framework"
            }
            
        except Exception as e:
            return {
                "raw_score": 5,
                "confidence": 0.0,
                "supporting_data": {"error": f"Innovation scoring calculation failed: {str(e)}"}
            }
    
    def _extract_innovation_data(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract innovation information from research results"""
        innovation_info = {}
        
        # Look for innovation analysis data
        if "trend_analysis" in research_data:
            innovation_info.update(research_data["trend_analysis"])
        
        # Extract from trend data
        if "trend_data" in research_data and "results" in research_data["trend_data"]:
            for result in research_data["trend_data"]["results"]:
                content = result.get("content", "")
                if content:
                    # Extract key innovation metrics
                    if "impact_level" in content.lower():
                        innovation_info["impact_level"] = self._extract_impact_level(content)
                    if "innovation" in content.lower():
                        innovation_info["innovation_indicators"] = self._extract_innovation_indicators(content)
        
        return innovation_info
    
    def _extract_impact_level(self, content: str) -> int:
        """Extract impact level from content"""
        try:
            # Look for impact level indicators
            if "high impact" in content.lower() or "transformative" in content.lower():
                return 9
            elif "medium impact" in content.lower() or "moderate" in content.lower():
                return 6
            elif "low impact" in content.lower() or "minimal" in content.lower():
                return 3
            else:
                return 5  # Default
        except:
            return 5
    
    def _extract_innovation_indicators(self, content: str) -> list:
        """Extract innovation indicators from content"""
        indicators = []
        # Simple keyword extraction for innovation
        innovation_keywords = ["innovative", "breakthrough", "revolutionary", "cutting-edge", "advanced", "novel", "unique"]
        for keyword in innovation_keywords:
            if keyword in content.lower():
                indicators.append(keyword)
        return indicators
    
    def _calculate_innovation_score(self, innovation_info: Dict[str, Any]) -> float:
        """Calculate innovation score based on indicators and impact"""
        score = 50  # Base score
        
        # Adjust based on impact level
        impact_level = innovation_info.get("impact_level", 5)
        if impact_level >= 8:
            score += 25  # High impact
        elif impact_level >= 6:
            score += 10  # Medium impact
        elif impact_level <= 3:
            score -= 10  # Low impact
        
        # Adjust based on innovation indicators
        indicators = innovation_info.get("innovation_indicators", [])
        if len(indicators) >= 3:
            score += 20
        elif len(indicators) >= 1:
            score += 10
        
        return max(0, min(100, score))
    
    def _calculate_confidence(self, innovation_info: Dict[str, Any]) -> float:
        """Calculate confidence level based on data quality"""
        confidence = 0.0
        
        # Base confidence from data availability
        if "impact_level" in innovation_info:
            confidence += 0.4
        if "innovation_indicators" in innovation_info:
            confidence += 0.3
        
        # Additional confidence from data sources
        source_count = len([k for k in innovation_info.keys() if k not in ["error"]])
        if source_count >= 2:
            confidence += 0.3
        elif source_count >= 1:
            confidence += 0.1
        
        return min(confidence, 1.0)
