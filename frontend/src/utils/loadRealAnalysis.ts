import { PergolaAnalysis } from '../types/pergola';

export const loadRealPergolaAnalysis = async (): Promise<PergolaAnalysis> => {
  try {
    // Try to load from the public directory first
    const response = await fetch('/real-pergola-analysis.json');
    if (response.ok) {
      return await response.json();
    }
    
    // Fallback to src/data directory
    const moduleResponse = await fetch('/src/data/real-pergola-analysis.json');
    if (moduleResponse.ok) {
      return await moduleResponse.json();
    }
    
    throw new Error('Real analysis file not found');
  } catch (error) {
    console.error('Failed to load real analysis:', error);
    throw error;
  }
};

// Alternative: Import the JSON directly (works in some bundlers)
export const getRealAnalysisData = (): PergolaAnalysis => {
  // This would be the actual data structure from the backend
  // For now, we'll return a placeholder that matches the expected structure
  return {
    query: "Strategic analysis for premium outdoor pergola business targeting homeowners in North America",
    overall_score: 78.5,
    overall_confidence: 0.85,
    segments: {},
    meta_scores: {
      market_fit: 78.5,
      innovation_score: 81.2,
      execution_readiness: 75.8,
      risk_index: 32.1,
      brand_strength: 71.4
    },
    executive_summary: "This analysis demonstrates strong strategic viability with comprehensive coverage of all strategic dimensions.",
    key_recommendations: [
      "Focus on premium positioning strategy",
      "Invest in brand building through digital marketing",
      "Develop intellectual property protection",
      "Maintain customer experience excellence"
    ],
    competitive_advantages: [
      "Premium product quality with innovative features",
      "Exceptional customer experience",
      "Strong market demand alignment"
    ],
    risk_factors: [
      "Brand awareness below category leaders",
      "Seasonal demand patterns",
      "Premium pricing strategy limitations"
    ],
    generated_at: "2025-08-29T12:48:37Z"
  };
};
