import React from 'react';

interface RadarData {
  name: string;
  score: number;
  confidence?: number;
  trend?: string;
  priority?: string;
}

interface Props {
  data: RadarData[];
  width?: number;
  height?: number;
  className?: string;
}

export const RadarChart: React.FC<Props> = ({ 
  data, 
  width = 300, 
  height = 300,
  className = ''
}) => {
  if (!data || data.length === 0) {
    return (
      <div className={`flex items-center justify-center ${className}`} style={{ width, height }}>
        <p className="text-gray-500">No data available</p>
      </div>
    );
  }

  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(width, height) * 0.35;
  const numPoints = data.length;
  const angleStep = (2 * Math.PI) / numPoints;

  // Generate polygon points
  const polygonPoints = data.map((item, index) => {
    const angle = index * angleStep - Math.PI / 2; // Start from top
    const scoreRadius = (item.score / 100) * radius;
    const x = centerX + scoreRadius * Math.cos(angle);
    const y = centerY + scoreRadius * Math.sin(angle);
    return `${x},${y}`;
  }).join(' ');

  // Generate axis lines
  const axisLines = data.map((item, index) => {
    const angle = index * angleStep - Math.PI / 2;
    const x1 = centerX;
    const y1 = centerY;
    const x2 = centerX + radius * Math.cos(angle);
    const y2 = centerY + radius * Math.sin(angle);
    
    return (
      <line
        key={`axis-${index}`}
        x1={x1}
        y1={y1}
        x2={x2}
        y2={y2}
        stroke="#E5E7EB"
        strokeWidth="1"
      />
    );
  });

  // Generate concentric circles
  const circles = [25, 50, 75, 100].map(percentage => {
    const circleRadius = (percentage / 100) * radius;
    return (
      <circle
        key={`circle-${percentage}`}
        cx={centerX}
        cy={centerY}
        r={circleRadius}
        fill="none"
        stroke="#E5E7EB"
        strokeWidth="1"
        strokeDasharray="2,2"
      />
    );
  });

  // Generate labels
  const labels = data.map((item, index) => {
    const angle = index * angleStep - Math.PI / 2;
    const labelRadius = radius + 20;
    const x = centerX + labelRadius * Math.cos(angle);
    const y = centerY + labelRadius * Math.sin(angle);
    
    // Adjust text anchor and alignment based on position
    let textAnchor: "start" | "middle" | "end" = 'middle';
    let dominantBaseline: "auto" | "middle" | "hanging" = 'middle';
    
    if (Math.abs(Math.cos(angle)) < 0.1) {
      // Top or bottom
      textAnchor = 'middle';
      dominantBaseline = angle > 0 ? 'hanging' : 'middle';
    } else if (Math.cos(angle) > 0) {
      // Right side
      textAnchor = 'start';
      dominantBaseline = 'middle';
    } else {
      // Left side
      textAnchor = 'end';
      dominantBaseline = 'middle';
    }

    return (
      <text
        key={`label-${index}`}
        x={x}
        y={y}
        textAnchor={textAnchor}
        dominantBaseline={dominantBaseline}
        className="text-xs font-medium fill-gray-600"
      >
        {item.name}
      </text>
    );
  });

  return (
    <div className={`${className}`} style={{ width, height }}>
      <svg width={width} height={height} className="w-full h-full">
        {/* Background circles */}
        {circles}
        
        {/* Axis lines */}
        {axisLines}
        
        {/* Data polygon */}
        <polygon
          points={polygonPoints}
          fill="rgba(59, 130, 246, 0.1)"
          stroke="rgb(59, 130, 246)"
          strokeWidth="2"
          fillOpacity="0.3"
        />
        
        {/* Data points */}
        {data.map((item, index) => {
          const angle = index * angleStep - Math.PI / 2;
          const scoreRadius = (item.score / 100) * radius;
          const x = centerX + scoreRadius * Math.cos(angle);
          const y = centerY + scoreRadius * Math.sin(angle);
          
          return (
            <circle
              key={`point-${index}`}
              cx={x}
              cy={y}
              r="4"
              fill="rgb(59, 130, 246)"
              stroke="white"
              strokeWidth="2"
            />
          );
        })}
        
        {/* Labels */}
        {labels}
        
        {/* Center point */}
        <circle
          cx={centerX}
          cy={centerY}
          r="3"
          fill="rgb(59, 130, 246)"
        />
      </svg>
    </div>
  );
};
