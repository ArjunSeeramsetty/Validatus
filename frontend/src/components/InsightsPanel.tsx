import React from 'react';
import { LightBulbIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

interface Props {
  title?: string;
  insights: string[];
  type?: 'insights' | 'warnings';
}

export const InsightsPanel: React.FC<Props> = ({ 
  title = "Key Insights", 
  insights, 
  type = 'insights' 
}) => {
  const Icon = type === 'warnings' ? ExclamationTriangleIcon : LightBulbIcon;
  const iconColor = type === 'warnings' ? 'text-red-500' : 'text-yellow-500';
  const bgColor = type === 'warnings' ? 'bg-red-50' : 'bg-yellow-50';
  const borderColor = type === 'warnings' ? 'border-red-200' : 'border-yellow-200';

  return (
    <div className={`bg-white rounded-xl shadow-lg p-6 ${bgColor} border ${borderColor}`}>
      <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <Icon className={`h-6 w-6 ${iconColor} mr-2`} />
        {title}
      </h4>
      <ul className="space-y-3">
        {insights.map((insight, index) => (
          <li key={index} className="flex items-start space-x-3">
            <div className={`flex-shrink-0 w-6 h-6 ${bgColor} ${iconColor} rounded-full flex items-center justify-center text-sm font-medium`}>
              {index + 1}
            </div>
            <span className="text-gray-700 leading-relaxed">{insight}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};
