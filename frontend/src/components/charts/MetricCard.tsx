import React from 'react';
import { ArrowTrendingUpIcon, ArrowTrendingDownIcon, MinusIcon } from '@heroicons/react/24/outline';

interface Props {
  title: string;
  value: number;
  unit?: string;
  icon?: React.ComponentType<any>;
  trend?: 'up' | 'down' | 'stable';
  className?: string;
}

export const MetricCard: React.FC<Props> = ({ 
  title, 
  value, 
  unit = '', 
  icon: Icon, 
  trend = 'stable',
  className = '' 
}) => {
  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <ArrowTrendingUpIcon className="h-5 w-5 text-green-500" />;
      case 'down':
        return <ArrowTrendingDownIcon className="h-5 w-5 text-red-500" />;
      default:
        return <MinusIcon className="h-5 w-5 text-gray-400" />;
    }
  };

  const getTrendColor = () => {
    switch (trend) {
      case 'up':
        return 'text-green-600';
      case 'down':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className={`bg-white rounded-xl shadow-lg p-6 ${className}`}>
      <div className="flex items-center justify-between mb-4">
        {Icon && <Icon className="h-6 w-6 text-blue-600" />}
        <div className={`flex items-center space-x-2 ${getTrendColor()}`}>
          {getTrendIcon()}
          <span className="text-sm font-medium capitalize">{trend}</span>
        </div>
      </div>
      
      <div className="mb-2">
        <div className="text-3xl font-bold text-gray-900">
          {value}{unit}
        </div>
        <div className="text-sm text-gray-600">{title}</div>
      </div>
    </div>
  );
};
