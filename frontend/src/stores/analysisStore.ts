import { create } from 'zustand';
import { AnalysisRequest, AnalysisResponse, AnalysisStatus } from '../types/analysis';
import { ApiService } from '../services/api';

interface AnalysisState {
  currentAnalysis: AnalysisResponse | null;
  analysisStatus: AnalysisStatus;
  segmentScores: Record<string, any> | null;
  factorScores: Record<string, any> | null;
  layerScores: Record<string, any> | null;
  recommendations: string[];
  isLoading: boolean;
  error: string | null;
  
  // Actions
  startAnalysis: (request: AnalysisRequest) => Promise<void>;
  checkAnalysisStatus: (analysisId: string) => Promise<void>;
  getAnalysisResults: (analysisId: string) => Promise<void>;
  resetAnalysis: () => void;
  setError: (error: string) => void;
  clearError: () => void;
}

export const useAnalysisStore = create<AnalysisState>((set, get) => ({
  currentAnalysis: null,
  analysisStatus: 'initiated',
  segmentScores: null,
  factorScores: null,
  layerScores: null,
  recommendations: [],
  isLoading: false,
  error: null,

  startAnalysis: async (request: AnalysisRequest) => {
    try {
      set({ isLoading: true, error: null });
      
      const response = await ApiService.createAnalysis(request);
      
      set({
        currentAnalysis: response,
        analysisStatus: response.status as AnalysisStatus,
        isLoading: false,
      });

      // Start polling for status updates
      const pollStatus = async () => {
        const currentAnalysis = get().currentAnalysis;
        if (currentAnalysis && currentAnalysis.status !== 'completed' && currentAnalysis.status !== 'failed') {
          await get().checkAnalysisStatus(currentAnalysis.analysis_id);
          
          // Continue polling if not completed
          if (get().analysisStatus !== 'completed' && get().analysisStatus !== 'failed') {
            setTimeout(pollStatus, 2000); // Poll every 2 seconds
          }
        }
      };

      // Start polling after a short delay
      setTimeout(pollStatus, 1000);
      
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to start analysis',
        isLoading: false 
      });
    }
  },

  checkAnalysisStatus: async (analysisId: string) => {
    try {
      const response = await ApiService.getAnalysisStatus(analysisId);
      
      set({
        analysisStatus: response.status as AnalysisStatus,
        currentAnalysis: response,
      });

      // If completed, fetch results
      if (response.status === 'completed') {
        await get().getAnalysisResults(analysisId);
      }
      
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to check analysis status',
        isLoading: false 
      });
    }
  },

  getAnalysisResults: async (analysisId: string) => {
    try {
      const results = await ApiService.getAnalysisResults(analysisId);
      
      set({
        segmentScores: results.segment_scores,
        factorScores: results.factor_scores,
        layerScores: results.layer_scores,
        recommendations: results.recommendations,
        isLoading: false,
      });
      
    } catch (error) {
      set({ 
        error: error instanceof Error ? error.message : 'Failed to get analysis results',
        isLoading: false 
      });
    }
  },

  resetAnalysis: () => {
    set({
      currentAnalysis: null,
      analysisStatus: 'initiated',
      segmentScores: null,
      factorScores: null,
      layerScores: null,
      recommendations: [],
      isLoading: false,
      error: null,
    });
  },

  setError: (error: string) => {
    set({ error });
  },

  clearError: () => {
    set({ error: null });
  },
}));
