import { AnalysisContext, AnalysisResponse, DashboardData } from '../types/analysis';

// Mock API service for development
export const api = {
  async startAnalysis(query: string, context: AnalysisContext): Promise<AnalysisResponse> {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return {
      analysis_id: `analysis_${Date.now()}`,
      status: 'initiated',
      progress: 0,
      estimated_completion: new Date(Date.now() + 5 * 60 * 1000).toISOString()
    };
  },

  async getAnalysisStatus(analysisId: string): Promise<AnalysisResponse> {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Simulate progress updates
    const progress = Math.min(100, Math.floor(Math.random() * 100));
    let status: AnalysisResponse['status'] = 'initiated';
    
    if (progress < 20) status = 'parsing';
    else if (progress < 40) status = 'planning';
    else if (progress < 60) status = 'researching';
    else if (progress < 80) status = 'scoring';
    else if (progress < 95) status = 'aggregating';
    else if (progress < 100) status = 'summarizing';
    else status = 'completed';
    
    return {
      analysis_id: analysisId,
      status,
      progress,
      estimated_completion: new Date(Date.now() + 2 * 60 * 1000).toISOString()
    };
  },

  async getAnalysisResults(analysisId: string): Promise<DashboardData> {
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Return mock data for development
    return {
      analysis_id: analysisId,
      query: "Sample strategic analysis",
      context: {
        business_case: 'Strategic analysis for business case',
        industry: "Technology",
        geography: ["North America", "Europe"],
        company_stage: "startup",
        target_audience: "B2B SaaS companies",
        budget_range: "10k_50k",
        timeline: "short_term",
        competitive_context: "Competitive market with established players"
      },
      segment_scores: {
        "Market": { score: 85, confidence: 0.9, summary: "Strong market opportunity", insights: ["High demand", "Growing market"], factor_count: 5, weighted_average: true },
        "Technology": { score: 78, confidence: 0.8, summary: "Good technical feasibility", insights: ["Proven technology", "Scalable architecture"], factor_count: 4, weighted_average: true }
      },
      factor_scores: {},
      layer_scores: {},
      recommendations: [
        "Focus on market differentiation",
        "Invest in user experience",
        "Build strong partnerships"
      ],
      meta_scores: {
        market_fit_score: 82,
        innovation_score: 75
      },
      generated_at: new Date().toISOString()
    };
  }
};
