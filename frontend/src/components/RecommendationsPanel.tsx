import React from 'react';
import { CheckCircleIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

interface Props {
  recommendations: string[];
  riskFactors: string[];
}

export const RecommendationsPanel: React.FC<Props> = ({ recommendations, riskFactors }) => {
  return (
    <div className="space-y-6">
      {/* Recommendations */}
      <div className="bg-white rounded-xl shadow-lg p-6 bg-green-50 border border-green-200">
        <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <CheckCircleIcon className="h-6 w-6 text-green-500 mr-2" />
          Strategic Recommendations
        </h4>
        <ul className="space-y-3">
          {recommendations.map((rec, index) => (
            <li key={index} className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-sm font-medium">
                {index + 1}
              </div>
              <span className="text-gray-700">{rec}</span>
            </li>
          ))}
        </ul>
      </div>
      
      {/* Risk Factors */}
      <div className="bg-white rounded-xl shadow-lg p-6 bg-red-50 border border-red-200">
        <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <ExclamationTriangleIcon className="h-6 w-6 text-red-500 mr-2" />
          Risk Factors
        </h4>
        <ul className="space-y-3">
          {riskFactors.map((risk, index) => (
            <li key={index} className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-red-100 text-red-600 rounded-full flex items-center justify-center text-sm font-medium">
                {index + 1}
              </div>
              <span className="text-gray-700">{risk}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
