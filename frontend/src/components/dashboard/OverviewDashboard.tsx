import React from 'react';
import { TransformedAnalysis } from '../../utils/dataTransformation';
import { ChartDataAdapters } from '../charts/ChartDataAdapters';
import { RadarChart } from '../charts/RadarChart';
import { ProgressRing } from '../charts/ProgressRing';
import { MetricCard } from '../charts/MetricCard';

interface OverviewDashboardProps {
  data: TransformedAnalysis;
}

const OverviewDashboard: React.FC<OverviewDashboardProps> = ({ data }) => {
  const segmentRadarData = ChartDataAdapters.prepareSegmentRadarData(data);
  const metaScoresData = ChartDataAdapters.prepareMetaScoresData(data);

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-4">Executive Summary & Overview</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="md:col-span-1 flex flex-col items-center justify-center">
          <ProgressRing value={data.overall_score} />
          <h3 className="text-lg font-semibold text-gray-600 mt-4">Overall Score</h3>
          <p className="text-sm text-gray-500">Confidence: {(data.overall_confidence * 100).toFixed(1)}%</p>
        </div>
        <div className="md:col-span-2">
          <RadarChart data={segmentRadarData} />
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8 text-center">
        <MetricCard title="Market Fit" value={data.meta_scores.market_fit} />
        <MetricCard title="Innovation" value={data.meta_scores.innovation_score} />
        <MetricCard title="Execution" value={data.meta_scores.execution_readiness} />
        <MetricCard title="Risk Index" value={data.meta_scores.risk_index} />
        <MetricCard title="Brand Strength" value={data.meta_scores.brand_strength} />
      </div>

      <div className="space-y-6">
        <div>
          <h4 className="text-xl font-semibold text-gray-700 mb-2">Executive Summary</h4>
          <p className="text-gray-600">{data.executive_summary}</p>
        </div>

        <div>
          <h4 className="text-xl font-semibold text-gray-700 mb-2">Key Recommendations</h4>
          <ul className="list-disc list-inside space-y-1 text-gray-600">
            {data.key_recommendations.map((recommendation, index) => (
              <li key={index}>{recommendation}</li>
            ))}
          </ul>
        </div>

        <div>
          <h4 className="text-xl font-semibold text-gray-700 mb-2">Competitive Advantages</h4>
          <ul className="list-disc list-inside space-y-1 text-gray-600">
            {data.competitive_advantages.map((advantage, index) => (
              <li key={index}>{advantage}</li>
            ))}
          </ul>
        </div>

        <div>
          <h4 className="text-xl font-semibold text-gray-700 mb-2">Risk Factors</h4>
          <ul className="list-disc list-inside space-y-1 text-gray-600">
            {data.risk_factors.map((risk, index) => (
              <li key={index}>{risk}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default OverviewDashboard;
