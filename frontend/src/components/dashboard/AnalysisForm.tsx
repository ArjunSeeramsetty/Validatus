import React, { useState } from 'react';
import { AnalysisContext } from '../../types/analysis';

interface AnalysisFormProps {
  onSubmit: (query: string, context: AnalysisContext) => void;
  isLoading: boolean;
}

export const AnalysisForm: React.FC<AnalysisFormProps> = ({ onSubmit, isLoading }) => {
  const [query, setQuery] = useState('');
  const [context, setContext] = useState<AnalysisContext>({
    industry: '',
    geography: [],
    company_stage: '',
    target_audience: '',
    budget_range: '',
    timeline: '',
    competitive_context: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && context.industry && context.company_stage && context.target_audience) {
      onSubmit(query.trim(), context);
    }
  };

  const handleGeographyChange = (value: string) => {
    if (value && !context.geography.includes(value)) {
      setContext(prev => ({
        ...prev,
        geography: [...prev.geography, value]
      }));
    }
  };

  const removeGeography = (index: number) => {
    setContext(prev => ({
      ...prev,
      geography: prev.geography.filter((_, i) => i !== index)
    }));
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Start Strategic Analysis</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            What would you like to analyze? *
          </label>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Describe your strategic question or business challenge..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows={4}
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Industry *
            </label>
            <input
              type="text"
              value={context.industry}
              onChange={(e) => setContext(prev => ({ ...prev, industry: e.target.value }))}
              placeholder="e.g., Technology, Healthcare, Finance"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Company Stage *
            </label>
            <select
              value={context.company_stage}
              onChange={(e) => setContext(prev => ({ ...prev, company_stage: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            >
              <option value="">Select stage</option>
              <option value="startup">Startup</option>
              <option value="growth">Growth Stage</option>
              <option value="mature">Mature</option>
              <option value="enterprise">Enterprise</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Target Audience *
            </label>
            <input
              type="text"
              value={context.target_audience}
              onChange={(e) => setContext(prev => ({ ...prev, target_audience: e.target.value }))}
              placeholder="e.g., B2B SaaS companies, Millennial consumers"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Budget Range
            </label>
            <select
              value={context.budget_range}
              onChange={(e) => setContext(prev => ({ ...prev, budget_range: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Select budget</option>
              <option value="under_10k">Under $10K</option>
              <option value="10k_50k">$10K - $50K</option>
              <option value="50k_100k">$50K - $100K</option>
              <option value="100k_500k">$100K - $500K</option>
              <option value="over_500k">Over $500K</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Geography
          </label>
          <div className="flex gap-2 mb-2">
            <input
              type="text"
              placeholder="Add geography (e.g., North America, Europe)"
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              onKeyPress={(e) => e.key === 'Enter' && handleGeographyChange(e.currentTarget.value)}
            />
            <button
              type="button"
              onClick={() => {
                const input = document.querySelector('input[placeholder*="geography"]') as HTMLInputElement;
                if (input && input.value) {
                  handleGeographyChange(input.value);
                  input.value = '';
                }
              }}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Add
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {context.geography.map((geo, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm flex items-center gap-2"
              >
                {geo}
                <button
                  type="button"
                  onClick={() => removeGeography(index)}
                  className="text-blue-600 hover:text-blue-800"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Timeline
          </label>
          <select
            value={context.timeline}
            onChange={(e) => setContext(prev => ({ ...prev, timeline: e.target.value }))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Select timeline</option>
            <option value="immediate">Immediate (0-3 months)</option>
            <option value="short_term">Short-term (3-12 months)</option>
            <option value="medium_term">Medium-term (1-3 years)</option>
            <option value="long_term">Long-term (3+ years)</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Competitive Context
          </label>
          <textarea
            value={context.competitive_context}
            onChange={(e) => setContext(prev => ({ ...prev, competitive_context: e.target.value }))}
            placeholder="Describe your competitive landscape, key competitors, or market positioning..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows={3}
          />
        </div>

        <button
          type="submit"
          disabled={isLoading || !query.trim() || !context.industry || !context.company_stage || !context.target_audience}
          className="w-full bg-blue-600 text-white py-3 px-6 rounded-md font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? 'Starting Analysis...' : 'Start Strategic Analysis'}
        </button>
      </form>
    </div>
  );
};
