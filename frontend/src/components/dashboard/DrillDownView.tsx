import React from 'react';
import { AnalysisResult } from '../../types/analysis';
import { ProgressRing } from '../charts/ProgressRing';

interface DrillDownViewProps {
  data: AnalysisResult;
  segmentName: string;
  layerName: string;
  factorName: string;
  onGoBack: () => void;
}

const DrillDownView: React.FC<DrillDownViewProps> = ({ 
  data, 
  segmentName, 
  layerName, 
  factorName, 
  onGoBack 
}) => {
  // Since we're working with layers, we'll show the layer details
  const layerData = data?.detailed_analysis?.layer_scores?.[layerName];

  if (!layerData) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <button
          onClick={onGoBack}
          className="text-blue-600 hover:text-blue-800 mb-4 flex items-center"
        >
          ← Back to Layers
        </button>
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Layer Details</h2>
        <p className="text-red-600">Layer data not found</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <button
        onClick={onGoBack}
        className="text-blue-600 hover:text-blue-800 mb-4 flex items-center"
      >
        ← Back to Layers
      </button>

      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          {layerName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())} Analysis
        </h1>
        
        <div className="flex items-center space-x-6">
          <ProgressRing value={layerData.score} size={100} />
          <div>
            <p className="text-2xl font-bold text-gray-800">Score: {layerData.score}/10</p>
            <p className="text-lg text-gray-600">
              Confidence: {Math.round(layerData.source_attribution.confidence * 100)}%
            </p>
            <p className="text-sm text-gray-500">
              Analyzed: {new Date(layerData.timestamp).toLocaleString()}
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-6">
        <div>
          <h3 className="text-xl font-semibold text-gray-700 mb-3">Analysis Rationale</h3>
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
              {layerData.rationale}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="font-semibold text-blue-800 mb-2">Source Attribution</h4>
            <div className="space-y-2 text-sm">
              <p><span className="font-medium">Type:</span> {layerData.source_attribution.source_type}</p>
              <p><span className="font-medium">Methodology:</span> {layerData.source_attribution.methodology}</p>
              <p><span className="font-medium">Confidence:</span> {Math.round(layerData.source_attribution.confidence * 100)}%</p>
            </div>
          </div>

          <div className="bg-green-50 p-4 rounded-lg">
            <h4 className="font-semibold text-green-800 mb-2">Analysis Metadata</h4>
            <div className="space-y-2 text-sm">
              <p><span className="font-medium">Timestamp:</span> {new Date(layerData.timestamp).toLocaleString()}</p>
              <p><span className="font-medium">Score:</span> {layerData.score}/10</p>
              <p><span className="font-medium">Status:</span> 
                <span className={`ml-2 px-2 py-1 rounded text-xs ${
                  layerData.score >= 8 ? 'bg-green-100 text-green-800' :
                  layerData.score >= 6 ? 'bg-yellow-100 text-yellow-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {layerData.score >= 8 ? 'Excellent' : layerData.score >= 6 ? 'Good' : 'Needs Improvement'}
                </span>
              </p>
            </div>
          </div>

          <div className="bg-purple-50 p-4 rounded-lg">
            <h4 className="font-semibold text-purple-800 mb-2">Strategic Insights</h4>
            <div className="space-y-2 text-sm">
              <p><span className="font-medium">Performance:</span> 
                {layerData.score >= 8 ? 'High performing area' : 
                 layerData.score >= 6 ? 'Moderate performance' : 
                 'Area for improvement'}
              </p>
              <p><span className="font-medium">Focus:</span> 
                {layerData.score >= 8 ? 'Leverage strength' : 
                 layerData.score >= 6 ? 'Maintain and improve' : 
                 'Prioritize improvement'}
              </p>
            </div>
          </div>
        </div>

        <div>
          <h3 className="text-xl font-semibold text-gray-700 mb-3">Recommendations</h3>
          <div className="bg-yellow-50 p-4 rounded-lg">
            <p className="text-gray-700">
              Based on the {layerData.score}/10 score for {layerName.replace(/_/g, ' ').toLowerCase()}, 
              this area {layerData.score >= 8 ? 'represents a significant strength' : 
                         layerData.score >= 6 ? 'shows moderate performance' : 
                         'requires attention and improvement'}.
            </p>
            {layerData.score < 8 && (
              <div className="mt-3 p-3 bg-white rounded border-l-4 border-yellow-400">
                <p className="text-sm text-gray-700">
                  <strong>Action Items:</strong> Consider reviewing the analysis rationale above 
                  for specific improvement opportunities and strategic recommendations.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DrillDownView;
