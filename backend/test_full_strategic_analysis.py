#!/usr/bin/env python3
"""
Test Full Strategic Analysis Workflow with New Framework-Based Scoring System
Tests the complete end-to-end workflow using StrategicScoringEngineV3
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import the new components
from app.core.enhanced_validatus_orchestrator import EnhancedValidatusOrchestrator
from app.core.strategic_scoring_v3 import StrategicScoringEngineV3, StrategicAnalysisResultV3

async def test_full_strategic_analysis():
    """
    Test the complete strategic analysis workflow with the new framework-based scoring system
    """
    try:
        logger.info("🚀 Starting Full Strategic Analysis Test with New Framework System")
        
        # Initialize the enhanced orchestrator
        orchestrator = EnhancedValidatusOrchestrator()
        
        # Test query and context
        test_query = "Analyze the strategic position of a fintech startup entering the digital payments market in 2024"
        test_context = {
            "industry": "fintech",
            "market": "digital payments",
            "company_type": "startup",
            "geographic_focus": ["North America", "Europe"],
            "target_customers": "small businesses and consumers",
            "technology_focus": "AI-powered fraud detection and real-time processing"
        }
        
        logger.info(f"📋 Test Query: {test_query}")
        logger.info(f"🔍 Test Context: {json.dumps(test_context, indent=2)}")
        
        # Execute the complete workflow
        logger.info("⚡ Executing complete workflow...")
        start_time = datetime.now()
        
        results = await orchestrator.execute_workflow(
            query=test_query,
            context=test_context,
            analysis_type="comprehensive"
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"✅ Workflow completed in {processing_time:.2f} seconds")
        
        # Display results summary
        await display_workflow_results(results)
        
        # Test individual components
        await test_individual_components(orchestrator)
        
        # Save detailed results
        save_detailed_results(results, "full_strategic_analysis_results_v3.json")
        
        logger.info("🎉 Full Strategic Analysis Test completed successfully!")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Full Strategic Analysis Test failed: {e}")
        raise

async def test_quick_analysis():
    """
    Test the quick analysis workflow
    """
    try:
        logger.info("🚀 Starting Quick Analysis Test")
        
        orchestrator = EnhancedValidatusOrchestrator()
        
        test_query = "Quick assessment of competitive landscape for electric vehicle charging stations"
        test_context = {
            "industry": "electric vehicles",
            "market": "charging infrastructure",
            "analysis_depth": "quick"
        }
        
        logger.info(f"📋 Quick Test Query: {test_query}")
        
        start_time = datetime.now()
        
        results = await orchestrator.execute_workflow(
            query=test_query,
            context=test_context,
            analysis_type="quick"
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"✅ Quick analysis completed in {processing_time:.2f} seconds")
        await display_workflow_results(results, analysis_type="Quick")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Quick Analysis Test failed: {e}")
        raise

async def test_individual_components(orchestrator: EnhancedValidatusOrchestrator):
    """
    Test individual components of the system
    """
    try:
        logger.info("🔧 Testing Individual Components")
        
        # Test health check
        logger.info("🏥 Testing Health Check...")
        health_status = await orchestrator.health_check()
        logger.info(f"Health Status: {health_status['status']}")
        
        for component, status in health_status['components'].items():
            if isinstance(status, dict):
                logger.info(f"  {component}: {status.get('status', 'unknown')}")
            else:
                logger.info(f"  {component}: {status}")
        
        # Test capabilities
        logger.info("📊 Testing Capabilities...")
        capabilities = await orchestrator.get_analysis_summary()
        
        if "scoring_capabilities" in capabilities:
            scoring_cap = capabilities["scoring_capabilities"]
            logger.info(f"Supported Frameworks: {len(scoring_cap.get('frameworks_supported', []))}")
            logger.info(f"Total Metrics: {scoring_cap.get('total_metrics', 0)}")
            
            for framework, details in scoring_cap.get('framework_details', {}).items():
                logger.info(f"  {framework}: {details.get('metrics_count', 0)} metrics")
        
        logger.info("✅ Individual Component Tests completed")
        
    except Exception as e:
        logger.error(f"❌ Individual Component Tests failed: {e}")

async def display_workflow_results(results: Dict[str, Any], analysis_type: str = "Comprehensive"):
    """
    Display the workflow results in a structured format
    """
    try:
        logger.info(f"\n{'='*80}")
        logger.info(f"📊 {analysis_type} Analysis Results")
        logger.info(f"{'='*80}")
        
        # Executive Summary
        if "executive_summary" in results:
            exec_summary = results["executive_summary"]
            logger.info(f"🎯 Executive Summary:")
            logger.info(f"  Overall Score: {exec_summary.get('overall_score', 0):.3f}")
            logger.info(f"  Overall Confidence: {exec_summary.get('overall_confidence', 0):.3f}")
            logger.info(f"  Strategic Position: {exec_summary.get('strategic_position', 'N/A')}")
            logger.info(f"  Risk Level: {exec_summary.get('risk_level', 'N/A')}")
            logger.info(f"  Opportunity Level: {exec_summary.get('opportunity_level', 'N/A')}")
        
        # Framework Breakdown
        if "framework_breakdown" in results:
            logger.info(f"\n🏗️  Framework Analysis:")
            for framework, data in results["framework_breakdown"].items():
                logger.info(f"  {framework.replace('_', ' ').title()}:")
                logger.info(f"    Score: {data.get('score', 0):.3f}")
                logger.info(f"    Confidence: {data.get('confidence', 0):.3f}")
                logger.info(f"    Metrics Used: {data.get('metrics_used', 0)}")
                if 'reasoning' in data:
                    logger.info(f"    Reasoning: {data['reasoning'][:100]}...")
        
        # Metrics Summary
        if "metrics_summary" in results:
            metrics_summary = results["metrics_summary"]
            logger.info(f"\n📈 Metrics Summary:")
            logger.info(f"  Total Metrics Extracted: {metrics_summary.get('total_metrics_extracted', 0)}")
            
            if "metrics_by_framework" in metrics_summary:
                logger.info(f"  Metrics by Framework:")
                for framework, count in metrics_summary["metrics_by_framework"].items():
                    logger.info(f"    {framework.replace('_', ' ').title()}: {count}")
        
        # Key Insights
        if "executive_summary" in results and "key_insights" in results["executive_summary"]:
            logger.info(f"\n💡 Key Insights:")
            for i, insight in enumerate(results["executive_summary"]["key_insights"][:5], 1):
                logger.info(f"  {i}. {insight}")
        
        # Top Recommendations
        if "executive_summary" in results and "top_recommendations" in results["executive_summary"]:
            logger.info(f"\n🎯 Top Recommendations:")
            for i, rec in enumerate(results["executive_summary"]["top_recommendations"][:3], 1):
                logger.info(f"  {i}. {rec}")
        
        # Processing Information
        logger.info(f"\n⏱️  Processing Information:")
        logger.info(f"  Total Processing Time: {results.get('processing_time', 0):.2f} seconds")
        logger.info(f"  Analysis Type: {results.get('analysis_type', 'N/A')}")
        logger.info(f"  Timestamp: {results.get('timestamp', 'N/A')}")
        
        logger.info(f"{'='*80}\n")
        
    except Exception as e:
        logger.error(f"❌ Failed to display workflow results: {e}")

def save_detailed_results(results: Dict[str, Any], filename: str):
    """
    Save detailed results to a JSON file
    """
    try:
        # Clean up the results for JSON serialization
        clean_results = clean_results_for_json(results)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(clean_results, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"💾 Detailed results saved to {filename}")
        
    except Exception as e:
        logger.error(f"❌ Failed to save detailed results: {e}")

def clean_results_for_json(obj: Any) -> Any:
    """
    Clean results object for JSON serialization
    """
    if isinstance(obj, dict):
        return {key: clean_results_for_json(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [clean_results_for_json(item) for item in obj]
    elif hasattr(obj, 'isoformat'):  # datetime objects
        return obj.isoformat()
    elif hasattr(obj, '__dict__'):  # custom objects
        return clean_results_for_json(obj.__dict__)
    else:
        return obj

async def main():
    """
    Main test function
    """
    try:
        logger.info("🚀 Starting Validatus Platform V3 Strategic Analysis Tests")
        logger.info("=" * 80)
        
        # Test 1: Full comprehensive analysis
        logger.info("\n🧪 Test 1: Full Comprehensive Analysis")
        logger.info("-" * 50)
        await test_full_strategic_analysis()
        
        # Test 2: Quick analysis
        logger.info("\n🧪 Test 2: Quick Analysis")
        logger.info("-" * 50)
        await test_quick_analysis()
        
        logger.info("\n🎉 All Tests Completed Successfully!")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"❌ Test Suite Failed: {e}")
        raise

if __name__ == "__main__":
    # Run the tests
    asyncio.run(main())
