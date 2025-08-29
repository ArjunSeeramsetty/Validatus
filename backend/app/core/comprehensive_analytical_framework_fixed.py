#!/usr/bin/env python3
"""
Comprehensive Analytical Framework for Validatus Platform - FIXED VERSION
Implements all 156+ layers with deterministic scoring and missing methods
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio

from app.core.multi_llm_orchestrator import MultiLLMOrchestrator
from app.core.specialized_agents import get_specialized_agent_orchestrator, AnalysisDomain

logger = logging.getLogger(__name__)

class StrategicDimension(Enum):
    """Strategic dimensions for analysis"""
    CONSUMER = "consumer"
    MARKET = "market"
    PRODUCT = "product"
    BRAND = "brand"
    EXPERIENCE = "experience"

class LayerType(Enum):
    """Types of analysis layers"""
    CONSUMER_INSIGHTS = "consumer_insights"
    MARKET_RESEARCH = "market_research"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    TREND_ANALYSIS = "trend_analysis"
    PRICING_RESEARCH = "pricing_research"

@dataclass
class SourceAttribution:
    """Source attribution for deterministic scoring"""
    source_name: str
    source_type: str
    source_url: Optional[str] = None
    publication_date: Optional[str] = None
    confidence_level: float = 0.0
    methodology: str = ""
    sample_size: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_name": self.source_name,
            "source_type": self.source_type,
            "source_url": self.source_url,
            "publication_date": self.publication_date,
            "confidence_level": self.confidence_level,
            "methodology": self.methodology,
            "sample_size": self.sample_size
        }

@dataclass
class LayerScore:
    """Individual layer score with source attribution"""
    layer_name: str
    layer_type: LayerType
    score: float  # 1-10 scale
    rationale: str
    sources: List[SourceAttribution]
    confidence: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "layer_name": self.layer_name,
            "layer_type": self.layer_type.value,
            "score": self.score,
            "rationale": self.rationale,
            "sources": [source.to_dict() for source in self.sources],
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }

@dataclass
class FactorScore:
    """Factor score calculated from layer scores"""
    factor_name: str
    factor_type: str
    score: float  # 1-10 scale
    contributing_layers: List[str]
    layer_scores: List[LayerScore]
    calculation_method: str
    rationale: str
    confidence: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "factor_name": self.factor_name,
            "factor_type": self.factor_type,
            "score": self.score,
            "contributing_layers": self.contributing_layers,
            "calculation_method": self.calculation_method,
            "rationale": self.rationale,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat()
        }

@dataclass
class SegmentScore:
    """Segment score calculated from factor scores"""
    segment_name: str
    segment_type: StrategicDimension
    score: float  # 1-10 scale
    contributing_factors: List[str]
    factor_scores: List[FactorScore]
    calculation_method: str
    rationale: str
    confidence: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "segment_name": self.segment_name,
            "segment_type": self.segment_type.value,
            "score": self.score,
            "contributing_factors": self.contributing_factors,
            "calculation_method": self.calculation_method,
            "rationale": self.rationale,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat()
        }

class ComprehensiveAnalyticalFramework:
    """
    Comprehensive analytical framework implementing all 156+ layers from hierarchical diagrams
    """
    
    def __init__(self):
        self.analytical_framework = {
            "CONSUMER": {
                "factors": {
                    "Consumer Demand & Need": [
                        "need_perception", "trust_level", "purchase_intent", "emotional_pull", "awareness",
                        "social_influence", "accessibility", "value_perception", "trend_alignment", "price_sensitivity"
                    ],
                    "Consumer Behavior & Habits": [
                        "usage_frequency", "engagement_level", "habit_formation", "emotional_tie", "ease_of_access",
                        "trust_in_usage", "interaction_rate", "perceived_value", "social_engagement", "incentives"
                    ],
                    "Consumer Loyalty & Retention": [
                        "repeat_purchase", "trust_level_retention", "value_perception_loyalty", "advocacy", "social_loyalty",
                        "emotional_bond", "switching_cost", "engagement_loyalty", "rewards", "access_loyalty"
                    ],
                    "Consumer Perception & Sentiment": [
                        "sentiment", "quality_perception", "value_perception_sentiment", "innovation_perception", "trend_alignment_sentiment",
                        "trust_perception", "prestige", "social_impact", "awareness_sentiment", "access_perception"
                    ],
                    "Consumer Adoption & Engagement": [
                        "adoption_rate", "trust_in_adoption", "value_perception_adoption", "frequency", "trend_alignment_adoption",
                        "engagement_adoption", "social_influence_adoption", "emotional_pull_adoption", "accessibility_adoption", "incentives_adoption"
                    ]
                },
                "agent": "consumer_insights"
            },
            "MARKET": {
                "factors": {
                    "market_trends": [
                        "future_trends", "technological_shifts", "current_trends", "cultural_shift", "regulatory_shifts"
                    ],
                    "Market Competition and Barriers": [
                        "rival_strength", "entry_barriers", "differentiation_advantage", "customer_switching_costs", "regulatory_barriers"
                    ],
                    "Market Demand and Adoption": [
                        "demand_volume", "demand_growth", "adoption_rate", "price_elasticity", "market_accessibility"
                    ],
                    "Market Growth and Expansion": [
                        "growth_potential", "regional_growth", "scalability_capacity", "investment_in_growth", "infrastructure_support"
                    ],
                    "Market Stability and Risk": [
                        "economic_stability", "political_stability", "supply_chain_stability", "risk_exposure", "regulatory_stability"
                    ]
                },
                "agent": "market_research"
            },
            "PRODUCT": {
                "factors": {
                    "Product Market Readiness": [
                        "entry_timing", "mid_cycle_impact", "market_saturation"
                    ],
                    "Product Competitive Disruption": [
                        "base_disruption", "incumbent_resistance", "response_time"
                    ],
                    "Product Dynamic Disruption": [
                        "base_disruption_dynamic", "product_strength", "awareness_width", "value_perception_dynamic", 
                        "adoption_growth", "error_perception", "retention_effect", "competitor_pull", "value_consistency"
                    ],
                    "Product Business Resilience": [
                        "profit_resilience", "expansion_growth"
                    ],
                    "Product Hype Cycle": [
                        "mid_cycle_buzz", "market_saturation_hype", "entry_timing_hype"
                    ],
                    "Product Quality Assurance": [
                        "material_quality", "functional_quality", "brand_trust", "complaint_rate", "social_verdict"
                    ],
                    "Product Differentiation": [
                        "tech_features", "competitor_strength"
                    ],
                    "Product Brand Perception": [
                        "ad_reach", "organic_buzz"
                    ],
                    "Product Experience Design": [
                        "visual_appeal", "haptic_feedback", "olfactory_appeal"
                    ],
                    "Product Innovation Lifecycle": [
                        "market_fit", "entry_barrier", "tech_gap"
                    ]
                },
                "agent": "product_strategist"
            },
            "BRAND": {
                "factors": {
                    "Brand Positioning Strategy": [
                        "heritage_legacy", "innovation_edge", "public_perception", "exclusivity_factor", "competitor_edge"
                    ],
                    "Brand Equity Profile": [
                        "review_score", "social_sentiment", "legacy_trust", "ai_driven_trust", "crisis_handling"
                    ],
                    "Brand Virality Impact": [
                        "shareability_rate", "influencer_push", "platform_fit", "cultural_embed"
                    ],
                    "Brand Monetization Model": [
                        "direct_sales", "licensing_deals", "pricing_power", "revenue_diversification"
                    ],
                    "Brand Longevity Outlook": [
                        "evolution_adapt", "generational_appeal", "resilience_factor", "esg_adaptation", "cultural_relevance"
                    ]
                },
                "agent": "brand_strategist"
            },
            "EXPERIENCE": {
                "factors": {
                    "User Engagement Metrics": [
                        "attention_focus", "interaction_rate", "community_activity", "emotional_pull", "user_flow"
                    ],
                    "Satisfaction Feedback": [
                        "value_perception", "sentiment_feedback", "support_quality", "expectation_match"
                    ],
                    "Interaction Design Elements": [
                        "usability_ease", "intuitive_design", "sensory_appeal", "personalization", "access_inclusivity"
                    ],
                    "Post-Purchase Loyalty": [
                        "repeat_usage", "emotional_bond", "practical_retention", "advocacy_power", "incentive_reward"
                    ],
                    "Experience Evolution": [
                        "feature_updates", "trend_alignment", "cognitive_shift", "ai_adaptation"
                    ]
                },
                "agent": "ux_strategist"
            }
        }
        
        # Initialize specialized agent orchestrator
        self.agent_orchestrator = get_specialized_agent_orchestrator()
        
        # Initialize LLM orchestrator
        self.llm_orchestrator = MultiLLMOrchestrator()

    async def analyze_layer(self, layer_name: str, idea_description: str, 
                           target_audience: str, context: Dict[str, Any]) -> LayerScore:
        """Analyze a specific layer using specialized agents"""
        try:
            logger.info(f"🔍 Analyzing layer: {layer_name}")
            
            # Get the appropriate specialized agent
            agent = self.agent_orchestrator.get_optimal_agent(layer_name)
            
            if not agent:
                logger.warning(f"⚠️ No specialized agent found for {layer_name}, using default")
                # Create a default layer score
                return LayerScore(
                    layer_name=layer_name,
                    layer_type=self._get_layer_type(layer_name),
                    score=5.0,
                    rationale=f"Default analysis for {layer_name} - no specialized agent available",
                    sources=[],
                    confidence=0.5
                )
            
            # Analyze the layer
            analysis_result = await agent.analyze_layer(layer_name, idea_description, target_audience, context)
            
            if not analysis_result:
                logger.error(f"❌ Analysis failed for {layer_name}")
                return LayerScore(
                    layer_name=layer_name,
                    layer_type=self._get_layer_type(layer_name),
                    score=5.0,
                    rationale=f"Analysis failed for {layer_name}",
                    sources=[],
                    confidence=0.3
                )
            
            # Extract score and rationale from the analysis
            score = self._extract_score_from_analysis(analysis_result)
            rationale = self._extract_rationale_from_analysis(analysis_result)
            
            # Create source attribution
            sources = self._create_source_attribution(analysis_result, context)
            
            # Create layer score
            layer_score = LayerScore(
                layer_name=layer_name,
                layer_type=self._get_layer_type(layer_name),
                score=score,
                rationale=rationale,
                sources=sources,
                confidence=0.8  # Default confidence for specialized analysis
            )
            
            logger.info(f"✅ Layer {layer_name} analyzed: {score}/10")
            return layer_score
            
        except Exception as e:
            logger.error(f"❌ Error analyzing {layer_name}: {str(e)}")
            # Return a default score on error
            return LayerScore(
                layer_name=layer_name,
                layer_type=self._get_layer_type(layer_name),
                score=5.0,
                rationale=f"Error during analysis: {str(e)}",
                sources=[],
                confidence=0.2
            )

    def _get_layer_type(self, layer_name: str) -> LayerType:
        """Determine layer type from layer name"""
        layer_lower = layer_name.lower()
        
        if any(term in layer_lower for term in ['consumer', 'need', 'purchase', 'loyalty', 'sentiment']):
            return LayerType.CONSUMER_INSIGHTS
        elif any(term in layer_lower for term in ['market', 'trend', 'competition', 'growth']):
            return LayerType.MARKET_RESEARCH
        elif any(term in layer_lower for term in ['competitor', 'rival', 'market_share']):
            return LayerType.COMPETITOR_ANALYSIS
        elif any(term in layer_lower for term in ['trend', 'innovation', 'technology']):
            return LayerType.TREND_ANALYSIS
        elif any(term in layer_lower for term in ['pricing', 'cost', 'value']):
            return LayerType.PRICING_RESEARCH
        else:
            return LayerType.CONSUMER_INSIGHTS  # Default

    def _extract_score_from_analysis(self, analysis_result: Dict[str, Any]) -> float:
        """Extract score from analysis result"""
        try:
            # Look for score in various formats
            if isinstance(analysis_result, dict):
                # Check for direct score field
                if 'score' in analysis_result:
                    score = float(analysis_result['score'])
                    return max(1.0, min(10.0, score))  # Clamp to 1-10 range
                
                # Check for consensus score
                if 'consensus' in analysis_result and isinstance(analysis_result['consensus'], dict):
                    if 'score' in analysis_result['consensus']:
                        score = float(analysis_result['consensus']['score'])
                        return max(1.0, min(10.0, score))
                
                # Check for analysis field
                if 'analysis' in analysis_result:
                    analysis_text = str(analysis_result['analysis'])
                    # Look for score pattern like "Score: 8/10" or "8/10"
                    import re
                    score_match = re.search(r'Score:\s*(\d+(?:\.\d+)?)/10', analysis_text)
                    if score_match:
                        score = float(score_match.group(1))
                        return max(1.0, min(10.0, score))
                    
                    score_match = re.search(r'(\d+(?:\.\d+)?)/10', analysis_text)
                    if score_match:
                        score = float(score_match.group(1))
                        return max(1.0, min(10.0, score))
            
            # Default score if no pattern found
            return 5.0
            
        except (ValueError, TypeError, KeyError):
            return 5.0

    def _extract_rationale_from_analysis(self, analysis_result: Dict[str, Any]) -> str:
        """Extract rationale from analysis result"""
        try:
            if isinstance(analysis_result, dict):
                # Check for direct rationale field
                if 'rationale' in analysis_result:
                    return str(analysis_result['rationale'])
                
                # Check for consensus analysis
                if 'consensus' in analysis_result and isinstance(analysis_result['consensus'], dict):
                    if 'analysis' in analysis_result['consensus']:
                        return str(analysis_result['consensus']['analysis'])
                
                # Check for analysis field
                if 'analysis' in analysis_result:
                    return str(analysis_result['analysis'])
                
                # Check for summary field
                if 'summary' in analysis_result:
                    return str(analysis_result['summary'])
            
            # Default rationale
            return "Analysis completed with specialized agent"
            
        except Exception:
            return "Analysis completed with specialized agent"

    def _create_source_attribution(self, analysis_result: Dict[str, Any], context: Dict[str, Any]) -> List[SourceAttribution]:
        """Create source attribution for the analysis"""
        sources = []
        
        try:
            # Add specialized agent as source
            agent_type = context.get('persona', 'specialized_agent')
            sources.append(SourceAttribution(
                source_name=f"Specialized {agent_type}",
                source_type="LLM Analysis",
                confidence_level=0.8,
                methodology="Specialized agent analysis with persona-based prompting"
            ))
            
            # Add context information as source
            if context.get('analysis_type'):
                sources.append(SourceAttribution(
                    source_name=f"{context['analysis_type'].title()} Analysis Context",
                    source_type="Strategic Context",
                    confidence_level=0.7,
                    methodology="Context-aware analysis with accumulated insights"
                ))
            
        except Exception as e:
            logger.warning(f"⚠️ Error creating source attribution: {str(e)}")
        
        return sources

    def calculate_factor_score(self, factor_name: str, layer_scores: List[LayerScore], 
                             calculation_method: str = "weighted_average") -> FactorScore:
        """Calculate factor score from contributing layer scores"""
        
        if not layer_scores:
            return FactorScore(
                factor_name=factor_name,
                factor_type="calculated",
                score=5.0,
                contributing_layers=[],
                layer_scores=[],
                calculation_method=calculation_method,
                rationale="No layer scores available",
                confidence=0.0
            )
        
        # Calculate factor score based on method
        if calculation_method == "weighted_average":
            # Weight by confidence levels
            total_weight = sum(layer.confidence for layer in layer_scores)
            if total_weight > 0:
                weighted_score = sum(layer.score * layer.confidence for layer in layer_scores) / total_weight
            else:
                weighted_score = sum(layer.score for layer in layer_scores) / len(layer_scores)
            
            score = weighted_score
            confidence = sum(layer.confidence for layer in layer_scores) / len(layer_scores)
            
        elif calculation_method == "geometric_mean":
            # Use geometric mean for multiplicative factors
            score = (product(layer.score for layer in layer_scores)) ** (1.0 / len(layer_scores))
            confidence = sum(layer.confidence for layer in layer_scores) / len(layer_scores)
            
        else:  # simple_average
            score = sum(layer.score for layer in layer_scores) / len(layer_scores)
            confidence = sum(layer.confidence for layer in layer_scores) / len(layer_scores)
        
        # Generate rationale
        contributing_layers = [layer.layer_name for layer in layer_scores]
        rationale = f"Factor score {score:.1f}/10 calculated from {len(layer_scores)} layers using {calculation_method}. Contributing layers: {', '.join(contributing_layers)}"
        
        return FactorScore(
            factor_name=factor_name,
            factor_type="calculated",
            score=round(score, 1),
            contributing_layers=contributing_layers,
            layer_scores=layer_scores,
            calculation_method=calculation_method,
            rationale=rationale,
            confidence=round(confidence, 2)
        )

    def calculate_segment_score(self, segment_name: str, factor_scores: List[FactorScore], 
                               calculation_method: str = "weighted_average") -> SegmentScore:
        """Calculate segment score from contributing factor scores"""
        
        if not factor_scores:
            return SegmentScore(
                segment_name=segment_name,
                segment_type=StrategicDimension.CONSUMER,
                score=5.0,
                contributing_factors=[],
                factor_scores=[],
                calculation_method=calculation_method,
                rationale="No factor scores available",
                confidence=0.0
            )
        
        # Calculate segment score
        if calculation_method == "weighted_average":
            total_weight = sum(factor.confidence for factor in factor_scores)
            if total_weight > 0:
                weighted_score = sum(factor.score * factor.confidence for factor in factor_scores) / total_weight
            else:
                weighted_score = sum(factor.score for factor in factor_scores) / len(factor_scores)
            
            score = weighted_score
            confidence = sum(factor.confidence for factor in factor_scores) / len(factor_scores)
            
        else:  # simple_average
            score = sum(factor.score for factor in factor_scores) / len(factor_scores)
            confidence = sum(factor.confidence for factor in factor_scores) / len(factor_scores)
        
        # Generate rationale
        contributing_factors = [factor.factor_name for factor in factor_scores]
        rationale = f"Segment score {score:.1f}/10 calculated from {len(factor_scores)} factors using {calculation_method}. Contributing factors: {', '.join(contributing_factors)}"
        
        return SegmentScore(
            segment_name=segment_name,
            segment_type=self._get_segment_type(segment_name),
            score=round(score, 1),
            contributing_factors=contributing_factors,
            factor_scores=factor_scores,
            calculation_method=calculation_method,
            rationale=rationale,
            confidence=round(confidence, 2)
        )

    def _get_segment_type(self, segment_name: str) -> StrategicDimension:
        """Get strategic dimension type from segment name"""
        segment_mapping = {
            "CONSUMER": StrategicDimension.CONSUMER,
            "MARKET": StrategicDimension.MARKET,
            "PRODUCT": StrategicDimension.PRODUCT,
            "BRAND": StrategicDimension.BRAND,
            "EXPERIENCE": StrategicDimension.EXPERIENCE
        }
        return segment_mapping.get(segment_name, StrategicDimension.CONSUMER)

    # ADDING THE MISSING METHODS THAT THE WORKFLOW NEEDS
    async def calculate_all_factors(self, layer_scores: Dict[str, LayerScore]) -> Dict[str, FactorScore]:
        """Calculate all factor scores from layer scores"""
        factor_scores = {}
        
        # Group layers by segment and factor
        for segment_name, segment_data in self.analytical_framework.items():
            for factor_name, layers in segment_data["factors"].items():
                # Get layer scores for this factor
                factor_layer_scores = []
                for layer in layers:
                    if layer in layer_scores:
                        factor_layer_scores.append(layer_scores[layer])
                
                if factor_layer_scores:
                    # Calculate factor score
                    factor_score = self.calculate_factor_score(factor_name, factor_layer_scores)
                    factor_scores[f"{segment_name}_{factor_name}"] = factor_score
        
        return factor_scores

    async def calculate_all_segments(self, layer_scores: Dict[str, LayerScore], 
                                   factor_scores: Dict[str, FactorScore]) -> Dict[str, SegmentScore]:
        """Calculate all segment scores from factor scores"""
        segment_scores = {}
        
        # Group factors by segment
        for segment_name, segment_data in self.analytical_framework.items():
            segment_factor_scores = []
            
            for factor_name in segment_data["factors"].keys():
                factor_key = f"{segment_name}_{factor_name}"
                if factor_key in factor_scores:
                    segment_factor_scores.append(factor_scores[factor_key])
            
            if segment_factor_scores:
                # Calculate segment score
                segment_score = self.calculate_segment_score(segment_name, segment_factor_scores)
                segment_scores[segment_name] = segment_score
        
        return segment_scores

    async def generate_comprehensive_analysis(self, layer_scores: Dict[str, LayerScore], 
                                           factor_scores: Dict[str, FactorScore], 
                                           segment_scores: Dict[str, SegmentScore]) -> Dict[str, Any]:
        """Generate comprehensive analysis results"""
        
        # Calculate overall viability score
        if segment_scores:
            overall_score = sum(segment.score for segment in segment_scores.values()) / len(segment_scores)
        else:
            overall_score = 5.0
        
        # Generate key insights
        key_insights = []
        if layer_scores:
            high_scores = [layer for layer in layer_scores.values() if layer.score >= 8.0]
            low_scores = [layer for layer in layer_scores.values() if layer.score <= 3.0]
            
            if high_scores:
                key_insights.append(f"Strong performance areas: {len(high_scores)} high-scoring layers")
            if low_scores:
                key_insights.append(f"Critical improvement areas: {len(low_scores)} low-scoring layers")
        
        # Generate recommendations
        recommendations = []
        if segment_scores:
            for segment_name, segment_score in segment_scores.items():
                if segment_score.score < 6.0:
                    recommendations.append(f"Focus on improving {segment_name} (current: {segment_score.score}/10)")
                elif segment_score.score > 8.0:
                    recommendations.append(f"Leverage {segment_name} strength (current: {segment_score.score}/10)")
        
        # Risk assessment
        risk_level = "medium"
        critical_areas = []
        strength_areas = []
        
        if segment_scores:
            low_segments = [name for name, score in segment_scores.items() if score.score < 5.0]
            high_segments = [name for name, score in segment_scores.items() if score.score >= 7.0]
            
            if len(low_segments) > 2:
                risk_level = "high"
            elif len(low_segments) > 0:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            critical_areas = low_segments
            strength_areas = high_segments
        
        # Execution details
        execution_details = {
            "total_layers_analyzed": len(layer_scores),
            "total_factors_calculated": len(factor_scores),
            "total_segments_evaluated": len(segment_scores),
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # Generate detailed layer-wise scores and summaries
        layer_details = {}
        for layer_name, layer_score in layer_scores.items():
            layer_details[layer_name] = {
                "score": layer_score.score,
                "rationale": layer_score.rationale,
                "source_attribution": {
                    "source_type": layer_score.layer_type.value,
                    "confidence": layer_score.confidence,
                    "methodology": "Specialized agent analysis with persona-based prompting"
                },
                "timestamp": layer_score.timestamp.isoformat()
            }
        
        # Generate detailed factor-wise scores and summaries
        factor_details = {}
        for factor_key, factor_score in factor_scores.items():
            factor_details[factor_key] = {
                "score": factor_score.score,
                "rationale": factor_score.rationale,
                "calculation_method": factor_score.calculation_method,
                "contributing_layers": factor_score.contributing_layers,
                "confidence": factor_score.confidence,
                "timestamp": factor_score.timestamp.isoformat()
            }
        
        # Generate detailed segment-wise scores and summaries
        segment_details = {}
        for segment_name, segment_score in segment_scores.items():
            segment_details[segment_name] = {
                "score": segment_score.score,
                "rationale": segment_score.rationale,
                "calculation_method": segment_score.calculation_method,
                "contributing_factors": segment_score.contributing_factors,
                "confidence": segment_score.confidence,
                "timestamp": segment_score.timestamp.isoformat()
            }
        
        # Generate comprehensive strategic insights
        strategic_insights = {
            "key_strengths": [],
            "critical_risks": [],
            "market_opportunities": [],
            "competitive_advantages": [],
            "implementation_recommendations": []
        }
        
        # Analyze high-scoring areas for strengths and opportunities
        high_scoring_layers = [layer for layer in layer_scores.values() if layer.score >= 8.0]
        if high_scoring_layers:
            strategic_insights["key_strengths"].append(f"Strong performance in {len(high_scoring_layers)} strategic layers")
            strategic_insights["competitive_advantages"].append(f"Competitive edge in {len(high_scoring_layers)} key areas")
        
        # Analyze low-scoring areas for risks and improvement opportunities
        low_scoring_layers = [layer for layer in layer_scores.values() if layer.score <= 3.0]
        if low_scoring_layers:
            strategic_insights["critical_risks"].append(f"Critical improvement needed in {len(low_scoring_layers)} areas")
            strategic_insights["implementation_recommendations"].append(f"Prioritize improvements in {len(low_scoring_layers)} low-scoring layers")
        
        # Analyze segment performance for opportunities
        high_scoring_segments = [name for name, score in segment_scores.items() if score.score >= 8.0]
        if high_scoring_segments:
            strategic_insights["market_opportunities"].append(f"Strong market position in {', '.join(high_scoring_segments)} segments")
        
        return {
            "overall_viability_score": round(overall_score, 1),
            "execution_details": execution_details,
            "analysis_summary": {
                "key_insights": key_insights,
                "total_layers": len(layer_scores),
                "total_factors": len(factor_scores),
                "total_segments": len(segment_scores)
            },
            "recommendations": recommendations,
            "risk_assessment": {
                "risk_level": risk_level,
                "critical_areas": critical_areas,
                "strength_areas": strength_areas
            },
            "detailed_analysis": {
                "layer_scores": layer_details,
                "factor_scores": factor_details,
                "segment_scores": segment_details
            },
            "strategic_insights": strategic_insights
        }

    def get_all_layers(self) -> List[str]:
        """Get all layer names from the framework"""
        all_layers = []
        for segment, segment_data in self.analytical_framework.items():
            for factor, layers in segment_data["factors"].items():
                all_layers.extend(layers)
        return all_layers

    def get_segment_layers(self, segment_name: str) -> List[str]:
        """Get all layers for a specific segment"""
        if segment_name not in self.analytical_framework:
            return []
        
        all_layers = []
        for factor, layers in self.analytical_framework[segment_name]["factors"].items():
            all_layers.extend(layers)
        return all_layers

    def get_factor_layers(self, segment_name: str, factor_name: str) -> List[str]:
        """Get layers for a specific factor within a segment"""
        if (segment_name not in self.analytical_framework or 
            factor_name not in self.analytical_framework[segment_name]["factors"]):
            return []
        
        return self.analytical_framework[segment_name]["factors"][factor_name]

def product(iterable):
    """Calculate product of iterable"""
    result = 1
    for item in iterable:
        result *= item
    return result
