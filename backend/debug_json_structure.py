#!/usr/bin/env python3
"""
Debug script to examine the actual JSON structure.
"""

import json

def debug_json_structure():
    """Debug the JSON structure to find where layer_scores are located."""
    
    input_file = "full_pergola_analysis_report_20250829_124837.json"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ JSON loaded successfully")
        print(f"Top-level keys: {list(data.keys())}")
        
        # Check if detailed_analysis exists
        if 'detailed_analysis' in data:
            print(f"✅ detailed_analysis found")
            detailed = data['detailed_analysis']
            print(f"detailed_analysis keys: {list(detailed.keys())}")
            
            # Check if layer_scores exists
            if 'layer_scores' in detailed:
                print(f"✅ layer_scores found")
                layer_scores = detailed['layer_scores']
                print(f"layer_scores type: {type(layer_scores)}")
                print(f"layer_scores length: {len(layer_scores)}")
                
                # Show first few layer names
                if layer_scores:
                    first_layers = list(layer_scores.keys())[:5]
                    print(f"First 5 layer names: {first_layers}")
                    
                    # Show structure of first layer
                    first_layer_name = first_layers[0]
                    first_layer_data = layer_scores[first_layer_name]
                    print(f"Structure of '{first_layer_name}': {list(first_layer_data.keys())}")
                else:
                    print("❌ layer_scores is empty")
            else:
                print("❌ layer_scores not found in detailed_analysis")
                
                # Search for layer_scores anywhere in the structure
                print("Searching for layer_scores in the entire structure...")
                search_for_layer_scores(data, "")
        else:
            print("❌ detailed_analysis not found")
            
            # Search for layer_scores anywhere in the structure
            print("Searching for layer_scores in the entire structure...")
            search_for_layer_scores(data, "")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def search_for_layer_scores(obj, path):
    """Recursively search for layer_scores in the object."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_path = f"{path}.{key}" if path else key
            if key == "layer_scores":
                print(f"🎯 Found layer_scores at: {current_path}")
                print(f"   Type: {type(value)}")
                print(f"   Length: {len(value) if hasattr(value, '__len__') else 'N/A'}")
                if value and hasattr(value, '__len__') and len(value) > 0:
                    first_key = list(value.keys())[0]
                    print(f"   First key: {first_key}")
                    print(f"   First value structure: {list(value[first_key].keys()) if isinstance(value[first_key], dict) else type(value[first_key])}")
                return True
            elif isinstance(value, dict):
                if search_for_layer_scores(value, current_path):
                    return True
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        if search_for_layer_scores(item, f"{current_path}[{i}]"):
                            return True
    return False

if __name__ == "__main__":
    debug_json_structure()
