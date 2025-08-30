import React, { useState } from 'react';
import { AnalysisResult } from '../types/analysis';
import OverviewDashboard from './dashboard/OverviewDashboard';
import SegmentsDashboard from './dashboard/SegmentsDashboard';
import DrillDownView from './dashboard/DrillDownView';

interface AnalysisDashboardProps {
  analysisData: AnalysisResult;
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
  console.log('AnalysisDashboard data structure:', {
    hasData: !!analysisData,
    hasAnalysisMetadata: !!analysisData?.analysis_metadata,
    hasBusinessCase: !!analysisData?.business_case,
    hasAnalysisResults: !!analysisData?.analysis_results,
    hasDetailedAnalysis: !!analysisData?.detailed_analysis,
    hasLayerScores: !!analysisData?.detailed_analysis?.layer_scores,
    layerKeys: analysisData?.detailed_analysis?.layer_scores ? Object.keys(analysisData.detailed_analysis.layer_scores) : []
  });
  
  // Add detailed data inspection
  console.log('Full data object keys:', Object.keys(analysisData || {}));
  console.log('Data type:', typeof analysisData);
  console.log('Data constructor:', analysisData?.constructor?.name);
  console.log('Is array:', Array.isArray(analysisData));
  console.log('Data stringified:', JSON.stringify(analysisData, null, 2).substring(0, 1000) + '...');

  const handleDrillDown = (layerName: string) => {
    setDrillDownState({ level: 'factor', segmentName: 'analysis', layerName, factorName: layerName });
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
        if (drillDownState.segmentName && drillDownState.layerName && drillDownState.factorName) {
          return (
            <DrillDownView 
              data={analysisData}
              segmentName={drillDownState.segmentName}
              layerName={drillDownState.layerName}
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
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              drillDownState.level === 'overview'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setDrillDownState({ level: 'segments' })}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              drillDownState.level === 'segments'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
            }`}
          >
            Layer Analysis
          </button>
          {drillDownState.level === 'factor' && (
            <button
              onClick={handleGoBack}
              className="px-4 py-2 rounded-lg font-medium text-blue-600 hover:text-blue-800 hover:bg-blue-50"
            >
              ← Back to Layers
            </button>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="p-6">
        {renderContent()}
      </div>
    </div>
  );
};
