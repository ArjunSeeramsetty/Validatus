import { create } from 'zustand';

interface AnalysisResult {
  [key: string]: any;
}

interface AnalysisState {
  analysisResult: AnalysisResult | null;
  isLoading: boolean;
  error: string | null;
  setLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
  setAnalysisData: (data: AnalysisResult) => void;
  reset: () => void;
}

const useAnalysisStore = create<AnalysisState>((set) => ({
  analysisResult: null,
  isLoading: false,
  error: null,
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  setAnalysisData: (data) => set({ analysisResult: data, isLoading: false, error: null }),
  reset: () => set({ analysisResult: null, isLoading: false, error: null }),
}));

export default useAnalysisStore;
