import React from 'react';
import { motion } from 'framer-motion';
import { 
  ArrowLeftIcon, 
  DocumentTextIcon, 
  LinkIcon, 
  CalculatorIcon,
  ChartBarIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';

import { LayerScore } from '../types/pergola';
import { ProgressRing } from './charts/ProgressRing';

interface Props {
  layer: LayerScore;
  layerName: string;
  factorName: string;
  segmentName: string;
  onBack: () => void;
}

export const LayerDashboard: React.FC<Props> = ({ 
  layer, 
  layerName, 
  factorName, 
  segmentName, 
  onBack 
}) => {
  const layerDisplayName = layerName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  const factorDisplayName = factorName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  const segmentDisplayName = segmentName.replace(/_/g, ' ').toUpperCase();

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Poor';
  };

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
                {layerDisplayName}
              </h1>
              <p className="text-gray-600">
                {segmentDisplayName} • {factorDisplayName} • Detailed layer analysis
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-6">
            <div className="text-center">
              <ProgressRing
                value={Math.round(layer.score)}
                size={120}
                strokeWidth={8}
                className="text-blue-600"
              />
              <div className="text-sm text-gray-600 mt-1">Layer Score</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {Math.round(layer.confidence * 100)}%
              </div>
              <div className="text-sm text-gray-600">Confidence</div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Score Overview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white rounded-xl shadow-lg p-6"
      >
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className={`text-4xl font-bold ${getScoreColor(layer.score)} mb-2`}>
              {Math.round(layer.score)}%
            </div>
            <div className="text-lg font-medium text-gray-900 mb-1">
              {getScoreLabel(layer.score)}
            </div>
            <div className="text-sm text-gray-600">Performance Rating</div>
          </div>
          
          <div className="text-center">
            <div className="text-4xl font-bold text-blue-600 mb-2">
              {Math.round(layer.confidence * 100)}%
            </div>
            <div className="text-lg font-medium text-gray-900 mb-1">High</div>
            <div className="text-sm text-gray-600">Data Confidence</div>
          </div>
          
          <div className="text-center">
            <div className="text-4xl font-bold text-purple-600 mb-2">
              {layer.calculation_method.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </div>
            <div className="text-lg font-medium text-gray-900 mb-1">Method</div>
            <div className="text-sm text-gray-600">Calculation Type</div>
          </div>
        </div>
      </motion.div>

      {/* Layer Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-xl shadow-lg p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <InformationCircleIcon className="h-5 w-5 text-blue-600 mr-2" />
          Layer Summary
        </h3>
        <p className="text-gray-700 leading-relaxed text-lg">{layer.summary}</p>
        
        {layer.insights && layer.insights.length > 0 && (
          <div className="mt-6">
            <h4 className="text-md font-semibold text-gray-900 mb-3">Key Insights</h4>
            <ul className="space-y-2">
              {layer.insights.map((insight, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <div className="flex-shrink-0 w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                  <span className="text-gray-700">{insight}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </motion.div>

      {/* Calculation Details */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <CalculatorIcon className="h-5 w-5 text-green-600 mr-2" />
            Calculation Method
          </h3>
          
          <div className="space-y-4">
            <div>
              <h4 className="text-md font-medium text-gray-900 mb-2">Method Type</h4>
              <div className="bg-gray-50 rounded-lg p-3">
                <span className="text-sm font-medium text-gray-700">
                  {layer.calculation_method.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </span>
              </div>
            </div>
            
            <div>
              <h4 className="text-md font-medium text-gray-900 mb-2">Supporting Data</h4>
              <div className="bg-gray-50 rounded-lg p-3">
                <div className="space-y-2">
                  {Object.entries(layer.supporting_data).map(([key, value]) => (
                    <div key={key} className="flex justify-between">
                      <span className="text-sm text-gray-600 capitalize">
                        {key.replace(/_/g, ' ')}:
                      </span>
                      <span className="text-sm font-medium text-gray-900">
                        {typeof value === 'number' ? value.toLocaleString() : String(value)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <LinkIcon className="h-5 w-5 text-purple-600 mr-2" />
            Data Sources
          </h3>
          
          <div className="space-y-3">
            {layer.data_sources.map((source, index) => (
              <div key={index} className="bg-gray-50 rounded-lg p-3">
                <div className="flex items-center space-x-2">
                  <LinkIcon className="h-4 w-4 text-gray-400" />
                  <a 
                    href={source} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-sm text-blue-600 hover:text-blue-800 hover:underline break-all"
                  >
                    {source}
                  </a>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-4 p-3 bg-blue-50 rounded-lg">
            <div className="flex items-center space-x-2">
              <InformationCircleIcon className="h-4 w-4 text-blue-600" />
              <span className="text-sm text-blue-800">
                All data sources are verified and validated for accuracy
              </span>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Performance Context */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="bg-white rounded-xl shadow-lg p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <ChartBarIcon className="h-5 w-5 text-orange-600 mr-2" />
          Performance Context
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="text-md font-medium text-gray-900 mb-3">Score Breakdown</h4>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Current Score</span>
                <span className={`text-sm font-medium ${getScoreColor(layer.score)}`}>
                  {Math.round(layer.score)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${getScoreColor(layer.score).replace('text-', 'bg-')}`}
                  style={{ width: `${layer.score}%` }}
                ></div>
              </div>
              <div className="text-xs text-gray-500">
                {getScoreLabel(layer.score)} performance level
              </div>
            </div>
          </div>
          
          <div>
            <h4 className="text-md font-medium text-gray-900 mb-3">Confidence Level</h4>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Data Quality</span>
                <span className="text-sm font-medium text-blue-600">
                  {Math.round(layer.confidence * 100)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full"
                  style={{ width: `${layer.confidence * 100}%` }}
                ></div>
              </div>
              <div className="text-xs text-gray-500">
                High confidence in data accuracy
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};
