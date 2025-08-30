import React, { useState } from 'react';
import useAnalysisStore from '../../stores/analysisStore';
import { AnalysisContext } from '../../types/analysis';

export const Dashboard: React.FC = () => {
  const { isLoading, error, setLoading, setError } = useAnalysisStore();
  
  const [query, setQuery] = useState('');
  const [context, setContext] = useState<AnalysisContext>({
    industry: '',
    geography: [],
    company_stage: '',
    target_audience: ''
  });

  const handleStartAnalysis = async () => {
    if (query.trim() && context.industry) {
      setLoading(true);
      setError(null);
      
      try {
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // For now, we'll just show a message that this would connect to the real API
        // In a real implementation, this would make an actual API call to start analysis
        alert('Analysis started! This would connect to the real backend API to generate analysis results. For now, please use the "Visualize Report" option to upload an existing analysis JSON file.');
        
        // Don't set mock data - only work with real uploaded files
      } catch (error) {
        setError(error instanceof Error ? error.message : 'Failed to start analysis');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleReset = () => {
    setQuery('');
    setContext({
      industry: '',
      geography: [],
      company_stage: '',
      target_audience: ''
    });
    setError(null);
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
                <option value="growth">Growth</option>
                <option value="mature">Mature</option>
                <option value="enterprise">Enterprise</option>
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
                placeholder="e.g., B2B, B2C, Enterprise"
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="flex space-x-4">
            <button
              onClick={handleStartAnalysis}
              disabled={isLoading || !query.trim() || !context.industry}
              className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Starting Analysis...' : 'Start Analysis'}
            </button>
            
            <button
              onClick={handleReset}
              className="bg-gray-500 text-white px-6 py-3 rounded-md hover:bg-gray-600"
            >
              Reset
            </button>
          </div>
        </div>

        {/* Info Message */}
        <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-blue-800">Note</h3>
              <div className="mt-2 text-sm text-blue-700">
                <p>This form is for demonstration purposes. To view actual analysis results, please use the "Visualize Report" option from the home page to upload an existing analysis JSON file.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
