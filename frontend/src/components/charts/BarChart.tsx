import React from 'react';
import { BarChart as RechartsBarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface Props {
  data: Array<{
    name: string;
    score: number;
    confidence?: number;
  }>;
  height?: number;
  onBarClick?: (data: any) => void;
}

export const BarChart: React.FC<Props> = ({ data, height = 300, onBarClick }) => {
  const colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];

  return (
    <div style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <RechartsBarChart data={data} onClick={onBarClick}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis 
            dataKey="name" 
            tick={{ fontSize: 12 }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis 
            tick={{ fontSize: 12 }}
            domain={[0, 100]}
          />
          <Tooltip
            formatter={(value: number, name: string) => [`${Math.round(value)}%`, name]}
            labelFormatter={(label) => `Factor: ${label}`}
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #E5E7EB',
              borderRadius: '8px',
              boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
            }}
          />
          <Bar 
            dataKey="score" 
            radius={[4, 4, 0, 0]}
            cursor="pointer"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Bar>
        </RechartsBarChart>
      </ResponsiveContainer>
    </div>
  );
};
