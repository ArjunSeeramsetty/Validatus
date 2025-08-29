#!/usr/bin/env python3
"""
Test Script: Verify 156 Layers in Expanded Framework
This script will confirm that we now have all 156 layers as expected
"""

from app.core.comprehensive_analytical_framework_fixed import ComprehensiveAnalyticalFramework

def test_156_layers():
    """Test that the framework has all 156 layers"""
    print("🔍 TESTING EXPANDED FRAMEWORK - 156 LAYERS")
    print("=" * 60)
    
    try:
        # Initialize framework
        framework = ComprehensiveAnalyticalFramework()
        print("✅ Framework initialized")
        
        # Get all layers
        all_layers = framework.get_all_layers()
        total_layers = len(all_layers)
        print(f"📊 Total layers available: {total_layers}")
        
        # Check segments
        segments = framework.analytical_framework.keys()
        print(f"🎯 Available segments: {', '.join(segments)}")
        
        # Check factors per segment
        total_factors = 0
        for segment_name, segment_data in framework.analytical_framework.items():
            factors = segment_data["factors"].keys()
            factor_count = len(factors)
            total_factors += factor_count
            print(f"   {segment_name}: {factor_count} factors")
            
            # Check layers per factor
            for factor_name, layers in segment_data["factors"].items():
                layer_count = len(layers)
                print(f"     • {factor_name}: {layer_count} layers")
        
        print(f"\n📋 SUMMARY:")
        print(f"   Total segments: {len(segments)}")
        print(f"   Total factors: {total_factors}")
        print(f"   Total layers: {total_layers}")
        print(f"   Expected: 156 layers")
        
        if total_layers == 156:
            print("✅ SUCCESS: Framework has exactly 156 layers!")
        else:
            print(f"❌ ISSUE: Framework has {total_layers} layers, expected 156")
        
        # Show first few layers from each segment
        print(f"\n🔍 SAMPLE LAYERS BY SEGMENT:")
        for segment_name, segment_data in framework.analytical_framework.items():
            print(f"\n   {segment_name}:")
            for factor_name, layers in segment_data["factors"].items():
                print(f"     • {factor_name}:")
                for layer in layers[:3]:  # Show first 3 layers
                    print(f"       - {layer}")
                if len(layers) > 3:
                    print(f"       - ... and {len(layers) - 3} more")
        
        return {
            "total_segments": len(segments),
            "total_factors": total_factors,
            "total_layers": total_layers,
            "success": total_layers == 156
        }
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🚀 Starting 156 Layer Test...")
    results = test_156_layers()
    
    if results:
        print(f"\n🏁 Test completed!")
        print(f"📊 Results: {results}")
    else:
        print(f"\n❌ Test failed!")
