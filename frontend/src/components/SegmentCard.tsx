import React from 'react';
import { ArrowTrendingUpIcon, ArrowTrendingDownIcon, MinusIcon, StarIcon } from '@heroicons/react/24/outline';
import { SegmentScore } from '../types/pergola';
 
interface Props {
  segment: SegmentScore;
  segmentName: string;
  onClick?: () => void;
  isClickable?: boolean;
}
 
export const SegmentCard: React.FC<Props> = ({ 
  segment, 
  segmentName, 
  onClick, 
  isClickable = false 
}) => {
  const getTrendIcon = () => {
    switch (segment.trend) {
      case 'up':
        return <ArrowTrendingUpIcon className="h-5 w-5 text-green-500" />;
      case 'down':
        return <ArrowTrendingDownIcon className="h-5 w-5 text-red-500" />;
      default:
        return <MinusIcon className="h-5 w-5 text-gray-400" />;
    }
  };
 
  const getPriorityIcon = () => {
    switch (segment.priority) {
      case 'high':
        return <StarIcon className="h-4 w-4 text-red-500" />;
      case 'medium':
        return <StarIcon className="h-4 w-4 text-yellow-500" />;
      default:
        return <StarIcon className="h-4 w-4 text-gray-400" />;
    }
  };
 
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };
 
  const segmentDisplayName = segmentName.replace(/_/g, ' ').toUpperCase();
 
  return (
    <div 
      className={`bg-white rounded-xl shadow-lg p-6 border-2 transition-all duration-200 ${
        isClickable 
          ? 'cursor-pointer hover:shadow-xl hover:border-blue-300 hover:scale-105' 
          : 'border-transparent'
      }`}
      onClick={isClickable ? onClick : undefined}
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <h4 className="text-lg font-semibold text-gray-900">{segmentDisplayName}</h4>
          {getPriorityIcon()}
        </div>
        <div className="flex items-center space-x-2">
          {getTrendIcon()}
          <span className="text-sm text-gray-500 capitalize">{segment.trend}</span>
        </div>
      </div>
      
      <div className="mb-4">
        <div className={`text-3xl font-bold ${getScoreColor(segment.score)}`}>
          {Math.round(segment.score)}%
        </div>
        <div className="text-sm text-gray-600">Segment Score</div>
      </div>
      
      <div className="flex items-center justify-between text-sm">
        <span className="text-gray-500">
          Confidence: {Math.round(segment.confidence * 100)}%
        </span>
        <span className="text-gray-500">
          {Object.keys(segment.factors).length} factors
        </span>
      </div>
      
      {isClickable && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <div className="text-xs text-blue-600 font-medium">
            Click to drill down →
          </div>
        </div>
      )}
    </div>
  );
};
