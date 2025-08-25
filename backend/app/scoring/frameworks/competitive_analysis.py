from .base_framework import BaseScoringFramework
from typing import Dict, Any

class CompetitiveAnalysisFramework(BaseScoringFramework):
    """Framework for analyzing competitive positioning and differentiation"""
    
    async def calculate_score(self, research_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate competitive analysis score from research data"""
        try:
            # Extract competitive information
            competitive_info = self._extract_competitive_data(research_data)
            
            if not competitive_info:
                return {
                    "raw_score": 5,  # Default middle score
                    "confidence": 0.1,
                    "supporting_data": {"error": "No competitive data found"}
                }
            
            # Calculate score based on competitive positioning
            score = self._calculate_competitive_score(competitive_info)
            confidence = self._calculate_confidence(competitive_info)
            
            return {
                "raw_score": score,
                "confidence": confidence,
                "supporting_data": competitive_info,
                "calculation_method": "competitive_analysis_framework"
            }
            
        except Exception as e:
            return {
                "raw_score": 5,
                "confidence": 0.0,
                "supporting_data": {"error": f"Competitive analysis calculation failed: {str(e)}"}
            }
    
    def _extract_competitive_data(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract competitive information from research results"""
        competitive_info = {}
        
        # Look for competitive analysis data
        if "competitive_analysis" in research_data:
            competitive_info.update(research_data["competitive_analysis"])
        
        # Extract from competitor data
        if "competitor_data" in research_data and "results" in research_data["competitor_data"]:
            for result in research_data["competitor_data"]["results"]:
                content = result.get("content", "")
                if content:
                    # Extract key competitive metrics
                    if "threat_level" in content.lower():
                        competitive_info["threat_level"] = self._extract_threat_level(content)
                    if "competitive_advantages" in content.lower():
                        competitive_info["advantages"] = self._extract_advantages(content)
        
        return competitive_info
    
    def _extract_threat_level(self, content: str) -> int:
        """Extract threat level from content"""
        try:
            # Look for threat level indicators
            if "high threat" in content.lower() or "strong competition" in content.lower():
                return 8
            elif "moderate threat" in content.lower() or "medium competition" in content.lower():
                return 5
            elif "low threat" in content.lower() or "weak competition" in content.lower():
                return 2
            else:
                return 5  # Default
        except:
            return 5
    
    def _extract_advantages(self, content: str) -> list:
        """Extract competitive advantages from content"""
        advantages = []
        # Simple keyword extraction for advantages
        advantage_keywords = ["unique", "differentiated", "innovative", "superior", "better", "advantage"]
        for keyword in advantage_keywords:
            if keyword in content.lower():
                advantages.append(keyword)
        return advantages
    
    def _calculate_competitive_score(self, competitive_info: Dict[str, Any]) -> float:
        """Calculate competitive score based on positioning and threats"""
        score = 50  # Base score
        
        # Adjust based on threat level (lower threat = higher score)
        threat_level = competitive_info.get("threat_level", 5)
        if threat_level <= 3:
            score += 20  # Low threat
        elif threat_level <= 6:
            score += 0   # Moderate threat
        else:
            score -= 20  # High threat
        
        # Adjust based on competitive advantages
        advantages = competitive_info.get("advantages", [])
        if len(advantages) >= 3:
            score += 15
        elif len(advantages) >= 1:
            score += 5
        
        return max(0, min(100, score))
    
    def _calculate_confidence(self, competitive_info: Dict[str, Any]) -> float:
        """Calculate confidence level based on data quality"""
        confidence = 0.0
        
        # Base confidence from data availability
        if "threat_level" in competitive_info:
            confidence += 0.4
        if "advantages" in competitive_info:
            confidence += 0.3
        
        # Additional confidence from data sources
        source_count = len([k for k in competitive_info.keys() if k not in ["error"]])
        if source_count >= 2:
            confidence += 0.3
        elif source_count >= 1:
            confidence += 0.1
        
        return min(confidence, 1.0)
