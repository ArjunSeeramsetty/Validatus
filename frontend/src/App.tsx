import React, { useState } from 'react';
import HomePage from './components/HomePage';
import { AnalysisDashboard } from './components/AnalysisDashboard';
import { AnalysisResult } from './types/analysis';

function App() {
  const [currentView, setCurrentView] = useState<'home' | 'dashboard'>('home');
  const [analysisData, setAnalysisData] = useState<AnalysisResult | null>(null);

  const handleFileUpload = (data: AnalysisResult) => {
    setAnalysisData(data);
    setCurrentView('dashboard');
  };

  const handleGoHome = () => {
    setCurrentView('home');
    setAnalysisData(null);
  };

  const handleStartNewAnalysis = () => {
    // TODO: Implement new analysis flow
    console.log('Starting new analysis...');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {currentView === 'home' ? (
        <HomePage 
          onStartNewAnalysis={handleStartNewAnalysis}
          onLoadAnalysis={handleFileUpload}
        />
      ) : (
        <AnalysisDashboard 
          analysisData={analysisData!}
          onGoHome={handleGoHome}
        />
      )}
    </div>
  );
}

export default App;
