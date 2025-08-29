import React from 'react';
import { ArrowTrendingUpIcon, ArrowTrendingDownIcon, MinusIcon } from '@heroicons/react/24/outline';
 
interface Props {
  overallScore: number;
  trend: 'positive' | 'negative';
  confidence: number;
}
 
export const PerformanceIndicators: React.FC<Props> = ({ overallScore, trend, confidence }) => {
  const getTrendIcon = () => {
    switch (trend) {
      case 'positive':
        return <ArrowTrendingUpIcon className="h-5 w-5 text-green-500" />;
      case 'negative':
        return <ArrowTrendingDownIcon className="h-5 w-5 text-red-500" />;
      default:
        return <MinusIcon className="h-5 w-5 text-gray-400" />;
    }
  };
 
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };
 
  return (
    <div className="flex items-center space-x-6">
      <div className="text-center">
        <div className={`text-2xl font-bold ${getScoreColor(overallScore)}`}>
          {Math.round(overallScore)}%
        </div>
        <div className="text-sm text-gray-500">Overall Score</div>
      </div>
      
      <div className="text-center">
        <div className="text-2xl font-bold text-gray-900">
          {Math.round(confidence * 100)}%
        </div>
        <div className="text-sm text-gray-500">Confidence</div>
      </div>
      
      <div className="flex items-center space-x-2 text-sm">
        {getTrendIcon()}
        <span className={`font-medium capitalize ${
          trend === 'positive' ? 'text-green-600' : 'text-red-600'
        }`}>
          {trend} trend
        </span>
      </div>
    </div>
  );
};
