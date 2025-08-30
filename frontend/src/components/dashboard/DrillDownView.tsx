import React from 'react';
import { TransformedAnalysis } from '../../utils/dataTransformation';
import { ChartDataAdapters } from '../charts/ChartDataAdapters';
import { BarChart } from '../charts/BarChart';

interface DrillDownViewProps {
  data: TransformedAnalysis;
  segmentName: string;
  factorName: string;
  onGoBack: () => void;
}

const DrillDownView: React.FC<DrillDownViewProps> = ({ 
  data, 
  segmentName, 
  factorName, 
  onGoBack 
}) => {
  const segment = data.segments[segmentName];
  const factor = segment?.factors[factorName];

  if (!segment || !factor) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Factor Analysis</h2>
        <p className="text-red-600">Factor not found</p>
        <button
          onClick={onGoBack}
          className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          ← Go Back
        </button>
      </div>
    );
  }

  const layerData = ChartDataAdapters.prepareLayerScatterData(segmentName, factorName, data);

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Factor Analysis</h2>
            <p className="text-gray-600">
              {segment.name} → {factor.name}
            </p>
          </div>
          <button
            onClick={onGoBack}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            ← Go Back
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-blue-800 mb-2">Factor Score</h3>
            <div className="text-3xl font-bold text-blue-600">{factor.score}/100</div>
            <p className="text-sm text-blue-700">Confidence: {(factor.confidence * 100).toFixed(1)}%</p>
          </div>
          
          <div className="bg-green-50 p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-green-800 mb-2">Layers Analyzed</h3>
            <div className="text-3xl font-bold text-green-600">{Object.keys(factor.layers).length}</div>
            <p className="text-sm text-green-700">Total layers in this factor</p>
          </div>
          
          <div className="bg-purple-50 p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-purple-800 mb-2">Average Layer Score</h3>
            <div className="text-3xl font-bold text-purple-600">
              {(Object.values(factor.layers).reduce((sum, layer) => sum + layer.score, 0) / Object.keys(factor.layers).length).toFixed(1)}/100
            </div>
            <p className="text-sm text-purple-700">Across all layers</p>
          </div>
        </div>

        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-700 mb-4">Factor Summary</h3>
          <p className="text-gray-600">{factor.summary}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div>
            <h3 className="text-xl font-semibold text-gray-700 mb-4">Key Insights</h3>
            <ul className="list-disc list-inside space-y-2 text-gray-600">
              {factor.key_insights.map((insight, index) => (
                <li key={index}>{insight}</li>
              ))}
            </ul>
          </div>
          
          <div>
            <h3 className="text-xl font-semibold text-gray-700 mb-4">Recommendations</h3>
            <ul className="list-disc list-inside space-y-2 text-gray-600">
              {factor.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-700 mb-4">Layer Performance</h3>
          {layerData.length > 0 ? (
            <BarChart data={layerData} />
          ) : (
            <p className="text-gray-500">No layer data available</p>
          )}
        </div>

        <div>
          <h3 className="text-xl font-semibold text-gray-700 mb-4">Detailed Layer Analysis</h3>
          <div className="space-y-4">
            {Object.entries(factor.layers).map(([layerKey, layer]) => (
              <div key={layerKey} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-lg font-semibold text-gray-800">{layer.name}</h4>
                  <div className="text-2xl font-bold text-blue-600">{layer.score}/100</div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-3">
                  <div className="bg-gray-50 p-3 rounded">
                    <h5 className="font-semibold text-gray-700 text-sm">Confidence</h5>
                    <p className="text-sm text-gray-600">{(layer.confidence * 100).toFixed(1)}%</p>
                  </div>
                  
                  <div className="bg-gray-50 p-3 rounded">
                    <h5 className="font-semibold text-gray-700 text-sm">Calculation Method</h5>
                    <p className="text-sm text-gray-600">{layer.calculation_method || 'Standard'}</p>
                  </div>
                  
                  <div className="bg-gray-50 p-3 rounded">
                    <h5 className="font-semibold text-gray-700 text-sm">Data Sources</h5>
                    <p className="text-sm text-gray-600">{layer.data_sources.length} sources</p>
                  </div>
                </div>
                
                <div>
                  <h5 className="font-semibold text-gray-700 mb-2">Summary</h5>
                  <p className="text-gray-600 text-sm">{layer.summary}</p>
                </div>
                
                {Object.keys(layer.supporting_data).length > 0 && (
                  <div className="mt-3">
                    <h5 className="font-semibold text-gray-700 mb-2">Supporting Data</h5>
                    <div className="bg-gray-50 p-3 rounded text-sm">
                      <pre className="text-xs text-gray-600 overflow-auto">
                        {JSON.stringify(layer.supporting_data, null, 2)}
                      </pre>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DrillDownView;
