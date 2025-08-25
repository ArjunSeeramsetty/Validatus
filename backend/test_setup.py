#!/usr/bin/env python3
"""
Simple test script to verify the Validatus Platform backend setup.
"""

def test_imports():
    """Test that all required modules can be imported."""
    try:
        print("Testing imports...")
        
        # Test core modules
        from app.core.state import AnalysisStatus, ValidatusState
        print("✓ Core state modules imported successfully")
        
        from app.core.analytical_structure import ANALYTICAL_FRAMEWORK
        print("✓ Analytical structure imported successfully")
        
        from app.core.models import AnalysisRequest, AnalysisContext
        print("✓ Analysis models imported successfully")
        
        from app.agents.market_agent import MarketResearchAgent
        print("✓ Market research agent imported successfully")
        
        from app.scoring.layer_scorers import LayerScoringEngine
        print("✓ Layer scoring engine imported successfully")
        
        from app.scoring.aggregators import ScoreAggregator
        print("✓ Score aggregator imported successfully")
        
        from app.utils.nlp import QueryParser
        print("✓ NLP utilities imported successfully")
        
        print("\n🎉 All imports successful! Backend setup is working correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_config():
    """Test configuration loading."""
    try:
        print("\nTesting configuration...")
        from config import settings
        
        print(f"✓ OpenAI API Key configured: {'Yes' if settings.OPENAI_API_KEY else 'No'}")
        print(f"✓ Tavily API Key configured: {'Yes' if settings.TAVILY_API_KEY else 'No'}")
        print(f"✓ Redis URL: {settings.REDIS_URL}")
        print(f"✓ Database URL: {settings.DATABASE_URL}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

if __name__ == "__main__":
    print("Validatus Platform Backend Setup Test")
    print("=" * 40)
    
    success = True
    success &= test_imports()
    success &= test_config()
    
    if success:
        print("\n✅ Backend setup test completed successfully!")
    else:
        print("\n❌ Backend setup test failed!")
        exit(1)
