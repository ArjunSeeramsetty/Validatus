import React from 'react';
import { AnalysisResult } from '../../types/analysis';
import { RadarChart } from '../charts/RadarChart';
import { ProgressRing } from '../charts/ProgressRing';
import { MetricCard } from '../charts/MetricCard';

interface OverviewDashboardProps {
  data: AnalysisResult;
}

const OverviewDashboard: React.FC<OverviewDashboardProps> = ({ data }) => {
  // Add debugging and null checks
  console.log('OverviewDashboard received data:', data);
  
  // Check if data has the expected structure
  if (!data) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-4">Executive Summary & Overview</h2>
        <p className="text-red-600">No data available</p>
      </div>
    );
  }

  const { analysis_results, business_case, analysis_metadata, progress_summary, strategic_insights, detailed_analysis } = data;

  // Check if we have the data we need
  if (!analysis_results) {
    console.warn('analysis_results not found in data:', data);
    return (
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-4">Executive Summary & Overview</h2>
        <p className="text-red-600">Analysis data structure is incomplete. Missing analysis_results</p>
        <pre className="mt-4 p-4 bg-gray-100 rounded text-sm overflow-auto">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    );
  }

  // Create radar chart data from available data
  // First try to use detailed_analysis.layer_scores, fallback to progress_summary
  let radarChartData: Array<{name: string, score: number, confidence: number}> = [];
  
  if (data.detailed_analysis?.layer_scores) {
    // Use actual layer scores for the radar chart
    radarChartData = Object.entries(data.detailed_analysis.layer_scores).slice(0, 8).map(([layerName, layerData]) => ({
      name: layerName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      score: layerData.score,
      confidence: layerData.source_attribution.confidence
    }));
  } else if (progress_summary) {
    // Fallback to progress summary data
    radarChartData = [
      {
        name: 'Average Score',
        score: progress_summary.performance_metrics?.average_score || 0,
        confidence: progress_summary.performance_metrics?.confidence_level || 0
      },
      {
        name: 'Quality Score',
        score: progress_summary.performance_metrics?.quality_score || 0,
        confidence: progress_summary.performance_metrics?.confidence_level || 0
      }
    ];
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-4">Executive Summary & Overview</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="md:col-span-1 flex flex-col items-center justify-center">
          <ProgressRing value={analysis_results?.overall_viability_score || 0} size={120} />
          <h3 className="text-lg font-semibold text-gray-600 mt-4">
            Overall Viability Score: {analysis_results?.overall_viability_score || 0}/10
          </h3>
          <p className="text-sm text-gray-500">Risk Level: {analysis_results?.risk_assessment?.risk_level || 'Unknown'}</p>
        </div>

        <div className="md:col-span-2">
          {radarChartData.length > 0 ? (
            <RadarChart 
              data={radarChartData} 
              width={400}
              height={400}
            />
          ) : (
            <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg">
              <p className="text-gray-500">Performance metrics chart</p>
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8 text-center">
        <MetricCard 
          title="Segments Analyzed" 
          value={analysis_metadata?.segments_analyzed || 0} 
          trend="stable"
        />
        <MetricCard 
          title="Layers Analyzed" 
          value={analysis_metadata?.total_layers_analyzed || 0} 
          trend="stable"
        />
        <MetricCard 
          title="Factors Analyzed" 
          value={analysis_metadata?.factors_analyzed || 0} 
          trend="stable"
        />
        <MetricCard 
          title="Analysis Duration" 
          value={analysis_metadata?.duration ? parseInt(analysis_metadata.duration.split('.')[0]) || 0 : 0} 
          trend="stable"
        />
      </div>

      <div className="space-y-6">
        <div>
          <h4 className="text-xl font-semibold text-gray-700 mb-2">Key Insights</h4>
          <ul className="list-disc list-inside space-y-1 text-gray-600">
            {analysis_results?.analysis_summary?.key_insights?.map((insight, index) => (
              <li key={index}>{insight}</li>
            )) || <li>No key insights available</li>}
          </ul>
        </div>
        
        <div>
          <h4 className="text-xl font-semibold text-gray-700 mb-2">Strategic Recommendations</h4>
          {analysis_results?.recommendations?.map((rec, index) => (
            <div key={index} className="p-4 bg-gray-50 rounded-lg mb-3">
              <p className="font-semibold text-gray-800">{rec}</p>
            </div>
          )) || <p className="text-gray-500">No strategic recommendations available</p>}
        </div>

        <div>
          <h4 className="text-xl font-semibold text-gray-700 mb-2">Risk Assessment</h4>
          <div className="p-4 bg-red-50 rounded-lg">
            <p className="text-gray-800 mb-2">Risk Level: <span className="font-semibold">{analysis_results?.risk_assessment?.risk_level || 'Unknown'}</span></p>
            {analysis_results?.risk_assessment?.critical_areas?.length > 0 && (
              <div className="mt-2">
                <p className="text-sm text-gray-600 font-semibold">Critical Areas:</p>
                <ul className="list-disc list-inside text-sm text-gray-600">
                  {analysis_results.risk_assessment.critical_areas.map((area, index) => (
                    <li key={index}>{area}</li>
                  ))}
                </ul>
              </div>
            )}
            {analysis_results?.risk_assessment?.strength_areas?.length > 0 && (
              <div className="mt-2">
                <p className="text-sm text-gray-600 font-semibold">Strength Areas:</p>
                <ul className="list-disc list-inside text-sm text-gray-600">
                  {analysis_results.risk_assessment.strength_areas.map((area, index) => (
                    <li key={index}>{area}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>

        <div>
          <h4 className="text-xl font-semibold text-gray-700 mb-2">Business Case</h4>
          <div className="p-4 bg-blue-50 rounded-lg">
            <p className="text-gray-800 mb-2">{business_case?.idea_description || 'No business case description available'}</p>
            <p className="text-sm text-gray-600">Target Audience: {business_case?.target_audience || 'Not specified'}</p>
            <div className="mt-2">
              <p className="text-sm text-gray-600">Industry: {business_case?.additional_context?.industry || 'Not specified'}</p>
              <p className="text-sm text-gray-600">Product Category: {business_case?.additional_context?.product_category || 'Not specified'}</p>
            </div>
          </div>
        </div>

        {strategic_insights && (
          <div>
            <h4 className="text-xl font-semibold text-gray-700 mb-2">Strategic Insights</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h5 className="font-semibold text-gray-800 mb-2">Key Findings</h5>
                <ul className="list-disc list-inside space-y-1 text-gray-600">
                  {strategic_insights.key_findings?.map((finding, index) => (
                    <li key={index}>{finding}</li>
                  )) || <li>No key findings available</li>}
                </ul>
              </div>
              <div>
                <h5 className="font-semibold text-gray-800 mb-2">Market Opportunities</h5>
                <ul className="list-disc list-inside space-y-1 text-gray-600">
                  {strategic_insights.market_opportunities?.map((opportunity, index) => (
                    <li key={index}>{opportunity}</li>
                  )) || <li>No market opportunities available</li>}
                </ul>
              </div>
            </div>
          </div>
        )}

        {progress_summary && (
          <div>
            <h4 className="text-xl font-semibold text-gray-700 mb-2">Progress Summary</h4>
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-green-600">{progress_summary.completed_layers}</div>
                  <div className="text-sm text-gray-600">Completed Layers</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-blue-600">{progress_summary.total_layers}</div>
                  <div className="text-sm text-gray-600">Total Layers</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-purple-600">{progress_summary.current_phase}</div>
                  <div className="text-sm text-gray-600">Current Phase</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default OverviewDashboard;
