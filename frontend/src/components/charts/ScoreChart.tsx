import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface ScoreChartProps {
  data: Array<{
    name: string;
    score: number;
    confidence: number;
  }>;
  title: string;
  color?: string;
}

export const ScoreChart: React.FC<ScoreChartProps> = ({ data, title, color = "#3B82F6" }) => {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis domain={[0, 100]} />
          <Tooltip 
            formatter={(value: number) => [`${value.toFixed(1)}%`, 'Score']}
            labelFormatter={(label: string) => `${label}`}
          />
          <Bar dataKey="score" fill={color} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
