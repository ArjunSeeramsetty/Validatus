import React, { useState } from 'react';
import { TransformedAnalysis } from '../utils/dataTransformation';
import OverviewDashboard from './dashboard/OverviewDashboard';
import SegmentsDashboard from './dashboard/SegmentsDashboard';
import DrillDownView from './dashboard/DrillDownView';

interface AnalysisDashboardProps {
  analysisData: TransformedAnalysis | null;
  onGoHome: () => void;
}

interface DrillDownState {
  level: 'overview' | 'segments' | 'factor';
  segmentName?: string;
  layerName?: string;
  factorName?: string;
}

export const AnalysisDashboard: React.FC<AnalysisDashboardProps> = ({ 
  analysisData, 
  onGoHome 
}) => {
  const [drillDownState, setDrillDownState] = useState<DrillDownState>({ level: 'overview' });

  // Add debugging
  console.log('AnalysisDashboard received analysisData:', analysisData);
  
  if (!analysisData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">No Analysis Data</h2>
          <p className="text-gray-600 mb-4">Please upload an analysis file or start a new analysis.</p>
          <button
            onClick={onGoHome}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            ← Back to Home
          </button>
        </div>
      </div>
    );
  }

  const handleDrillDown = (level: 'segments' | 'factor', segmentName?: string, factorName?: string, layerName?: string) => {
    setDrillDownState({ level, segmentName, factorName, layerName });
  };

  const handleGoBack = () => {
    if (drillDownState.level === 'factor') {
      setDrillDownState({ level: 'segments' });
    } else {
      setDrillDownState({ level: 'overview' });
    }
  };

  const renderContent = () => {
    switch (drillDownState.level) {
      case 'segments':
        return (
          <SegmentsDashboard 
            data={analysisData} 
            onDrillDown={handleDrillDown}
          />
        );
      case 'factor':
        if (drillDownState.segmentName && drillDownState.factorName) {
          return (
            <DrillDownView 
              data={analysisData}
              segmentName={drillDownState.segmentName}
              factorName={drillDownState.factorName}
              onGoBack={handleGoBack}
            />
          );
        }
        return <div>Invalid drill-down state</div>;
      default:
        return <OverviewDashboard data={analysisData} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="flex items-center justify-between px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Validatus Dashboard</h1>
          <button
            onClick={onGoHome}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            ← Back to Home
          </button>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white shadow-sm border-b px-6 py-3">
        <div className="flex items-center space-x-6">
          <button
            onClick={() => setDrillDownState({ level: 'overview' })}
            className={`px-3 py-2 rounded-lg font-medium transition-colors ${
              drillDownState.level === 'overview'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setDrillDownState({ level: 'segments' })}
            className={`px-3 py-2 rounded-lg font-medium transition-colors ${
              drillDownState.level === 'segments'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Segments Analysis
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="p-6">
        {renderContent()}
      </div>
    </div>
  );
};
