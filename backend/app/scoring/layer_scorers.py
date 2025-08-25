from typing import Dict, Any, List
from datetime import datetime
import asyncio
from .frameworks.sentiment import SentimentAnalysisFramework
from .frameworks.porters import PortersFiveForcesFramework
from .frameworks.pestle import PESTLEAnalysisFramework
from .frameworks.market_sizing import MarketSizingFramework
from .frameworks.competitive_analysis import CompetitiveAnalysisFramework
from .frameworks.innovation_scoring import InnovationScoringFramework

class LayerScoringEngine:
    """Central engine for calculating layer scores using strategic frameworks"""
    
    def __init__(self):
        self.frameworks = {
            "sentiment": SentimentAnalysisFramework(),
            "porters": PortersFiveForcesFramework(),
            "pestle": PESTLEAnalysisFramework(),
            "market_sizing": MarketSizingFramework(),
            "competitive": CompetitiveAnalysisFramework(),
            "innovation": InnovationScoringFramework(),
        }
        
        # Comprehensive mapping ensuring every layer gets scored
        self.layer_framework_map = {
            # Consumer Segment
            "need_perception": "sentiment",
            "purchase_intent": "sentiment", 
            "emotional_pull": "sentiment",
            "unmet_needs": "sentiment",
            "shopping_habits": "sentiment",
            "media_consumption": "sentiment",
            "decision_making_process": "sentiment",
            "brand_interaction": "sentiment",
            "repeat_purchase_rate": "market_sizing",
            "churn_risk": "sentiment",
            "advocacy_potential": "sentiment",
            "loyalty_program_effectiveness": "market_sizing",
            "overall_sentiment": "sentiment",
            "quality_perception": "sentiment",
            "trust_perception": "sentiment",
            "value_for_money": "sentiment",
            "product_usage_frequency": "market_sizing",
            "feature_adoption_rate": "market_sizing",
            "community_engagement": "sentiment",
            "feedback_submission_rate": "market_sizing",
            
            # Market Segment
            "total_addressable_market": "market_sizing",
            "serviceable_addressable_market": "market_sizing",
            "market_growth_rate": "market_sizing",
            "future_projections": "market_sizing",
            "emerging_trends": "pestle",
            "technological_shifts": "pestle",
            "white_space_opportunities": "pestle",
            "macroeconomic_factors": "pestle",
            "key_competitors": "competitive",
            "market_share_distribution": "competitive",
            "competitor_strengths_weaknesses": "competitive",
            "rival_intensity": "porters",
            "key_regulations": "pestle",
            "compliance_requirements": "pestle",
            "political_stability": "pestle",
            "trade_policies": "pestle",
            "economic_risks": "pestle",
            "competitive_threats": "competitive",
            "supply_chain_vulnerabilities": "pestle",
            "market_volatility": "pestle",
            
            # Product Segment
            "core_features_analysis": "competitive",
            "feature_completeness": "competitive",
            "user_friendliness": "sentiment",
            "performance_reliability": "competitive",
            "unique_selling_proposition": "competitive",
            "technological_innovation": "innovation",
            "design_innovation": "innovation",
            "patent_portfolio": "innovation",
            "clarity_of_value": "sentiment",
            "problem_solution_fit": "sentiment",
            "cost_benefit_analysis": "market_sizing",
            "emotional_benefits": "sentiment",
            "supply_chain_resilience": "pestle",
            "cost_structure_stability": "market_sizing",
            "scalability_potential": "market_sizing",
            "dependency_risks": "pestle",
            "defect_rate": "competitive",
            "customer_reported_issues": "sentiment",
            "performance_benchmarks": "competitive",
            "compliance_standards": "competitive",
            
            # Brand Segment
            "unaided_brand_recall": "market_sizing",
            "aided_brand_recognition": "market_sizing",
            "share_of_voice": "market_sizing",
            "social_media_presence": "market_sizing",
            "brand_associations": "sentiment",
            "perceived_quality": "sentiment",
            "brand_loyalty_metrics": "market_sizing",
            "brand_advocacy": "sentiment",
            "market_positioning": "competitive",
            "target_audience_alignment": "sentiment",
            "competitive_differentiation": "competitive",
            "brand_story_clarity": "sentiment",
            "message_consistency": "sentiment",
            "tone_of_voice": "sentiment",
            "channel_effectiveness": "market_sizing",
            "content_engagement": "market_sizing",
            "pricing_strategy": "market_sizing",
            "customer_lifetime_value": "market_sizing",
            "revenue_streams": "market_sizing",
            "profitability_analysis": "market_sizing",
            
            # Experience Segment
            "onboarding_experience": "sentiment",
            "ease_of_use": "sentiment",
            "navigation_clarity": "sentiment",
            "visual_appeal": "sentiment",
            "touchpoint_analysis": "market_sizing",
            "friction_points": "sentiment",
            "emotional_journey": "sentiment",
            "channel_consistency": "market_sizing",
            "first_response_time": "market_sizing",
            "resolution_rate": "market_sizing",
            "support_channel_effectiveness": "market_sizing",
            "agent_satisfaction": "sentiment",
            "post_purchase_communication": "market_sizing",
            "loyalty_program_engagement": "market_sizing",
            "review_and_rating_behavior": "sentiment",
            "referral_rate": "market_sizing",
            "community_activity_level": "market_sizing",
            "user_generated_content": "market_sizing",
            "brand_interaction_rate": "market_sizing",
            "event_participation": "market_sizing",
        }
    
    async def calculate_layer_score(self, layer_name: str, research_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate score for a specific layer using the appropriate framework"""
        try:
            framework_name = self.layer_framework_map.get(layer_name, "sentiment")  # Default to sentiment
            framework = self.frameworks[framework_name]
            
            score_result = await framework.calculate_score(research_data, context)
            
            normalized_score = self._normalize_score(score_result["raw_score"], framework_name)
            
            return {
                "score": normalized_score,
                "confidence": score_result.get("confidence", 0.5),
                "calculation_method": framework_name,
                "supporting_data": score_result.get("supporting_data", {}),
                "data_sources": research_data.get("results", [{}])[0].get("url") if research_data.get("results") else [],
                "summary": f"Score based on {framework_name} analysis.",
                "raw_score": score_result.get("raw_score", 0),
                "framework_used": framework_name
            }
        except Exception as e:
            return {
                "score": 50.0, 
                "confidence": 0.0, 
                "error": str(e),
                "calculation_method": "error_fallback",
                "supporting_data": {},
                "data_sources": [],
                "summary": f"Error in scoring: {str(e)}"
            }

    def _normalize_score(self, raw_score: float, framework_name: str) -> float:
        """Normalize raw score to a 0-100 range based on the framework used."""
        normalization_ranges = {
            "sentiment": {"min": -1, "max": 1},
            "porters": {"min": 0, "max": 10},
            "pestle": {"min": -2, "max": 2},
            "market_sizing": {"min": 0, "max": 1000000000},  # Market sizes in USD
            "competitive": {"min": 0, "max": 10},
            "innovation": {"min": 0, "max": 10},
            "default": {"min": 0, "max": 1}
        }
        
        config = normalization_ranges.get(framework_name, {"min": 0, "max": 1})
        min_val, max_val = config["min"], config["max"]
        
        if max_val == min_val:
            return 50.0
            
        normalized = ((raw_score - min_val) / (max_val - min_val)) * 100
        return max(0, min(100, normalized))

    async def calculate_all_layer_scores(self, research_results: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate scores for all layers in parallel for better performance"""
        tasks = []
        layer_keys = []
        
        for layer_key, research_data in research_results.items():
            if research_data.get("error"):
                continue
                
            segment, factor, layer = layer_key.split('.')
            task = self.calculate_layer_score(layer, research_data.get("data", {}), context)
            tasks.append(task)
            layer_keys.append(layer_key)
        
        if not tasks:
            return {}
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        layer_scores = {}
        for i, result in enumerate(results):
            layer_key = layer_keys[i]
            segment, factor, layer = layer_key.split('.')
            
            if isinstance(result, Exception):
                result = {
                    "score": 50.0,
                    "confidence": 0.0,
                    "error": str(result),
                    "calculation_method": "error_fallback"
                }
            
            if segment not in layer_scores:
                layer_scores[segment] = {}
            if factor not in layer_scores[segment]:
                layer_scores[segment][factor] = {}
                
            layer_scores[segment][factor][layer] = result
        
        return layer_scores
