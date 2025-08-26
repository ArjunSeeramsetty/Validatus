#!/usr/bin/env python3
"""
Strategic Analysis API endpoints for the Validatus Platform
Provides comprehensive and quick strategic analysis using the new framework-based scoring system
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ..core.enhanced_validatus_orchestrator import EnhancedValidatusOrchestrator
from ..core.strategic_scoring_v3 import StrategicAnalysisResultV3

# Initialize router
router = APIRouter(prefix="/strategic-analysis", tags=["strategic-analysis"])

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize orchestrator
orchestrator = EnhancedValidatusOrchestrator()

# Pydantic models for API requests and responses
class StrategicAnalysisRequest(BaseModel):
    """Request model for strategic analysis"""
    query: str = Field(..., description="Strategic analysis query", min_length=10)
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context for analysis")
    analysis_type: str = Field(default="comprehensive", description="Type of analysis: 'comprehensive' or 'quick'")

class StrategicAnalysisResponse(BaseModel):
    """Response model for strategic analysis"""
    status: str = Field(..., description="Analysis status")
    timestamp: str = Field(..., description="Analysis timestamp")
    processing_time: float = Field(..., description="Processing time in seconds")
    
    # Executive Summary
    executive_summary: Dict[str, Any] = Field(..., description="Executive summary of results")
    
    # Framework Breakdown
    framework_breakdown: Dict[str, Any] = Field(..., description="Scores for each strategy framework")
    
    # Metrics Summary
    metrics_summary: Dict[str, Any] = Field(..., description="Summary of extracted metrics")
    
    # Full Results (for comprehensive analysis)
    full_results: Optional[Dict[str, Any]] = Field(default=None, description="Complete analysis results")

class HealthCheckResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Overall health status")
    timestamp: str = Field(..., description="Health check timestamp")
    components: Dict[str, Any] = Field(..., description="Health status of individual components")

@router.post("/comprehensive", response_model=StrategicAnalysisResponse)
async def comprehensive_strategic_analysis(
    request: StrategicAnalysisRequest,
    background_tasks: BackgroundTasks
) -> StrategicAnalysisResponse:
    """
    Perform comprehensive strategic analysis using all available frameworks
    """
    try:
        logger.info(f"Starting comprehensive strategic analysis for query: {request.query[:100]}...")
        
        # Execute the complete workflow
        results = await orchestrator.execute_workflow(
            query=request.query,
            context=request.context,
            analysis_type="comprehensive"
        )
        
        # Create response
        response = StrategicAnalysisResponse(
            status="completed",
            timestamp=results["timestamp"],
            processing_time=results["processing_time"],
            executive_summary=results["executive_summary"],
            framework_breakdown=results["framework_breakdown"],
            metrics_summary=results["metrics_summary"],
            full_results=results
        )
        
        logger.info(f"Comprehensive analysis completed in {results['processing_time']:.2f}s")
        return response
        
    except Exception as e:
        logger.error(f"Comprehensive analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/quick", response_model=StrategicAnalysisResponse)
async def quick_strategic_analysis(
    request: StrategicAnalysisRequest,
    background_tasks: BackgroundTasks
) -> StrategicAnalysisResponse:
    """
    Perform quick strategic analysis focusing on key frameworks
    """
    try:
        logger.info(f"Starting quick strategic analysis for query: {request.query[:100]}...")
        
        # Execute the workflow with quick analysis
        results = await orchestrator.execute_workflow(
            query=request.query,
            context=request.context,
            analysis_type="quick"
        )
        
        # Create response (same structure but potentially fewer frameworks)
        response = StrategicAnalysisResponse(
            status="completed",
            timestamp=results["timestamp"],
            processing_time=results["processing_time"],
            executive_summary=results["executive_summary"],
            framework_breakdown=results["framework_breakdown"],
            metrics_summary=results["metrics_summary"],
            full_results=results
        )
        
        logger.info(f"Quick analysis completed in {results['processing_time']:.2f}s")
        return response
        
    except Exception as e:
        logger.error(f"Quick analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """
    Check the health of all system components
    """
    try:
        health_status = await orchestrator.health_check()
        
        response = HealthCheckResponse(
            status=health_status["status"],
            timestamp=health_status["timestamp"],
            components=health_status["components"]
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@router.get("/capabilities")
async def get_capabilities() -> Dict[str, Any]:
    """
    Get information about system capabilities and supported frameworks
    """
    try:
        capabilities = await orchestrator.get_analysis_summary()
        return capabilities
        
    except Exception as e:
        logger.error(f"Failed to get capabilities: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get capabilities: {str(e)}")

@router.get("/frameworks")
async def get_supported_frameworks() -> Dict[str, Any]:
    """
    Get information about supported strategic frameworks and their metrics
    """
    try:
        # Get capabilities to extract framework information
        capabilities = await orchestrator.get_analysis_summary()
        
        if "scoring_capabilities" in capabilities:
            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "frameworks": capabilities["scoring_capabilities"]
            }
        else:
            return {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "message": "Framework information not available"
            }
        
    except Exception as e:
        logger.error(f"Failed to get framework information: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get framework information: {str(e)}")

@router.post("/test")
async def test_analysis() -> Dict[str, Any]:
    """
    Test endpoint to verify the analysis system is working
    """
    try:
        test_query = "Analyze the strategic position of a fintech startup in the digital payments market"
        test_context = {
            "industry": "fintech",
            "market": "digital payments",
            "company_type": "startup"
        }
        
        logger.info("Running test analysis...")
        
        # Execute test workflow
        results = await orchestrator.execute_workflow(
            query=test_query,
            context=test_context,
            analysis_type="comprehensive"
        )
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "test_query": test_query,
            "processing_time": results["processing_time"],
            "overall_score": results["executive_summary"]["overall_score"],
            "frameworks_analyzed": len(results["framework_breakdown"]),
            "metrics_extracted": results["metrics_summary"]["total_metrics_extracted"]
        }
        
    except Exception as e:
        logger.error(f"Test analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Test analysis failed: {str(e)}")

# Helper functions for response formatting
def _format_executive_summary(strategic_analysis: StrategicAnalysisResultV3) -> Dict[str, Any]:
    """Format executive summary from strategic analysis results"""
    return {
        "overall_score": strategic_analysis.overall_score,
        "overall_confidence": strategic_analysis.overall_confidence,
        "strategic_position": strategic_analysis.strategic_position,
        "key_insights": strategic_analysis.key_insights[:5],  # Top 5 insights
        "top_recommendations": strategic_analysis.strategic_recommendations[:3],  # Top 3 recommendations
        "risk_level": strategic_analysis.risk_assessment.get("overall_risk_level", "medium"),
        "opportunity_level": strategic_analysis.opportunity_analysis.get("overall_opportunity_level", "medium")
    }

def _format_framework_breakdown(strategic_analysis: StrategicAnalysisResultV3) -> Dict[str, Any]:
    """Format framework breakdown from strategic analysis results"""
    return {
        framework_score.framework.value: {
            "score": framework_score.score,
            "confidence": framework_score.confidence,
            "reasoning": framework_score.reasoning,
            "metrics_used": len(framework_score.metrics_used)
        }
        for framework_score in strategic_analysis.framework_scores
    }

def _format_metrics_summary(strategic_analysis: StrategicAnalysisResultV3) -> Dict[str, Any]:
    """Format metrics summary from strategic analysis results"""
    return {
        "total_metrics_extracted": len(strategic_analysis.extracted_metrics),
        "metrics_by_framework": {
            framework_score.framework.value: len(framework_score.metrics_used)
            for framework_score in strategic_analysis.framework_scores
        }
    }
