import React from 'react';
import { ArrowTrendingUpIcon, ArrowTrendingDownIcon, MinusIcon, ChartBarIcon } from '@heroicons/react/24/outline';
import { FactorScore } from '../types/pergola';
 
interface Props {
  factor: FactorScore;
  factorName: string;
  onClick?: () => void;
  isClickable?: boolean;
}
 
export const FactorCard: React.FC<Props> = ({ 
  factor, 
  factorName, 
  onClick, 
  isClickable = false 
}) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };
 
  const factorDisplayName = factorName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
 
  return (
    <div 
      className={`bg-white rounded-lg shadow-md p-4 border-2 transition-all duration-200 ${
        isClickable 
          ? 'cursor-pointer hover:shadow-lg hover:border-blue-300 hover:scale-102' 
          : 'border-transparent'
      }`}
      onClick={isClickable ? onClick : undefined}
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <ChartBarIcon className="h-5 w-5 text-blue-600" />
          <h5 className="text-md font-semibold text-gray-900">{factorDisplayName}</h5>
        </div>
        <div className="text-sm text-gray-500">
          {Object.keys(factor.layers).length} layers
        </div>
      </div>
      
      <div className="mb-3">
        <div className={`text-2xl font-bold ${getScoreColor(factor.score)}`}>
          {Math.round(factor.score)}%
        </div>
        <div className="text-sm text-gray-600">Factor Score</div>
      </div>
      
      <div className="flex items-center justify-between text-sm">
        <span className="text-gray-500">
          Confidence: {Math.round(factor.confidence * 100)}%
        </span>
      </div>
      
      {isClickable && (
        <div className="mt-3 pt-3 border-t border-gray-100">
          <div className="text-xs text-blue-600 font-medium">
            Click to drill down →
          </div>
        </div>
      )}
    </div>
  );
};
