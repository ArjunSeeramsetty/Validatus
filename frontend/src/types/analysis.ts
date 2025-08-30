// Legacy types for backward compatibility
export interface AnalysisContext {
  business_case: string;
  target_audience: string;
  geography: string[];
  timeline: string;
  industry: string;
  company_stage: string;
  budget_range?: string;
  competitive_context?: string;
}

export interface AnalysisRequest {
  query: string;
  context: AnalysisContext;
}

export interface AnalysisResponse {
  analysis_id: string;
  status: string;
  progress: number;
  estimated_completion?: string;
}

export type AnalysisStatus = 
  | 'initiated'
  | 'parsing'
  | 'planning'
  | 'researching'
  | 'scoring'
  | 'aggregating'
  | 'summarizing'
  | 'completed'
  | 'failed';

export interface DashboardData {
  analysis_id: string;
  query: string;
  context: AnalysisContext;
  segment_scores: Record<string, any>;
  factor_scores: Record<string, Record<string, any>>;
  layer_scores: Record<string, Record<string, Record<string, any>>>;
  recommendations: string[];
  meta_scores: {
    market_fit_score: number;
    innovation_score: number;
  };
  generated_at: string;
}

// New types matching the actual JSON structure
export interface AnalysisMetadata {
  test_suite: string;
  timestamp: string;
  duration: string;
  total_layers_analyzed: number;
  segments_analyzed: number;
  factors_analyzed: number;
  platform_version: string;
}

export interface BusinessCase {
  idea_description: string;
  target_audience: string;
  additional_context: {
    industry: string;
    primary_markets: string[];
    product_category: string;
    key_features: string[];
    target_segments: string[];
    competitive_advantage: string;
    market_positioning: string;
    price_positioning: string;
    distribution_strategy: string;
    service_model: string;
  };
}

export interface AnalysisResults {
  overall_viability_score: number;
  execution_details: {
    total_layers_analyzed: number;
    total_factors_calculated: number;
    total_segments_evaluated: number;
    analysis_timestamp: string;
  };
  analysis_summary: {
    key_insights: string[];
    total_layers: number;
    total_factors: number;
    total_segments: number;
  };
  recommendations: string[];
  risk_assessment: {
    risk_level: string;
    critical_areas: string[];
    strength_areas: string[];
  };
}

export interface ProgressSummary {
  total_layers: number;
  completed_layers: number;
  current_phase: string;
  estimated_completion: string;
  performance_metrics: {
    average_score: number;
    confidence_level: number;
    quality_score: number;
  };
}

export interface StrategicInsights {
  key_findings: string[];
  market_opportunities: string[];
  risk_factors: string[];
  competitive_advantages: string[];
  strategic_recommendations: string[];
  implementation_priorities: string[];
}

export interface LayerScore {
  score: number;
  rationale: string;
  source_attribution: {
    source_type: string;
    confidence: number;
    methodology: string;
  };
  timestamp: string;
}

// New hierarchical structure
export interface Factor {
  factor_name: string;
  overall_score: number;
  summary: string;
  layers: Record<string, LayerScore>;
  factor_insights: string[];
  recommendations: string[];
}

export interface Segment {
  segment_name: string;
  overall_score: number;
  summary: string;
  factors: Record<string, Factor>;
  segment_insights: string[];
  strategic_priorities: string[];
}

export interface DetailedAnalysis {
  segments: Record<string, Segment>;
  // Keep backward compatibility
  layer_scores?: Record<string, LayerScore>;
}

export interface AnalysisResult {
  analysis_metadata: AnalysisMetadata;
  business_case: BusinessCase;
  analysis_results: AnalysisResults;
  progress_summary: ProgressSummary;
  strategic_insights: StrategicInsights;
  detailed_analysis: DetailedAnalysis;
}

