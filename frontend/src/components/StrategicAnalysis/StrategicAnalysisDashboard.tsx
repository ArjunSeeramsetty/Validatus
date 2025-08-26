import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, TrendingUp, TrendingDown, Target, AlertTriangle, Lightbulb } from 'lucide-react';

interface StrategicAnalysisRequest {
  query: string;
  context?: Record<string, any>;
  consensus_method?: string;
}

interface StrategicAnalysisResponse {
  success: boolean;
  data?: any;
  error?: string;
  message: string;
}

interface SegmentScore {
  segment_name: string;
  score: number;
  confidence: number;
  key_insights: string[];
  recommendations: string[];
  factors: Record<string, any>;
}

interface ExecutiveSummary {
  strategic_position: string;
  overall_performance: {
    score: number;
    confidence: number;
    risk_level: string;
    opportunity_level: string;
  };
  performance_distribution: {
    average: number;
    range: string;
    variance: number;
  };
  top_performer: {
    segment: string;
    score: number;
  };
  bottom_performer: {
    segment: string;
    score: number;
  };
  priority_actions: string[];
  key_insights: string[];
}

const StrategicAnalysisDashboard: React.FC = () => {
  const [query, setQuery] = useState('');
  const [context, setContext] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResults, setAnalysisResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('overview');

  const handleAnalysis = async (type: 'comprehensive' | 'quick') => {
    if (!query.trim()) {
      setError('Please enter a strategic analysis query');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const request: StrategicAnalysisRequest = {
        query: query.trim(),
        context: context.trim() ? JSON.parse(context) : undefined,
        consensus_method: type === 'comprehensive' ? 'clustering_based' : 'confidence_based'
      };

      const response = await fetch(`/api/strategic-analysis/${type}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      const result: StrategicAnalysisResponse = await response.json();

      if (result.success && result.data) {
        setAnalysisResults(result.data);
      } else {
        setError(result.error || 'Analysis failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBadgeColor = (score: number) => {
    if (score >= 0.8) return 'bg-green-100 text-green-800';
    if (score >= 0.6) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  const getRiskLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'low': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'high': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getOpportunityLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold text-gray-900">
          Strategic Analysis Dashboard
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Comprehensive strategic intelligence with layer, factor, and segment level scoring
        </p>
      </div>

      {/* Input Section */}
      <Card>
        <CardHeader>
          <CardTitle>Strategic Analysis Query</CardTitle>
          <CardDescription>
            Enter your strategic business question and optional context
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="query">Strategic Query</Label>
            <Textarea
              id="query"
              placeholder="e.g., What are the strategic opportunities and risks for launching a sustainable AI-powered fintech platform in emerging markets?"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="min-h-[100px]"
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="context">Business Context (Optional JSON)</Label>
            <Textarea
              id="context"
              placeholder='{"industry": "Financial Technology", "target_audience": "Unbanked populations", "geographic_focus": ["Southeast Asia", "Africa"]}'
              value={context}
              onChange={(e) => setContext(e.target.value)}
              className="min-h-[80px] font-mono text-sm"
            />
          </div>

          <div className="flex gap-4">
            <Button
              onClick={() => handleAnalysis('comprehensive')}
              disabled={isLoading}
              className="flex-1"
            >
              {isLoading ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <Target className="mr-2 h-4 w-4" />
              )}
              Comprehensive Analysis
            </Button>
            <Button
              onClick={() => handleAnalysis('quick')}
              disabled={isLoading}
              variant="outline"
              className="flex-1"
            >
              {isLoading ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <TrendingUp className="mr-2 h-4 w-4" />
              )}
              Quick Analysis
            </Button>
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Results Section */}
      {analysisResults && (
        <div className="space-y-6">
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-5">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="segments">Segments</TabsTrigger>
              <TabsTrigger value="factors">Factors</TabsTrigger>
              <TabsTrigger value="layers">Layers</TabsTrigger>
              <TabsTrigger value="insights">Insights</TabsTrigger>
            </TabsList>

            {/* Overview Tab */}
            <TabsContent value="overview" className="space-y-6">
              {analysisResults.executive_summary && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Target className="h-5 w-5" />
                      Executive Summary
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-4">
                        <div>
                          <Label className="text-sm font-medium text-gray-600">
                            Strategic Position
                          </Label>
                          <p className="text-lg font-semibold">
                            {analysisResults.executive_summary.strategic_position}
                          </p>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <Label className="text-sm font-medium text-gray-600">
                              Overall Score
                            </Label>
                            <div className="flex items-center gap-2">
                              <Progress 
                                value={analysisResults.executive_summary.overall_performance.score * 100} 
                                className="flex-1"
                              />
                              <span className="text-lg font-bold">
                                {(analysisResults.executive_summary.overall_performance.score * 100).toFixed(1)}%
                              </span>
                            </div>
                          </div>
                          
                          <div>
                            <Label className="text-sm font-medium text-gray-600">
                              Confidence
                            </Label>
                            <div className="flex items-center gap-2">
                              <Progress 
                                value={analysisResults.executive_summary.overall_performance.confidence * 100} 
                                className="flex-1"
                              />
                              <span className="text-lg font-bold">
                                {(analysisResults.executive_summary.overall_performance.confidence * 100).toFixed(1)}%
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <Label className="text-sm font-medium text-gray-600">
                              Risk Level
                            </Label>
                            <Badge className={getRiskLevelColor(analysisResults.executive_summary.overall_performance.risk_level)}>
                              {analysisResults.executive_summary.overall_performance.risk_level.toUpperCase()}
                            </Badge>
                          </div>
                          
                          <div>
                            <Label className="text-sm font-medium text-gray-600">
                              Opportunity Level
                            </Label>
                            <Badge className={getOpportunityLevelColor(analysisResults.executive_summary.overall_performance.opportunity_level)}>
                              {analysisResults.executive_summary.overall_performance.opportunity_level.toUpperCase()}
                            </Badge>
                          </div>
                        </div>

                        <div>
                          <Label className="text-sm font-medium text-gray-600">
                            Performance Range
                          </Label>
                          <p className="text-lg font-semibold">
                            {analysisResults.executive_summary.performance_distribution.range}
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* Top and Bottom Performers */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {analysisResults.executive_summary.top_performer?.segment && (
                        <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                          <div className="flex items-center gap-2 mb-2">
                            <TrendingUp className="h-5 w-5 text-green-600" />
                            <Label className="text-sm font-medium text-green-800">
                              Top Performer
                            </Label>
                          </div>
                          <p className="text-lg font-semibold text-green-900">
                            {analysisResults.executive_summary.top_performer.segment}
                          </p>
                          <p className="text-sm text-green-700">
                            Score: {(analysisResults.executive_summary.top_performer.score * 100).toFixed(1)}%
                          </p>
                        </div>
                      )}

                      {analysisResults.executive_summary.bottom_performer?.segment && (
                        <div className="p-4 bg-red-50 rounded-lg border border-red-200">
                          <div className="flex items-center gap-2 mb-2">
                            <TrendingDown className="h-5 w-5 text-red-600" />
                            <Label className="text-sm font-medium text-red-800">
                              Bottom Performer
                            </Label>
                          </div>
                          <p className="text-lg font-semibold text-red-900">
                            {analysisResults.executive_summary.bottom_performer.segment}
                          </p>
                          <p className="text-sm text-red-700">
                            Score: {(analysisResults.executive_summary.bottom_performer.score * 100).toFixed(1)}%
                          </p>
                        </div>
                      )}
                    </div>

                    {/* Priority Actions */}
                    {analysisResults.executive_summary.priority_actions?.length > 0 && (
                      <div>
                        <Label className="text-sm font-medium text-gray-600 mb-3 block">
                          Priority Actions
                        </Label>
                        <div className="space-y-2">
                          {analysisResults.executive_summary.priority_actions.map((action: string, index: number) => (
                            <div key={index} className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                              <Badge variant="secondary" className="mt-1">
                                {index + 1}
                              </Badge>
                              <p className="text-sm text-blue-900">{action}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              )}
            </TabsContent>

            {/* Segments Tab */}
            <TabsContent value="segments" className="space-y-6">
              {analysisResults.strategic_analysis?.segment_scores && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {analysisResults.strategic_analysis.segment_scores.map((segment: SegmentScore) => (
                    <Card key={segment.segment_name}>
                      <CardHeader>
                        <CardTitle className="flex items-center justify-between">
                          <span className="capitalize">{segment.segment_name}</span>
                          <Badge className={getScoreBadgeColor(segment.score)}>
                            {(segment.score * 100).toFixed(1)}%
                          </Badge>
                        </CardTitle>
                        <CardDescription>
                          Confidence: {(segment.confidence * 100).toFixed(1)}%
                        </CardDescription>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div>
                          <Label className="text-sm font-medium text-gray-600 mb-2 block">
                            Key Insights
                          </Label>
                          <div className="space-y-2">
                            {segment.key_insights.slice(0, 2).map((insight: string, index: number) => (
                              <div key={index} className="text-sm text-gray-700 bg-gray-50 p-2 rounded">
                                • {insight}
                              </div>
                            ))}
                          </div>
                        </div>

                        <div>
                          <Label className="text-sm font-medium text-gray-600 mb-2 block">
                            Top Factors
                          </Label>
                          <div className="space-y-2">
                            {Object.entries(segment.factors)
                              .sort(([, a], [, b]) => b.score - a.score)
                              .slice(0, 3)
                              .map(([factorName, factorData]: [string, any]) => (
                                <div key={factorName} className="flex justify-between items-center text-sm">
                                  <span className="text-gray-700 capitalize">
                                    {factorName.replace(/_/g, ' ')}
                                  </span>
                                  <Badge variant="outline">
                                    {(factorData.score * 100).toFixed(1)}%
                                  </Badge>
                                </div>
                              ))}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </TabsContent>

            {/* Factors Tab */}
            <TabsContent value="factors" className="space-y-6">
              {analysisResults.strategic_analysis?.segment_scores && (
                <div className="space-y-6">
                  {analysisResults.strategic_analysis.segment_scores.map((segment: SegmentScore) => (
                    <Card key={segment.segment_name}>
                      <CardHeader>
                        <CardTitle className="capitalize">{segment.segment_name} Segment Factors</CardTitle>
                        <CardDescription>
                          Detailed factor-level analysis with scoring and recommendations
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          {Object.entries(segment.factors).map(([factorName, factorData]: [string, any]) => (
                            <div key={factorName} className="border rounded-lg p-4">
                              <div className="flex items-center justify-between mb-3">
                                <h4 className="font-semibold capitalize">
                                  {factorName.replace(/_/g, ' ')}
                                </h4>
                                <div className="flex items-center gap-2">
                                  <span className="text-sm text-gray-600">Score:</span>
                                  <Badge className={getScoreBadgeColor(factorData.score)}>
                                    {(factorData.score * 100).toFixed(1)}%
                                  </Badge>
                                </div>
                              </div>
                              
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                  <Label className="text-sm font-medium text-gray-600 mb-2 block">
                                    Summary
                                  </Label>
                                  <p className="text-sm text-gray-700">{factorData.summary}</p>
                                </div>
                                
                                <div>
                                  <Label className="text-sm font-medium text-gray-600 mb-2 block">
                                    Recommendations
                                  </Label>
                                  <div className="space-y-1">
                                    {factorData.recommendations.slice(0, 2).map((rec: string, index: number) => (
                                      <div key={index} className="text-sm text-gray-700 bg-blue-50 p-2 rounded">
                                        • {rec}
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </TabsContent>

            {/* Layers Tab */}
            <TabsContent value="layers" className="space-y-6">
              {analysisResults.strategic_analysis?.segment_scores && (
                <div className="space-y-6">
                  {analysisResults.strategic_analysis.segment_scores.map((segment: SegmentScore) => (
                    <Card key={segment.segment_name}>
                      <CardHeader>
                        <CardTitle className="capitalize">{segment.segment_name} Segment Layers</CardTitle>
                        <CardDescription>
                          Layer-level analysis with calculation methods and data sources
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          {Object.entries(segment.factors).map(([factorName, factorData]: [string, any]) => (
                            <div key={factorName} className="border rounded-lg p-4">
                              <h4 className="font-semibold capitalize mb-3">
                                {factorName.replace(/_/g, ' ')} Factor Layers
                              </h4>
                              
                              <div className="space-y-3">
                                {factorData.layers && Object.entries(factorData.layers).map(([layerName, layerData]: [string, any]) => (
                                  <div key={layerName} className="bg-gray-50 rounded-lg p-3">
                                    <div className="flex items-center justify-between mb-2">
                                      <span className="font-medium text-sm">{layerName}</span>
                                      <Badge variant="outline">
                                        {(layerData.score * 100).toFixed(1)}%
                                      </Badge>
                                    </div>
                                    
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                                      <div>
                                        <span className="text-gray-600">Method:</span>
                                        <span className="ml-2 text-gray-800">{layerData.calculation_method}</span>
                                      </div>
                                      <div>
                                        <span className="text-gray-600">Confidence:</span>
                                        <span className="ml-2 text-gray-800">
                                          {(layerData.confidence * 100).toFixed(1)}%
                                        </span>
                                      </div>
                                      <div className="md:col-span-2">
                                        <span className="text-gray-600">Data Sources:</span>
                                        <span className="ml-2 text-gray-800">
                                          {layerData.data_sources.join(', ')}
                                        </span>
                                      </div>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </TabsContent>

            {/* Insights Tab */}
            <TabsContent value="insights" className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Key Insights */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Lightbulb className="h-5 w-5" />
                      Key Strategic Insights
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {analysisResults.strategic_analysis?.key_insights?.map((insight: string, index: number) => (
                        <div key={index} className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                          <Badge variant="secondary" className="mt-1">
                            {index + 1}
                          </Badge>
                          <p className="text-sm text-blue-900">{insight}</p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Strategic Recommendations */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Target className="h-5 w-5" />
                      Strategic Recommendations
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {analysisResults.strategic_analysis?.strategic_recommendations?.map((rec: string, index: number) => (
                        <div key={index} className="flex items-start gap-3 p-3 bg-green-50 rounded-lg border border-green-200">
                          <Badge variant="secondary" className="mt-1">
                            {index + 1}
                          </Badge>
                          <p className="text-sm text-green-900">{rec}</p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Risk and Opportunity Analysis */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <AlertTriangle className="h-5 w-5" />
                      Risk Assessment
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    {analysisResults.strategic_analysis?.risk_assessment && (
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium">Overall Risk Level</span>
                          <Badge className={getRiskLevelColor(analysisResults.strategic_analysis.risk_assessment.overall_risk_level)}>
                            {analysisResults.strategic_analysis.risk_assessment.overall_risk_level.toUpperCase()}
                          </Badge>
                        </div>
                        
                        {analysisResults.strategic_analysis.risk_assessment.high_risk_segments?.length > 0 && (
                          <div>
                            <Label className="text-sm font-medium text-red-800 mb-2 block">
                              High Risk Segments
                            </Label>
                            <div className="space-y-2">
                              {analysisResults.strategic_analysis.risk_assessment.high_risk_segments.map((risk: any, index: number) => (
                                <div key={index} className="text-sm text-red-700 bg-red-50 p-2 rounded border border-red-200">
                                  <strong>{risk.segment}:</strong> {risk.risk}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5" />
                      Opportunity Analysis
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    {analysisResults.strategic_analysis?.opportunity_analysis && (
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium">Overall Opportunity Level</span>
                          <Badge className={getOpportunityLevelColor(analysisResults.strategic_analysis.opportunity_analysis.overall_opportunity_level)}>
                            {analysisResults.strategic_analysis.opportunity_analysis.overall_opportunity_level.toUpperCase()}
                          </Badge>
                        </div>
                        
                        {analysisResults.strategic_analysis.opportunity_analysis.high_potential_segments?.length > 0 && (
                          <div>
                            <Label className="text-sm font-medium text-green-800 mb-2 block">
                              High Potential Segments
                            </Label>
                            <div className="space-y-2">
                              {analysisResults.strategic_analysis.opportunity_analysis.high_potential_segments.map((opp: any, index: number) => (
                                <div key={index} className="text-sm text-green-700 bg-green-50 p-2 rounded border border-green-200">
                                  <strong>{opp.segment}:</strong> {opp.opportunity}
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      )}
    </div>
  );
};

export default StrategicAnalysisDashboard;
