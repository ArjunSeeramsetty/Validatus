#!/usr/bin/env python3
"""
Fixed Comprehensive LangGraph Workflow with Context-Aware Layer Scoring
Implements proper state management and intelligent orchestration of layer analysis order
"""

import os
import sys
import asyncio
import logging
import json
from typing import Dict, List, Any, TypedDict, Optional
from langgraph.graph import StateGraph, END
from datetime import datetime
from dataclasses import dataclass

from app.core.comprehensive_analytical_framework_fixed import (
    ComprehensiveAnalyticalFramework, LayerScore, FactorScore, SegmentScore
)
from app.core.simple_state import State as AppState

logger = logging.getLogger(__name__)

@dataclass
class LayerContext:
    """Context information for a layer analysis"""
    segment: str
    factor: str
    layer: str
    dependencies: List[str]  # Layers this depends on
    provides_context_for: List[str]  # Layers this provides context for
    analysis_priority: int  # Lower number = higher priority
    persona: str
    context_summary: Optional[str] = None

class ComprehensiveGraphState(TypedDict):
    """Enhanced state for LangGraph workflow with context management"""
    app_state: AppState
    layer_scores: Dict[str, LayerScore]
    factor_scores: Dict[str, FactorScore]
    segment_scores: Dict[str, SegmentScore]
    analysis_results: Dict[str, Any]
    error_message: str
    current_step: str
    completed_steps: List[str]
    retry_count: int
    context_memory: Dict[str, str]  # Layer -> Context summary
    analysis_progress: Dict[str, Dict[str, Any]]  # Segment -> Progress info
    strategic_insights: List[str]  # Accumulated strategic insights

class ContextAwareLangGraphWorkflow:
    """
    Fixed LangGraph workflow with context-aware layer scoring and proper state management
    """
    
    def __init__(self):
        self.analytical_framework = ComprehensiveAnalyticalFramework()
        self.layer_contexts = self._build_layer_contexts()
        self.graph = self.build_graph()
        
    def _build_layer_contexts(self) -> Dict[str, LayerContext]:
        """Build context-aware layer orchestration map"""
        contexts = {}
        
        # Define layer dependencies and context flow
        layer_mapping = {
            # CONSUMER SEGMENT - Foundation for other analyses
            "need_perception_consumer_demand": LayerContext(
                segment="CONSUMER", factor="Consumer Demand & Need", layer="need_perception_consumer_demand",
                dependencies=[], provides_context_for=["purchase_intent_consumer_demand", "emotional_pull_consumer_demand"],
                analysis_priority=1, persona="consumer_insights"
            ),
            "purchase_intent_consumer_demand": LayerContext(
                segment="CONSUMER", factor="Consumer Demand & Need", layer="purchase_intent_consumer_demand",
                dependencies=["need_perception_consumer_demand"], provides_context_for=["unmet_needs_consumer_demand"],
                analysis_priority=2, persona="consumer_insights"
            ),
            "emotional_pull_consumer_demand": LayerContext(
                segment="CONSUMER", factor="Consumer Demand & Need", layer="emotional_pull_consumer_demand",
                dependencies=["need_perception_consumer_demand"], provides_context_for=["unmet_needs_consumer_demand"],
                analysis_priority=2, persona="consumer_insights"
            ),
            "unmet_needs_consumer_demand": LayerContext(
                segment="CONSUMER", factor="Consumer Demand & Need", layer="unmet_needs_consumer_demand",
                dependencies=["need_perception_consumer_demand", "purchase_intent_consumer_demand", "emotional_pull_consumer_demand"],
                provides_context_for=["shopping_habits_consumer_behavior", "decision_making_process_consumer_behavior"],
                analysis_priority=3, persona="consumer_insights"
            ),
            
            # MARKET SEGMENT - Builds on consumer insights
            "total_addressable_market_market_size": LayerContext(
                segment="MARKET", factor="Market Size & Growth", layer="total_addressable_market_market_size",
                dependencies=["need_perception_consumer_demand", "purchase_intent_consumer_demand"],
                provides_context_for=["serviceable_addressable_market_market_size", "market_growth_rate_market_size"],
                analysis_priority=4, persona="market_researcher"
            ),
            "key_competitors_competitive_landscape": LayerContext(
                segment="MARKET", factor="Competitive Landscape", layer="key_competitors_competitive_landscape",
                dependencies=["total_addressable_market_market_size", "unmet_needs_consumer_demand"],
                provides_context_for=["market_share_distribution_competitive_landscape", "competitor_strengths_weaknesses_competitive_landscape"],
                analysis_priority=5, persona="competitor_analysis"
            ),
            
            # PRODUCT SEGMENT - Builds on market and consumer insights
            "core_features_analysis_features_functionality": LayerContext(
                segment="PRODUCT", factor="Features & Functionality", layer="core_features_analysis_features_functionality",
                dependencies=["unmet_needs_consumer_demand", "key_competitors_competitive_landscape"],
                provides_context_for=["feature_completeness_features_functionality", "user_friendliness_features_functionality"],
                analysis_priority=6, persona="product_strategist"
            ),
            "unique_selling_proposition_innovation_differentiation": LayerContext(
                segment="PRODUCT", factor="Innovation & Differentiation", layer="unique_selling_proposition_innovation_differentiation",
                dependencies=["core_features_analysis_features_functionality", "competitor_strengths_weaknesses_competitive_landscape"],
                provides_context_for=["technological_innovation_innovation_differentiation", "design_innovation_innovation_differentiation"],
                analysis_priority=7, persona="product_strategist"
            ),
            
            # BRAND SEGMENT - Builds on product and consumer insights
            "brand_positioning_brand_positioning_strategy": LayerContext(
                segment="BRAND", factor="Brand Positioning Strategy", layer="brand_positioning_brand_positioning_strategy",
                dependencies=["unique_selling_proposition_innovation_differentiation", "emotional_pull_consumer_demand"],
                provides_context_for=["target_audience_alignment_brand_positioning_strategy", "competitive_differentiation_brand_positioning_strategy"],
                analysis_priority=8, persona="brand_strategist"
            ),
            
            # EXPERIENCE SEGMENT - Builds on all previous insights
            "onboarding_experience_user_experience_ux_design": LayerContext(
                segment="EXPERIENCE", factor="User Experience (UX) & Design", layer="onboarding_experience_user_experience_ux_design",
                dependencies=["user_friendliness_features_functionality", "brand_positioning_brand_positioning_strategy"],
                provides_context_for=["ease_of_use_user_experience_ux_design", "navigation_clarity_user_experience_ux_design"],
                analysis_priority=9, persona="ux_strategist"
            )
        }
        
        # Add all other layers with default contexts
        all_layers = self.analytical_framework.get_all_layers()
        for layer in all_layers:
            if layer not in layer_mapping:
                # Determine segment and factor from layer name
                segment, factor = self._extract_segment_factor(layer)
                contexts[layer] = LayerContext(
                    segment=segment, factor=factor, layer=layer,
                    dependencies=[], provides_context_for=[], analysis_priority=10,
                    persona=self._get_default_persona(segment)
                )
            else:
                contexts[layer] = layer_mapping[layer]
        
        return contexts
    
    def _extract_segment_factor(self, layer_name: str) -> tuple:
        """Extract segment and factor from context-aware layer name"""
        # Handle context-aware naming: layer_segment_factor
        parts = layer_name.split('_')
        if len(parts) >= 3:
            # Last two parts are factor and segment
            factor = '_'.join(parts[-2:])
            segment = parts[-1].upper()
            return segment, factor
        else:
            # Fallback to default mapping
            return "CONSUMER", "General Analysis"
    
    def _get_default_persona(self, segment: str) -> str:
        """Get default persona for a segment"""
        persona_map = {
            "CONSUMER": "consumer_insights",
            "MARKET": "market_researcher", 
            "PRODUCT": "product_strategist",
            "BRAND": "brand_strategist",
            "EXPERIENCE": "ux_strategist"
        }
        return persona_map.get(segment, "strategic_analyst")
    
    def _get_analysis_order(self) -> List[str]:
        """Get optimal analysis order based on dependencies"""
        # Sort layers by priority and dependencies
        sorted_layers = sorted(
            self.layer_contexts.values(),
            key=lambda x: (x.analysis_priority, len(x.dependencies))
        )
        return [ctx.layer for ctx in sorted_layers]
    
    def build_graph(self):
        """Build the fixed computational graph with proper state management"""
        try:
            workflow = StateGraph(ComprehensiveGraphState)
            
            # Add nodes for each analytical segment with context awareness
            workflow.add_node("consumer_analysis", self.run_consumer_analysis)
            workflow.add_node("market_analysis", self.run_market_analysis)
            workflow.add_node("product_analysis", self.run_product_analysis)
            workflow.add_node("brand_analysis", self.run_brand_analysis)
            workflow.add_node("experience_analysis", self.run_experience_analysis)
            workflow.add_node("factor_calculation", self.calculate_all_factors)
            workflow.add_node("segment_calculation", self.calculate_all_segments)
            workflow.add_node("strategic_synthesis", self.generate_strategic_synthesis)
            
            # Define sequential workflow with proper state flow
            workflow.set_entry_point("consumer_analysis")
            workflow.add_edge("consumer_analysis", "market_analysis")
            workflow.add_edge("market_analysis", "product_analysis")
            workflow.add_edge("product_analysis", "brand_analysis")
            workflow.add_edge("brand_analysis", "experience_analysis")
            workflow.add_edge("experience_analysis", "factor_calculation")
            workflow.add_edge("factor_calculation", "segment_calculation")
            workflow.add_edge("segment_calculation", "strategic_synthesis")
            workflow.add_edge("strategic_synthesis", END)
            
            compiled_graph = workflow.compile()
            logger.info("✅ Fixed LangGraph workflow compiled successfully")
            return compiled_graph
            
        except Exception as e:
            logger.error(f"❌ Failed to build fixed workflow: {str(e)}")
            raise

    async def run_consumer_analysis(self, state: ComprehensiveGraphState) -> ComprehensiveGraphState:
        """Run consumer analysis with context-aware layer ordering"""
        logger.info("👥 Running Context-Aware Consumer Analysis")
        
        try:
            app_state = state['app_state']
            idea_description = app_state.idea_description
            target_audience = app_state.target_audience
            
            # Get consumer layers in optimal order
            consumer_layers = [layer for layer in self._get_analysis_order() 
                             if self.layer_contexts[layer].segment == "CONSUMER"]
            
            layer_scores = {}
            context_memory = state.get('context_memory', {})
            
            for layer in consumer_layers:
                # Build context from previous analyses
                context = self._build_layer_context(layer, context_memory, layer_scores)
                
                # Analyze layer with context
                layer_score = await self.analytical_framework.analyze_layer(
                    layer, idea_description, target_audience, 
                    {
                        "analysis_type": "consumer", 
                        "layer": layer, 
                        "persona": self.layer_contexts[layer].persona,
                        "context": context,
                        "previous_insights": list(context_memory.values())
                    }
                )
                
                layer_scores[layer] = layer_score
                
                # Store context for future layers
                context_memory[layer] = f"Consumer {layer}: {layer_score.score}/10 - {layer_score.rationale[:100] if layer_score.rationale else 'No rationale'}"
                
                logger.info(f"✅ Consumer layer {layer}: {layer_score.score}/10")
            
            # Update state properly
            new_state = state.copy()
            new_state['layer_scores'].update(layer_scores)
            new_state['context_memory'] = context_memory
            new_state['completed_steps'].append("consumer_analysis")
            new_state['current_step'] = "consumer_analysis"
            new_state['analysis_progress']['CONSUMER'] = {
                'layers_analyzed': len(layer_scores),
                'average_score': sum(ls.score for ls in layer_scores.values()) / len(layer_scores) if layer_scores else 0.0,
                'completion_time': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Consumer analysis completed with {len(layer_scores)} layers")
            return new_state
            
        except Exception as e:
            logger.error(f"❌ Consumer analysis failed: {str(e)}")
            new_state = state.copy()
            new_state['error_message'] = f"Consumer analysis failed: {str(e)}"
            return new_state

    async def run_market_analysis(self, state: ComprehensiveGraphState) -> ComprehensiveGraphState:
        """Run market analysis with consumer context"""
        logger.info("🔍 Running Context-Aware Market Analysis")
        
        try:
            app_state = state['app_state']
            idea_description = app_state.idea_description
            target_audience = app_state.target_audience
            
            # Get market layers in optimal order
            market_layers = [layer for layer in self._get_analysis_order() 
                           if self.layer_contexts[layer].segment == "MARKET"]
            
            layer_scores = {}
            context_memory = state.get('context_memory', {})
            
            for layer in market_layers:
                # Build context from consumer analysis
                context = self._build_layer_context(layer, context_memory, layer_scores)
                
                layer_score = await self.analytical_framework.analyze_layer(
                    layer, idea_description, target_audience,
                    {
                        "analysis_type": "market", 
                        "layer": layer, 
                        "persona": self.layer_contexts[layer].persona,
                        "context": context,
                        "consumer_insights": {k: v for k, v in context_memory.items() if 'consumer' in k.lower()}
                    }
                )
                
                layer_scores[layer] = layer_score
                context_memory[layer] = f"Market {layer}: {layer_score.score}/10 - {layer_score.rationale[:100] if layer_score.rationale else 'No rationale'}"
                
                logger.info(f"✅ Market layer {layer}: {layer_score.score}/10")
            
            # Update state properly
            new_state = state.copy()
            new_state['layer_scores'].update(layer_scores)
            new_state['context_memory'] = context_memory
            new_state['completed_steps'].append("market_analysis")
            new_state['current_step'] = "market_analysis"
            new_state['analysis_progress']['MARKET'] = {
                'layers_analyzed': len(layer_scores),
                'average_score': sum(ls.score for ls in layer_scores.values()) / len(layer_scores) if layer_scores else 0.0,
                'completion_time': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Market analysis completed with {len(layer_scores)} layers")
            return new_state
            
        except Exception as e:
            logger.error(f"❌ Market analysis failed: {str(e)}")
            new_state = state.copy()
            new_state['error_message'] = f"Market analysis failed: {str(e)}"
            return new_state

    async def run_product_analysis(self, state: ComprehensiveGraphState) -> ComprehensiveGraphState:
        """Run product analysis with consumer and market context"""
        logger.info("📦 Running Context-Aware Product Analysis")
        
        try:
            app_state = state['app_state']
            idea_description = app_state.idea_description
            target_audience = app_state.target_audience
            
            # Get product layers in optimal order
            product_layers = [layer for layer in self._get_analysis_order() 
                            if self.layer_contexts[layer].segment == "PRODUCT"]
            
            layer_scores = {}
            context_memory = state.get('context_memory', {})
            
            for layer in product_layers:
                # Build context from previous analyses
                context = self._build_layer_context(layer, context_memory, layer_scores)
                
                layer_score = await self.analytical_framework.analyze_layer(
                    layer, idea_description, target_audience,
                    {
                        "analysis_type": "product", 
                        "layer": layer, 
                        "persona": self.layer_contexts[layer].persona,
                        "context": context,
                        "consumer_insights": {k: v for k, v in context_memory.items() if 'consumer' in k.lower()},
                        "market_insights": {k: v for k, v in context_memory.items() if 'market' in k.lower()}
                    }
                )
                
                layer_scores[layer] = layer_score
                context_memory[layer] = f"Product {layer}: {layer_score.score}/10 - {layer_score.rationale[:100] if layer_score.rationale else 'No rationale'}"
                
                logger.info(f"✅ Product layer {layer}: {layer_score.score}/10")
            
            # Update state properly
            new_state = state.copy()
            new_state['layer_scores'].update(layer_scores)
            new_state['context_memory'] = context_memory
            new_state['completed_steps'].append("product_analysis")
            new_state['current_step'] = "product_analysis"
            new_state['analysis_progress']['PRODUCT'] = {
                'layers_analyzed': len(layer_scores),
                'average_score': sum(ls.score for ls in layer_scores.values()) / len(layer_scores) if layer_scores else 0.0,
                'completion_time': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Product analysis completed with {len(layer_scores)} layers")
            return new_state
            
        except Exception as e:
            logger.error(f"❌ Product analysis failed: {str(e)}")
            new_state = state.copy()
            new_state['error_message'] = f"Product analysis failed: {str(e)}"
            return new_state

    async def run_brand_analysis(self, state: ComprehensiveGraphState) -> ComprehensiveGraphState:
        """Run brand analysis with comprehensive context"""
        logger.info("🏷️ Running Context-Aware Brand Analysis")
        
        try:
            app_state = state['app_state']
            idea_description = app_state.idea_description
            target_audience = app_state.target_audience
            
            # Get brand layers in optimal order
            brand_layers = [layer for layer in self._get_analysis_order() 
                          if self.layer_contexts[layer].segment == "BRAND"]
            
            layer_scores = {}
            context_memory = state.get('context_memory', {})
            
            for layer in brand_layers:
                # Build context from all previous analyses
                context = self._build_layer_context(layer, context_memory, layer_scores)
                
                layer_score = await self.analytical_framework.analyze_layer(
                    layer, idea_description, target_audience,
                    {
                        "analysis_type": "brand", 
                        "layer": layer, 
                        "persona": self.layer_contexts[layer].persona,
                        "context": context,
                        "strategic_context": {
                            "consumer_insights": {k: v for k, v in context_memory.items() if 'consumer' in k.lower()},
                            "market_insights": {k: v for k, v in context_memory.items() if 'market' in k.lower()},
                            "product_insights": {k: v for k, v in context_memory.items() if 'product' in k.lower()}
                        }
                    }
                )
                
                layer_scores[layer] = layer_score
                context_memory[layer] = f"Brand {layer}: {layer_score.score}/10 - {layer_score.rationale[:100] if layer_score.rationale else 'No rationale'}"
                
                logger.info(f"✅ Brand layer {layer}: {layer_score.score}/10")
            
            # Update state properly
            new_state = state.copy()
            new_state['layer_scores'].update(layer_scores)
            new_state['context_memory'] = context_memory
            new_state['completed_steps'].append("brand_analysis")
            new_state['current_step'] = "brand_analysis"
            new_state['analysis_progress']['BRAND'] = {
                'layers_analyzed': len(layer_scores),
                'average_score': sum(ls.score for ls in layer_scores.values()) / len(layer_scores) if layer_scores else 0.0,
                'completion_time': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Brand analysis completed with {len(layer_scores)} layers")
            return new_state
            
        except Exception as e:
            logger.error(f"❌ Brand analysis failed: {str(e)}")
            new_state = state.copy()
            new_state['error_message'] = f"Brand analysis failed: {str(e)}"
            return new_state

    async def run_experience_analysis(self, state: ComprehensiveGraphState) -> ComprehensiveGraphState:
        """Run experience analysis with full strategic context"""
        logger.info("🎯 Running Context-Aware Experience Analysis")
        
        try:
            app_state = state['app_state']
            idea_description = app_state.idea_description
            target_audience = app_state.target_audience
            
            # Get experience layers in optimal order
            experience_layers = [layer for layer in self._get_analysis_order() 
                               if self.layer_contexts[layer].segment == "EXPERIENCE"]
            
            layer_scores = {}
            context_memory = state.get('context_memory', {})
            
            for layer in experience_layers:
                # Build context from all previous analyses
                context = self._build_layer_context(layer, context_memory, layer_scores)
                
                layer_score = await self.analytical_framework.analyze_layer(
                    layer, idea_description, target_audience,
                    {
                        "analysis_type": "experience", 
                        "layer": layer, 
                        "persona": self.layer_contexts[layer].persona,
                        "context": context,
                        "comprehensive_strategic_context": {
                            "consumer_insights": {k: v for k, v in context_memory.items() if 'consumer' in k.lower()},
                            "market_insights": {k: v for k, v in context_memory.items() if 'market' in k.lower()},
                            "product_insights": {k: v for k, v in context_memory.items() if 'product' in k.lower()},
                            "brand_insights": {k: v for k, v in context_memory.items() if 'brand' in k.lower()}
                        }
                    }
                )
                
                layer_scores[layer] = layer_score
                context_memory[layer] = f"Experience {layer}: {layer_score.score}/10 - {layer_score.rationale[:100] if layer_score.rationale else 'No rationale'}"
                
                logger.info(f"✅ Experience layer {layer}: {layer_score.score}/10")
            
            # Update state properly
            new_state = state.copy()
            new_state['layer_scores'].update(layer_scores)
            new_state['context_memory'] = context_memory
            new_state['completed_steps'].append("experience_analysis")
            new_state['current_step'] = "experience_analysis"
            new_state['analysis_progress']['EXPERIENCE'] = {
                'layers_analyzed': len(layer_scores),
                'average_score': sum(ls.score for ls in layer_scores.values()) / len(layer_scores) if layer_scores else 0.0,
                'completion_time': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Experience analysis completed with {len(layer_scores)} layers")
            return new_state
            
        except Exception as e:
            logger.error(f"❌ Experience analysis failed: {str(e)}")
            new_state = state.copy()
            new_state['error_message'] = f"Experience analysis failed: {str(e)}"
            return new_state

    def _build_layer_context(self, layer: str, context_memory: Dict[str, str], 
                           current_scores: Dict[str, LayerScore]) -> str:
        """Build context string for a layer based on previous analyses"""
        layer_ctx = self.layer_contexts[layer]
        
        # Get relevant context from dependencies
        relevant_context = []
        for dep in layer_ctx.dependencies:
            if dep in context_memory:
                relevant_context.append(context_memory[dep])
            elif dep in current_scores:
                relevant_context.append(f"{dep}: {current_scores[dep].score}/10")
        
        # Get strategic insights from related segments
        segment_insights = []
        for ctx_layer, ctx_summary in context_memory.items():
            if self.layer_contexts[ctx_layer].segment == layer_ctx.segment:
                segment_insights.append(ctx_summary)
        
        context_parts = []
        if relevant_context:
            context_parts.append(f"Dependencies: {'; '.join(relevant_context)}")
        if segment_insights:
            context_parts.append(f"Segment Context: {'; '.join(segment_insights[:3])}")  # Limit to 3 insights
        
        return " | ".join(context_parts) if context_parts else "No specific context dependencies"

    async def calculate_all_factors(self, state: ComprehensiveGraphState) -> ComprehensiveGraphState:
        """Calculate factor scores with context awareness"""
        logger.info("🧮 Calculating Factor Scores with Context")
        
        try:
            # Use the existing framework method
            factor_scores = await self.analytical_framework.calculate_all_factors(state['layer_scores'])
            
            # Update state properly
            new_state = state.copy()
            new_state['factor_scores'] = factor_scores
            new_state['completed_steps'].append("factor_calculation")
            new_state['current_step'] = "factor_calculation"
            
            logger.info(f"✅ Factor calculation completed: {len(factor_scores)} factors")
            return new_state
            
        except Exception as e:
            logger.error(f"❌ Factor calculation failed: {str(e)}")
            new_state = state.copy()
            new_state['error_message'] = f"Factor calculation failed: {str(e)}"
            return new_state

    async def calculate_all_segments(self, state: ComprehensiveGraphState) -> ComprehensiveGraphState:
        """Calculate segment scores with context awareness"""
        logger.info("📊 Calculating Segment Scores with Context")
        
        try:
            # Use the existing framework method
            segment_scores = await self.analytical_framework.calculate_all_segments(
                state['layer_scores'], state['factor_scores']
            )
            
            # Update state properly
            new_state = state.copy()
            new_state['segment_scores'] = segment_scores
            new_state['completed_steps'].append("segment_calculation")
            new_state['current_step'] = "segment_calculation"
            
            logger.info(f"✅ Segment calculation completed: {len(segment_scores)} segments")
            return new_state
            
        except Exception as e:
            logger.error(f"❌ Segment calculation failed: {str(e)}")
            new_state = state.copy()
            new_state['error_message'] = f"Segment calculation failed: {str(e)}"
            return new_state

    async def generate_strategic_synthesis(self, state: ComprehensiveGraphState) -> ComprehensiveGraphState:
        """Generate strategic synthesis with full context"""
        logger.info("🎯 Generating Strategic Synthesis with Full Context")
        
        try:
            # Generate comprehensive analysis using the framework
            analysis_results = await self.analytical_framework.generate_comprehensive_analysis(
                state['layer_scores'], state['factor_scores'], state['segment_scores']
            )
            
            # Add context-aware insights
            context_insights = self._extract_strategic_insights(state['context_memory'])
            analysis_results['context_insights'] = context_insights
            analysis_results['analysis_progress'] = state['analysis_progress']
            
            # Update state properly
            new_state = state.copy()
            new_state['analysis_results'] = analysis_results
            new_state['completed_steps'].append("strategic_synthesis")
            new_state['current_step'] = "strategic_synthesis"
            
            logger.info("✅ Strategic synthesis completed")
            return new_state
            
        except Exception as e:
            logger.error(f"❌ Strategic synthesis failed: {str(e)}")
            new_state = state.copy()
            new_state['error_message'] = f"Strategic synthesis failed: {str(e)}"
            return new_state

    def _extract_strategic_insights(self, context_memory: Dict[str, str]) -> List[str]:
        """Extract strategic insights from context memory"""
        insights = []
        
        # Analyze patterns in scores
        high_scores = [ctx for ctx in context_memory.values() if "8/10" in ctx or "9/10" in ctx or "10/10" in ctx]
        low_scores = [ctx for ctx in context_memory.values() if "1/10" in ctx or "2/10" in ctx or "3/10" in ctx]
        
        if high_scores:
            insights.append(f"Strong performance areas: {len(high_scores)} high-scoring layers")
        if low_scores:
            insights.append(f"Critical improvement areas: {len(low_scores)} low-scoring layers")
        
        # Extract segment-specific insights
        segment_analysis = {}
        for layer, context in context_memory.items():
            if ':' in context:
                score_part = context.split(':')[1].split('-')[0].strip()
                if any(segment in layer.lower() for segment in ['consumer', 'market', 'product', 'brand', 'experience']):
                    segment = next(s for s in ['consumer', 'market', 'product', 'brand', 'experience'] if s in layer.lower())
                    if segment not in segment_analysis:
                        segment_analysis[segment] = []
                    segment_analysis[segment].append(score_part)
        
        for segment, scores in segment_analysis.items():
            avg_score = sum(float(s.split('/')[0]) for s in scores) / len(scores)
            insights.append(f"{segment.title()} segment average: {avg_score:.1f}/10")
        
        return insights

    async def execute(self, idea_description: str, target_audience: str, 
                     additional_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the fixed comprehensive workflow"""
        try:
            logger.info("🚀 Starting Fixed Context-Aware LangGraph Workflow")
            logger.info(f"📊 Framework: {len(self.analytical_framework.get_all_layers())} total layers")
            
            # Initialize enhanced state
            initial_app_state = AppState(
                idea_description=idea_description,
                target_audience=target_audience,
                additional_context=additional_context or {}
            )
            
            initial_graph_state = ComprehensiveGraphState(
                app_state=initial_app_state,
                layer_scores={},
                factor_scores={},
                segment_scores={},
                analysis_results={},
                error_message="",
                current_step="",
                completed_steps=[],
                retry_count=0,
                context_memory={},
                analysis_progress={},
                strategic_insights=[]
            )
            
            # Execute workflow with proper state management
            final_state = await self.graph.ainvoke(initial_graph_state)
            
            logger.info("✅ Fixed context-aware workflow completed successfully")
            return final_state.get('analysis_results', {})
            
        except Exception as e:
            logger.error(f"❌ Fixed workflow execution failed: {str(e)}")
            return {"error": str(e), "success": False}

if __name__ == "__main__":
    # Test the fixed comprehensive workflow
    async def test_fixed_workflow():
        workflow = ContextAwareLangGraphWorkflow()
        results = await workflow.execute(
            idea_description="A smart home device that automates pet feeding and playtime with AI monitoring and health tracking",
            target_audience="Busy pet owners aged 25-45 who want to ensure their pets are cared for while away",
            additional_context={
                "market_focus": "smart_home_pet_care",
                "competition_level": "medium",
                "innovation_focus": "automation_and_ai",
                "target_market_size": "growing_pet_tech_sector",
                "analysis_depth": "comprehensive",
                "context_awareness": True
            }
        )
        print(json.dumps(results, indent=2))
    
    asyncio.run(test_fixed_workflow())
