import React, { useState } from 'react';
import { PergolaDashboard } from './components/PergolaDashboard';
import { AnalysisSelector } from './components/AnalysisSelector';
import { PergolaAnalysis } from './types/pergola';
 
function App() {
  const [selectedAnalysis, setSelectedAnalysis] = useState<PergolaAnalysis | null>(null);
  const [showAnalysisSelector, setShowAnalysisSelector] = useState(true);

  const handleAnalysisSelect = (analysis: PergolaAnalysis) => {
    console.log('Analysis selected:', analysis);
    setSelectedAnalysis(analysis);
    setShowAnalysisSelector(false);
  };

  const handleNewAnalysis = () => {
    // This would typically open a form to start a new analysis
    // For now, we'll just show the selector again
    setShowAnalysisSelector(true);
    setSelectedAnalysis(null);
  };

  const handleBackToSelector = () => {
    setShowAnalysisSelector(true);
    setSelectedAnalysis(null);
  };

  return (
    <div className="App">
      {showAnalysisSelector ? (
        <AnalysisSelector 
          onAnalysisSelect={handleAnalysisSelect}
          onNewAnalysis={handleNewAnalysis}
        />
      ) : selectedAnalysis ? (
        <div>
          {/* Back to Analysis Selector Button */}
          <div className="fixed top-4 left-4 z-50">
            <button
              onClick={handleBackToSelector}
              className="bg-white hover:bg-gray-100 text-gray-700 font-medium py-2 px-4 rounded-lg shadow-lg border border-gray-200 transition-colors"
            >
              ← Back to Analysis Selector
            </button>
          </div>
          
          <PergolaDashboard data={selectedAnalysis} />
        </div>
      ) : (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading...</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
