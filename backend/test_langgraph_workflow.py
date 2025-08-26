#!/usr/bin/env python3
"""
Test script for the LangGraph workflow implementation
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

async def test_langgraph_workflow():
    """Test the LangGraph workflow implementation"""
    try:
        print("🧪 Testing LangGraph Workflow Implementation...")
        
        # Import the workflow
        from app.core.langgraph_workflow import LangGraphWorkflow
        
        print("✅ Successfully imported LangGraphWorkflow")
        
        # Test workflow initialization
        print("\n🔧 Initializing workflow...")
        workflow = LangGraphWorkflow()
        
        print("✅ Workflow initialized successfully")
        
        # Get workflow status
        status = workflow.get_workflow_status()
        print(f"\n📊 Workflow Status:")
        print(f"   Type: {status['workflow_type']}")
        print(f"   Status: {status['status']}")
        print(f"   Nodes: {', '.join(status['nodes'])}")
        print(f"   Features: {', '.join(status['features'])}")
        
        # Test with a simple idea
        print("\n🚀 Testing parallel workflow execution...")
        test_idea = "A smart home device that automates pet feeding and playtime"
        test_audience = "Busy pet owners who want to ensure their pets are cared for while they are away"
        
        results = await workflow.execute(
            idea_description=test_idea,
            target_audience=test_audience,
            additional_context={
                "market_focus": "smart_home_pet_care",
                "competition_level": "medium",
                "innovation_focus": "automation_and_ai"
            }
        )
        
        print("\n📋 Execution Results:")
        if results.get('success'):
            print(f"   ✅ Success: {results['success']}")
            print(f"   📊 Completed Steps: {', '.join(results.get('completed_steps', []))}")
            print(f"   🎯 Final Step: {results.get('final_step', 'N/A')}")
            print(f"   📈 Analysis Results: {len(results.get('analysis_results', {}))} items")
        else:
            print(f"   ❌ Error: {results.get('error', 'Unknown error')}")
        
        print("\n🎉 LangGraph Workflow test completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {str(e)}")
        print("   Make sure all dependencies are installed and paths are correct")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 LangGraph Workflow Test Suite")
    print("=" * 50)
    
    # Run the test
    success = asyncio.run(test_langgraph_workflow())
    
    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
