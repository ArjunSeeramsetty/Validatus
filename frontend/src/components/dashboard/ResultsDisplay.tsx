import React from 'react';
import { DashboardData } from '../../types/analysis';
import { ScoreChart } from '../charts/ScoreChart';
import { RadarChartComponent } from '../charts/RadarChart';

interface ResultsDisplayProps {
  data: DashboardData;
}

export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ data }) => {
  const segmentChartData = Object.entries(data.segment_scores).map(([segment, score]) => ({
    name: segment.charAt(0).toUpperCase() + segment.slice(1).replace('_', ' '),
    score: score.score,
    confidence: score.confidence
  }));

  const factorChartData = Object.entries(data.factor_scores).map(([factor, factorScores]) => {
    // Calculate average score for this factor across all segments
    const scores = Object.values(factorScores).map(s => s.score);
    const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
    const avgConfidence = Object.values(factorScores).reduce((a, b) => a + b.confidence, 0) / scores.length;
    
    return {
      name: factor.charAt(0).toUpperCase() + factor.slice(1).replace('_', ' '),
      score: avgScore,
      confidence: avgConfidence
    };
  });

  return (
    <div className="space-y-6">
      {/* Strategic Overview */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Strategic Overview</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(data.segment_scores).map(([segment, score]) => (
            <div key={segment} className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {score.score.toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600 capitalize">
                {segment.replace('_', ' ')}
              </div>
              <div className="text-xs text-gray-500">
                Confidence: {(score.confidence * 100).toFixed(0)}%
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Segment Scores Chart */}
      <ScoreChart
        data={segmentChartData}
        title="Strategic Segment Scores"
        color="#3B82F6"
      />

      {/* Factor Scores Chart */}
      <ScoreChart
        data={factorChartData}
        title="Factor-Level Scores"
        color="#10B981"
      />

      {/* Radar Chart */}
      <RadarChartComponent
        data={Object.entries(data.segment_scores).map(([segment, score]) => ({
          segment: segment.charAt(0).toUpperCase() + segment.slice(1).replace('_', ' '),
          score: score.score,
          confidence: score.confidence
        }))}
        title="Strategic Positioning Radar"
      />

      {/* Detailed Factor Analysis */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Detailed Factor Analysis</h3>
        <div className="space-y-4">
          {Object.entries(data.factor_scores).map(([factor, factorScores]) => {
            // Calculate average score for this factor across all segments
            const scores = Object.values(factorScores).map(s => s.score);
            const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
            const avgConfidence = Object.values(factorScores).reduce((a, b) => a + b.confidence, 0) / scores.length;
            const summaries = Object.values(factorScores).map(s => s.summary);
            const avgSummary = summaries.length > 0 ? summaries[0] : 'No summary available';
            
            return (
              <div key={factor} className="border-l-4 border-blue-500 pl-4">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-medium text-gray-900 capitalize">
                    {factor.replace('_', ' ')}
                  </h4>
                  <div className="text-right">
                    <div className="text-lg font-semibold text-blue-600">
                      {avgScore.toFixed(1)}%
                    </div>
                    <div className="text-sm text-gray-500">
                      {(avgConfidence * 100).toFixed(0)}% confidence
                    </div>
                  </div>
                </div>
                <p className="text-gray-600 text-sm">{avgSummary}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recommendations */}
      {data.recommendations && data.recommendations.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Strategic Recommendations</h3>
          <div className="space-y-3">
            {data.recommendations.map((recommendation, index) => (
              <div key={index} className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
                <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
                  {index + 1}
                </div>
                <p className="text-gray-700">{recommendation}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
