import { useState, useCallback } from 'react';
import { validatusApi, HierarchicalAnalysisRequest, HierarchicalAnalysisResponse } from '../services/validatusApi';
import { DataTransformationUtils, TransformedAnalysis, PerformanceMetrics } from '../utils/dataTransformation';

export interface AnalysisState {
  analysis: TransformedAnalysis | null;
  performanceMetrics: PerformanceMetrics | null;
  isLoading: boolean;
  error: string | null;
  progress: {
    stage: string;
    percentage: number;
  };
}

export const useValidatusAnalysis = () => {
  const [state, setState] = useState<AnalysisState>({
    analysis: null,
    performanceMetrics: null,
    isLoading: false,
    error: null,
    progress: { stage: 'idle', percentage: 0 }
  });

  const startAnalysis = useCallback(async (request: HierarchicalAnalysisRequest) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      // Check backend health first
      const isHealthy = await validatusApi.healthCheck();
      if (!isHealthy) {
        throw new Error('Backend service is not available');
      }

      setState(prev => ({ 
        ...prev, 
        progress: { stage: 'starting', percentage: 10 } 
      }));

      // Start comprehensive analysis
      const response = await validatusApi.startComprehensiveAnalysis(request);
      
      setState(prev => ({ 
        ...prev, 
        progress: { stage: 'processing', percentage: 50 } 
      }));

      // Validate the response data
      const validation = DataTransformationUtils.validateAnalysisData(response);
      if (!validation.isValid) {
        throw new Error(`Invalid response data: ${validation.errors.join(', ')}`);
      }

      setState(prev => ({ 
        ...prev, 
        progress: { stage: 'transforming', percentage: 80 } 
      }));

      // Transform to internal format
      const analysis = DataTransformationUtils.transformToAnalysis(response);
      const performanceMetrics = DataTransformationUtils.calculatePerformanceMetrics(analysis);

      setState({
        analysis,
        performanceMetrics,
        isLoading: false,
        error: null,
        progress: { stage: 'completed', percentage: 100 }
      });

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
        progress: { stage: 'error', percentage: 0 }
      }));
    }
  }, []);

  const loadLegacyAnalysis = useCallback(async (legacyData: any) => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));
      
      // Transform legacy data to new format
      const analysis = DataTransformationUtils.transformLegacyAnalysis(legacyData);
      
      if (analysis) {
        const performanceMetrics = DataTransformationUtils.calculatePerformanceMetrics(analysis);
        setState({
          analysis,
          performanceMetrics,
          isLoading: false,
          error: null,
          progress: { stage: 'completed', percentage: 100 }
        });
      } else {
        throw new Error('Failed to transform legacy analysis data');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
        progress: { stage: 'error', percentage: 0 }
      }));
    }
  }, []);

  const reset = useCallback(() => {
    setState({
      analysis: null,
      performanceMetrics: null,
      isLoading: false,
      error: null,
      progress: { stage: 'idle', percentage: 0 }
    });
  }, []);

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  return {
    ...state,
    startAnalysis,
    loadLegacyAnalysis,
    reset,
    clearError
  };
};
