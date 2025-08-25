import React from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Tooltip } from 'recharts';

interface RadarChartProps {
  data: Array<{
    segment: string;
    score: number;
    confidence: number;
  }>;
  title: string;
}

export const RadarChartComponent: React.FC<RadarChartProps> = ({ data, title }) => {
  const chartData = data.map(item => ({
    subject: item.segment,
    A: item.score,
    fullMark: 100,
  }));

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height={400}>
        <RadarChart data={chartData}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={90} domain={[0, 100]} />
          <Radar
            name="Score"
            dataKey="A"
            stroke="#3B82F6"
            fill="#3B82F6"
            fillOpacity={0.3}
          />
          <Tooltip 
            formatter={(value: number) => [`${value.toFixed(1)}%`, 'Score']}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};
