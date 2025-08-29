export interface LayerScore {
  name: string;
  score: number;
  confidence: number;
  calculation_method: string;
  supporting_data: Record<string, any>;
  data_sources: string[];
  summary: string;
  insights?: string[];
}

export interface FactorScore {
  name: string;
  score: number;
  confidence: number;
  layers: Record<string, LayerScore>;
  summary: string;
  key_insights: string[];
  recommendations: string[];
}

export interface SegmentScore {
  name: string;
  score: number;
  confidence: number;
  factors: Record<string, FactorScore>;
  key_insights: string[];
  recommendations: string[];
  trend: 'up' | 'down' | 'stable';
  priority: 'high' | 'medium' | 'low';
}

export interface PergolaAnalysis {
  query: string;
  overall_score: number;
  overall_confidence: number;
  segments: Record<string, SegmentScore>;
  meta_scores: {
    market_fit: number;
    innovation_score: number;
    execution_readiness: number;
    risk_index: number;
    brand_strength: number;
  };
  executive_summary: string;
  key_recommendations: string[];
  competitive_advantages: string[];
  risk_factors: string[];
  generated_at: string;
}

export interface DrillDownState {
  level: 'overview' | 'segment' | 'factor' | 'layer';
  selectedSegment?: string;
  selectedFactor?: string;
  selectedLayer?: string;
  breadcrumb: Array<{
    level: string;
    name: string;
    path: string;
  }>;
}

export interface PerformanceMetrics {
  segmentScores: Array<{
    name: string;
    score: number;
    confidence: number;
    trend: 'up' | 'down' | 'stable';
    priority: 'high' | 'medium' | 'low';
  }>;
  bestSegment: {
    name: string;
    score: number;
    confidence: number;
    trend: 'up' | 'down' | 'stable';
    priority: 'high' | 'medium' | 'low';
  };
  worstSegment: {
    name: string;
    score: number;
    confidence: number;
    trend: 'up' | 'down' | 'stable';
    priority: 'high' | 'medium' | 'low';
  };
  topFactors: Array<{
    segmentName: string;
    factorName: string;
    score: number;
    confidence: number;
  }>;
  overallTrend: 'positive' | 'negative';
}
