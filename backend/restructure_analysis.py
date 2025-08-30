#!/usr/bin/env python3
"""
Script to restructure the analysis JSON from flat layer_scores to hierarchical segments->factors->layers structure.
Based on the Validatus Platform Framework: 5 segments, 30 factors, 156 layers.
"""

import json
import os
from typing import Dict, Any, List
from datetime import datetime

# Define the expected structure based on FRAMEWORK_STRUCTURE_REFERENCE.md
SEGMENTS = {
    "consumer": {
        "name": "Consumer Segment",
        "description": "Consumer insights, behavior, loyalty, perception, and adoption",
        "factors": {
            "consumer_demand_need": "Consumer demand, need perception, trust, and purchase intent",
            "consumer_behavior_habits": "Usage patterns, engagement, habits, and emotional ties",
            "consumer_loyalty_retention": "Repeat purchase, loyalty, advocacy, and retention",
            "consumer_perception_sentiment": "Quality perception, sentiment, trust, and prestige",
            "consumer_adoption_engagement": "Adoption rates, engagement, and social influence"
        }
    },
    "market": {
        "name": "Market Segment", 
        "description": "Market research, trends, competition, demand, and growth",
        "factors": {
            "market_trends": "Future trends, technological shifts, cultural changes, and regulatory shifts",
            "market_competition_barriers": "Competition analysis, entry barriers, and differentiation",
            "market_demand_adoption": "Demand volume, growth, adoption rates, and accessibility",
            "market_growth_expansion": "Growth potential, scalability, and regional expansion",
            "market_stability_risk": "Economic stability, political stability, and risk exposure"
        }
    },
    "product": {
        "name": "Product Segment",
        "description": "Product strategy, innovation, quality, differentiation, and lifecycle",
        "factors": {
            "product_market_readiness": "Entry timing, market saturation, and cycle impact",
            "product_competitive_disruption": "Disruption potential, incumbent resistance, and response time",
            "product_dynamic_disruption": "Dynamic disruption, product strength, and value perception",
            "product_business_resilience": "Profit resilience and expansion growth",
            "product_hype_cycle": "Hype cycle analysis and market saturation",
            "product_quality_assurance": "Material quality, functional quality, and brand trust",
            "product_differentiation": "Technical features and competitive strength",
            "product_brand_perception": "Ad reach and organic buzz",
            "product_experience_design": "Visual appeal, haptic feedback, and sensory design",
            "product_innovation_lifecycle": "Market fit, entry barriers, and technology gaps"
        }
    },
    "brand": {
        "name": "Brand Segment",
        "description": "Brand positioning, equity, virality, monetization, and longevity",
        "factors": {
            "brand_positioning_strategy": "Heritage, innovation edge, and competitive positioning",
            "brand_equity_profile": "Review scores, social sentiment, and trust metrics",
            "brand_virality_impact": "Shareability, influencer impact, and cultural embedding",
            "brand_monetization_model": "Direct sales, licensing, and revenue diversification",
            "brand_longevity_outlook": "Evolution, generational appeal, and cultural relevance"
        }
    },
    "experience": {
        "name": "Experience Segment",
        "description": "User experience, engagement, satisfaction, interaction design, and loyalty",
        "factors": {
            "user_engagement_metrics": "Attention focus, interaction rates, and community activity",
            "satisfaction_feedback": "Value perception, sentiment, and support quality",
            "interaction_design_elements": "Usability, intuitive design, and personalization",
            "post_purchase_loyalty": "Repeat usage, emotional bonds, and advocacy",
            "experience_evolution": "Feature updates, trend alignment, and AI adaptation"
        }
    }
}

def restructure_analysis(input_file: str, output_file: str = None) -> Dict[str, Any]:
    """
    Restructure the analysis JSON from flat layer_scores to hierarchical segments->factors->layers.
    """
    
    # Load the input JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get the layer scores from the correct location
    layer_scores = data.get('analysis_results', {}).get('detailed_analysis', {}).get('layer_scores', {})
    print(f"Loaded analysis data with {len(layer_scores)} layers")
    
    # Create the new hierarchical structure
    new_detailed_analysis = {
        "segments": {},
        "layer_scores": layer_scores  # Keep for backward compatibility
    }
    
    # Process each segment
    for segment_key, segment_info in SEGMENTS.items():
        segment_data = {
            "segment_name": segment_info["name"],
            "description": segment_info["description"],
            "overall_score": 0,
            "summary": "",
            "factors": {},
            "segment_insights": [],
            "strategic_priorities": []
        }
        
        total_segment_score = 0
        factor_count = 0
        
        # Process each factor in the segment
        for factor_key, factor_description in segment_info["factors"].items():
            factor_data = {
                "factor_name": factor_description,
                "overall_score": 0,
                "summary": "",
                "layers": {},
                "factor_insights": [],
                "recommendations": []
            }
            
            total_factor_score = 0
            layer_count = 0
            
            # Find layers that belong to this factor
            factor_layers = {}
            for layer_name, layer_data in layer_scores.items():
                # Map layers to factors based on naming patterns and descriptions
                if should_map_layer_to_factor(layer_name, factor_key, factor_description):
                    factor_layers[layer_name] = layer_data
                    total_factor_score += layer_data.get('score', 0)
                    layer_count += 1
            
            # Calculate factor score
            if layer_count > 0:
                factor_data["overall_score"] = round(total_factor_score / layer_count, 2)
                factor_data["summary"] = f"Analyzed {layer_count} layers with average score {factor_data['overall_score']}/10"
                factor_data["layers"] = factor_layers
                
                # Generate factor insights
                if factor_data["overall_score"] >= 8:
                    factor_data["factor_insights"] = [f"Strong performance in {factor_description.lower()}"]
                    factor_data["recommendations"] = ["Leverage this strength", "Maintain current approach"]
                elif factor_data["overall_score"] >= 6:
                    factor_data["factor_insights"] = [f"Moderate performance in {factor_description.lower()}"]
                    factor_data["recommendations"] = ["Focus on improvement areas", "Develop action plan"]
                else:
                    factor_data["factor_insights"] = [f"Needs improvement in {factor_description.lower()}"]
                    factor_data["recommendations"] = ["Prioritize this area", "Develop improvement strategy"]
                
                total_segment_score += factor_data["overall_score"]
                factor_count += 1
            
            segment_data["factors"][factor_key] = factor_data
        
        # Calculate segment score
        if factor_count > 0:
            segment_data["overall_score"] = round(total_segment_score / factor_count, 2)
            segment_data["summary"] = f"Overall segment score: {segment_data['overall_score']}/10 based on {factor_count} factors"
            
            # Generate segment insights
            if segment_data["overall_score"] >= 8:
                segment_data["segment_insights"] = [f"Strong performance across {segment_info['name'].lower()}"]
                segment_data["strategic_priorities"] = ["Maintain leadership position", "Leverage strengths"]
            elif segment_data["overall_score"] >= 6:
                segment_data["segment_insights"] = [f"Solid performance in {segment_info['name'].lower()}"]
                segment_data["strategic_priorities"] = ["Focus on improvement areas", "Build on strengths"]
            else:
                segment_data["segment_insights"] = [f"Needs attention in {segment_info['name'].lower()}"]
                segment_data["strategic_priorities"] = ["Develop improvement plan", "Allocate resources"]
        
        new_detailed_analysis["segments"][segment_key] = segment_data
    
    # Update the main data structure
    data["detailed_analysis"] = new_detailed_analysis
    
    # Update metadata to reflect new structure
    if "analysis_metadata" in data:
        data["analysis_metadata"]["segments_analyzed"] = len(SEGMENTS)
        data["analysis_metadata"]["factors_analyzed"] = sum(len(segment["factors"]) for segment in SEGMENTS.values())
    
    # Save the restructured data
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"restructured_analysis_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Restructured analysis saved to: {output_file}")
    print(f"Created {len(new_detailed_analysis['segments'])} segments")
    
    total_factors = sum(len(segment["factors"]) for segment in new_detailed_analysis["segments"].values())
    total_layers = sum(len(factor["layers"]) for segment in new_detailed_analysis["segments"].values() 
                      for factor in segment["factors"].values())
    
    print(f"Total factors: {total_factors}")
    print(f"Total layers mapped: {total_layers}")
    
    return data

def should_map_layer_to_factor(layer_name: str, factor_key: str, factor_description: str) -> bool:
    """
    Determine if a layer should be mapped to a specific factor based on naming patterns.
    """
    layer_lower = layer_name.lower()
    factor_lower = factor_key.lower()
    
    # Direct keyword matching
    if factor_lower in layer_lower:
        return True
    
    # Factor-specific mapping rules
    factor_mapping = {
        "consumer_demand_need": ["need", "trust", "purchase", "emotional", "awareness", "social", "accessibility", "value", "trend", "price"],
        "consumer_behavior_habits": ["usage", "engagement", "habit", "emotional", "access", "trust", "interaction", "social", "incentive"],
        "consumer_loyalty_retention": ["repeat", "loyalty", "advocacy", "retention", "switching", "reward"],
        "consumer_perception_sentiment": ["sentiment", "quality", "perception", "innovation", "prestige", "impact"],
        "consumer_adoption_engagement": ["adoption", "engagement", "frequency", "social", "emotional"],
        
        "market_trends": ["trend", "technological", "cultural", "regulatory", "future"],
        "market_competition_barriers": ["competition", "barrier", "differentiation", "rival", "switching"],
        "market_demand_adoption": ["demand", "growth", "adoption", "price", "accessibility"],
        "market_growth_expansion": ["growth", "expansion", "scalability", "regional", "investment"],
        "market_stability_risk": ["stability", "risk", "economic", "political", "regulatory"],
        
        "product_market_readiness": ["timing", "saturation", "cycle", "entry"],
        "product_competitive_disruption": ["disruption", "incumbent", "response", "competitive"],
        "product_dynamic_disruption": ["dynamic", "strength", "awareness", "value", "adoption", "error", "retention"],
        "product_business_resilience": ["profit", "resilience", "expansion"],
        "product_hype_cycle": ["hype", "buzz", "saturation"],
        "product_quality_assurance": ["quality", "material", "functional", "trust", "complaint"],
        "product_differentiation": ["tech", "feature", "competitive"],
        "product_brand_perception": ["ad", "reach", "buzz", "organic"],
        "product_experience_design": ["visual", "haptic", "sensory", "appeal"],
        "product_innovation_lifecycle": ["market_fit", "barrier", "tech_gap", "innovation"],
        
        "brand_positioning_strategy": ["heritage", "legacy", "innovation", "edge", "exclusivity"],
        "brand_equity_profile": ["review", "score", "sentiment", "trust", "crisis"],
        "brand_virality_impact": ["shareability", "influencer", "platform", "cultural", "viral"],
        "brand_monetization_model": ["sales", "licensing", "pricing", "revenue", "monetization"],
        "brand_longevity_outlook": ["evolution", "generational", "resilience", "esg", "cultural"],
        
        "user_engagement_metrics": ["attention", "focus", "interaction", "community", "activity"],
        "satisfaction_feedback": ["satisfaction", "feedback", "sentiment", "support", "expectation"],
        "interaction_design_elements": ["usability", "intuitive", "design", "personalization", "inclusive"],
        "post_purchase_loyalty": ["post_purchase", "loyalty", "repeat", "emotional", "advocacy"],
        "experience_evolution": ["evolution", "update", "trend", "cognitive", "ai"]
    }
    
    if factor_key in factor_mapping:
        keywords = factor_mapping[factor_key]
        return any(keyword in layer_lower for keyword in keywords)
    
    return False

def main():
    """Main function to run the restructuring."""
    input_file = "full_pergola_analysis_report_20250829_124837.json"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return
    
    try:
        restructured_data = restructure_analysis(input_file)
        print("✅ Analysis restructuring completed successfully!")
        
        # Show summary of new structure
        segments = restructured_data["detailed_analysis"]["segments"]
        for segment_key, segment_data in segments.items():
            print(f"\n📊 {segment_data['segment_name']}: {segment_data['overall_score']}/10")
            for factor_key, factor_data in segment_data["factors"].items():
                layer_count = len(factor_data["layers"])
                print(f"  └─ {factor_data['factor_name']}: {factor_data['overall_score']}/10 ({layer_count} layers)")
        
    except Exception as e:
        print(f"❌ Error during restructuring: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
