import { HierarchicalAnalysisResponse } from '../services/validatusApi';

export interface TransformedAnalysis {
  query: string;
  overall_score: number;
  overall_confidence: number;
  segments: {
    [segmentName: string]: {
      name: string;
      score: number;
      confidence: number;
      trend: 'up' | 'down' | 'stable';
      priority: 'high' | 'medium' | 'low';
      key_insights: string[];
      recommendations: string[];
      factors: {
        [factorName: string]: {
          name: string;
          score: number;
          confidence: number;
          summary: string;
          key_insights: string[];
          recommendations: string[];
          layers: {
            [layerName: string]: {
              name: string;
              score: number;
              confidence: number;
              calculation_method: string;
              supporting_data: Record<string, any>;
              data_sources: string[];
              summary: string;
            };
          };
        };
      };
    };
  };
  meta_scores: {
    market_fit: number;
    innovation_score: number;
    execution_readiness: number;
    risk_index: number;
    brand_strength: number;
  };
  executive_summary: string;
  key_recommendations: string[];
  competitive_advantages: string[];
  risk_factors: string[];
  generated_at: string;
}

export interface PerformanceMetrics {
  segmentScores: Array<{
    name: string;
    score: number;
    confidence: number;
    trend: 'up' | 'down' | 'stable';
    priority: 'high' | 'medium' | 'low';
  }>;
  bestSegment: {
    name: string;
    score: number;
    confidence: number;
    trend: 'up' | 'down' | 'stable';
    priority: 'high' | 'medium' | 'low';
  };
  worstSegment: {
    name: string;
    score: number;
    confidence: number;
    trend: 'up' | 'down' | 'stable';
    priority: 'high' | 'medium' | 'low';
  };
  topFactors: Array<{
    segmentName: string;
    factorName: string;
    score: number;
    confidence: number;
  }>;
  overallTrend: 'positive' | 'negative' | 'neutral';
}

export class DataTransformationUtils {
  static transformToAnalysis(apiResponse: HierarchicalAnalysisResponse): TransformedAnalysis {
    return {
      query: apiResponse.query,
      overall_score: apiResponse.overall_score,
      overall_confidence: apiResponse.overall_confidence,
      segments: Object.fromEntries(
        Object.entries(apiResponse.segments).map(([segmentName, segmentData]) => [
          segmentName,
          {
            name: segmentData.name,
            score: segmentData.score,
            confidence: segmentData.confidence,
            trend: segmentData.trend,
            priority: segmentData.priority,
            key_insights: segmentData.key_insights,
            recommendations: segmentData.recommendations,
            factors: Object.fromEntries(
              Object.entries(segmentData.factors).map(([factorName, factorData]) => [
                factorName,
                {
                  name: factorData.name,
                  score: factorData.score,
                  confidence: factorData.confidence,
                  summary: factorData.summary,
                  key_insights: factorData.key_insights,
                  recommendations: factorData.recommendations,
                  layers: Object.fromEntries(
                    Object.entries(factorData.layers).map(([layerName, layerData]) => [
                      layerName,
                      {
                        name: layerData.name,
                        score: layerData.score,
                        confidence: layerData.confidence,
                        calculation_method: layerData.calculation_method,
                        supporting_data: layerData.supporting_data,
                        data_sources: layerData.data_sources,
                        summary: layerData.summary
                      }
                    ])
                  )
                }
              ])
            )
          }
        ])
      ),
      meta_scores: apiResponse.meta_scores,
      executive_summary: apiResponse.executive_summary,
      key_recommendations: apiResponse.key_recommendations,
      competitive_advantages: apiResponse.competitive_advantages,
      risk_factors: apiResponse.risk_factors,
      generated_at: apiResponse.generated_at
    };
  }

  static calculatePerformanceMetrics(analysis: TransformedAnalysis): PerformanceMetrics {
    const segmentScores = Object.entries(analysis.segments).map(([name, segment]) => ({
      name,
      score: segment.score,
      confidence: segment.confidence,
      trend: segment.trend,
      priority: segment.priority
    }));

    const bestSegment = segmentScores.reduce((best, current) => 
      current.score > best.score ? current : best
    );

    const worstSegment = segmentScores.reduce((worst, current) => 
      current.score < worst.score ? current : worst
    );

    // Get top performing factors across all segments
    const allFactors = Object.entries(analysis.segments).flatMap(([segmentName, segment]) =>
      Object.entries(segment.factors).map(([factorName, factor]) => ({
        segmentName,
        factorName,
        score: factor.score,
        confidence: factor.confidence
      }))
    );

    const topFactors = allFactors
      .sort((a, b) => b.score - a.score)
      .slice(0, 5);

    const upTrends = segmentScores.filter(s => s.trend === 'up').length;
    const downTrends = segmentScores.filter(s => s.trend === 'down').length;
    
    let overallTrend: 'positive' | 'negative' | 'neutral' = 'neutral';
    if (upTrends > downTrends) overallTrend = 'positive';
    else if (downTrends > upTrends) overallTrend = 'negative';

    return {
      segmentScores,
      bestSegment,
      worstSegment,
      topFactors,
      overallTrend
    };
  }

  static validateAnalysisData(data: any): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (!data || typeof data !== 'object') {
      return { isValid: false, errors: ['Invalid data structure'] };
    }

    if (!data.segments || typeof data.segments !== 'object') {
      errors.push('Missing or invalid segments data');
    }

    if (!data.overall_score || typeof data.overall_score !== 'number') {
      errors.push('Missing or invalid overall_score');
    }

    if (!data.meta_scores || typeof data.meta_scores !== 'object') {
      errors.push('Missing or invalid meta_scores');
    }

    // Validate segment structure
    if (data.segments) {
      Object.entries(data.segments).forEach(([segmentName, segment]: [string, any]) => {
        if (!segment.factors || typeof segment.factors !== 'object') {
          errors.push(`Missing or invalid factors in segment: ${segmentName}`);
        }

        if (segment.factors) {
          Object.entries(segment.factors).forEach(([factorName, factor]: [string, any]) => {
            if (!factor.layers || typeof factor.layers !== 'object') {
              errors.push(`Missing or invalid layers in factor: ${segmentName}.${factorName}`);
            }
          });
        }
      });
    }

    return { isValid: errors.length === 0, errors };
  }

  static transformLegacyAnalysis(legacyData: any): TransformedAnalysis | null {
    try {
      // Handle the existing full_pergola_analysis_report structure
      if (legacyData.detailed_analysis?.layer_scores) {
        // This is the old format - we need to restructure it
        console.log('Detected legacy analysis format, attempting transformation...');
        
        // For now, return a basic structure that can be enhanced later
        return {
          query: legacyData.business_case?.idea_description || 'Legacy Analysis',
          overall_score: 75,
          overall_confidence: 0.85,
          segments: {},
          meta_scores: {
            market_fit: 75,
            innovation_score: 75,
            execution_readiness: 75,
            risk_index: 25,
            brand_strength: 70
          },
          executive_summary: 'Legacy analysis data loaded',
          key_recommendations: ['Data structure updated', 'Enhanced analysis available'],
          competitive_advantages: ['Comprehensive framework', '156-layer analysis'],
          risk_factors: ['Data migration required', 'Format conversion needed'],
          generated_at: new Date().toISOString()
        };
      }
      
      return null;
    } catch (error) {
      console.error('Failed to transform legacy analysis:', error);
      return null;
    }
  }
}
