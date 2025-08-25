import { useState, useEffect, useCallback } from 'react';
import { useAnalysisStore } from '../stores/analysisStore';
import { AnalysisContext } from '../types/analysis';

export const useAnalysis = () => {
  const {
    currentAnalysis,
    startAnalysis,
    checkAnalysisStatus,
    setError,
    isLoading,
    error
  } = useAnalysisStore();

  const [pollingInterval, setPollingInterval] = useState<number | null>(null);

  const startNewAnalysis = useCallback(async (query: string, context: AnalysisContext) => {
    try {
      await startAnalysis({ query, context });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start analysis');
    }
  }, [startAnalysis, setError]);

  const stopPolling = useCallback(() => {
    if (pollingInterval) {
      clearInterval(pollingInterval);
      setPollingInterval(null);
    }
  }, [pollingInterval]);

  const startPolling = useCallback((analysisId: string) => {
    stopPolling();
    
    const interval = setInterval(async () => {
      try {
        await checkAnalysisStatus(analysisId);
      } catch (err) {
        console.error('Polling error:', err);
        stopPolling();
      }
    }, 5000); // Poll every 5 seconds

    setPollingInterval(interval);
  }, [checkAnalysisStatus, stopPolling]);

  useEffect(() => {
    if (currentAnalysis?.analysis_id && currentAnalysis.status !== 'completed' && currentAnalysis.status !== 'failed') {
      startPolling(currentAnalysis.analysis_id);
    } else {
      stopPolling();
    }

    return () => stopPolling();
  }, [currentAnalysis?.analysis_id, currentAnalysis?.status, startPolling, stopPolling]);

  useEffect(() => {
    return () => stopPolling();
  }, [stopPolling]);

  return {
    currentAnalysis,
    startNewAnalysis,
    isLoading,
    error,
    stopPolling
  };
};
