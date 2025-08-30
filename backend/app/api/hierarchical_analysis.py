from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from datetime import datetime
import logging
from ..core.comprehensive_langgraph_workflow_fixed import ContextAwareLangGraphWorkflow

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/hierarchical-analysis", tags=["hierarchical-analysis"])

@router.post("/comprehensive")
async def comprehensive_hierarchical_analysis(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return analysis results in hierarchical segments->factors->layers structure
    """
    try:
        # Extract request parameters
        idea_description = request.get('query', '')
        target_audience = request.get('context', {}).get('target_audience', '')
        additional_context = request.get('context', {})
        
        if not idea_description:
            raise HTTPException(status_code=400, detail="Query is required")
        
        logger.info(f"Starting comprehensive analysis for: {idea_description}")
        
        # Execute the comprehensive workflow
        workflow = ContextAwareLangGraphWorkflow()
        results = await workflow.execute(
            idea_description=idea_description,
            target_audience=target_audience,
            additional_context=additional_context
        )
        
        # Convert flat results to hierarchical structure
        hierarchical_results = workflow._restructure_results_hierarchical(results)
        
        # Transform to match frontend expected format
        transformed_results = {
            "query": idea_description,
            "overall_score": hierarchical_results.get("overall_viability_score", 75),
            "overall_confidence": 0.85,
            "segments": {},
            "meta_scores": {
                "market_fit": 75,
                "innovation_score": 75,
                "execution_readiness": 75,
                "risk_index": 25,
                "brand_strength": 70
            },
            "executive_summary": "Comprehensive strategic analysis completed successfully",
            "key_recommendations": ["Focus on high-scoring segments", "Address critical risk factors"],
            "competitive_advantages": ["Strong market positioning", "Innovative product features"],
            "risk_factors": ["Market volatility", "Competitive pressure"],
            "generated_at": datetime.now().isoformat()
        }
        
        # Build hierarchical segments structure
        for segment_name, segment_data in hierarchical_results.get("segments", {}).items():
            transformed_results["segments"][segment_name] = {
                "name": segment_data.get("segment_name", segment_name),
                "score": segment_data.get("overall_score", 0),
                "confidence": 0.85,
                "trend": "stable",
                "priority": "medium",
                "key_insights": segment_data.get("segment_insights", []),
                "recommendations": segment_data.get("strategic_priorities", []),
                "factors": {}
            }
            
            # Build factors within segments
            for factor_name, factor_data in segment_data.get("factors", {}).items():
                transformed_results["segments"][segment_name]["factors"][factor_name] = {
                    "name": factor_data.get("factor_name", factor_name),
                    "score": factor_data.get("overall_score", 0),
                    "confidence": 0.85,
                    "summary": factor_data.get("summary", ""),
                    "key_insights": factor_data.get("factor_insights", []),
                    "recommendations": factor_data.get("recommendations", []),
                    "layers": {}
                }
                
                # Build layers within factors
                for layer_name, layer_data in factor_data.get("layers", {}).items():
                    transformed_results["segments"][segment_name]["factors"][factor_name]["layers"][layer_name] = {
                        "name": layer_name,
                        "score": layer_data.get("score", 0),
                        "confidence": layer_data.get("confidence", 0.85),
                        "calculation_method": layer_data.get("calculation_method", ""),
                        "supporting_data": layer_data.get("supporting_data", {}),
                        "data_sources": layer_data.get("data_sources", []),
                        "summary": layer_data.get("summary", "")
                    }
        
        logger.info(f"Analysis completed successfully with {len(transformed_results['segments'])} segments")
        return transformed_results
        
    except Exception as e:
        logger.error(f"Hierarchical analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@router.get("/capabilities")
async def get_capabilities() -> Dict[str, Any]:
    """Get analysis capabilities"""
    return {
        "framework": "Validatus Platform V4.0",
        "segments": 5,
        "factors": 30,
        "layers": 156,
        "analysis_types": ["comprehensive", "segment_focused", "factor_analysis"],
        "supported_industries": ["technology", "healthcare", "finance", "retail", "manufacturing"]
    }
