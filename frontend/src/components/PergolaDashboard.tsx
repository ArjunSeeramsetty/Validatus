import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ChartBarIcon,
  ExclamationTriangleIcon,
  LightBulbIcon,
  ArrowLeftIcon,
  StarIcon
} from '@heroicons/react/24/outline';

import { PergolaAnalysis, DrillDownState, PerformanceMetrics } from '../types/pergola';
import { OverviewDashboard } from './OverviewDashboard';
import { SegmentDashboard } from './SegmentDashboard';
import { FactorDashboard } from './FactorDashboard';
import { LayerDashboard } from './LayerDashboard';
import { NavigationBreadcrumb } from './NavigationBreadcrumb';
import { PerformanceIndicators } from './PerformanceIndicators';

interface Props {
  data: PergolaAnalysis;
}

export const PergolaDashboard: React.FC<Props> = ({ data }) => {
  console.log('PergolaDashboard rendered with data:', data);
  console.log('PergolaDashboard: Data validation:', {
    hasData: !!data,
    hasSegments: !!data?.segments,
    segmentCount: Object.keys(data?.segments || {}).length,
    hasMetaScores: !!data?.meta_scores,
    metaScoreCount: Object.keys(data?.meta_scores || {}).length,
    overallScore: data?.overall_score,
    overallConfidence: data?.overall_confidence
  });
  
  // Add defensive checks
  if (!data || !data.segments) {
    console.error('PergolaDashboard: Missing required data:', data);
    return (
      <div className="text-center py-8">
        <p className="text-red-600">Error: Missing required data for dashboard</p>
        <pre className="text-xs mt-2 text-left bg-gray-100 p-2 rounded">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    );
  }

  const [drillDownState, setDrillDownState] = useState<DrillDownState>({
    level: 'overview',
    breadcrumb: [{ level: 'overview', name: 'Pergola Case Analysis', path: '/' }]
  });

  // Calculate best performing segments and factors
  const performanceMetrics = useMemo((): PerformanceMetrics => {
    console.log('Calculating performance metrics for segments:', Object.keys(data.segments));
    
    const segmentScores = Object.entries(data.segments).map(([name, segment]) => ({
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
    const allFactors = Object.entries(data.segments).flatMap(([segmentName, segment]) =>
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

    return {
      segmentScores,
      bestSegment,
      worstSegment,
      topFactors,
      overallTrend: segmentScores.filter(s => s.trend === 'up').length > 
                    segmentScores.filter(s => s.trend === 'down').length ? 'positive' : 'negative'
    };
  }, [data]);

  const handleDrillDown = (level: DrillDownState['level'], name: string, path?: string) => {
    console.log('Drilling down to:', level, name);
    const newBreadcrumb = [...drillDownState.breadcrumb];
    
    switch (level) {
      case 'segment':
        newBreadcrumb.push({ level: 'segment', name, path: `/segment/${name}` });
        setDrillDownState({
          level: 'segment',
          selectedSegment: name,
          breadcrumb: newBreadcrumb
        });
        break;
        
      case 'factor':
        newBreadcrumb.push({ level: 'factor', name, path: `/factor/${name}` });
        setDrillDownState({
          ...drillDownState,
          level: 'factor',
          selectedFactor: name,
          breadcrumb: newBreadcrumb
        });
        break;
        
      case 'layer':
        newBreadcrumb.push({ level: 'layer', name, path: `/layer/${name}` });
        setDrillDownState({
          ...drillDownState,
          level: 'layer',
          selectedLayer: name,
          breadcrumb: newBreadcrumb
        });
        break;
    }
  };

  const handleNavigateBack = (targetIndex?: number) => {
    console.log('Navigating back to index:', targetIndex);
    const targetBreadcrumb = targetIndex !== undefined 
      ? drillDownState.breadcrumb.slice(0, targetIndex + 1)
      : drillDownState.breadcrumb.slice(0, -1);
    
    const lastItem = targetBreadcrumb[targetBreadcrumb.length - 1];
    
    setDrillDownState({
      level: lastItem.level as DrillDownState['level'],
      selectedSegment: lastItem.level === 'segment' || lastItem.level === 'factor' || lastItem.level === 'layer' 
        ? drillDownState.selectedSegment : undefined,
      selectedFactor: lastItem.level === 'factor' || lastItem.level === 'layer' 
        ? drillDownState.selectedFactor : undefined,
      selectedLayer: lastItem.level === 'layer' ? drillDownState.selectedLayer : undefined,
      breadcrumb: targetBreadcrumb
    });
  };

  const getCurrentData = () => {
    switch (drillDownState.level) {
      case 'segment':
        return data.segments[drillDownState.selectedSegment!];
      case 'factor':
        return data.segments[drillDownState.selectedSegment!]?.factors[drillDownState.selectedFactor!];
      case 'layer':
        return data.segments[drillDownState.selectedSegment!]?.factors[drillDownState.selectedFactor!]?.layers[drillDownState.selectedLayer!];
      default:
        return data;
    }
  };

  console.log('Current drill down state:', drillDownState);
  console.log('Current data:', getCurrentData());

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
                <p className="text-sm text-gray-500">Pergola Case Study Dashboard</p>
              </div>
            </div>
            
            <PerformanceIndicators 
              overallScore={data.overall_score}
              trend={performanceMetrics.overallTrend}
              confidence={data.overall_confidence}
            />
          </div>
        </div>
      </div>

      {/* Navigation Breadcrumb */}
      <NavigationBreadcrumb 
        breadcrumb={drillDownState.breadcrumb}
        onNavigate={handleNavigateBack}
      />

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <AnimatePresence mode="wait">
          <motion.div
            key={drillDownState.level}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            {drillDownState.level === 'overview' && (
              <OverviewDashboard 
                data={data}
                performanceMetrics={performanceMetrics}
                onDrillDown={handleDrillDown}
              />
            )}
            
            {drillDownState.level === 'segment' && drillDownState.selectedSegment && (
              <SegmentDashboard
                segment={data.segments[drillDownState.selectedSegment]}
                segmentName={drillDownState.selectedSegment}
                onDrillDown={handleDrillDown}
                onBack={() => handleNavigateBack()}
              />
            )}
            
            {drillDownState.level === 'factor' && drillDownState.selectedFactor && (
              <FactorDashboard
                factor={data.segments[drillDownState.selectedSegment!].factors[drillDownState.selectedFactor]}
                factorName={drillDownState.selectedFactor}
                segmentName={drillDownState.selectedSegment!}
                onDrillDown={handleDrillDown}
                onBack={() => handleNavigateBack()}
              />
            )}
            
            {drillDownState.level === 'layer' && drillDownState.selectedLayer && (
              <LayerDashboard
                layer={data.segments[drillDownState.selectedSegment!].factors[drillDownState.selectedFactor!].layers[drillDownState.selectedLayer]}
                layerName={drillDownState.selectedLayer}
                factorName={drillDownState.selectedFactor!}
                segmentName={drillDownState.selectedSegment!}
                onBack={() => handleNavigateBack()}
              />
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
};
