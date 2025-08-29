import React from 'react';
import { RadarChart as RechartsRadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from 'recharts';

interface Props {
  data: Array<{
    name: string;
    score: number;
    confidence?: number;
  }>;
  width?: number;
  height?: number;
  className?: string;
}

export const RadarChart: React.FC<Props> = ({ data, width = 400, height = 400, className = '' }) => {
  return (
    <div className={className} style={{ width, height }}>
      <ResponsiveContainer width="100%" height="100%">
        <RechartsRadarChart data={data}>
          <PolarGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.3)" />
          <PolarAngleAxis 
            dataKey="name" 
            tick={{ fontSize: 12, fill: 'currentColor' }}
            className="text-white"
          />
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 100]} 
            tick={{ fontSize: 10, fill: 'currentColor' }}
            tickCount={6}
          />
          <Radar
            name="Score"
            dataKey="score"
            stroke="rgba(255,255,255,0.8)"
            fill="rgba(255,255,255,0.2)"
            strokeWidth={2}
            dot={{ r: 4, fill: 'white' }}
          />
        </RechartsRadarChart>
      </ResponsiveContainer>
    </div>
  );
};
