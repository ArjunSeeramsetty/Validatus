import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface HierarchicalAnalysisRequest {
  query: string;
  context: {
    industry?: string;
    geography?: string[];
    company_stage?: string;
    target_audience?: string;
    budget_range?: string;
    timeline?: string;
  };
}

export interface HierarchicalAnalysisResponse {
  query: string;
  overall_score: number;
  overall_confidence: number;
  segments: {
    [segmentName: string]: {
      name: string;
      score: number;
      confidence: number;
      trend: 'up' | 'down' | 'stable';
      priority: 'high' | 'medium' | 'low';
      key_insights: string[];
      recommendations: string[];
      factors: {
        [factorName: string]: {
          name: string;
          score: number;
          confidence: number;
          summary: string;
          key_insights: string[];
          recommendations: string[];
          layers: {
            [layerName: string]: {
              name: string;
              score: number;
              confidence: number;
              calculation_method: string;
              supporting_data: Record<string, any>;
              data_sources: string[];
              summary: string;
            };
          };
        };
      };
    };
  };
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

export class ValidatusApiService {
  private client = axios.create({
    baseURL: API_BASE_URL,
    timeout: 300000, // 5 minutes for comprehensive analysis
    headers: {
      'Content-Type': 'application/json',
    },
  });

  async startComprehensiveAnalysis(
    request: HierarchicalAnalysisRequest
  ): Promise<HierarchicalAnalysisResponse> {
    try {
      const response = await this.client.post('/api/v1/hierarchical-analysis/comprehensive', request);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`API Error: ${error.response?.data?.detail || error.message}`);
      }
      throw error;
    }
  }

  async getAnalysisCapabilities(): Promise<any> {
    try {
      const response = await this.client.get('/api/v1/hierarchical-analysis/capabilities');
      return response.data;
    } catch (error) {
      console.warn('Failed to fetch capabilities:', error);
      return null;
    }
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.client.get('/api/v1/hierarchical-analysis/health');
      return response.data.status === 'healthy';
    } catch (error) {
      return false;
    }
  }
}

export const validatusApi = new ValidatusApiService();
