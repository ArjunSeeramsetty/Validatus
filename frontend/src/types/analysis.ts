export interface AnalysisContext {
  industry: string;
  geography: string[];
  company_stage: string;
  target_audience: string;
  budget_range?: string;
  timeline?: string;
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

export interface LayerScore {
  score: number;
  confidence: number;
  calculation_method: string;
  supporting_data: Record<string, any>;
  data_sources: string[];
  summary: string;
  raw_score: number;
  framework_used: string;
}

export interface FactorScore {
  score: number;
  confidence: number;
  summary: string;
}

export interface SegmentScore {
  score: number;
  confidence: number;
  summary: string;
  insights: string[];
  factor_count: number;
  weighted_average: boolean;
}

export interface DashboardData {
  analysis_id: string;
  query: string;
  context: AnalysisContext;
  segment_scores: Record<string, SegmentScore>;
  factor_scores: Record<string, Record<string, FactorScore>>;
  layer_scores: Record<string, Record<string, Record<string, LayerScore>>>;
  recommendations: string[];
  meta_scores: {
    market_fit_score: number;
    innovation_score: number;
  };
  generated_at: string;
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
