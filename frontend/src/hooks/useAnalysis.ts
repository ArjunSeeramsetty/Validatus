import { useState, useCallback } from 'react';
import useAnalysisStore from '../stores/analysisStore';

export const useAnalysis = () => {
  const {
    analysisResult,
    isLoading,
    error,
    setLoading,
    setError,
    setAnalysisData
  } = useAnalysisStore();

  const startNewAnalysis = useCallback(async (query: string, context: any) => {
    try {
      setLoading(true);
      setError(null);
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // For now, we'll simulate setting analysis data
      // In a real implementation, this would come from the API response
      const mockAnalysisData = {
        business_case: {
          idea_description: query
        },
        analysis_results: {
          overall_score: 75.0,
          overall_confidence: 0.85,
          segments: {
            CONSUMER: { score: 80, confidence: 0.9 },
            MARKET: { score: 70, confidence: 0.8 },
            TECHNOLOGY: { score: 75, confidence: 0.85 },
            FINANCIAL: { score: 65, confidence: 0.75 },
            COMPETITIVE: { score: 70, confidence: 0.8 }
          }
        }
      };
      
      setAnalysisData(mockAnalysisData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start analysis');
    } finally {
      setLoading(false);
    }
  }, [setLoading, setError, setAnalysisData]);

  return {
    analysisResult,
    startNewAnalysis,
    isLoading,
    error
  };
};
