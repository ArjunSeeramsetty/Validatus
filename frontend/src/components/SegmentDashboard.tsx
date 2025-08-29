import React from 'react';
import { motion } from 'framer-motion';
import { ArrowLeftIcon, ChartBarIcon } from '@heroicons/react/24/outline';

import { SegmentScore } from '../types/pergola';
import { FactorCard } from './FactorCard';
import { BarChart } from './charts/BarChart';
import { ProgressRing } from './charts/ProgressRing';
import { InsightsPanel } from './InsightsPanel';

interface Props {
  segment: SegmentScore;
  segmentName: string;
  onDrillDown: (level: 'factor', name: string) => void;
  onBack: () => void;
}

export const SegmentDashboard: React.FC<Props> = ({ 
  segment, 
  segmentName, 
  onDrillDown, 
  onBack 
}) => {
  const factorData = Object.entries(segment.factors).map(([name, factor]) => ({
    name: name.replace(/_/g, ' '),
    score: factor.score,
    confidence: factor.confidence
  }));

  const segmentDisplayName = segmentName.replace(/_/g, ' ').toUpperCase();

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl shadow-lg p-6"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={onBack}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <ArrowLeftIcon className="h-5 w-5 text-gray-600" />
            </button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                {segmentDisplayName} Analysis
              </h1>
              <p className="text-gray-600">Detailed factor breakdown and insights</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-6">
            <div className="text-center">
              <ProgressRing 
                percentage={Math.round(segment.score)} 
                size={80}
                strokeWidth={8}
                className="text-blue-600"
              />
              <div className="text-sm text-gray-600 mt-1">Segment Score</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {Math.round(segment.confidence * 100)}%
              </div>
              <div className="text-sm text-gray-600">Confidence</div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Factor Performance Chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white rounded-xl shadow-lg p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Factor Performance Overview</h3>
        <BarChart 
          data={factorData}
          height={300}
          onBarClick={(data) => onDrillDown('factor', Object.keys(segment.factors)[factorData.findIndex(f => f.name === data.name)])}
        />
      </motion.div>

      {/* Factor Cards Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <ChartBarIcon className="h-5 w-5 text-blue-600 mr-2" />
            Factor Details
          </h3>
          <div className="space-y-4">
            {Object.entries(segment.factors).map(([factorName, factor], index) => (
              <motion.div
                key={factorName}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 + index * 0.1 }}
              >
                <FactorCard
                  factor={factor}
                  factorName={factorName}
                  onClick={() => onDrillDown('factor', factorName)}
                  isClickable={true}
                />
              </motion.div>
            ))}
          </div>
        </div>

        <div className="space-y-6">
          <InsightsPanel
            title={`${segmentDisplayName} Key Insights`}
            insights={segment.key_insights}
          />
          
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h4 className="text-lg font-semibold text-gray-900 mb-4">Strategic Recommendations</h4>
            <ul className="space-y-3">
              {segment.recommendations.map((rec, index) => (
                <li key={index} className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-medium">
                    {index + 1}
                  </div>
                  <span className="text-gray-700">{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
