import React from 'react';
import { motion } from 'framer-motion';
import {
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  ExclamationTriangleIcon,
  LightBulbIcon,
  StarIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

import { PergolaAnalysis, PerformanceMetrics } from '../types/pergola';
import { RadarChart } from './charts/RadarChart';
import { MetricCard } from './charts/MetricCard';
import { SegmentCard } from './SegmentCard';
import { InsightsPanel } from './InsightsPanel';
import { RecommendationsPanel } from './RecommendationsPanel';

interface Props {
  data: PergolaAnalysis;
  performanceMetrics: PerformanceMetrics;
  onDrillDown: (level: 'segment', name: string) => void;
}

export const OverviewDashboard: React.FC<Props> = ({ 
  data, 
  performanceMetrics, 
  onDrillDown 
}) => {
  const segmentData = Object.entries(data.segments).map(([name, segment]) => ({
    name: name.replace('_', ' ').toUpperCase(),
    score: segment.score,
    confidence: segment.confidence,
    trend: segment.trend,
    priority: segment.priority
  }));

  const metaScoresData = Object.entries(data.meta_scores).map(([name, score]) => ({
    name: name.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
    score: score,
    icon: getMetaScoreIcon(name)
  }));

  return (
    <div className="space-y-6">
      {/* Hero Section with Overall Score */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl shadow-xl p-8 text-white"
      >
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <div>
            <h2 className="text-3xl font-bold mb-2">Strategic Analysis Overview</h2>
            <p className="text-blue-100 mb-6 text-lg">
              {data.query}
            </p>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white/10 rounded-lg p-4 backdrop-blur-sm">
                <div className="text-4xl font-bold mb-1">
                  {Math.round(data.overall_score)}%
                </div>
                <div className="text-blue-100 text-sm">Overall Score</div>
              </div>
              <div className="bg-white/10 rounded-lg p-4 backdrop-blur-sm">
                <div className="text-4xl font-bold mb-1">
                  {Math.round(data.overall_confidence * 100)}%
                </div>
                <div className="text-blue-100 text-sm">Confidence</div>
              </div>
            </div>
          </div>
          
          <div className="flex justify-center">
            <RadarChart 
              data={segmentData}
              width={300}
              height={300}
              className="text-white"
            />
          </div>
        </div>
      </motion.div>

      {/* Meta Scores */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {metaScoresData.map((metric, index) => (
          <motion.div
            key={metric.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <MetricCard
              title={metric.name}
              value={Math.round(metric.score)}
              unit="%"
              icon={metric.icon}
              trend={metric.score > 70 ? 'up' : metric.score < 40 ? 'down' : 'stable'}
              className="h-full"
            />
          </motion.div>
        ))}
      </div>

      {/* Segment Performance */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-gray-900">Segment Performance</h3>
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <span>Click to drill down</span>
                <ChartBarIcon className="h-4 w-4" />
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(data.segments).map(([segmentName, segment], index) => (
                <motion.div
                  key={segmentName}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <SegmentCard
                    segment={segment}
                    segmentName={segmentName}
                    onClick={() => onDrillDown('segment', segmentName)}
                    isClickable={true}
                  />
                </motion.div>
              ))}
            </div>
          </div>
        </div>

        {/* Key Insights */}
        <div className="space-y-6">
          <InsightsPanel
            insights={[
              `Best performing segment: ${performanceMetrics.bestSegment.name} (${Math.round(performanceMetrics.bestSegment.score)}%)`,
              `Highest confidence area: ${performanceMetrics.topFactors[0]?.factorName || 'N/A'}`,
              `Overall trend: ${performanceMetrics.overallTrend === 'positive' ? 'Positive momentum' : 'Needs attention'}`,
              ...(data.competitive_advantages?.slice(0, 2) || [])
            ]}
          />
          
          <RecommendationsPanel
            recommendations={data.key_recommendations?.slice(0, 3) || []}
            riskFactors={data.risk_factors?.slice(0, 2) || []}
          />
        </div>
      </div>

      {/* Executive Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="bg-white rounded-xl shadow-lg p-6"
      >
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
          <LightBulbIcon className="h-6 w-6 text-yellow-500 mr-2" />
          Executive Summary
        </h3>
        <p className="text-gray-700 leading-relaxed">{data.executive_summary}</p>
        
        <div className="mt-6 flex items-center justify-between text-sm text-gray-500">
          <span>Analysis completed: {new Date(data.generated_at).toLocaleString()}</span>
          <div className="flex items-center space-x-4">
            <span className="flex items-center">
              <StarIcon className="h-4 w-4 text-yellow-400 mr-1" />
              Confidence: {Math.round(data.overall_confidence * 100)}%
            </span>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

function getMetaScoreIcon(name: string) {
  const iconMap: Record<string, React.ComponentType<any>> = {
    'market_fit': ChartBarIcon,
    'innovation_score': LightBulbIcon,
    'execution_readiness': ArrowTrendingUpIcon,
    'risk_index': ExclamationTriangleIcon,
    'brand_strength': StarIcon
  };
  
  return iconMap[name] || ChartBarIcon;
}
