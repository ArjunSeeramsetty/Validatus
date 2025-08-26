#!/usr/bin/env python3
"""
Enhanced Validatus Orchestrator - Top-level coordinator for the Validatus Platform
Integrates Multi-LLM Orchestration, Strategic Scoring, and Knowledge Graph Analysis
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from .multi_llm_orchestrator import MultiLLMOrchestrator
from .strategic_scoring_v4 import StrategicScoringV4, StrategicAnalysisResultV4
from .knowledge_graph_analyzer import KnowledgeGraphAnalyzer

class EnhancedValidatusOrchestrator:
    """
    Top-level orchestrator that coordinates all components of the Validatus Platform
    """
    
    def __init__(self):
        self.logger = logging.getLogger("enhanced.validatus.orchestrator")
        
        # Initialize core components
        self.llm_orchestrator = MultiLLMOrchestrator()
        self.scoring_engine = StrategicScoringV4(self.llm_orchestrator)  # Updated to V4 with LLM orchestrator
        self.knowledge_graph = KnowledgeGraphAnalyzer()
        
        self.logger.info("Enhanced Validatus Orchestrator initialized")
    
    async def execute_workflow(self,
                             query: str,
                             context: Dict[str, Any] = None,
                             analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Execute the complete Validatus workflow
        """
        start_time = datetime.now()
        
        try:
            self.logger.info(f"Starting {analysis_type} analysis workflow for query: {query}")
            
            # Step 1: Multi-LLM Analysis
            self.logger.info("Step 1: Executing Multi-LLM analysis")
            llm_analysis = await self.llm_orchestrator.consensus_analysis(
                query=query,
                context=context or {}
            )
            
            # Step 2: Strategic Framework Analysis
            self.logger.info("Step 2: Executing strategic framework analysis")
            strategic_analysis = await self.scoring_engine.run(
                state={
                    "llm_analysis": llm_analysis,
                    "query": query,
                    "context": context,
                    "idea_description": query
                }
            )
            
            # Step 3: Knowledge Graph Integration (if available)
            self.logger.info("Step 3: Integrating knowledge graph insights")
            knowledge_insights = await self._integrate_knowledge_graph(
                query, strategic_analysis, context
            )
            
            # Step 4: Generate comprehensive results
            self.logger.info("Step 4: Generating comprehensive results")
            results = await self._generate_comprehensive_results(
                query=query,
                context=context or {},
                llm_analysis=llm_analysis,
                strategic_analysis=strategic_analysis,
                knowledge_insights=knowledge_insights,
                analysis_type=analysis_type,
                start_time=start_time
            )
            
            self.logger.info(f"Workflow completed successfully in {results['processing_time']:.2f}s")
            return results
            
        except Exception as e:
            self.logger.error(f"Workflow execution failed: {e}")
            raise
    
    async def _integrate_knowledge_graph(self,
                                       query: str,
                                       strategic_analysis: Dict[str, Any],
                                       context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Integrate knowledge graph insights with strategic analysis
        """
        try:
            # Extract key entities and relationships from strategic analysis
            entities = self._extract_entities_from_analysis(strategic_analysis)
            
            # Query knowledge graph for additional insights
            knowledge_insights = await self.knowledge_graph.relationship_analysis(
                entities=entities
            )
            
            return knowledge_insights
            
        except Exception as e:
            self.logger.warning(f"Knowledge graph integration failed: {e}")
            return {"entities": [], "relationships": [], "insights": []}
    
    def _extract_entities_from_analysis(self, strategic_analysis: Dict[str, Any]) -> List[str]:
        """
        Extract key entities from strategic analysis for knowledge graph querying
        """
        entities = []
        
        # Extract from dimension scores
        for dimension_score in strategic_analysis.get("dimension_scores", []):
            if hasattr(dimension_score, 'dimension'):
                entities.append(dimension_score.dimension.value)
            elif isinstance(dimension_score, dict):
                entities.append(dimension_score.get("dimension", "unknown"))
        
        # Extract from key insights and recommendations
        entities.extend(strategic_analysis.get("key_strengths", []))
        entities.extend(strategic_analysis.get("key_weaknesses", []))
        entities.extend(strategic_analysis.get("strategic_recommendations", []))
        
        # Extract from market positioning and competitive advantage
        entities.append(strategic_analysis.get("market_positioning", ""))
        entities.append(strategic_analysis.get("competitive_advantage", ""))
        
        # Filter out empty strings and convert to strings
        entities = [str(entity) for entity in entities if entity and str(entity).strip()]
        
        return list(set(entities))  # Remove duplicates
    
    async def _generate_comprehensive_results(self,
                                           query: str,
                                           context: Dict[str, Any],
                                           llm_analysis: Dict[str, Any],
                                           strategic_analysis: Dict[str, Any],
                                           knowledge_insights: Dict[str, Any],
                                           analysis_type: str,
                                           start_time: datetime) -> Dict[str, Any]:
        """
        Generate comprehensive results combining all analysis components
        """
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Strategic analysis is already in dict format for V4
        strategic_analysis_dict = strategic_analysis
        
        return {
            "query": query,
            "context": context,
            "analysis_type": analysis_type,
            "timestamp": datetime.now().isoformat(),
            "processing_time": processing_time,
            
            # LLM Analysis Results
            "llm_analysis": llm_analysis,
            
            # Strategic Framework Results
            "strategic_analysis": strategic_analysis_dict,
            
            # Knowledge Graph Insights
            "knowledge_insights": knowledge_insights,
            
            # Executive Summary
            "executive_summary": {
                "overall_score": strategic_analysis.get("overall_viability_score", 0),
                "overall_confidence": 0.8,  # Default confidence for V4
                "strategic_position": strategic_analysis.get("market_positioning", "Standard positioning"),
                "key_insights": strategic_analysis.get("key_strengths", [])[:5],  # Top 5 strengths
                "top_recommendations": strategic_analysis.get("strategic_recommendations", [])[:3],  # Top 3 recommendations
                "risk_level": strategic_analysis.get("risk_assessment", {}).get("overall_risk_level", "medium"),
                "opportunity_level": strategic_analysis.get("opportunity_analysis", {}).get("overall_opportunity_level", "medium")
            },
            
            # Framework Breakdown
            "framework_breakdown": {
                dimension_score.dimension.value: {
                    "score": dimension_score.score,
                    "confidence": dimension_score.confidence,
                    "reasoning": dimension_score.rationale,
                    "metrics_used": 0  # V4 doesn't use metrics in the same way
                }
                for dimension_score in strategic_analysis.get("dimension_scores", [])
                if hasattr(dimension_score, 'dimension')
            },
            
            # Metrics Summary
            "metrics_summary": {
                "total_dimensions_analyzed": len(strategic_analysis.get("dimension_scores", [])),
                "dimensions_by_category": {
                    dimension_score.dimension.value: 1
                    for dimension_score in strategic_analysis.get("dimension_scores", [])
                    if hasattr(dimension_score, 'dimension')
                }
            }
        }
    

    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on all components
        """
        try:
            health_status = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "components": {}
            }
            
            # Check LLM Orchestrator
            try:
                llm_health = await self.llm_orchestrator.health_check()
                health_status["components"]["llm_orchestrator"] = llm_health
            except Exception as e:
                health_status["components"]["llm_orchestrator"] = {"status": "unhealthy", "error": str(e)}
                health_status["status"] = "degraded"
            
            # Check Strategic Scoring Engine
            try:
                # Simple health check for scoring engine
                health_status["components"]["strategic_scoring_engine"] = {
                    "status": "healthy",
                    "version": "V4",
                    "method": "LLM-Based Qualitative Analysis",
                    "dimensions_supported": 8  # Number of strategic dimensions in V4
                }
            except Exception as e:
                health_status["components"]["strategic_scoring_engine"] = {"status": "unhealthy", "error": str(e)}
                health_status["status"] = "degraded"
            
            # Check Knowledge Graph
            try:
                kg_health = await self.knowledge_graph.health_check()
                health_status["components"]["knowledge_graph"] = kg_health
            except Exception as e:
                health_status["components"]["knowledge_graph"] = {"status": "unhealthy", "error": str(e)}
                health_status["status"] = "degraded"
            
            return health_status
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    async def get_analysis_summary(self) -> Dict[str, Any]:
        """
        Get summary of analysis capabilities and recent performance
        """
        try:
            # Get LLM capabilities
            llm_capabilities = await self.llm_orchestrator.get_capabilities()
            
            # Get scoring engine capabilities
            scoring_capabilities = {
                "frameworks_supported": list(self.scoring_engine.framework_metrics.keys()),
                "total_metrics": sum(len(metrics) for metrics in self.scoring_engine.framework_metrics.values()),
                "framework_details": {
                    framework.value: {
                        "metrics_count": len(metrics),
                        "metrics": [metric.value for metric in metrics]
                    }
                    for framework, metrics in self.scoring_engine.framework_metrics.items()
                }
            }
            
            return {
                "timestamp": datetime.now().isoformat(),
                "llm_capabilities": llm_capabilities,
                "scoring_capabilities": scoring_capabilities,
                "knowledge_graph_status": "available" if self.knowledge_graph else "not_configured"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get analysis summary: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
