#!/usr/bin/env python3
"""
Test Analysis Script for Validatus Platform
Demonstrates the full analysis workflow with a sample strategic query
"""

import asyncio
import json
from datetime import datetime
from app.core.multi_llm_orchestrator import MultiLLMOrchestrator, ConsensusMethod
from app.core.knowledge_graph_analyzer import KnowledgeGraphAnalyzer

async def test_strategic_analysis():
    """Test the full strategic analysis workflow"""
    
    print("🚀 Starting Validatus Strategic Analysis Test")
    print("=" * 60)
    
    # Sample strategic query
    sample_query = """
    Analyze the market opportunity for launching an AI-powered 
    personal finance management app targeting millennials in the 
    United States. Focus on market size, competitive landscape, 
    user adoption barriers, and monetization potential.
    """
    
    print(f"📋 Analysis Query:\n{sample_query.strip()}")
    print("\n" + "=" * 60)
    
    try:
        # Initialize Multi-LLM Orchestrator
        print("🔧 Initializing Multi-LLM Orchestrator...")
        orchestrator = MultiLLMOrchestrator(
            consensus_method=ConsensusMethod.CLUSTERING_BASED
        )
        
        # Check available models
        available_models = await orchestrator.get_available_models()
        print(f"✅ Available LLM Models: {list(available_models.keys())}")
        
        # Perform consensus analysis
        print("\n🧠 Performing Multi-LLM Consensus Analysis...")
        start_time = datetime.now()
        
        analysis_result = await orchestrator.consensus_analysis(
            query=sample_query,
            context={
                "industry": "FinTech",
                "target_audience": "Millennials (25-40)",
                "geography": "United States",
                "product_type": "Mobile App",
                "analysis_focus": ["market_size", "competition", "adoption", "monetization"]
            }
        )
        
        end_time = datetime.now()
        analysis_duration = (end_time - start_time).total_seconds()
        
        print(f"✅ Analysis completed in {analysis_duration:.2f} seconds")
        
        # Display results
        print("\n📊 Analysis Results:")
        print("-" * 40)
        
        if "consensus_insights" in analysis_result:
            print("🎯 Key Strategic Insights:")
            for i, insight in enumerate(analysis_result["consensus_insights"][:5], 1):
                print(f"  {i}. {insight}")
        
        if "consensus_recommendations" in analysis_result:
            print("\n💡 Strategic Recommendations:")
            for i, rec in enumerate(analysis_result["consensus_recommendations"][:5], 1):
                print(f"  {i}. {rec}")
        
        if "confidence_score" in analysis_result:
            print(f"\n🎯 Overall Confidence: {analysis_result['confidence_score']:.2%}")
        
        if "model_contributions" in analysis_result:
            print(f"\n🤖 Models Used: {len(analysis_result['model_contributions'])}")
            for model, contribution in analysis_result["model_contributions"].items():
                print(f"  - {model}: {contribution['confidence']:.2%} confidence")
        
        # Test Knowledge Graph Analysis (if Neo4j is available)
        print("\n" + "=" * 60)
        print("🔗 Testing Knowledge Graph Analysis...")
        
        try:
            kg_analyzer = KnowledgeGraphAnalyzer()
            health_status = await kg_analyzer.health_check()
            print(f"✅ Knowledge Graph Status: {health_status.get('status', 'Unknown')}")
            
            # Simulate relationship analysis
            print("📈 Simulating Market Relationship Analysis...")
            relationships = await kg_analyzer.relationship_analysis(
                entity_type="company",
                target_entity="AI Finance App",
                relationship_depth=2
            )
            
            if relationships and "insights" in relationships:
                print("🔍 Market Relationship Insights:")
                for insight in relationships["insights"][:3]:
                    print(f"  • {insight}")
            
        except Exception as kg_error:
            print(f"⚠️ Knowledge Graph Analysis: {kg_error}")
            print("   (This is expected if Neo4j is not configured)")
        
        # Save detailed results
        output_file = f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(analysis_result, f, indent=2, default=str)
        
        print(f"\n💾 Detailed results saved to: {output_file}")
        
        return analysis_result
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return None

async def test_quick_analysis():
    """Test a quick analysis with minimal context"""
    
    print("\n🔄 Testing Quick Analysis Mode...")
    print("-" * 40)
    
    try:
        orchestrator = MultiLLMOrchestrator(
            consensus_method=ConsensusMethod.CONFIDENCE_BASED
        )
        
        quick_query = "What are the top 3 trends in AI-powered productivity tools for 2024?"
        
        print(f"📝 Quick Query: {quick_query}")
        
        result = await orchestrator.consensus_analysis(
            query=quick_query,
            context={"analysis_type": "trend_analysis", "timeframe": "2024"}
        )
        
        if result and "consensus_insights" in result:
            print("✅ Quick Analysis Results:")
            for i, insight in enumerate(result["consensus_insights"][:3], 1):
                print(f"  {i}. {insight}")
        
        return result
        
    except Exception as e:
        print(f"❌ Quick analysis failed: {e}")
        return None

if __name__ == "__main__":
    print("🎯 Validatus Platform - Analysis Test Suite")
    print("=" * 60)
    
    # Run the main analysis test
    asyncio.run(test_strategic_analysis())
    
    # Run quick analysis test
    asyncio.run(test_quick_analysis())
    
    print("\n🏁 Analysis Test Suite Completed!")
