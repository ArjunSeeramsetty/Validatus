import { PergolaAnalysis } from '../types/pergola';

export const exportAnalysisToJSON = (analysis: PergolaAnalysis) => {
  const dataStr = JSON.stringify(analysis, null, 2);
  const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
  
  const exportFileDefaultName = `validatus_analysis_${analysis.generated_at || new Date().toISOString()}.json`;
  
  const linkElement = document.createElement('a');
  linkElement.setAttribute('href', dataUri);
  linkElement.setAttribute('download', exportFileDefaultName);
  linkElement.click();
};

export const exportAnalysisToCSV = (analysis: PergolaAnalysis) => {
  // Convert analysis data to CSV format
  const csvData = [
    ['Metric', 'Value', 'Confidence', 'Trend', 'Priority'],
    ['Overall Score', analysis.overall_score, analysis.overall_confidence, '', ''],
    ['', '', '', '', ''],
    ['Segment', 'Score', 'Confidence', 'Trend', 'Priority']
  ];

  // Add segment data
  Object.entries(analysis.segments).forEach(([name, segment]) => {
    csvData.push([
      name,
      segment.score.toString(),
      segment.confidence.toString(),
      segment.trend,
      segment.priority
    ]);
  });

  csvData.push(['', '', '', '', '']);
  csvData.push(['Meta Scores', '', '', '', '']);

  // Add meta scores
  Object.entries(analysis.meta_scores).forEach(([name, score]) => {
    csvData.push([name, score.toString(), '', '', '']);
  });

  const csvContent = csvData.map(row => row.join(',')).join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  
  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `validatus_analysis_${analysis.generated_at || new Date().toISOString()}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
};

export const exportAnalysisToPDF = async (analysis: PergolaAnalysis) => {
  // This would require a PDF library like jsPDF
  // For now, we'll show a message that PDF export is coming soon
  alert('PDF export functionality is coming soon! For now, please use JSON or CSV export.');
};

export const getExportOptions = () => [
  { label: 'Export as JSON', action: exportAnalysisToJSON, icon: '📄' },
  { label: 'Export as CSV', action: exportAnalysisToCSV, icon: '📊' },
  { label: 'Export as PDF', action: exportAnalysisToPDF, icon: '📑' }
];
