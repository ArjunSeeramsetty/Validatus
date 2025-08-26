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
from .strategic_scoring_v3 import StrategicScoringEngineV3, StrategicAnalysisResultV3
from .knowledge_graph_analyzer import KnowledgeGraphAnalyzer

class EnhancedValidatusOrchestrator:
    """
    Top-level orchestrator that coordinates all components of the Validatus Platform
    """
    
    def __init__(self):
        self.logger = logging.getLogger("enhanced.validatus.orchestrator")
        
        # Initialize core components
        self.llm_orchestrator = MultiLLMOrchestrator()
        self.scoring_engine = StrategicScoringEngineV3()  # Updated to V3
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
            llm_analysis = await self.llm_orchestrator.analyze_with_consensus(
                query=query,
                context=context or {},
                analysis_type=analysis_type
            )
            
            # Step 2: Strategic Framework Analysis
            self.logger.info("Step 2: Executing strategic framework analysis")
            strategic_analysis = await self.scoring_engine.analyze_strategic_framework(
                llm_analysis=llm_analysis,
                query=query,
                context=context
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
                                       strategic_analysis: StrategicAnalysisResultV3,
                                       context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Integrate knowledge graph insights with strategic analysis
        """
        try:
            # Extract key entities and relationships from strategic analysis
            entities = self._extract_entities_from_analysis(strategic_analysis)
            
            # Query knowledge graph for additional insights
            knowledge_insights = await self.knowledge_graph.analyze_entities(
                entities=entities,
                query=query,
                context=context
            )
            
            return knowledge_insights
            
        except Exception as e:
            self.logger.warning(f"Knowledge graph integration failed: {e}")
            return {"entities": [], "relationships": [], "insights": []}
    
    def _extract_entities_from_analysis(self, strategic_analysis: StrategicAnalysisResultV3) -> List[str]:
        """
        Extract key entities from strategic analysis for knowledge graph querying
        """
        entities = []
        
        # Extract from extracted metrics
        for metric in strategic_analysis.extracted_metrics:
            if hasattr(metric.value, '__str__'):
                entities.append(str(metric.value))
        
        # Extract from framework scores
        for framework_score in strategic_analysis.framework_scores:
            entities.append(framework_score.framework.value)
        
        # Extract from insights and recommendations
        entities.extend(strategic_analysis.key_insights)
        entities.extend(strategic_analysis.strategic_recommendations)
        
        return list(set(entities))  # Remove duplicates
    
    async def _generate_comprehensive_results(self,
                                           query: str,
                                           context: Dict[str, Any],
                                           llm_analysis: Dict[str, Any],
                                           strategic_analysis: StrategicAnalysisResultV3,
                                           knowledge_insights: Dict[str, Any],
                                           analysis_type: str,
                                           start_time: datetime) -> Dict[str, Any]:
        """
        Generate comprehensive results combining all analysis components
        """
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Convert strategic analysis to serializable format
        strategic_analysis_dict = self._convert_strategic_analysis_to_dict(strategic_analysis)
        
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
                "overall_score": strategic_analysis.overall_score,
                "overall_confidence": strategic_analysis.overall_confidence,
                "strategic_position": strategic_analysis.strategic_position,
                "key_insights": strategic_analysis.key_insights[:5],  # Top 5 insights
                "top_recommendations": strategic_analysis.strategic_recommendations[:3],  # Top 3 recommendations
                "risk_level": strategic_analysis.risk_assessment.get("overall_risk_level", "medium"),
                "opportunity_level": strategic_analysis.opportunity_analysis.get("overall_opportunity_level", "medium")
            },
            
            # Framework Breakdown
            "framework_breakdown": {
                framework_score.framework.value: {
                    "score": framework_score.score,
                    "confidence": framework_score.confidence,
                    "reasoning": framework_score.reasoning,
                    "metrics_used": len(framework_score.metrics_used)
                }
                for framework_score in strategic_analysis.framework_scores
            },
            
            # Metrics Summary
            "metrics_summary": {
                "total_metrics_extracted": len(strategic_analysis.extracted_metrics),
                "metrics_by_framework": {
                    framework_score.framework.value: len(framework_score.metrics_used)
                    for framework_score in strategic_analysis.framework_scores
                }
            }
        }
    
    def _convert_strategic_analysis_to_dict(self, strategic_analysis: StrategicAnalysisResultV3) -> Dict[str, Any]:
        """
        Convert StrategicAnalysisResultV3 to a serializable dictionary
        """
        return {
            "query": strategic_analysis.query,
            "context": strategic_analysis.context,
            "overall_score": strategic_analysis.overall_score,
            "overall_confidence": strategic_analysis.overall_confidence,
            "strategic_position": strategic_analysis.strategic_position,
            "key_insights": strategic_analysis.key_insights,
            "strategic_recommendations": strategic_analysis.strategic_recommendations,
            "risk_assessment": strategic_analysis.risk_assessment,
            "opportunity_analysis": strategic_analysis.opportunity_analysis,
            "timestamp": strategic_analysis.timestamp.isoformat(),
            "processing_time": strategic_analysis.processing_time,
            
            # Framework scores
            "framework_scores": [
                {
                    "framework": fs.framework.value,
                    "score": fs.score,
                    "confidence": fs.confidence,
                    "calculation_method": fs.calculation_method,
                    "reasoning": fs.reasoning,
                    "timestamp": fs.timestamp.isoformat(),
                    "metrics_used": [
                        {
                            "metric": em.metric.value,
                            "value": em.value,
                            "unit": em.unit,
                            "confidence": em.confidence,
                            "source_text": em.source_text[:200] + "..." if len(em.source_text) > 200 else em.source_text,
                            "extraction_method": em.extraction_method,
                            "timestamp": em.timestamp.isoformat()
                        }
                        for em in fs.metrics_used
                    ]
                }
                for fs in strategic_analysis.framework_scores
            ],
            
            # Extracted metrics
            "extracted_metrics": [
                {
                    "metric": em.metric.value,
                    "value": em.value,
                    "unit": em.unit,
                    "confidence": em.confidence,
                    "source_text": em.source_text[:200] + "..." if len(em.source_text) > 200 else em.source_text,
                    "extraction_method": em.extraction_method,
                    "timestamp": em.timestamp.isoformat()
                }
                for em in strategic_analysis.extracted_metrics
            ]
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
                    "frameworks_supported": len(self.scoring_engine.framework_metrics),
                    "metrics_supported": sum(len(metrics) for metrics in self.scoring_engine.framework_metrics.values())
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
