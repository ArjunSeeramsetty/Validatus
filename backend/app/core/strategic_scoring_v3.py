#!/usr/bin/env python3
"""
Strategic Scoring System V3 - LLM Data Extraction + Traditional Strategy Frameworks
Uses LLM to extract specific metrics, then applies established strategy frameworks for scoring
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json
import numpy as np
from dataclasses import dataclass
from enum import Enum

class StrategyFramework(Enum):
    """Traditional strategy frameworks for scoring"""
    PORTERS_FIVE_FORCES = "porters_five_forces"
    PESTLE_ANALYSIS = "pestle_analysis"
    SWOT_ANALYSIS = "swot_analysis"
    BCG_MATRIX = "bcg_matrix"
    ANSOFF_MATRIX = "ansoff_matrix"
    VALUE_CHAIN_ANALYSIS = "value_chain_analysis"

class StrategicMetric(Enum):
    """Specific metrics to extract from LLM analysis"""
    # Porter's Five Forces Metrics
    RIVALRY_INTENSITY = "rivalry_intensity"                    # 1-5 scale
    SUPPLIER_POWER = "supplier_power"                          # 1-5 scale
    BUYER_POWER = "buyer_power"                                # 1-5 scale
    THREAT_OF_NEW_ENTRANTS = "threat_of_new_entrants"         # 1-5 scale
    THREAT_OF_SUBSTITUTES = "threat_of_substitutes"            # 1-5 scale
    
    # PESTLE Metrics
    POLITICAL_STABILITY = "political_stability"                # 1-5 scale
    ECONOMIC_GROWTH_RATE = "economic_growth_rate"              # Percentage
    SOCIAL_TREND_STRENGTH = "social_trend_strength"            # 1-5 scale
    TECHNOLOGICAL_ADVANCEMENT = "technological_advancement"     # 1-5 scale
    LEGAL_COMPLEXITY = "legal_complexity"                      # 1-5 scale
    ENVIRONMENTAL_IMPACT = "environmental_impact"              # 1-5 scale
    
    # Market Metrics
    MARKET_SIZE_USD = "market_size_usd"                        # USD value
    MARKET_GROWTH_RATE = "market_growth_rate"                  # Percentage
    MARKET_MATURITY_STAGE = "market_maturity_stage"            # 1-5 scale
    CUSTOMER_SEGMENT_SIZE = "customer_segment_size"            # Number of customers
    CUSTOMER_ACQUISITION_COST = "customer_acquisition_cost"    # USD value
    
    # Competitive Metrics
    MARKET_SHARE_PERCENTAGE = "market_share_percentage"        # Percentage
    COMPETITOR_COUNT = "competitor_count"                      # Number
    DIFFERENTIATION_LEVEL = "differentiation_level"            # 1-5 scale
    BARRIERS_TO_ENTRY_HEIGHT = "barriers_to_entry_height"      # 1-5 scale
    BRAND_RECOGNITION = "brand_recognition"                    # 1-5 scale
    
    # Financial Metrics
    REVENUE_POTENTIAL_USD = "revenue_potential_usd"            # USD value
    PROFIT_MARGIN_PERCENTAGE = "profit_margin_percentage"      # Percentage
    COST_STRUCTURE_EFFICIENCY = "cost_structure_efficiency"     # 1-5 scale
    SCALABILITY_FACTOR = "scalability_factor"                   # 1-5 scale
    BREAK_EVEN_TIMEFRAME = "break_even_timeframe"              # Months

@dataclass
class ExtractedMetric:
    """A specific metric extracted from LLM analysis"""
    metric: StrategicMetric
    value: Any  # Could be number, string, or other type
    unit: str   # e.g., "USD", "percentage", "scale_1_5"
    confidence: float  # 0.0 to 1.0
    source_text: str   # Text that led to this extraction
    extraction_method: str
    timestamp: datetime

@dataclass
class FrameworkScore:
    """Score for a specific strategy framework"""
    framework: StrategyFramework
    score: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    metrics_used: List[ExtractedMetric]
    calculation_method: str
    reasoning: str
    timestamp: datetime

@dataclass
class StrategicAnalysisResultV3:
    """Complete strategic analysis result with framework-based scoring"""
    query: str
    context: Dict[str, Any]
    extracted_metrics: List[ExtractedMetric]
    framework_scores: List[FrameworkScore]
    overall_score: float
    overall_confidence: float
    strategic_position: str
    key_insights: List[str]
    strategic_recommendations: List[str]
    risk_assessment: Dict[str, Any]
    opportunity_analysis: Dict[str, Any]
    timestamp: datetime
    processing_time: float

class StrategicScoringEngineV3:
    """
    LLM Data Extraction + Traditional Strategy Framework Scoring
    Uses LLM to extract specific metrics, then applies established strategy frameworks
    """
    
    def __init__(self):
        self.logger = logging.getLogger("strategic.scoring.v3")
        self.framework_metrics = self._initialize_framework_metrics()
        
    def _initialize_framework_metrics(self) -> Dict[StrategyFramework, List[StrategicMetric]]:
        """Initialize which metrics are needed for each framework"""
        return {
            StrategyFramework.PORTERS_FIVE_FORCES: [
                StrategicMetric.RIVALRY_INTENSITY,
                StrategicMetric.SUPPLIER_POWER,
                StrategicMetric.BUYER_POWER,
                StrategicMetric.THREAT_OF_NEW_ENTRANTS,
                StrategicMetric.THREAT_OF_SUBSTITUTES
            ],
            StrategyFramework.PESTLE_ANALYSIS: [
                StrategicMetric.POLITICAL_STABILITY,
                StrategicMetric.ECONOMIC_GROWTH_RATE,
                StrategicMetric.SOCIAL_TREND_STRENGTH,
                StrategicMetric.TECHNOLOGICAL_ADVANCEMENT,
                StrategicMetric.LEGAL_COMPLEXITY,
                StrategicMetric.ENVIRONMENTAL_IMPACT
            ],
            StrategyFramework.SWOT_ANALYSIS: [
                StrategicMetric.MARKET_SIZE_USD,
                StrategicMetric.MARKET_GROWTH_RATE,
                StrategicMetric.DIFFERENTIATION_LEVEL,
                StrategicMetric.BRAND_RECOGNITION,
                StrategicMetric.REVENUE_POTENTIAL_USD,
                StrategicMetric.COST_STRUCTURE_EFFICIENCY
            ],
            StrategyFramework.BCG_MATRIX: [
                StrategicMetric.MARKET_GROWTH_RATE,
                StrategicMetric.MARKET_SHARE_PERCENTAGE,
                StrategicMetric.MARKET_SIZE_USD,
                StrategicMetric.COMPETITOR_COUNT
            ],
            StrategyFramework.ANSOFF_MATRIX: [
                StrategicMetric.MARKET_MATURITY_STAGE,
                StrategicMetric.DIFFERENTIATION_LEVEL,
                StrategicMetric.CUSTOMER_SEGMENT_SIZE,
                StrategicMetric.SCALABILITY_FACTOR
            ]
        }
    
    async def analyze_strategic_framework(self,
                                       llm_analysis: Dict[str, Any],
                                       query: str,
                                       context: Dict[str, Any] = None) -> StrategicAnalysisResultV3:
        """Perform comprehensive strategic analysis with framework-based scoring"""
        start_time = datetime.now()
        
        try:
            self.logger.info("Starting framework-based strategic analysis")
            
            # Step 1: Extract specific metrics using LLM
            extracted_metrics = await self._extract_metrics_from_llm(llm_analysis, query, context)
            
            # Step 2: Calculate framework scores using traditional methods
            framework_scores = await self._calculate_framework_scores(extracted_metrics)
            
            # Step 3: Calculate overall metrics
            overall_score = np.mean([f.score for f in framework_scores])
            overall_confidence = np.mean([f.confidence for f in framework_scores])
            
            # Step 4: Generate strategic insights and recommendations
            strategic_position = self._determine_strategic_position(overall_score, framework_scores)
            key_insights = self._generate_strategic_insights(framework_scores, extracted_metrics)
            strategic_recommendations = self._generate_strategic_recommendations(framework_scores, extracted_metrics)
            
            # Step 5: Risk and opportunity analysis
            risk_assessment = self._assess_strategic_risks(framework_scores, extracted_metrics)
            opportunity_analysis = self._analyze_strategic_opportunities(framework_scores, extracted_metrics)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return StrategicAnalysisResultV3(
                query=query,
                context=context or {},
                extracted_metrics=extracted_metrics,
                framework_scores=framework_scores,
                overall_score=overall_score,
                overall_confidence=overall_confidence,
                strategic_position=strategic_position,
                key_insights=key_insights,
                strategic_recommendations=strategic_recommendations,
                risk_assessment=risk_assessment,
                opportunity_analysis=opportunity_analysis,
                timestamp=datetime.now(),
                processing_time=processing_time
            )
            
        except Exception as e:
            self.logger.error(f"Framework-based strategic analysis failed: {e}")
            raise
    
    async def _extract_metrics_from_llm(self, 
                                       llm_analysis: Dict[str, Any], 
                                       query: str, 
                                       context: Dict[str, Any] = None) -> List[ExtractedMetric]:
        """Extract specific metrics from LLM analysis using structured prompts"""
        
        extracted_metrics = []
        
        # Get insights and recommendations from LLM analysis
        insights = self._extract_insights_from_llm(llm_analysis)
        recommendations = self._extract_recommendations_from_llm(llm_analysis)
        
        # For each framework that has metrics defined, extract the required metrics
        for framework, required_metrics in self.framework_metrics.items():
            for metric in required_metrics:
                metric_value = await self._extract_specific_metric(
                    metric, insights, recommendations, context
                )
                if metric_value:
                    extracted_metrics.append(metric_value)
        
        return extracted_metrics
    
    async def _extract_specific_metric(self,
                                     metric: StrategicMetric,
                                     insights: List[str],
                                     recommendations: List[str],
                                     context: Dict[str, Any] = None) -> Optional[ExtractedMetric]:
        """Extract a specific metric using targeted analysis"""
        
        try:
            # Define extraction rules for each metric type
            extraction_rules = self._get_extraction_rules(metric)
            
            # Apply extraction rules
            extracted_value = None
            source_text = ""
            confidence = 0.5
            
            for rule in extraction_rules:
                value, text, conf = await self._apply_extraction_rule(
                    rule, metric, insights, recommendations, context
                )
                
                if value is not None and conf > confidence:
                    extracted_value = value
                    source_text = text
                    confidence = conf
            
            if extracted_value is not None:
                return ExtractedMetric(
                    metric=metric,
                    value=extracted_value,
                    unit=self._get_metric_unit(metric),
                    confidence=confidence,
                    source_text=source_text,
                    extraction_method="rule_based_extraction",
                    timestamp=datetime.now()
                )
            
            return None
            
        except Exception as e:
            self.logger.error(f"Metric extraction failed for {metric.value}: {e}")
            return None
    
    def _get_extraction_rules(self, metric: StrategicMetric) -> List[Dict[str, Any]]:
        """Get extraction rules for a specific metric"""
        
        rules = {
            # Porter's Five Forces Metrics
            StrategicMetric.RIVALRY_INTENSITY: [
                {
                    "type": "keyword_search",
                    "keywords": ["intense competition", "price wars", "market share battles"],
                    "scale_mapping": {
                        "intense competition": 5,
                        "moderate competition": 3,
                        "low competition": 1
                    }
                }
            ],
            
            StrategicMetric.MARKET_SIZE_USD: [
                {
                    "type": "numeric_extraction",
                    "patterns": [
                        r"(\d+(?:\.\d+)?)\s*(billion|million|trillion)\s*USD",
                        r"USD\s*(\d+(?:\.\d+)?)\s*(billion|million|trillion)",
                        r"market.*?(\d+(?:\.\d+)?)\s*(billion|million|trillion)"
                    ],
                    "multipliers": {"billion": 1e9, "million": 1e6, "trillion": 1e12}
                }
            ],
            
            StrategicMetric.MARKET_GROWTH_RATE: [
                {
                    "type": "percentage_extraction",
                    "patterns": [
                        r"(\d+(?:\.\d+)?)\s*%\s*growth",
                        r"growing.*?(\d+(?:\.\d+)?)\s*%",
                        r"growth.*?rate.*?(\d+(?:\.\d+)?)\s*%"
                    ]
                }
            ],
            
            StrategicMetric.DIFFERENTIATION_LEVEL: [
                {
                    "type": "keyword_search",
                    "keywords": ["unique", "differentiated", "commodity", "standard"],
                    "scale_mapping": {
                        "highly unique": 5,
                        "unique": 4,
                        "differentiated": 3,
                        "standard": 2,
                        "commodity": 1
                    }
                }
            ]
        }
        
        return rules.get(metric, [])
    
    async def _apply_extraction_rule(self,
                                   rule: Dict[str, Any],
                                   metric: StrategicMetric,
                                   insights: List[str],
                                   recommendations: List[str],
                                   context: Dict[str, Any] = None) -> Tuple[Any, str, float]:
        """Apply a specific extraction rule"""
        
        rule_type = rule.get("type")
        
        if rule_type == "keyword_search":
            return self._apply_keyword_search_rule(rule, insights, recommendations)
        elif rule_type == "numeric_extraction":
            return self._apply_numeric_extraction_rule(rule, insights, recommendations)
        elif rule_type == "percentage_extraction":
            return self._apply_percentage_extraction_rule(rule, insights, recommendations)
        elif rule_type == "context_lookup":
            return self._apply_context_lookup_rule(rule, context)
        
        return None, "", 0.0
    
    def _apply_keyword_search_rule(self, rule: Dict[str, Any], insights: List[str], recommendations: List[str]) -> Tuple[Any, str, float]:
        """Apply keyword search extraction rule"""
        
        keywords = rule.get("keywords", [])
        scale_mapping = rule.get("scale_mapping", {})
        
        all_text = " ".join(insights + recommendations).lower()
        
        for keyword in keywords:
            if keyword in all_text:
                # Find the source text
                for text in insights + recommendations:
                    if keyword.lower() in text.lower():
                        # Map to scale if available
                        if scale_mapping:
                            for mapping_key, mapping_value in scale_mapping.items():
                                if mapping_key.lower() in text.lower():
                                    return mapping_value, text, 0.8
                        
                        # Default scale mapping based on keyword
                        if "high" in keyword or "intense" in keyword:
                            return 5, text, 0.7
                        elif "moderate" in keyword or "medium" in keyword:
                            return 3, text, 0.7
                        elif "low" in keyword:
                            return 1, text, 0.7
                        else:
                            return 3, text, 0.6
        
        return None, "", 0.0
    
    def _apply_numeric_extraction_rule(self, rule: Dict[str, Any], insights: List[str], recommendations: List[str]) -> Tuple[Any, str, float]:
        """Apply numeric extraction rule"""
        
        import re
        
        patterns = rule.get("patterns", [])
        multipliers = rule.get("multipliers", {})
        
        all_text = " ".join(insights + recommendations)
        
        for pattern in patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                for match in matches:
                    try:
                        if isinstance(match, tuple):
                            number = float(match[0])
                            unit = match[1].lower()
                        else:
                            number = float(match)
                            unit = "million"  # Default unit
                        
                        # Apply multiplier
                        if unit in multipliers:
                            final_value = number * multipliers[unit]
                            return final_value, all_text[:200] + "...", 0.8
                        
                    except (ValueError, TypeError):
                        continue
        
        return None, "", 0.0
    
    def _apply_percentage_extraction_rule(self, rule: Dict[str, Any], insights: List[str], recommendations: List[str]) -> Tuple[Any, str, float]:
        """Apply percentage extraction rule"""
        
        import re
        
        patterns = rule.get("patterns", [])
        
        all_text = " ".join(insights + recommendations)
        
        for pattern in patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            if matches:
                for match in matches:
                    try:
                        percentage = float(match)
                        return percentage, all_text[:200] + "...", 0.8
                    except (ValueError, TypeError):
                        continue
        
        return None, "", 0.0
    
    def _apply_context_lookup_rule(self, rule: Dict[str, Any], context: Dict[str, Any]) -> Tuple[Any, str, float]:
        """Apply context lookup rule"""
        
        lookup_key = rule.get("lookup_key")
        default_value = rule.get("default_value")
        
        if context and lookup_key in context:
            value = context[lookup_key]
            return value, f"Context: {lookup_key}", 0.9
        
        if default_value is not None:
            return default_value, "Default value", 0.5
        
        return None, "", 0.0
    
    def _get_metric_unit(self, metric: StrategicMetric) -> str:
        """Get the unit for a specific metric"""
        
        unit_mapping = {
            # Porter's Five Forces
            StrategicMetric.RIVALRY_INTENSITY: "scale_1_5",
            StrategicMetric.SUPPLIER_POWER: "scale_1_5",
            StrategicMetric.BUYER_POWER: "scale_1_5",
            StrategicMetric.THREAT_OF_NEW_ENTRANTS: "scale_1_5",
            StrategicMetric.THREAT_OF_SUBSTITUTES: "scale_1_5",
            
            # PESTLE
            StrategicMetric.POLITICAL_STABILITY: "scale_1_5",
            StrategicMetric.ECONOMIC_GROWTH_RATE: "percentage",
            StrategicMetric.SOCIAL_TREND_STRENGTH: "scale_1_5",
            StrategicMetric.TECHNOLOGICAL_ADVANCEMENT: "scale_1_5",
            StrategicMetric.LEGAL_COMPLEXITY: "scale_1_5",
            StrategicMetric.ENVIRONMENTAL_IMPACT: "scale_1_5",
            
            # Market
            StrategicMetric.MARKET_SIZE_USD: "USD",
            StrategicMetric.MARKET_GROWTH_RATE: "percentage",
            StrategicMetric.MARKET_MATURITY_STAGE: "scale_1_5",
            StrategicMetric.CUSTOMER_SEGMENT_SIZE: "number",
            StrategicMetric.CUSTOMER_ACQUISITION_COST: "USD",
            
            # Competitive
            StrategicMetric.MARKET_SHARE_PERCENTAGE: "percentage",
            StrategicMetric.COMPETITOR_COUNT: "number",
            StrategicMetric.DIFFERENTIATION_LEVEL: "scale_1_5",
            StrategicMetric.BARRIERS_TO_ENTRY_HEIGHT: "scale_1_5",
            StrategicMetric.BRAND_RECOGNITION: "scale_1_5",
            
            # Financial
            StrategicMetric.REVENUE_POTENTIAL_USD: "USD",
            StrategicMetric.PROFIT_MARGIN_PERCENTAGE: "percentage",
            StrategicMetric.COST_STRUCTURE_EFFICIENCY: "scale_1_5",
            StrategicMetric.SCALABILITY_FACTOR: "scale_1_5",
            StrategicMetric.BREAK_EVEN_TIMEFRAME: "months"
        }
        
        return unit_mapping.get(metric, "unknown")
    
    async def _calculate_framework_scores(self, extracted_metrics: List[ExtractedMetric]) -> List[FrameworkScore]:
        """Calculate scores for each strategy framework using traditional methods"""
        
        framework_scores = []
        
        for framework, required_metrics in self.framework_metrics.items():
            
            # Get metrics for this framework
            framework_metrics = [m for m in extracted_metrics if m.metric in required_metrics]
            
            if framework_metrics:
                score, confidence, reasoning = await self._calculate_framework_score(
                    framework, framework_metrics
                )
                
                framework_scores.append(FrameworkScore(
                    framework=framework,
                    score=score,
                    confidence=confidence,
                    metrics_used=framework_metrics,
                    calculation_method=f"traditional_{framework.value}",
                    reasoning=reasoning,
                    timestamp=datetime.now()
                ))
        
        return framework_scores
    
    async def _calculate_framework_score(self,
                                      framework: StrategyFramework,
                                      metrics: List[ExtractedMetric]) -> Tuple[float, float, str]:
        """Calculate score for a specific framework using traditional methods"""
        
        if framework == StrategyFramework.PORTERS_FIVE_FORCES:
            return self._calculate_porters_five_forces_score(metrics)
        elif framework == StrategyFramework.PESTLE_ANALYSIS:
            return self._calculate_pestle_score(metrics)
        elif framework == StrategyFramework.SWOT_ANALYSIS:
            return self._calculate_swot_score(metrics)
        elif framework == StrategyFramework.BCG_MATRIX:
            return self._calculate_bcg_matrix_score(metrics)
        elif framework == StrategyFramework.ANSOFF_MATRIX:
            return self._calculate_ansoff_matrix_score(metrics)
        else:
            return 0.5, 0.5, "Unknown framework"
    
    def _calculate_porters_five_forces_score(self, metrics: List[ExtractedMetric]) -> Tuple[float, float, str]:
        """Calculate Porter's Five Forces score using traditional methodology"""
        
        # Porter's Five Forces: Lower scores = better competitive position
        # We invert the scale so higher scores = better position
        
        force_scores = {}
        reasoning_parts = []
        
        for metric in metrics:
            if metric.metric == StrategicMetric.RIVALRY_INTENSITY:
                # Invert: 5 (intense) -> 1 (bad), 1 (low) -> 5 (good)
                force_scores["rivalry"] = 6 - metric.value
                reasoning_parts.append(f"Rivalry: {metric.value}/5 -> {6-metric.value}/5")
            
            elif metric.metric == StrategicMetric.SUPPLIER_POWER:
                # Invert: 5 (high power) -> 1 (bad), 1 (low power) -> 5 (good)
                force_scores["supplier_power"] = 6 - metric.value
                reasoning_parts.append(f"Supplier Power: {metric.value}/5 -> {6-metric.value}/5")
            
            elif metric.metric == StrategicMetric.BUYER_POWER:
                # Invert: 5 (high power) -> 1 (bad), 1 (low power) -> 5 (good)
                force_scores["buyer_power"] = 6 - metric.value
                reasoning_parts.append(f"Buyer Power: {metric.value}/5 -> {6-metric.value}/5")
            
            elif metric.metric == StrategicMetric.THREAT_OF_NEW_ENTRANTS:
                # Invert: 5 (high threat) -> 1 (bad), 1 (low threat) -> 5 (good)
                force_scores["new_entrants"] = 6 - metric.value
                reasoning_parts.append(f"New Entrants: {metric.value}/5 -> {6-metric.value}/5")
            
            elif metric.metric == StrategicMetric.THREAT_OF_SUBSTITUTES:
                # Invert: 5 (high threat) -> 1 (bad), 1 (low threat) -> 5 (good)
                force_scores["substitutes"] = 6 - metric.value
                reasoning_parts.append(f"Substitutes: {metric.value}/5 -> {6-metric.value}/5")
        
        if force_scores:
            # Calculate average score (0-1 scale)
            avg_score = sum(force_scores.values()) / (len(force_scores) * 5)
            
            # Calculate confidence based on available metrics
            confidence = min(1.0, len(force_scores) / 5.0)
            
            reasoning = f"Porter's Five Forces: {'; '.join(reasoning_parts)}. Average: {avg_score:.2f}"
            
            return avg_score, confidence, reasoning
        
        return 0.5, 0.3, "No Porter's Five Forces metrics available"
    
    def _calculate_pestle_score(self, metrics: List[ExtractedMetric]) -> Tuple[float, float, str]:
        """Calculate PESTLE score using traditional methodology"""
        
        category_scores = {}
        reasoning_parts = []
        
        for metric in metrics:
            if metric.metric == StrategicMetric.POLITICAL_STABILITY:
                category_scores["political"] = metric.value / 5.0
                reasoning_parts.append(f"Political: {metric.value}/5")
            
            elif metric.metric == StrategicMetric.ECONOMIC_GROWTH_RATE:
                # Convert percentage to 0-1 scale (assume 0-20% range)
                normalized_value = min(1.0, max(0.0, metric.value / 20.0))
                category_scores["economic"] = normalized_value
                reasoning_parts.append(f"Economic: {metric.value}% -> {normalized_value:.2f}")
            
            elif metric.metric == StrategicMetric.SOCIAL_TREND_STRENGTH:
                category_scores["social"] = metric.value / 5.0
                reasoning_parts.append(f"Social: {metric.value}/5")
            
            elif metric.metric == StrategicMetric.TECHNOLOGICAL_ADVANCEMENT:
                category_scores["technological"] = metric.value / 5.0
                reasoning_parts.append(f"Technological: {metric.value}/5")
            
            elif metric.metric == StrategicMetric.LEGAL_COMPLEXITY:
                # Invert: 5 (complex) -> 0 (bad), 1 (simple) -> 1 (good)
                category_scores["legal"] = (6 - metric.value) / 5.0
                reasoning_parts.append(f"Legal: {metric.value}/5 -> {(6-metric.value)/5:.2f}")
            
            elif metric.metric == StrategicMetric.ENVIRONMENTAL_IMPACT:
                # Invert: 5 (high impact) -> 0 (bad), 1 (low impact) -> 1 (good)
                category_scores["environmental"] = (6 - metric.value) / 5.0
                reasoning_parts.append(f"Environmental: {metric.value}/5 -> {(6-metric.value)/5:.2f}")
        
        if category_scores:
            avg_score = sum(category_scores.values()) / len(category_scores)
            confidence = min(1.0, len(category_scores) / 6.0)
            reasoning = f"PESTLE Analysis: {'; '.join(reasoning_parts)}. Average: {avg_score:.2f}"
            
            return avg_score, confidence, reasoning
        
        return 0.5, 0.3, "No PESTLE metrics available"
    
    def _calculate_swot_score(self, metrics: List[ExtractedMetric]) -> Tuple[float, float, str]:
        """Calculate SWOT score using traditional methodology"""
        
        # SWOT: Higher scores = better position
        swot_scores = []
        reasoning_parts = []
        
        for metric in metrics:
            if metric.metric == StrategicMetric.MARKET_SIZE_USD:
                # Normalize market size (assume 0-1T range)
                normalized_value = min(1.0, max(0.0, metric.value / 1e12))
                swot_scores.append(normalized_value)
                reasoning_parts.append(f"Market Size: ${metric.value:,.0f} -> {normalized_value:.2f}")
            
            elif metric.metric == StrategicMetric.MARKET_GROWTH_RATE:
                # Convert percentage to 0-1 scale (assume 0-50% range)
                normalized_value = min(1.0, max(0.0, metric.value / 50.0))
                swot_scores.append(normalized_value)
                reasoning_parts.append(f"Market Growth: {metric.value}% -> {normalized_value:.2f}")
            
            elif metric.metric == StrategicMetric.DIFFERENTIATION_LEVEL:
                swot_scores.append(metric.value / 5.0)
                reasoning_parts.append(f"Differentiation: {metric.value}/5")
            
            elif metric.metric == StrategicMetric.BRAND_RECOGNITION:
                swot_scores.append(metric.value / 5.0)
                reasoning_parts.append(f"Brand Recognition: {metric.value}/5")
            
            elif metric.metric == StrategicMetric.REVENUE_POTENTIAL_USD:
                # Normalize revenue potential (assume 0-100M range)
                normalized_value = min(1.0, max(0.0, metric.value / 1e8))
                swot_scores.append(normalized_value)
                reasoning_parts.append(f"Revenue Potential: ${metric.value:,.0f} -> {normalized_value:.2f}")
            
            elif metric.metric == StrategicMetric.COST_STRUCTURE_EFFICIENCY:
                swot_scores.append(metric.value / 5.0)
                reasoning_parts.append(f"Cost Efficiency: {metric.value}/5")
        
        if swot_scores:
            avg_score = sum(swot_scores) / len(swot_scores)
            confidence = min(1.0, len(swot_scores) / 6.0)
            reasoning = f"SWOT Analysis: {'; '.join(reasoning_parts)}. Average: {avg_score:.2f}"
            
            return avg_score, confidence, reasoning
        
        return 0.5, 0.3, "No SWOT metrics available"
    
    def _calculate_bcg_matrix_score(self, metrics: List[ExtractedMetric]) -> Tuple[float, float, str]:
        """Calculate BCG Matrix score using traditional methodology"""
        
        # BCG Matrix: Higher scores = better position
        bcg_scores = []
        reasoning_parts = []
        
        for metric in metrics:
            if metric.metric == StrategicMetric.MARKET_GROWTH_RATE:
                # Convert percentage to 0-1 scale (assume 0-30% range)
                normalized_value = min(1.0, max(0.0, metric.value / 30.0))
                bcg_scores.append(normalized_value)
                reasoning_parts.append(f"Market Growth: {metric.value}% -> {normalized_value:.2f}")
            
            elif metric.metric == StrategicMetric.MARKET_SHARE_PERCENTAGE:
                # Convert percentage to 0-1 scale (assume 0-100% range)
                normalized_value = metric.value / 100.0
                bcg_scores.append(normalized_value)
                reasoning_parts.append(f"Market Share: {metric.value}% -> {normalized_value:.2f}")
            
            elif metric.metric == StrategicMetric.MARKET_SIZE_USD:
                # Normalize market size (assume 0-1T range)
                normalized_value = min(1.0, max(0.0, metric.value / 1e12))
                bcg_scores.append(normalized_value)
                reasoning_parts.append(f"Market Size: ${metric.value:,.0f} -> {normalized_value:.2f}")
            
            elif metric.metric == StrategicMetric.COMPETITOR_COUNT:
                # Invert: More competitors = lower score (assume 0-100 range)
                normalized_value = max(0.0, 1.0 - (metric.value / 100.0))
                bcg_scores.append(normalized_value)
                reasoning_parts.append(f"Competitors: {metric.value} -> {normalized_value:.2f}")
        
        if bcg_scores:
            avg_score = sum(bcg_scores) / len(bcg_scores)
            confidence = min(1.0, len(bcg_scores) / 4.0)
            reasoning = f"BCG Matrix: {'; '.join(reasoning_parts)}. Average: {avg_score:.2f}"
            
            return avg_score, confidence, reasoning
        
        return 0.5, 0.3, "No BCG Matrix metrics available"
    
    def _calculate_ansoff_matrix_score(self, metrics: List[ExtractedMetric]) -> Tuple[float, float, str]:
        """Calculate Ansoff Matrix score using traditional methodology"""
        
        # Ansoff Matrix: Higher scores = better position
        ansoff_scores = []
        reasoning_parts = []
        
        for metric in metrics:
            if metric.metric == StrategicMetric.MARKET_MATURITY_STAGE:
                # Invert: 1 (mature) -> 0 (bad), 5 (early) -> 1 (good)
                normalized_value = (6 - metric.value) / 5.0
                ansoff_scores.append(normalized_value)
                reasoning_parts.append(f"Market Maturity: {metric.value}/5 -> {normalized_value:.2f}")
            
            elif metric.metric == StrategicMetric.DIFFERENTIATION_LEVEL:
                ansoff_scores.append(metric.value / 5.0)
                reasoning_parts.append(f"Differentiation: {metric.value}/5")
            
            elif metric.metric == StrategicMetric.CUSTOMER_SEGMENT_SIZE:
                # Normalize customer segment size (assume 0-100M range)
                normalized_value = min(1.0, max(0.0, metric.value / 1e8))
                ansoff_scores.append(normalized_value)
                reasoning_parts.append(f"Customer Segment: {metric.value:,} -> {normalized_value:.2f}")
            
            elif metric.metric == StrategicMetric.SCALABILITY_FACTOR:
                ansoff_scores.append(metric.value / 5.0)
                reasoning_parts.append(f"Scalability: {metric.value}/5")
        
        if ansoff_scores:
            avg_score = sum(ansoff_scores) / len(ansoff_scores)
            confidence = min(1.0, len(ansoff_scores) / 4.0)
            reasoning = f"Ansoff Matrix: {'; '.join(reasoning_parts)}. Average: {avg_score:.2f}"
            
            return avg_score, confidence, reasoning
        
        return 0.5, 0.3, "No Ansoff Matrix metrics available"
    
    def _determine_strategic_position(self, overall_score: float, framework_scores: List[FrameworkScore]) -> str:
        """Determine strategic position based on overall score and framework analysis"""
        if overall_score >= 0.8:
            return "Strong competitive advantage with excellent market positioning"
        elif overall_score >= 0.6:
            return "Moderate competitive position with room for improvement"
        elif overall_score >= 0.4:
            return "Challenged competitive position requiring strategic intervention"
        else:
            return "Weak competitive position requiring significant strategic changes"
    
    def _generate_strategic_insights(self, framework_scores: List[FrameworkScore], metrics: List[ExtractedMetric]) -> List[str]:
        """Generate strategic insights from framework scores and metrics"""
        insights = []
        
        # Find strongest and weakest frameworks
        sorted_frameworks = sorted(framework_scores, key=lambda x: x.score, reverse=True)
        
        if sorted_frameworks:
            strongest = sorted_frameworks[0]
            weakest = sorted_frameworks[-1]
            
            insights.append(f"Strongest strategic framework: {strongest.framework.value.replace('_', ' ').title()} (Score: {strongest.score:.2f})")
            insights.append(f"Area for improvement: {weakest.framework.value.replace('_', ' ').title()} (Score: {weakest.score:.2f})")
            
            # Framework-specific insights
            if strongest.framework == StrategyFramework.PORTERS_FIVE_FORCES:
                insights.append("Strong competitive positioning with favorable industry structure")
            elif strongest.framework == StrategyFramework.PESTLE_ANALYSIS:
                insights.append("Excellent external environment with supportive macro factors")
            elif strongest.framework == StrategyFramework.SWOT_ANALYSIS:
                insights.append("Strong internal capabilities with good market opportunities")
            
            if weakest.framework == StrategyFramework.PORTERS_FIVE_FORCES:
                insights.append("Industry structure presents significant competitive challenges")
            elif weakest.framework == StrategyFramework.PESTLE_ANALYSIS:
                insights.append("External environment poses risks and challenges")
            elif weakest.framework == StrategyFramework.SWOT_ANALYSIS:
                insights.append("Internal weaknesses and external threats require attention")
        
        # Metric-specific insights
        high_value_metrics = [m for m in metrics if hasattr(m.value, '__float__') and m.value > 0.7]
        low_value_metrics = [m for m in metrics if hasattr(m.value, '__float__') and m.value < 0.3]
        
        if high_value_metrics:
            insights.append(f"Key strengths identified in {len(high_value_metrics)} strategic areas")
        
        if low_value_metrics:
            insights.append(f"Critical weaknesses identified in {len(low_value_metrics)} strategic areas")
        
        return insights
    
    def _generate_strategic_recommendations(self, framework_scores: List[FrameworkScore], metrics: List[ExtractedMetric]) -> List[str]:
        """Generate strategic recommendations from framework scores and metrics"""
        recommendations = []
        
        for framework in framework_scores:
            if framework.score < 0.5:
                if framework.framework == StrategyFramework.PORTERS_FIVE_FORCES:
                    recommendations.append("Develop strategies to improve competitive positioning and reduce industry threats")
                elif framework.framework == StrategyFramework.PESTLE_ANALYSIS:
                    recommendations.append("Address external environment challenges and leverage supportive macro factors")
                elif framework.framework == StrategyFramework.SWOT_ANALYSIS:
                    recommendations.append("Strengthen internal capabilities and mitigate external threats")
                elif framework.framework == StrategyFramework.BCG_MATRIX:
                    recommendations.append("Optimize market portfolio strategy and improve market share positioning")
                elif framework.framework == StrategyFramework.ANSOFF_MATRIX:
                    recommendations.append("Refine market expansion strategy and product development approach")
            
            if framework.score > 0.7:
                if framework.framework == StrategyFramework.PORTERS_FIVE_FORCES:
                    recommendations.append("Leverage strong competitive position for market expansion")
                elif framework.framework == StrategyFramework.PESTLE_ANALYSIS:
                    recommendations.append("Capitalize on favorable external environment for growth")
                elif framework.framework == StrategyFramework.SWOT_ANALYSIS:
                    recommendations.append("Maximize strengths and opportunities for competitive advantage")
        
        return recommendations
    
    def _assess_strategic_risks(self, framework_scores: List[FrameworkScore], metrics: List[ExtractedMetric]) -> Dict[str, Any]:
        """Assess strategic risks based on framework scores and metrics"""
        risks = {
            "overall_risk_level": "medium",
            "high_risk_frameworks": [],
            "risk_factors": []
        }
        
        for framework in framework_scores:
            if framework.score < 0.4:
                risks["high_risk_frameworks"].append({
                    "framework": framework.framework.value,
                    "score": framework.score,
                    "risk": f"Critical weakness in {framework.framework.value.replace('_', ' ').title()} analysis"
                })
        
        # Determine overall risk level
        low_scores = [f for f in framework_scores if f.score < 0.4]
        if len(low_scores) >= 3:
            risks["overall_risk_level"] = "high"
        elif len(low_scores) >= 1:
            risks["overall_risk_level"] = "medium"
        else:
            risks["overall_risk_level"] = "low"
        
        return risks
    
    def _analyze_strategic_opportunities(self, framework_scores: List[FrameworkScore], metrics: List[ExtractedMetric]) -> Dict[str, Any]:
        """Analyze strategic opportunities based on framework scores and metrics"""
        opportunities = {
            "overall_opportunity_level": "medium",
            "high_potential_frameworks": [],
            "opportunity_factors": []
        }
        
        for framework in framework_scores:
            if framework.score > 0.7:
                opportunities["high_potential_frameworks"].append({
                    "framework": framework.framework.value,
                    "score": framework.score,
                    "opportunity": f"Strong foundation in {framework.framework.value.replace('_', ' ').title()} for growth"
                })
        
        # Determine overall opportunity level
        high_scores = [f for f in framework_scores if f.score > 0.7]
        if len(high_scores) >= 3:
            opportunities["overall_opportunity_level"] = "high"
        elif len(high_scores) >= 1:
            opportunities["overall_opportunity_level"] = "medium"
        else:
            opportunities["overall_opportunity_level"] = "low"
        
        return opportunities
    
    def _extract_insights_from_llm(self, llm_analysis: Dict[str, Any]) -> List[str]:
        """Extract insights from LLM analysis results"""
        insights = []
        
        if "consensus_result" in llm_analysis and "insights" in llm_analysis["consensus_result"]:
            insights.extend(llm_analysis["consensus_result"]["insights"])
        
        if "individual_results" in llm_analysis:
            for result in llm_analysis["individual_results"]:
                if "key_insights" in result:
                    insights.extend(result["key_insights"])
        
        return list(set(insights))  # Remove duplicates
    
    def _extract_recommendations_from_llm(self, llm_analysis: Dict[str, Any]) -> List[str]:
        """Extract recommendations from LLM analysis results"""
        recommendations = []
        
        if "consensus_result" in llm_analysis and "recommendations" in llm_analysis["consensus_result"]:
            recommendations.extend(llm_analysis["consensus_result"]["recommendations"])
        
        if "individual_results" in llm_analysis:
            for result in llm_analysis["individual_results"]:
                if "recommendations" in result:
                    recommendations.extend(result["recommendations"])
        
        return list(set(recommendations))  # Remove duplicates
