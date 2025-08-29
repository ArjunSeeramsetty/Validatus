import React from 'react';
import { motion } from 'framer-motion';
import { ArrowLeftIcon, ChartBarIcon, DocumentTextIcon } from '@heroicons/react/24/outline';

import { FactorScore } from '../types/pergola';
import { BarChart } from './charts/BarChart';
import { ProgressRing } from './charts/ProgressRing';
import { InsightsPanel } from './InsightsPanel';

interface Props {
  factor: FactorScore;
  factorName: string;
  segmentName: string;
  onDrillDown: (level: 'layer', name: string) => void;
  onBack: () => void;
}

export const FactorDashboard: React.FC<Props> = ({ 
  factor, 
  factorName, 
  segmentName, 
  onDrillDown, 
  onBack 
}) => {
  const layerData = Object.entries(factor.layers).map(([name, layer]) => ({
    name: name.replace(/_/g, ' '),
    score: layer.score,
    confidence: layer.confidence
  }));

  const factorDisplayName = factorName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
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
                {factorDisplayName}
              </h1>
              <p className="text-gray-600">
                {segmentDisplayName} • Detailed layer breakdown and insights
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-6">
            <div className="text-center">
              <ProgressRing 
                percentage={Math.round(factor.score)} 
                size={80}
                strokeWidth={8}
                className="text-green-600"
              />
              <div className="text-sm text-gray-600 mt-1">Factor Score</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {Math.round(factor.confidence * 100)}%
              </div>
              <div className="text-sm text-gray-600">Confidence</div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Factor Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white rounded-xl shadow-lg p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Factor Summary</h3>
        <p className="text-gray-700 leading-relaxed mb-4">{factor.summary}</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="text-md font-semibold text-gray-900 mb-3">Key Insights</h4>
            <ul className="space-y-2">
              {factor.key_insights.map((insight, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <div className="flex-shrink-0 w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                  <span className="text-gray-700 text-sm">{insight}</span>
                </li>
              ))}
            </ul>
          </div>
          
          <div>
            <h4 className="text-md font-semibold text-gray-900 mb-3">Recommendations</h4>
            <ul className="space-y-2">
              {factor.recommendations.map((rec, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <div className="flex-shrink-0 w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                  <span className="text-gray-700 text-sm">{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </motion.div>

      {/* Layer Performance Chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-xl shadow-lg p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Layer Performance Overview</h3>
        <BarChart 
          data={layerData}
          height={300}
          onBarClick={(data) => onDrillDown('layer', Object.keys(factor.layers)[layerData.findIndex(l => l.name === data.name)])}
        />
      </motion.div>

      {/* Layer Details Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <DocumentTextIcon className="h-5 w-5 text-blue-600 mr-2" />
            Layer Details
          </h3>
          <div className="space-y-4">
            {Object.entries(factor.layers).map(([layerName, layer], index) => (
              <motion.div
                key={layerName}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                className="bg-white rounded-lg shadow-md p-4 border-2 border-transparent hover:border-blue-300 transition-all duration-200 cursor-pointer"
                onClick={() => onDrillDown('layer', layerName)}
              >
                <div className="flex items-center justify-between mb-3">
                  <h5 className="text-md font-semibold text-gray-900">
                    {layerName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </h5>
                  <div className="text-sm text-gray-500">
                    {Math.round(layer.confidence * 100)}% confidence
                  </div>
                </div>
                
                <div className="mb-3">
                  <div className={`text-2xl font-bold ${
                    layer.score >= 80 ? 'text-green-600' :
                    layer.score >= 60 ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {Math.round(layer.score)}%
                  </div>
                  <div className="text-sm text-gray-600">Layer Score</div>
                </div>
                
                <p className="text-sm text-gray-600 line-clamp-2">{layer.summary}</p>
                
                <div className="mt-3 pt-3 border-t border-gray-100">
                  <div className="text-xs text-blue-600 font-medium">
                    Click to view details →
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h4 className="text-lg font-semibold text-gray-900 mb-4">Calculation Methods</h4>
            <div className="space-y-3">
              {Object.entries(factor.layers).map(([layerName, layer]) => (
                <div key={layerName} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">
                    {layerName.replace(/_/g, ' ')}
                  </span>
                  <span className="text-xs text-gray-500 bg-white px-2 py-1 rounded">
                    {layer.calculation_method}
                  </span>
                </div>
              ))}
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h4 className="text-lg font-semibold text-gray-900 mb-4">Data Sources</h4>
            <div className="space-y-2">
              {Object.entries(factor.layers).flatMap(([layerName, layer]) =>
                layer.data_sources.map((source, index) => (
                  <div key={`${layerName}-${index}`} className="text-sm text-gray-600">
                    <span className="font-medium">{layerName.replace(/_/g, ' ')}:</span> {source}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
