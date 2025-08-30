import React, { useState } from 'react';
import { TransformedAnalysis } from '../../utils/dataTransformation';
import { ChartDataAdapters } from '../charts/ChartDataAdapters';
import { BarChart } from '../charts/BarChart';

interface SegmentsDashboardProps {
  data: TransformedAnalysis;
  onDrillDown: (level: 'segments' | 'factor', segmentName?: string, factorName?: string, layerName?: string) => void;
}

const SegmentsDashboard: React.FC<SegmentsDashboardProps> = ({ data, onDrillDown }) => {
  const [expandedSegments, setExpandedSegments] = useState<Set<string>>(new Set());
  const [expandedFactors, setExpandedFactors] = useState<Set<string>>(new Set());

  const toggleSegment = (segmentName: string) => {
    const newExpanded = new Set(expandedSegments);
    if (newExpanded.has(segmentName)) {
      newExpanded.delete(segmentName);
    } else {
      newExpanded.add(segmentName);
    }
    setExpandedSegments(newExpanded);
  };

  const toggleFactor = (factorKey: string) => {
    const newExpanded = new Set(expandedFactors);
    if (newExpanded.has(factorKey)) {
      newExpanded.delete(factorKey);
    } else {
      newExpanded.add(factorKey);
    }
    setExpandedFactors(newExpanded);
  };

  const handleFactorDrillDown = (segmentName: string, factorName: string) => {
    onDrillDown('factor', segmentName, factorName);
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Segments Analysis</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Object.entries(data.segments).map(([segmentKey, segment]) => (
            <div key={segmentKey} className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-semibold text-gray-800">{segment.name}</h3>
                <button
                  onClick={() => toggleSegment(segmentKey)}
                  className="text-blue-600 hover:text-blue-800"
                >
                  {expandedSegments.has(segmentKey) ? '▼' : '▶'}
                </button>
              </div>
              
              <div className="mb-3">
                <div className="text-2xl font-bold text-blue-600">{segment.score}/100</div>
                <div className="text-sm text-gray-600">Confidence: {(segment.confidence * 100).toFixed(1)}%</div>
                <div className="text-sm text-gray-600">Priority: {segment.priority}</div>
                <div className="text-sm text-gray-600">Trend: {segment.trend}</div>
              </div>

              {expandedSegments.has(segmentKey) && (
                <div className="space-y-3">
                  <div>
                    <h4 className="font-semibold text-gray-700 mb-2">Key Insights</h4>
                    <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                      {segment.key_insights.map((insight, index) => (
                        <li key={index}>{insight}</li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-700 mb-2">Recommendations</h4>
                    <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                      {segment.recommendations.map((rec, index) => (
                        <li key={index}>{rec}</li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-700 mb-2">Factors ({Object.keys(segment.factors).length})</h4>
                    {Object.entries(segment.factors).map(([factorKey, factor]) => (
                      <div key={factorKey} className="bg-white rounded p-3 mb-2">
                        <div className="flex items-center justify-between mb-2">
                          <h5 className="font-medium text-gray-800">{factor.name}</h5>
                          <button
                            onClick={() => toggleFactor(factorKey)}
                            className="text-blue-600 hover:text-blue-800 text-sm"
                          >
                            {expandedFactors.has(factorKey) ? '▼' : '▶'}
                          </button>
                        </div>
                        
                        <div className="mb-2">
                          <div className="text-lg font-semibold text-blue-600">{factor.score}/100</div>
                          <div className="text-sm text-gray-600">Confidence: {(factor.confidence * 100).toFixed(1)}%</div>
                        </div>

                        {expandedFactors.has(factorKey) && (
                          <div className="space-y-2">
                            <p className="text-sm text-gray-600">{factor.summary}</p>
                            
                            <div>
                              <h6 className="font-medium text-gray-700 text-sm">Key Insights</h6>
                              <ul className="list-disc list-inside text-xs text-gray-600 space-y-1">
                                {factor.key_insights.map((insight, index) => (
                                  <li key={index}>{insight}</li>
                                ))}
                              </ul>
                            </div>

                            <div>
                              <h6 className="font-medium text-gray-700 text-sm">Recommendations</h6>
                              <ul className="list-disc list-inside text-xs text-gray-600 space-y-1">
                                {factor.recommendations.map((rec, index) => (
                                  <li key={index}>{rec}</li>
                                ))}
                              </ul>
                            </div>

                            <div>
                              <h6 className="font-medium text-gray-700 text-sm">Layers ({Object.keys(factor.layers).length})</h6>
                              <div className="text-xs text-gray-600">
                                {Object.entries(factor.layers).slice(0, 3).map(([layerKey, layer]) => (
                                  <div key={layerKey} className="flex justify-between">
                                    <span>{layer.name}</span>
                                    <span>{layer.score}/100</span>
                                  </div>
                                ))}
                                {Object.keys(factor.layers).length > 3 && (
                                  <div className="text-gray-500 italic">... and {Object.keys(factor.layers).length - 3} more</div>
                                )}
                              </div>
                            </div>

                            <button
                              onClick={() => handleFactorDrillDown(segmentKey, factorKey)}
                              className="w-full bg-blue-600 text-white text-xs py-1 px-2 rounded hover:bg-blue-700 transition-colors"
                            >
                              Drill Down to Layers
                            </button>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SegmentsDashboard;
