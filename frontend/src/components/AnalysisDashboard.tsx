import React, { useState, useEffect } from 'react';
import { RadarChart } from './charts/RadarChart';
import { MetricCard } from './charts/MetricCard';
import { ProgressRing } from './charts/ProgressRing';
import { LoadingSpinner } from './LoadingSpinner';

interface AnalysisData {
  [key: string]: any;
}

interface TransformedSegment {
  name: string;
  score: number;
  confidence: number;
  trend: "up" | "down" | "stable";
  priority: string;
  key_insights: string[];
  recommendations: string[];
  factors: Record<string, TransformedFactor>;
}

interface TransformedFactor {
  name: string;
  score: number;
  confidence: number;
  summary: string;
  key_insights: string[];
  recommendations: string[];
  layers: Record<string, TransformedLayer>;
  trend: "up" | "down" | "stable";
}

interface TransformedLayer {
  name: string;
  score: number;
  confidence: number;
  calculation_method: string;
  supporting_data: Record<string, any>;
  data_sources: string[];
  summary: string;
  trend: "up" | "down" | "stable";
}

interface TransformedData {
  query: string;
  overall_score: number;
  overall_confidence: number;
  segments: Record<string, TransformedSegment>;
  meta_scores: Record<string, number>;
  executive_summary: string;
  key_recommendations: string[];
  competitive_advantages: string[];
  risk_factors: string[];
  generated_at: string;
}

interface AnalysisDashboardProps {
  analysisData: AnalysisData;
  onGoHome: () => void;
}

interface DrillDownState {
  level: 'overview' | 'segment' | 'factor' | 'layer';
  segmentName?: string;
  factorName?: string;
  layerName?: string;
}

export const AnalysisDashboard: React.FC<AnalysisDashboardProps> = ({ 
  analysisData, 
  onGoHome 
}) => {
  const [drillDownState, setDrillDownState] = useState<DrillDownState>({ level: 'overview' });
  const [transformedData, setTransformedData] = useState<TransformedData | null>(null);

  useEffect(() => {
    // Transform the analysis data to a standardized format
    const transformData = (data: AnalysisData): TransformedData => {
      console.log('Transforming analysis data:', data);
      
      // Extract the actual analysis results from the backend format
      const analysisResults = data.analysis_results || data.strategic_analysis || data;
      
      // Create a standardized structure - ONLY use what's in the JSON
      const transformed: TransformedData = {
        query: data.business_case?.idea_description || "Strategic analysis for business case",
        overall_score: analysisResults.overall_score || 0,
        overall_confidence: analysisResults.overall_confidence || 0,
        segments: {},
        meta_scores: analysisResults.meta_scores || {},
        executive_summary: analysisResults.executive_summary || "",
        key_recommendations: analysisResults.key_recommendations || [],
        competitive_advantages: analysisResults.competitive_advantages || [],
        risk_factors: analysisResults.risk_factors || [],
        generated_at: data.analysis_metadata?.timestamp || new Date().toISOString()
      };

      // Transform segments - they are directly in analysis_results, not nested under "segments"
      // Look for segment keys like "CONSUMER", "MARKET", "TECHNOLOGY", etc.
      if (analysisResults) {
        const segmentKeys = Object.keys(analysisResults).filter(key => 
          ['CONSUMER', 'MARKET', 'TECHNOLOGY', 'FINANCIAL', 'COMPETITIVE'].includes(key) ||
          (typeof analysisResults[key] === 'object' && analysisResults[key] !== null && 
           analysisResults[key].score !== undefined)
        );

        segmentKeys.forEach(segmentName => {
          const segmentData = analysisResults[segmentName];
          if (segmentData && typeof segmentData === 'object') {
            transformed.segments[segmentName] = {
              name: segmentName,
              score: segmentData.score || 0,
              confidence: segmentData.confidence || 0,
              trend: segmentData.trend || "stable",
              priority: segmentData.priority || "medium",
              key_insights: segmentData.key_insights || [],
              recommendations: segmentData.recommendations || [],
              factors: {}
            };

            // Transform factors - they are directly in the segment data
            if (segmentData.factors) {
              Object.entries(segmentData.factors).forEach(([factorName, factorData]: [string, any]) => {
                transformed.segments[segmentName].factors[factorName] = {
                  name: factorName,
                  score: factorData.score || 0,
                  confidence: factorData.confidence || 0,
                  summary: factorData.summary || "",
                  key_insights: factorData.key_insights || [],
                  recommendations: factorData.recommendations || [],
                  layers: {},
                  trend: factorData.trend || "stable"
                };

                // Transform layers - they are directly in the factor data
                if (factorData.layers) {
                  Object.entries(factorData.layers).forEach(([layerName, layerData]: [string, any]) => {
                    transformed.segments[segmentName].factors[factorName].layers[layerName] = {
                      name: layerName,
                      score: layerData.score || 0,
                      confidence: layerData.confidence || 0,
                      calculation_method: layerData.calculation_method || "",
                      supporting_data: layerData.supporting_data || {},
                      data_sources: layerData.data_sources || [],
                      summary: layerData.summary || "",
                      trend: layerData.trend || "stable"
                    };
                  });
                }
              });
            }
          }
        });
      }

      // NO FALLBACK LOGIC - only show what's actually in the JSON
      console.log('Transformation complete. Transformed data:', transformed);
      console.log('Found segments:', Object.keys(transformed.segments));
      return transformed;
    };

    setTransformedData(transformData(analysisData));
  }, [analysisData]);

  if (!transformedData) {
    return <LoadingSpinner message="Processing analysis data..." />;
  }

  const handleDrillDown = (level: DrillDownState['level'], segmentName?: string, factorName?: string, layerName?: string) => {
    setDrillDownState({ level, segmentName, factorName, layerName });
  };

  const renderOverview = () => (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Strategic Analysis Overview</h1>
        <p className="text-gray-600">{transformedData.query}</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <MetricCard
          title="Overall Score"
          value={transformedData.overall_score}
          unit="%"
          trend="up"
        />
        <MetricCard
          title="Confidence"
          value={Math.round(transformedData.overall_confidence * 100)}
          unit="%"
          trend="stable"
        />
        <MetricCard
          title="Segments Analyzed"
          value={Object.keys(transformedData.segments).length}
          trend="stable"
        />
        <MetricCard
          title="Analysis Date"
          value={new Date(transformedData.generated_at).getTime()}
          trend="stable"
        />
      </div>

      {/* Meta Scores - only if they exist */}
      {Object.keys(transformedData.meta_scores).length > 0 && (
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Strategic Metrics</h2>
          <RadarChart 
            data={Object.entries(transformedData.meta_scores).map(([name, value]) => ({ 
              name, 
              score: value,
              confidence: 0.8 
            }))} 
            width={400}
            height={400}
          />
        </div>
      )}

      {/* Executive Summary - only if it exists */}
      {transformedData.executive_summary && (
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Executive Summary</h2>
          <p className="text-gray-800">{transformedData.executive_summary}</p>
        </div>
      )}

      {/* Key Recommendations - only if they exist */}
      {transformedData.key_recommendations.length > 0 && (
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Key Recommendations</h2>
          <ul className="list-disc list-inside text-gray-700 space-y-2">
            {transformedData.key_recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Segments Grid - only if segments exist */}
      {Object.keys(transformedData.segments).length > 0 ? (
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Analysis Segments</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Object.entries(transformedData.segments).map(([name, segment]: [string, TransformedSegment]) => (
              <div
                key={name}
                className="bg-white rounded-lg shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow"
                onClick={() => handleDrillDown('segment', name)}
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">{name}</h3>
                  <ProgressRing value={segment.score} size={60} />
                </div>
                <p className="text-sm text-gray-600 mb-3">
                  {segment.key_insights?.[0] || 'No insights available'}
                </p>
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    segment.trend === 'up' ? 'bg-green-100 text-green-800' :
                    segment.trend === 'down' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {segment.trend}
                  </span>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    segment.priority === 'high' ? 'bg-red-100 text-red-800' :
                    segment.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {segment.priority}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center py-8">
          <p className="text-gray-500">No segments found in the analysis data.</p>
          <p className="text-sm text-gray-400 mt-2">Please check the console for debugging information.</p>
        </div>
      )}
    </div>
  );

  const renderSegment = () => {
    if (!drillDownState.segmentName || !transformedData.segments[drillDownState.segmentName]) {
      return <div>Segment not found</div>;
    }

    const segment = transformedData.segments[drillDownState.segmentName];
    
    return (
      <div className="p-6">
        <div className="mb-6">
          <button
            onClick={() => handleDrillDown('overview')}
            className="text-blue-600 hover:text-blue-800 mb-4"
          >
            ← Back to Overview
          </button>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{segment.name} Segment</h1>
          <div className="flex items-center space-x-4">
            <ProgressRing value={segment.score} size={80} />
            <div>
              <p className="text-lg text-gray-600">Score: {segment.score}%</p>
              <p className="text-sm text-gray-500">Confidence: {Math.round(segment.confidence * 100)}%</p>
            </div>
          </div>
        </div>

        {/* Key Insights - only if they exist */}
        {segment.key_insights.length > 0 && (
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Key Insights</h3>
            <ul className="list-disc list-inside text-gray-700 space-y-2">
              {segment.key_insights.map((insight, index) => (
                <li key={index}>{insight}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommendations - only if they exist */}
        {segment.recommendations.length > 0 && (
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Recommendations</h3>
            <ul className="list-disc list-inside text-gray-700 space-y-2">
              {segment.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Factors Grid - only if factors exist */}
        {Object.keys(segment.factors).length > 0 ? (
          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Factors</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Object.entries(segment.factors).map(([name, factor]: [string, TransformedFactor]) => (
                <div
                  key={name}
                  className="bg-white rounded-lg shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => handleDrillDown('factor', drillDownState.segmentName, name)}
                >
                  <h4 className="text-lg font-semibold text-gray-900 mb-3">{name}</h4>
                  <ProgressRing value={factor.score} size={60} />
                  <p className="text-sm text-gray-600 mt-3">{factor.summary || 'No summary available'}</p>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="text-center py-4">
            <p className="text-gray-500">No factors found for this segment.</p>
          </div>
        )}
      </div>
    );
  };

  const renderFactor = () => {
    if (!drillDownState.segmentName || !drillDownState.factorName) {
      return <div>Factor not found</div>;
    }

    const factor = transformedData.segments[drillDownState.segmentName].factors[drillDownState.factorName];
    
    return (
      <div className="p-6">
        <div className="mb-6">
          <button
            onClick={() => handleDrillDown('segment', drillDownState.segmentName)}
            className="text-blue-600 hover:text-blue-800 mb-4"
          >
            ← Back to {drillDownState.segmentName} Segment
          </button>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{factor.name}</h1>
          <div className="flex items-center space-x-4">
            <ProgressRing value={factor.score} size={80} />
            <div>
              <p className="text-lg text-gray-600">Score: {factor.score}%</p>
              <p className="text-sm text-gray-500">Confidence: {Math.round(factor.confidence * 100)}%</p>
            </div>
          </div>
        </div>

        {/* Key Insights - only if they exist */}
        {factor.key_insights.length > 0 && (
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Key Insights</h3>
            <ul className="list-disc list-inside text-gray-700 space-y-2">
              {factor.key_insights.map((insight, index) => (
                <li key={index}>{insight}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommendations - only if they exist */}
        {factor.recommendations.length > 0 && (
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Recommendations</h3>
            <ul className="list-disc list-inside text-gray-700 space-y-2">
              {factor.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Layers Grid - only if layers exist */}
        {Object.keys(factor.layers).length > 0 ? (
          <div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Layers</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {Object.entries(factor.layers).map(([name, layer]: [string, TransformedLayer]) => (
                <div
                  key={name}
                  className="bg-white rounded-lg shadow-sm p-6 cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => handleDrillDown('layer', drillDownState.segmentName, drillDownState.factorName, name)}
                >
                  <h4 className="text-lg font-semibold text-gray-900 mb-3">{name}</h4>
                  <ProgressRing value={layer.score} size={60} />
                  <p className="text-sm text-gray-600 mt-3">{layer.summary || 'No summary available'}</p>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="text-center py-4">
            <p className="text-gray-500">No layers found for this factor.</p>
          </div>
        )}
      </div>
    );
  };

  const renderLayer = () => {
    if (!drillDownState.segmentName || !drillDownState.factorName || !drillDownState.layerName) {
      return <div>Layer not found</div>;
    }

    const layer = transformedData.segments[drillDownState.segmentName]
      .factors[drillDownState.factorName].layers[drillDownState.layerName];
    
    return (
      <div className="p-6">
        <div className="mb-6">
          <button
            onClick={() => handleDrillDown('factor', drillDownState.segmentName, drillDownState.factorName)}
            className="text-blue-600 hover:text-blue-800 mb-4"
          >
            ← Back to {drillDownState.factorName}
          </button>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{layer.name}</h1>
          <div className="flex items-center space-x-4">
            <ProgressRing value={layer.score} size={80} />
            <div>
              <p className="text-lg text-gray-600">Score: {layer.score}%</p>
              <p className="text-sm text-gray-500">Confidence: {Math.round(layer.confidence * 100)}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          {/* Summary - only if it exists */}
          {layer.summary && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Summary</h3>
              <p className="text-gray-600 mb-4">{layer.summary}</p>
            </div>
          )}
          
          {/* Calculation Method - only if it exists */}
          {layer.calculation_method && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Calculation Method</h3>
              <p className="text-gray-600 mb-4">{layer.calculation_method}</p>
            </div>
          )}
          
          {/* Data Sources - only if they exist */}
          {layer.data_sources.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Data Sources</h3>
              <ul className="list-disc list-inside text-gray-600 mb-4">
                {layer.data_sources.map((source: string, index: number) => (
                  <li key={index}>{source}</li>
                ))}
              </ul>
            </div>
          )}
          
          {/* Supporting Data - only if it exists */}
          {layer.supporting_data && Object.keys(layer.supporting_data).length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Supporting Data</h3>
              <pre className="bg-gray-50 p-4 rounded text-sm overflow-auto">
                {JSON.stringify(layer.supporting_data, null, 2)}
              </pre>
            </div>
          )}
        </div>
      </div>
    );
  };

  const renderContent = () => {
    switch (drillDownState.level) {
      case 'segment':
        return renderSegment();
      case 'factor':
        return renderFactor();
      case 'layer':
        return renderLayer();
      default:
        return renderOverview();
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

      {/* Breadcrumb */}
      <div className="bg-white shadow-sm border-b px-6 py-3">
        <div className="flex items-center space-x-2 text-sm text-gray-600">
          <span
            className="cursor-pointer hover:text-blue-600"
            onClick={() => handleDrillDown('overview')}
          >
            Overview
          </span>
          {drillDownState.segmentName && (
            <>
              <span>→</span>
              <span
                className="cursor-pointer hover:text-blue-600"
                onClick={() => handleDrillDown('segment', drillDownState.segmentName)}
              >
                {drillDownState.segmentName}
              </span>
            </>
          )}
          {drillDownState.factorName && (
            <>
              <span>→</span>
              <span
                className="cursor-pointer hover:text-blue-600"
                onClick={() => handleDrillDown('factor', drillDownState.segmentName, drillDownState.factorName)}
              >
                {drillDownState.factorName}
              </span>
            </>
          )}
          {drillDownState.layerName && (
            <>
              <span>→</span>
              <span className="text-gray-900">{drillDownState.layerName}</span>
            </>
          )}
        </div>
      </div>

      {/* Main Content */}
      {renderContent()}
    </div>
  );
};
