import React, { useState } from 'react';
import { useAnalysisStore } from '../../stores/analysisStore';
import { AnalysisContext } from '../../types/analysis';

export const Dashboard: React.FC = () => {
  const { 
    currentAnalysis, 
    startAnalysis, 
    analysisStatus, 
    segmentScores,
    isLoading,
    error,
    resetAnalysis
  } = useAnalysisStore();
  
  const [query, setQuery] = useState('');
  const [context, setContext] = useState<AnalysisContext>({
    industry: '',
    geography: [],
    company_stage: '',
    target_audience: ''
  });

  const handleStartAnalysis = async () => {
    if (query.trim() && context.industry) {
      await startAnalysis({
        query,
        context
      });
    }
  };

  const handleReset = () => {
    resetAnalysis();
    setQuery('');
    setContext({
      industry: '',
      geography: [],
      company_stage: '',
      target_audience: ''
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Validatus Platform
          </h1>
          <p className="text-gray-600">
            Strategic Decision Intelligence - From Scattered Insights to Decision Clarity
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <div className="mt-2 text-sm text-red-700">{error}</div>
              </div>
            </div>
          </div>
        )}

        {/* Analysis Input */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Start New Analysis</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Strategic Query
              </label>
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., Should we enter the electric vehicle market in Europe?"
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={3}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Industry
              </label>
              <input
                type="text"
                value={context.industry}
                onChange={(e) => setContext({...context, industry: e.target.value})}
                placeholder="e.g., Automotive, Technology"
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Company Stage
              </label>
              <select
                value={context.company_stage}
                onChange={(e) => setContext({...context, company_stage: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select stage</option>
                <option value="startup">Startup</option>
                <option value="scaleup">Scale-up</option>
                <option value="enterprise">Enterprise</option>
                <option value="mature">Mature</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Audience
              </label>
              <input
                type="text"
                value={context.target_audience}
                onChange={(e) => setContext({...context, target_audience: e.target.value})}
                placeholder="e.g., Enterprise customers, B2B, Consumers"
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={handleStartAnalysis}
              disabled={!query.trim() || !context.industry || isLoading}
              className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Starting Analysis...' : 'Start Analysis'}
            </button>
            
            {currentAnalysis && (
              <button
                onClick={handleReset}
                className="bg-gray-500 text-white px-6 py-3 rounded-md hover:bg-gray-600"
              >
                Reset
              </button>
            )}
          </div>
        </div>

        {/* Analysis Status */}
        {currentAnalysis && (
          <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
            <h3 className="text-lg font-semibold mb-4">Analysis Progress</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span>Status:</span>
                <span className={`px-3 py-1 rounded-full text-sm ${
                  analysisStatus === 'completed' ? 'bg-green-100 text-green-800' :
                  analysisStatus === 'failed' ? 'bg-red-100 text-red-800' :
                  analysisStatus === 'researching' ? 'bg-blue-100 text-blue-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {analysisStatus}
                </span>
              </div>
              
              {analysisStatus !== 'completed' && analysisStatus !== 'failed' && (
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300" 
                    style={{width: `${currentAnalysis.progress}%`}}
                  ></div>
                </div>
              )}
              
              <div className="text-sm text-gray-600">
                Analysis ID: {currentAnalysis.analysis_id}
              </div>
            </div>
          </div>
        )}

        {/* Results Dashboard */}
        {analysisStatus === 'completed' && segmentScores && (
          <div className="space-y-8">
            {/* Segment Overview */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold mb-4">Strategic Overview</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Object.entries(segmentScores).map(([segment, data]: [string, any]) => (
                  <div key={segment} className="border rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 mb-2">{segment}</h4>
                    <div className="text-2xl font-bold text-blue-600 mb-2">
                      {data.score}/100
                    </div>
                    <div className="text-sm text-gray-600 mb-2">
                      Confidence: {(data.confidence * 100).toFixed(0)}%
                    </div>
                    <p className="text-sm text-gray-700">{data.summary}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Recommendations */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold mb-4">Strategic Recommendations</h3>
              <div className="space-y-3">
                {useAnalysisStore.getState().recommendations.map((recommendation, index) => (
                  <div key={index} className="flex items-start">
                    <div className="flex-shrink-0 w-2 h-2 bg-blue-600 rounded-full mt-2 mr-3"></div>
                    <p className="text-gray-700">{recommendation}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
