import React, { useState } from 'react';
import { AnalysisResult } from '../../types/analysis';
import { ProgressRing } from '../charts/ProgressRing';

interface SegmentsDashboardProps {
  data: AnalysisResult;
  onDrillDown: (layerName: string) => void;
}

const SegmentsDashboard: React.FC<SegmentsDashboardProps> = ({ data, onDrillDown }) => {
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set());
  const [expandedLayers, setExpandedLayers] = useState<Set<string>>(new Set());

  const toggleSection = (sectionName: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(sectionName)) {
      newExpanded.delete(sectionName);
    } else {
      newExpanded.add(sectionName);
    }
    setExpandedSections(newExpanded);
  };

  const toggleLayer = (layerName: string) => {
    const newExpanded = new Set(expandedLayers);
    if (newExpanded.has(layerName)) {
      newExpanded.delete(layerName);
    } else {
      newExpanded.add(layerName);
    }
    setExpandedLayers(newExpanded);
  };

  // Check if we have layer scores for drill-down
  const hasLayerScores = data?.detailed_analysis?.layer_scores;
  const layerEntries = hasLayerScores ? Object.entries(data.detailed_analysis!.layer_scores) : [];

  // Add detailed debugging
  console.log('SegmentsDashboard debugging:', {
    hasDetailedAnalysis: !!data?.detailed_analysis,
    detailedAnalysisKeys: data?.detailed_analysis ? Object.keys(data.detailed_analysis) : [],
    hasLayerScores: !!hasLayerScores,
    layerEntriesCount: layerEntries.length,
    detailedAnalysisType: typeof data?.detailed_analysis,
    detailedAnalysisStringified: data?.detailed_analysis ? JSON.stringify(data.detailed_analysis).substring(0, 500) + '...' : 'undefined'
  });

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Analysis Details</h2>
      
      {/* Layer Scores Section - This is the main drill-down functionality */}
      {hasLayerScores && layerEntries.length > 0 && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-700 mb-4">Layer Analysis & Scores</h3>
          <div className="space-y-4">
            {layerEntries.map(([layerName, layerData]) => (
              <div key={layerName} className="border border-gray-200 rounded-lg">
                <div 
                  className="p-4 cursor-pointer hover:bg-gray-50 flex items-center justify-between"
                  onClick={() => toggleLayer(layerName)}
                >
                  <div className="flex items-center space-x-4">
                    <ProgressRing value={layerData.score} size={50} />
                    <div>
                      <h4 className="text-lg font-semibold text-gray-800">
                        {layerName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </h4>
                      <p className="text-sm text-gray-600">
                        Score: {layerData.score}/10 | Confidence: {Math.round(layerData.source_attribution.confidence * 100)}%
                      </p>
                    </div>
                  </div>
                  <div className="text-gray-400">
                    {expandedLayers.has(layerName) ? '▼' : '▶'}
                  </div>
                </div>
                
                {expandedLayers.has(layerName) && (
                  <div className="px-4 pb-4 border-t border-gray-200">
                    <div className="mt-4 space-y-4">
                      <div>
                        <h5 className="font-semibold text-gray-700 mb-2">Analysis Rationale</h5>
                        <div className="bg-gray-50 p-3 rounded text-sm text-gray-700 whitespace-pre-wrap">
                          {layerData.rationale}
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="bg-blue-50 p-3 rounded">
                          <h6 className="font-semibold text-blue-800 mb-1">Source Type</h6>
                          <p className="text-sm text-blue-700">{layerData.source_attribution.source_type}</p>
                        </div>
                        <div className="bg-green-50 p-3 rounded">
                          <h6 className="font-semibold text-green-800 mb-1">Methodology</h6>
                          <p className="text-sm text-green-700">{layerData.source_attribution.methodology}</p>
                        </div>
                        <div className="bg-purple-50 p-3 rounded">
                          <h6 className="font-semibold text-purple-800 mb-1">Timestamp</h6>
                          <p className="text-sm text-purple-700">
                            {new Date(layerData.timestamp).toLocaleString()}
                          </p>
                        </div>
                      </div>

                      <div className="flex justify-end">
                        <button
                          onClick={() => onDrillDown(layerName)}
                          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm"
                        >
                          View Detailed Analysis →
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Debug Section - Show what we actually have */}
      {!hasLayerScores && (
        <div className="mb-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <h3 className="text-lg font-semibold text-yellow-800 mb-2">Debug: Layer Scores Not Found</h3>
          <p className="text-sm text-yellow-700 mb-2">
            The detailed_analysis.layer_scores section is missing. Here's what we found:
          </p>
          <div className="text-xs bg-white p-2 rounded border">
            <p><strong>Has detailed_analysis:</strong> {!!data?.detailed_analysis}</p>
            <p><strong>detailed_analysis keys:</strong> {data?.detailed_analysis ? Object.keys(data.detailed_analysis).join(', ') : 'none'}</p>
            <p><strong>Data structure:</strong> {JSON.stringify(data, null, 2).substring(0, 1000)}...</p>
          </div>
        </div>
      )}

      {/* Progress Summary Section */}
      {data.progress_summary && (
        <div className="mb-8">
          <div 
            className="border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50"
            onClick={() => toggleSection('progress')}
          >
            <div className="p-4 flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-800">Progress Summary</h3>
              <div className="text-gray-400">
                {expandedSections.has('progress') ? '▼' : '▶'}
              </div>
            </div>
            
            {expandedSections.has('progress') && (
              <div className="px-4 pb-4 border-t border-gray-200">
                <div className="mt-4 space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                    <div className="bg-blue-50 p-4 rounded">
                      <div className="text-2xl font-bold text-blue-600">{data.progress_summary.completed_layers}</div>
                      <div className="text-sm text-blue-700">Completed Layers</div>
                    </div>
                    <div className="bg-green-50 p-4 rounded">
                      <div className="text-2xl font-bold text-green-600">{data.progress_summary.total_layers}</div>
                      <div className="text-sm text-blue-700">Total Layers</div>
                    </div>
                    <div className="bg-purple-50 p-4 rounded">
                      <div className="text-2xl font-bold text-purple-600">{data.progress_summary.current_phase}</div>
                      <div className="text-sm text-purple-700">Current Phase</div>
                    </div>
                  </div>
                  
                  {data.progress_summary.performance_metrics && (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="bg-yellow-50 p-3 rounded">
                        <h5 className="font-semibold text-yellow-800 mb-1">Average Score</h5>
                        <p className="text-sm text-yellow-700">{data.progress_summary.performance_metrics.average_score}/10</p>
                      </div>
                      <div className="bg-indigo-50 p-3 rounded">
                        <h5 className="font-semibold text-indigo-800 mb-1">Confidence Level</h5>
                        <p className="text-sm text-indigo-700">{Math.round(data.progress_summary.performance_metrics.confidence_level * 100)}%</p>
                      </div>
                      <div className="bg-pink-50 p-3 rounded">
                        <h5 className="font-semibold text-pink-800 mb-1">Quality Score</h5>
                        <p className="text-sm text-pink-700">{data.progress_summary.performance_metrics.quality_score}/10</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Strategic Insights Section */}
      {data.strategic_insights && (
        <div className="mb-8">
          <div 
            className="border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50"
            onClick={() => toggleSection('insights')}
          >
            <div className="p-4 flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-800">Strategic Insights</h3>
              <div className="text-gray-400">
                {expandedSections.has('insights') ? '▼' : '▶'}
              </div>
            </div>
            
            {expandedSections.has('insights') && (
              <div className="px-4 pb-4 border-t border-gray-200">
                <div className="mt-4 space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-semibold text-gray-700 mb-2">Key Findings</h4>
                      <ul className="list-disc list-inside space-y-1 text-gray-600">
                        {data.strategic_insights.key_findings?.map((finding, index) => (
                          <li key={index}>{finding}</li>
                        )) || <li>No key findings available</li>}
                      </ul>
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-700 mb-2">Market Opportunities</h4>
                      <ul className="list-disc list-inside space-y-1 text-gray-600">
                        {data.strategic_insights.market_opportunities?.map((opportunity, index) => (
                          <li key={index}>{opportunity}</li>
                        )) || <li>No market opportunities available</li>}
                      </ul>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-semibold text-gray-700 mb-2">Risk Factors</h4>
                      <ul className="list-disc list-inside space-y-1 text-gray-600">
                        {data.strategic_insights.risk_factors?.map((risk, index) => (
                          <li key={index}>{risk}</li>
                        )) || <li>No risk factors identified</li>}
                      </ul>
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-700 mb-2">Competitive Advantages</h4>
                      <ul className="list-disc list-inside space-y-1 text-gray-600">
                        {data.strategic_insights.competitive_advantages?.map((advantage, index) => (
                          <li key={index}>{advantage}</li>
                        )) || <li>No competitive advantages identified</li>}
                      </ul>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-700 mb-2">Strategic Recommendations</h4>
                    <ul className="list-disc list-inside space-y-1 text-gray-600">
                      {data.strategic_insights.strategic_recommendations?.map((rec, index) => (
                        <li key={index}>{rec}</li>
                      )) || <li>No strategic recommendations available</li>}
                    </ul>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-700 mb-2">Implementation Priorities</h4>
                    <ul className="list-disc list-inside space-y-1 text-gray-600">
                      {data.strategic_insights.implementation_priorities?.map((priority, index) => (
                        <li key={index}>{priority}</li>
                      )) || <li>No implementation priorities available</li>}
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Analysis Metadata Summary */}
      <div className="mt-8 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">Analysis Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-blue-600">{data.analysis_metadata?.total_layers_analyzed || 0}</div>
            <div className="text-sm text-gray-600">Total Layers</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600">{data.analysis_metadata?.segments_analyzed || 0}</div>
            <div className="text-sm text-gray-600">Segments</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-purple-600">{data.analysis_metadata?.factors_analyzed || 0}</div>
            <div className="text-sm text-gray-600">Factors</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-orange-600">{data.analysis_results?.overall_viability_score || 0}</div>
            <div className="text-sm text-gray-600">Viability Score</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SegmentsDashboard;
