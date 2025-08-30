import React, { useState } from 'react';
import HomePage from './components/HomePage';
import { AnalysisDashboard } from './components/AnalysisDashboard';
import { useValidatusAnalysis } from './hooks/useValidatusAnalysis';
import { TransformedAnalysis } from './utils/dataTransformation';

function App() {
  const [currentView, setCurrentView] = useState<'home' | 'dashboard'>('home');
  const [analysisData, setAnalysisData] = useState<TransformedAnalysis | null>(null);
  
  const { 
    analysis, 
    performanceMetrics, 
    isLoading, 
    error, 
    progress,
    loadLegacyAnalysis,
    reset 
  } = useValidatusAnalysis();

  const handleFileUpload = async (data: any) => {
    try {
      // Try to load as legacy analysis first
      await loadLegacyAnalysis(data);
      setAnalysisData(analysis);
      setCurrentView('dashboard');
    } catch (error) {
      console.error('Failed to load analysis:', error);
      // Fallback to direct data loading
      setAnalysisData(data);
      setCurrentView('dashboard');
    }
  };

  const handleNewAnalysis = () => {
    reset();
    setAnalysisData(null);
    setCurrentView('home');
  };

  const handleBackToHome = () => {
    setCurrentView('home');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {currentView === 'home' ? (
        <HomePage 
          onStartNewAnalysis={handleNewAnalysis}
          onLoadAnalysis={handleFileUpload}
        />
      ) : (
        <AnalysisDashboard 
          analysisData={analysisData || analysis}
          onGoHome={handleBackToHome}
        />
      )}
    </div>
  );
}

export default App;
