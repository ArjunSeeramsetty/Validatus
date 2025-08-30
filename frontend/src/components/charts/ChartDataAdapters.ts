import { TransformedAnalysis } from '../../utils/dataTransformation';

export class ChartDataAdapters {
  static prepareSegmentRadarData(analysis: TransformedAnalysis) {
    return Object.entries(analysis.segments).map(([name, segment]) => ({
      name: name.replace('_', ' ').toUpperCase(),
      score: segment.score,
      confidence: segment.confidence * 100,
      trend: segment.trend,
      priority: segment.priority
    }));
  }

  static prepareFactorBarData(segmentName: string, analysis: TransformedAnalysis) {
    const segment = analysis.segments[segmentName];
    if (!segment) return [];

    return Object.entries(segment.factors).map(([name, factor]) => ({
      name: name.replace(/_/g, ' '),
      score: factor.score,
      confidence: factor.confidence * 100
    }));
  }

  static prepareLayerScatterData(segmentName: string, factorName: string, analysis: TransformedAnalysis) {
    const factor = analysis.segments[segmentName]?.factors[factorName];
    if (!factor) return [];

    return Object.entries(factor.layers).map(([name, layer]) => ({
      name: name.replace(/_/g, ' '),
      score: layer.score,
      confidence: layer.confidence * 100,
      x: layer.score,
      y: layer.confidence * 100
    }));
  }

  static prepareMetaScoresData(analysis: TransformedAnalysis) {
    return Object.entries(analysis.meta_scores).map(([name, score]) => ({
      name: name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      score: score,
      fullMark: 100
    }));
  }

  static prepareHierarchyTreeData(analysis: TransformedAnalysis) {
    return {
      name: 'Strategic Analysis',
      children: Object.entries(analysis.segments).map(([segmentName, segment]) => ({
        name: segment.name,
        score: segment.score,
        children: Object.entries(segment.factors).map(([factorName, factor]) => ({
          name: factor.name,
          score: factor.score,
          children: Object.entries(factor.layers).map(([layerName, layer]) => ({
            name: layer.name,
            score: layer.score,
            size: layer.confidence * 100
          }))
        }))
      }))
    };
  }

  static prepareSegmentComparisonData(analysis: TransformedAnalysis) {
    const segments = Object.entries(analysis.segments);
    return {
      labels: segments.map(([name, segment]) => segment.name),
      datasets: [
        {
          label: 'Segment Scores',
          data: segments.map(([name, segment]) => segment.score),
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        },
        {
          label: 'Confidence Levels',
          data: segments.map(([name, segment]) => segment.confidence * 100),
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }
      ]
    };
  }

  static prepareFactorHeatmapData(segmentName: string, analysis: TransformedAnalysis) {
    const segment = analysis.segments[segmentName];
    if (!segment) return [];

    return Object.entries(segment.factors).map(([factorName, factor]) => ({
      factor: factor.name,
      score: factor.score,
      confidence: factor.confidence,
      layerCount: Object.keys(factor.layers).length,
      avgLayerScore: Object.values(factor.layers).reduce((sum, layer) => sum + layer.score, 0) / Object.keys(factor.layers).length
    }));
  }

  static prepareTrendAnalysisData(analysis: TransformedAnalysis) {
    const segments = Object.entries(analysis.segments);
    const trends = {
      up: segments.filter(([name, segment]) => segment.trend === 'up').length,
      down: segments.filter(([name, segment]) => segment.trend === 'down').length,
      stable: segments.filter(([name, segment]) => segment.trend === 'stable').length
    };

    return [
      { name: 'Upward Trend', value: trends.up, color: '#10B981' },
      { name: 'Downward Trend', value: trends.down, color: '#EF4444' },
      { name: 'Stable', value: trends.stable, color: '#6B7280' }
    ];
  }

  static preparePriorityMatrixData(analysis: TransformedAnalysis) {
    const segments = Object.entries(analysis.segments);
    const priorities = {
      high: segments.filter(([name, segment]) => segment.priority === 'high').length,
      medium: segments.filter(([name, segment]) => segment.priority === 'medium').length,
      low: segments.filter(([name, segment]) => segment.priority === 'low').length
    };

    return [
      { name: 'High Priority', value: priorities.high, color: '#DC2626' },
      { name: 'Medium Priority', value: priorities.medium, color: '#F59E0B' },
      { name: 'Low Priority', value: priorities.low, color: '#10B981' }
    ];
  }
}
