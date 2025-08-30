import React from 'react';
import { AnalysisStatus } from '../../types/analysis';

interface ProgressIndicatorProps {
  status: AnalysisStatus;
  progress: number;
}

const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({ status, progress }) => {
  const statusConfig: Record<AnalysisStatus, { label: string; color: string }> = {
    initiated: { label: 'Analysis Initiated', color: 'bg-blue-500' },
    parsing: { label: 'Parsing Request', color: 'bg-blue-500' },
    planning: { label: 'Planning Analysis', color: 'bg-yellow-500' },
    researching: { label: 'Researching', color: 'bg-yellow-500' },
    scoring: { label: 'Scoring Factors', color: 'bg-purple-500' },
    aggregating: { label: 'Aggregating Results', color: 'bg-purple-500' },
    summarizing: { label: 'Generating Summary', color: 'bg-green-500' },
    completed: { label: 'Analysis Complete', color: 'bg-green-500' },
    failed: { label: 'Analysis Failed', color: 'bg-red-500' }
  };

  const config = statusConfig[status] || statusConfig.initiated;

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">Analysis Progress</h3>
        <span className={`px-3 py-1 rounded-full text-sm font-medium text-white ${config.color}`}>
          {config.label}
        </span>
      </div>
      
      <div className="mb-4">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>Progress</span>
          <span>{Math.round(progress)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className={`h-2 rounded-full transition-all duration-500 ${config.color}`}
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>
      
      <div className="text-sm text-gray-600">
        {status === 'completed' && 'Your analysis is ready! Check the results below.'}
        {status === 'failed' && 'Analysis encountered an error. Please try again.'}
        {status !== 'completed' && status !== 'failed' && 'Analysis is in progress...'}
      </div>
    </div>
  );
};

export default ProgressIndicator;
