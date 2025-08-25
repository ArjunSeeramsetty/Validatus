# This file defines the complete analytical structure of the Validatus platform.
# It serves as a central repository for all segments, factors, and layers.

ANALYTICAL_FRAMEWORK = {
    "CONSUMER": {
        "factors": {
            "Consumer Demand & Need": ["need_perception", "purchase_intent", "emotional_pull", "unmet_needs"],
            "Consumer Behavior & Habits": ["shopping_habits", "media_consumption", "decision_making_process", "brand_interaction"],
            "Consumer Loyalty & Retention": ["repeat_purchase_rate", "churn_risk", "advocacy_potential", "loyalty_program_effectiveness"],
            "Consumer Perception & Sentiment": ["overall_sentiment", "quality_perception", "trust_perception", "value_for_money"],
            "Consumer Adoption & Engagement": ["product_usage_frequency", "feature_adoption_rate", "community_engagement", "feedback_submission_rate"]
        },
        "agent": "consumer_insights"
    },
    "MARKET": {
        "factors": {
            "Market Size & Growth": ["total_addressable_market", "serviceable_addressable_market", "market_growth_rate", "future_projections"],
            "Market Trends & Opportunities": ["emerging_trends", "technological_shifts", "white_space_opportunities", "macroeconomic_factors", "perplexity_market_deep_dive"],
            "Competitive Landscape": ["key_competitors", "market_share_distribution", "competitor_strengths_weaknesses", "rival_intensity"],
            "Regulatory Environment": ["key_regulations", "compliance_requirements", "political_stability", "trade_policies"],
            "Market Risks & Challenges": ["economic_risks", "competitive_threats", "supply_chain_vulnerabilities", "market_volatility"]
        },
        "agent": "market_research"
    },
    "PRODUCT": {
        "factors": {
            "Features & Functionality": ["core_features_analysis", "feature_completeness", "user_friendliness", "performance_reliability"],
            "Innovation & Differentiation": ["unique_selling_proposition", "technological_innovation", "design_innovation", "patent_portfolio"],
            "Value Proposition": ["clarity_of_value", "problem_solution_fit", "cost_benefit_analysis", "emotional_benefits"],
            "Business Resilience": ["supply_chain_resilience", "cost_structure_stability", "scalability_potential", "dependency_risks"],
            "Product Quality & Assurance": ["defect_rate", "customer_reported_issues", "performance_benchmarks", "compliance_standards"]
        },
        "agent": "competitor_analysis" # A mix of agents would be used here in reality
    },
    "BRAND": {
        "factors": {
            "Brand Awareness & Recognition": ["unaided_brand_recall", "aided_brand_recognition", "share_of_voice", "social_media_presence"],
            "Brand Equity Profile": ["brand_associations", "perceived_quality", "brand_loyalty_metrics", "brand_advocacy"],
            "Brand Positioning Strategy": ["market_positioning", "target_audience_alignment", "competitive_differentiation", "brand_story_clarity"],
            "Brand Messaging & Communication": ["message_consistency", "tone_of_voice", "channel_effectiveness", "content_engagement"],
            "Brand Monetization Model": ["pricing_strategy", "customer_lifetime_value", "revenue_streams", "profitability_analysis"]
        },
        "agent": "trend_analysis" # A mix of agents would be used here
    },
    "EXPERIENCE": {
        "factors": {
            "User Experience (UX) & Design": ["onboarding_experience", "ease_of_use", "navigation_clarity", "visual_appeal"],
            "Customer Journey Mapping": ["touchpoint_analysis", "friction_points", "emotional_journey", "channel_consistency"],
            "Customer Support & Service": ["first_response_time", "resolution_rate", "support_channel_effectiveness", "agent_satisfaction"],
            "Post-Purchase Loyalty & Advocacy": ["post_purchase_communication", "loyalty_program_engagement", "review_and_rating_behavior", "referral_rate"],
            "Customer Engagement & Community": ["community_activity_level", "user_generated_content", "brand_interaction_rate", "event_participation"]
        },
        "agent": "consumer_insights"
    }
}

LAYER_TO_AGENT_MAP = {
    # This map provides a more granular mapping from a specific layer to the best agent for the job.
    # Defaulting to the segment's agent if not specified here.
    "key_competitors": "competitor_analysis",
    "market_share_distribution": "competitor_analysis",
    "competitor_strengths_weaknesses": "competitor_analysis",
    "rival_intensity": "competitor_analysis",
    "emerging_trends": "trend_analysis",
    "technological_shifts": "trend_analysis",
    "perplexity_market_deep_dive": "perplexity_research",  # New Perplexity-specific layer
    "pricing_strategy": "pricing_research",
    "cost_benefit_analysis": "pricing_research",
    #... add more specific overrides as needed
}
