import { AnalysisRequest, AnalysisResponse, DashboardData } from '../types/analysis';

const API_BASE_URL = 'http://localhost:8000';

export class ApiService {
  private static async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  static async createAnalysis(request: AnalysisRequest): Promise<AnalysisResponse> {
    return this.request<AnalysisResponse>('/api/v1/analysis', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  static async getAnalysisStatus(analysisId: string): Promise<AnalysisResponse> {
    return this.request<AnalysisResponse>(`/api/v1/analysis/${analysisId}/status`);
  }

  static async getAnalysisResults(analysisId: string): Promise<DashboardData> {
    return this.request<DashboardData>(`/api/v1/analysis/${analysisId}/results`);
  }

  static async healthCheck(): Promise<{ status: string; timestamp: string }> {
    return this.request<{ status: string; timestamp: string }>('/health');
  }
}
