import React, { useState, useEffect } from 'react';
import { 
  FolderIcon, 
  DocumentTextIcon, 
  CalendarIcon, 
  ChartBarIcon,
  MagnifyingGlassIcon,
  ArrowDownTrayIcon,
  PlayIcon
} from '@heroicons/react/24/outline';
import { PergolaAnalysis } from '../types/pergola';

interface AnalysisMetadata {
  id: string;
  name: string;
  description: string;
  createdAt: string;
  overallScore: number;
  segments: number;
  factors: number;
  layers: number;
  filePath: string;
}

interface Props {
  onAnalysisSelect: (analysis: PergolaAnalysis) => void;
  onNewAnalysis: () => void;
}

export const AnalysisSelector: React.FC<Props> = ({ onAnalysisSelect, onNewAnalysis }) => {
  console.log('AnalysisSelector component rendering...');
  
  const [analyses, setAnalyses] = useState<AnalysisMetadata[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [selectedAnalysis, setSelectedAnalysis] = useState<string | null>(null);

  // Load mock analyses
  useEffect(() => {
    console.log('AnalysisSelector useEffect running...');
    const mockAnalyses: AnalysisMetadata[] = [
      {
        id: 'pergola-2025-08-29',
        name: 'Pergola Market Analysis',
        description: 'Strategic analysis for premium outdoor pergola business targeting homeowners in North America',
        createdAt: '2025-08-29T12:48:37Z',
        overallScore: 78.5,
        segments: 5,
        factors: 30,
        layers: 156,
        filePath: 'pergola_analysis_results_20250829_124837.json'
      },
      {
        id: 'tech-startup-2025-08-28',
        name: 'Tech Startup Viability',
        description: 'AI-powered SaaS platform for small business analytics',
        createdAt: '2025-08-28T15:30:00Z',
        overallScore: 72.3,
        segments: 5,
        factors: 30,
        layers: 156,
        filePath: 'tech_startup_analysis_20250828_153000.json'
      },
      {
        id: 'restaurant-chain-2025-08-27',
        name: 'Restaurant Chain Expansion',
        description: 'Fast-casual restaurant chain expansion into new markets',
        createdAt: '2025-08-27T09:15:00Z',
        overallScore: 65.8,
        segments: 5,
        factors: 30,
        layers: 156,
        filePath: 'restaurant_chain_analysis_20250827_091500.json'
      }
    ];

    console.log('Setting mock analyses:', mockAnalyses);
    setAnalyses(mockAnalyses);
    setIsLoading(false);
  }, []);

  const handleAnalysisSelect = async (analysis: AnalysisMetadata) => {
    try {
      console.log('AnalysisSelector: handleAnalysisSelect called with:', analysis);
      setSelectedAnalysis(analysis.id);
      
      // Create mock analysis data for testing
      const mockAnalysisData: PergolaAnalysis = {
        query: analysis.description,
        overall_score: analysis.overallScore,
        overall_confidence: 0.85,
        segments: {
          "CONSUMER": {
            name: "CONSUMER",
            score: 82.3,
            confidence: 0.88,
            trend: "up",
            priority: "high",
            key_insights: [
              "Strong demand from affluent homeowners aged 35-60",
              "Growing interest in outdoor living spaces post-pandemic"
            ],
            recommendations: [
              "Focus on premium positioning strategy",
              "Develop targeted marketing for high-income demographics"
            ],
            factors: {
              "Consumer_Demand_Need": {
                name: "Consumer_Demand_Need",
                score: 85.2,
                confidence: 0.90,
                summary: "Strong market demand for premium outdoor structures",
                key_insights: [
                  "Market research shows 78% of target demographic interested in pergolas"
                ],
                recommendations: [
                  "Position as premium lifestyle enhancement"
                ],
                layers: {
                  "need_perception": {
                    name: "need_perception",
                    score: 87.5,
                    confidence: 0.92,
                    calculation_method: "market_survey_analysis",
                    supporting_data: {
                      "survey_respondents": 1250,
                      "interest_rate": 0.78
                    },
                    data_sources: [
                      "https://outdoor-living-market-research-2025.com"
                    ],
                    summary: "High perceived need for premium outdoor structures"
                  }
                }
              }
            }
          },
          "MARKET": {
            name: "MARKET",
            score: 76.8,
            confidence: 0.84,
            trend: "up",
            priority: "high",
            key_insights: [
              "Growing outdoor living market with 12% annual growth"
            ],
            recommendations: [
              "Focus on premium market positioning"
            ],
            factors: {
              "Market_Size_Growth": {
                name: "Market_Size_Growth",
                score: 78.9,
                confidence: 0.85,
                summary: "Strong market growth in premium outdoor living segment",
                key_insights: [
                  "Total market size: $8.2 billion"
                ],
                recommendations: [
                  "Target premium segment aggressively"
                ],
                layers: {
                  "total_addressable_market": {
                    name: "total_addressable_market",
                    score: 79.5,
                    confidence: 0.86,
                    calculation_method: "market_size_analysis",
                    supporting_data: {
                      "market_size": 8200000000,
                      "growth_rate": 0.12
                    },
                    data_sources: [
                      "https://outdoor-living-market-report.com"
                    ],
                    summary: "Large and growing market with $8.2B total size"
                  }
                }
              }
            }
          }
        },
        meta_scores: {
          market_fit: 78.5,
          innovation_score: 81.2,
          execution_readiness: 75.8,
          risk_index: 32.1,
          brand_strength: 71.4
        },
        executive_summary: "This analysis demonstrates strong strategic viability with comprehensive coverage of all strategic dimensions.",
        key_recommendations: [
          "Focus on premium positioning strategy",
          "Invest in brand building through digital marketing",
          "Develop intellectual property protection",
          "Maintain customer experience excellence"
        ],
        competitive_advantages: [
          "Premium product quality with innovative features",
          "Exceptional customer experience",
          "Strong market demand alignment"
        ],
        risk_factors: [
          "Brand awareness below category leaders",
          "Seasonal demand patterns",
          "Premium pricing strategy limitations"
        ],
        generated_at: analysis.createdAt
      };

      console.log('Mock analysis data created:', mockAnalysisData);
      onAnalysisSelect(mockAnalysisData);
    } catch (error) {
      console.error('Failed to load analysis data:', error);
      alert('Failed to load analysis. Please try again.');
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const analysisData = JSON.parse(e.target?.result as string);
          onAnalysisSelect(analysisData);
        } catch (error) {
          console.error('Failed to parse analysis file:', error);
          alert('Invalid analysis file format. Please upload a valid JSON file.');
        }
      };
      reader.readAsText(file);
    }
  };

  const filteredAnalyses = analyses.filter(analysis =>
    analysis.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    analysis.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  console.log('AnalysisSelector render state:', { isLoading, analyses: analyses.length, filteredAnalyses: filteredAnalyses.length });

  if (isLoading) {
    console.log('AnalysisSelector: Showing loading state');
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading analyses...</p>
        </div>
      </div>
    );
  }

  console.log('AnalysisSelector: Rendering main content');

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <div className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="flex-shrink-0">
                <ChartBarIcon className="h-8 w-8 text-blue-600" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  Validatus Strategic Analysis
                </h1>
                <p className="text-sm text-gray-500">Select Previous Analysis or Start New</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <button
            onClick={onNewAnalysis}
            className="flex items-center justify-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            <ChartBarIcon className="h-5 w-5 mr-2" />
            Start New Analysis
          </button>
          
          <label className="flex items-center justify-center px-6 py-3 bg-purple-600 text-white font-medium rounded-lg hover:bg-purple-700 transition-colors cursor-pointer">
            <ArrowDownTrayIcon className="h-5 w-5 mr-2" />
            Upload Analysis File
            <input
              type="file"
              accept=".json"
              onChange={handleFileUpload}
              className="hidden"
            />
          </label>
        </div>

        {/* Search */}
        <div className="mb-6">
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search analyses by name or description..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Analyses Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAnalyses.map((analysis) => (
            <div
              key={analysis.id}
              className={`bg-white rounded-xl shadow-lg p-6 border-2 transition-all duration-200 cursor-pointer hover:shadow-xl hover:scale-105 ${
                selectedAnalysis === analysis.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-transparent hover:border-blue-300'
              }`}
              onClick={() => handleAnalysisSelect(analysis)}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <DocumentTextIcon className="h-6 w-6 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{analysis.name}</h3>
                    <p className="text-sm text-gray-500">{analysis.description}</p>
                  </div>
                </div>
              </div>

              <div className="space-y-3 mb-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Overall Score</span>
                  <span className={`text-lg font-bold ${
                    analysis.overallScore >= 80 ? 'text-green-600' :
                    analysis.overallScore >= 60 ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {analysis.overallScore}%
                  </span>
                </div>
                
                <div className="grid grid-cols-3 gap-2 text-center">
                  <div>
                    <div className="text-sm font-medium text-gray-900">{analysis.segments}</div>
                    <div className="text-xs text-gray-500">Segments</div>
                  </div>
                  <div>
                    <div className="text-sm font-medium text-gray-900">{analysis.factors}</div>
                    <div className="text-xs text-gray-500">Factors</div>
                  </div>
                  <div>
                    <div className="text-sm font-medium text-gray-900">{analysis.layers}</div>
                    <div className="text-xs text-gray-500">Layers</div>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between text-sm text-gray-500">
                <div className="flex items-center space-x-1">
                  <CalendarIcon className="h-4 w-4" />
                  <span>{new Date(analysis.createdAt).toLocaleDateString()}</span>
                </div>
                <span className="text-blue-600 font-medium">Click to load →</span>
              </div>
            </div>
          ))}
        </div>

        {filteredAnalyses.length === 0 && (
          <div className="text-center py-12">
            <FolderIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No analyses found</h3>
            <p className="text-gray-500">
              {searchTerm ? 'Try adjusting your search terms.' : 'Start by creating your first analysis or uploading an existing one.'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
