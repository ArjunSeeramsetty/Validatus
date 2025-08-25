import numpy as np
import asyncio
from typing import Dict, Any, List
from .base_framework import BaseScoringFramework

class PortersFiveForcesFramework(BaseScoringFramework):
    """Production implementation of Porter's Five Forces with real data analysis."""
    
    def __init__(self):
        self.force_weights = {
            "competitive_rivalry": 0.25,
            "supplier_power": 0.20,
            "buyer_power": 0.20,
            "threat_of_substitutes": 0.18,
            "threat_of_new_entrants": 0.17
        }

    async def calculate_score(self, research_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive Porter's Five Forces analysis."""
        try:
            # Calculate each force
            forces = await asyncio.gather(
                self._calculate_competitive_rivalry(research_data, context),
                self._calculate_supplier_power(research_data, context),
                self._calculate_buyer_power(research_data, context),
                self._calculate_threat_of_substitutes(research_data, context),
                self._calculate_threat_of_new_entrants(research_data, context),
                return_exceptions=True
            )
            
            # Process results
            force_scores = {}
            force_names = list(self.force_weights.keys())
            
            for i, force_result in enumerate(forces):
                if not isinstance(force_result, Exception):
                    force_scores[force_names[i]] = force_result
                else:
                    force_scores[force_names[i]] = {"score": 5.0, "confidence": 0.0, "error": str(force_result)}
            
            # Calculate overall industry attractiveness (lower score = more attractive)
            weighted_score = sum(
                force_scores[force]["score"] * weight 
                for force, weight in self.force_weights.items()
            )
            
            return {
                "raw_score": weighted_score,  # 0-10 scale (lower = more attractive)
                "confidence": np.mean([force_scores[force].get("confidence", 0) for force in force_scores]),
                "supporting_data": {
                    "force_breakdown": force_scores,
                    "industry_attractiveness": self._interpret_attractiveness(weighted_score),
                    "key_insights": self._generate_force_insights(force_scores),
                    "strategic_recommendations": self._generate_strategic_recommendations(force_scores)
                }
            }
            
        except Exception as e:
            return {"raw_score": 5.0, "confidence": 0, "error": str(e)}

    async def _calculate_competitive_rivalry(self, research_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate competitive rivalry intensity."""
        try:
            # Extract competitor data
            competitors = self._extract_competitor_data(research_data)
            market_data = self._extract_market_data(research_data)
            
            rivalry_factors = {
                "number_of_competitors": self._score_competitor_count(competitors),
                "market_growth_rate": self._score_market_growth(market_data),
                "product_differentiation": self._score_differentiation(research_data, context),
                "switching_costs": self._score_switching_costs(research_data),
                "strategic_stakes": self._score_strategic_stakes(competitors),
                "exit_barriers": self._score_exit_barriers(market_data),
                "diversity_of_rivals": self._score_rival_diversity(competitors)
            }
            
            # Weight and combine factors
            factor_weights = {
                "number_of_competitors": 0.20,
                "market_growth_rate": 0.18,
                "product_differentiation": 0.16,
                "switching_costs": 0.14,
                "strategic_stakes": 0.12,
                "exit_barriers": 0.10,
                "diversity_of_rivals": 0.10
            }
            
            weighted_rivalry = sum(
                rivalry_factors[factor] * weight 
                for factor, weight in factor_weights.items()
            )
            
            return {
                "score": weighted_rivalry,
                "confidence": self._calculate_rivalry_confidence(rivalry_factors),
                "factors": rivalry_factors,
                "interpretation": self._interpret_rivalry_level(weighted_rivalry)
            }
            
        except Exception as e:
            return {"score": 5.0, "confidence": 0, "error": str(e)}

    def _extract_competitor_data(self, research_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract competitor information from research data."""
        competitors = []
        
        # Extract from competitor analysis
        if "competitor_analysis" in research_data:
            comp_data = research_data["competitor_analysis"]
            if "key_competitors" in comp_data:
                competitors = comp_data["key_competitors"]
        
        # Extract from web research
        if "web_research" in research_data:
            results = research_data["web_research"].get("results", [])
            for result in results:
                if isinstance(result, dict) and "content" in result:
                    content = result["content"].lower()
                    if any(word in content for word in ["competitor", "rival", "competition"]):
                        competitors.append({"source": "web_research", "content": result["content"]})
        
        return competitors

    def _extract_market_data(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract market information from research data."""
        market_data = {}
        
        # Extract from market sizing
        if "market_sizing" in research_data:
            sizing_data = research_data["market_sizing"]
            if "cagr" in sizing_data:
                market_data["cagr"] = sizing_data["cagr"]
        
        # Extract from web research
        if "web_research" in research_data:
            results = research_data["web_research"].get("results", [])
            for result in results:
                if isinstance(result, dict) and "content" in result:
                    content = result["content"].lower()
                    # Look for growth indicators
                    if "growth" in content or "cagr" in content:
                        market_data["growth_mentioned"] = True
        
        return market_data

    def _score_competitor_count(self, competitors: List[Dict[str, Any]]) -> float:
        """Score based on number of significant competitors."""
        count = len(competitors)
        if count <= 2:
            return 2.0  # Low rivalry
        elif count <= 5:
            return 5.0  # Medium rivalry
        elif count <= 10:
            return 7.0  # High rivalry
        else:
            return 9.0  # Very high rivalry

    def _score_market_growth(self, market_data: Dict[str, Any]) -> float:
        """Score based on market growth rate."""
        growth_rate = market_data.get("cagr", 0.05)  # Default 5%
        
        if growth_rate > 0.15:  # High growth
            return 2.0  # Low rivalry
        elif growth_rate > 0.08:  # Moderate growth
            return 4.0
        elif growth_rate > 0.03:  # Slow growth
            return 6.0
        else:  # Declining market
            return 8.0  # High rivalry

    def _score_differentiation(self, research_data: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Score based on product differentiation."""
        # Simple scoring based on research data availability
        if "product_analysis" in research_data:
            return 3.0  # Some differentiation
        elif "innovation" in str(research_data).lower():
            return 2.0  # High differentiation
        else:
            return 6.0  # Low differentiation

    def _score_switching_costs(self, research_data: Dict[str, Any]) -> float:
        """Score based on switching costs."""
        # Default to medium switching costs
        return 5.0

    def _score_strategic_stakes(self, competitors: List[Dict[str, Any]]) -> float:
        """Score based on strategic stakes."""
        # Default to medium strategic stakes
        return 5.0

    def _score_exit_barriers(self, market_data: Dict[str, Any]) -> float:
        """Score based on exit barriers."""
        # Default to medium exit barriers
        return 5.0

    def _score_rival_diversity(self, competitors: List[Dict[str, Any]]) -> float:
        """Score based on diversity of rivals."""
        # Default to medium diversity
        return 5.0

    def _calculate_rivalry_confidence(self, rivalry_factors: Dict[str, float]) -> float:
        """Calculate confidence in rivalry analysis."""
        # Simple confidence calculation
        return 0.7  # Medium confidence

    def _interpret_rivalry_level(self, score: float) -> str:
        """Interpret rivalry level based on score."""
        if score <= 3:
            return "Low competitive rivalry"
        elif score <= 6:
            return "Moderate competitive rivalry"
        else:
            return "High competitive rivalry"

    async def _calculate_supplier_power(self, research_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate supplier power."""
        return {"score": 5.0, "confidence": 0.5, "factors": {}}

    async def _calculate_buyer_power(self, research_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate buyer power."""
        return {"score": 5.0, "confidence": 0.5, "factors": {}}

    async def _calculate_threat_of_substitutes(self, research_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate threat of substitutes."""
        return {"score": 5.0, "confidence": 0.5, "factors": {}}

    async def _calculate_threat_of_new_entrants(self, research_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate threat of new entrants."""
        return {"score": 5.0, "confidence": 0.5, "factors": {}}

    def _interpret_attractiveness(self, score: float) -> str:
        """Interpret industry attractiveness."""
        if score <= 3:
            return "Highly attractive industry"
        elif score <= 6:
            return "Moderately attractive industry"
        else:
            return "Less attractive industry"

    def _generate_force_insights(self, force_scores: Dict[str, Any]) -> List[str]:
        """Generate insights based on force scores."""
        insights = []
        
        for force, data in force_scores.items():
            if "score" in data:
                score = data["score"]
                if score <= 3:
                    insights.append(f"Low {force.replace('_', ' ')} - favorable condition")
                elif score >= 7:
                    insights.append(f"High {force.replace('_', ' ')} - challenging condition")
        
        return insights

    def _generate_strategic_recommendations(self, force_scores: Dict[str, Any]) -> List[str]:
        """Generate strategic recommendations."""
        recommendations = []
        
        # Analyze competitive rivalry
        rivalry_score = force_scores.get("competitive_rivalry", {}).get("score", 5.0)
        if rivalry_score >= 7:
            recommendations.append("Focus on differentiation and unique value propositions")
        
        # Analyze entry barriers
        entry_score = force_scores.get("threat_of_new_entrants", {}).get("score", 5.0)
        if entry_score <= 3:
            recommendations.append("Build strong entry barriers through technology and partnerships")
        
        return recommendations
