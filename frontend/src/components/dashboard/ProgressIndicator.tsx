import React from 'react';
import { AnalysisStatus } from '../../types/analysis';

interface ProgressIndicatorProps {
  status: AnalysisStatus;
  progress: number;
  estimatedCompletion?: string;
}

const statusConfig = {
  initiated: { label: 'Analysis Initiated', color: 'bg-blue-500' },
  parsing: { label: 'Parsing Query', color: 'bg-blue-500' },
  planning: { label: 'Planning Research', color: 'bg-blue-500' },
  researching: { label: 'Gathering Data', color: 'bg-yellow-500' },
  scoring: { label: 'Calculating Scores', color: 'bg-purple-500' },
  aggregating: { label: 'Aggregating Results', color: 'bg-purple-500' },
  summarizing: { label: 'Generating Insights', color: 'bg-green-500' },
  completed: { label: 'Analysis Complete', color: 'bg-green-500' },
  failed: { label: 'Analysis Failed', color: 'bg-red-500' }
};

export const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({ 
  status, 
  progress, 
  estimatedCompletion 
}) => {
  const config = statusConfig[status] || statusConfig.initiated;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Analysis Progress</h3>
        <span className={`px-3 py-1 rounded-full text-sm font-medium text-white ${config.color}`}>
          {config.label}
        </span>
      </div>

      <div className="mb-4">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>Progress</span>
          <span>{progress}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className={`h-2 rounded-full transition-all duration-500 ${config.color}`}
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {estimatedCompletion && status !== 'completed' && status !== 'failed' && (
        <div className="text-sm text-gray-600">
          <span className="font-medium">Estimated completion:</span> {estimatedCompletion}
        </div>
      )}

      {status === 'completed' && (
        <div className="text-sm text-green-600 font-medium">
          ✓ Analysis completed successfully!
        </div>
      )}

      {status === 'failed' && (
        <div className="text-sm text-red-600 font-medium">
          ✗ Analysis encountered an error. Please try again.
        </div>
      )}
    </div>
  );
};
