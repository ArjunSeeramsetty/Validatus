import React, { useState } from 'react';
import { Dashboard } from './components/dashboard/Dashboard';
import { AnalysisDashboard } from './components/AnalysisDashboard';
import HomePage from './components/HomePage';
import { ErrorBoundary } from './components/ErrorBoundary';

function App() {
  // View states: 'home', 'form', 'dashboard'
  const [currentView, setCurrentView] = useState<'home' | 'form' | 'dashboard'>('home');
  const [analysisData, setAnalysisData] = useState<any | null>(null);

  const handleStartNew = () => {
    setCurrentView('form');
  };

  const handleLoadAnalysis = (data: any) => {
    setAnalysisData(data);
    setCurrentView('dashboard');
  };
  
  const handleGoHome = () => {
    setAnalysisData(null);
    setCurrentView('home');
  };

  const renderContent = () => {
    switch (currentView) {
      case 'form':
        return <Dashboard />;
      case 'dashboard':
        return <AnalysisDashboard analysisData={analysisData} onGoHome={handleGoHome} />;
      case 'home':
      default:
        return <HomePage onStartNewAnalysis={handleStartNew} onLoadAnalysis={handleLoadAnalysis} />;
    }
  };

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gray-100">
        <main>
          {renderContent()}
        </main>
      </div>
    </ErrorBoundary>
  );
}

export default App;
