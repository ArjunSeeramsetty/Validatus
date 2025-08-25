from typing import Dict, Any, List
import openai
from ..core.state import LayerScoreResult, FactorScoreResult
from config import settings

class ScoreAggregator:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Define weights for different factors based on strategic importance
        self.factor_weights = {
            "CONSUMER": {
                "Consumer Demand & Need": 0.25,
                "Consumer Behavior & Habits": 0.20,
                "Consumer Loyalty & Retention": 0.20,
                "Consumer Perception & Sentiment": 0.20,
                "Consumer Adoption & Engagement": 0.15
            },
            "MARKET": {
                "Market Size & Growth": 0.30,
                "Market Trends & Opportunities": 0.25,
                "Competitive Landscape": 0.25,
                "Regulatory Environment": 0.10,
                "Market Risks & Challenges": 0.10
            },
            "PRODUCT": {
                "Features & Functionality": 0.25,
                "Innovation & Differentiation": 0.30,
                "Value Proposition": 0.25,
                "Business Resilience": 0.15,
                "Product Quality & Assurance": 0.05
            },
            "BRAND": {
                "Brand Awareness & Recognition": 0.20,
                "Brand Equity Profile": 0.25,
                "Brand Positioning Strategy": 0.25,
                "Brand Messaging & Communication": 0.15,
                "Brand Monetization Model": 0.15
            },
            "EXPERIENCE": {
                "User Experience (UX) & Design": 0.30,
                "Customer Journey Mapping": 0.25,
                "Customer Support & Service": 0.20,
                "Post-Purchase Loyalty & Advocacy": 0.15,
                "Customer Engagement & Community": 0.10
            }
        }

    async def aggregate_factors(self, layer_scores: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate layer scores into factor scores with proper weighting"""
        factor_scores = {}
        
        for segment, factors in layer_scores.items():
            factor_scores[segment] = {}
            
            for factor, layers in factors.items():
                valid_layers = [l for l in layers.values() if "error" not in l and l.get("score") is not None]
                
                if not valid_layers:
                    # If no valid layers, create a default factor score
                    factor_scores[segment][factor] = FactorScoreResult(
                        score=50.0,
                        confidence=0.0,
                        summary=f"No valid data available for {factor}"
                    )
                    continue
                
                # Calculate weighted average score
                weighted_score = 0
                total_weight = 0
                total_confidence = 0
                
                for layer_name, layer_data in layers.items():
                    if "error" not in layer_data and layer_data.get("score") is not None:
                        # Use confidence as weight for individual layers
                        weight = layer_data.get("confidence", 0.5)
                        weighted_score += layer_data["score"] * weight
                        total_weight += weight
                        total_confidence += layer_data.get("confidence", 0.5)
                
                if total_weight > 0:
                    avg_score = weighted_score / total_weight
                    avg_confidence = total_confidence / len(valid_layers)
                else:
                    avg_score = 50.0
                    avg_confidence = 0.0
                
                # Generate summary for the factor
                summary = await self._summarize_layers(factor, layers)
                
                factor_scores[segment][factor] = FactorScoreResult(
                    score=round(avg_score, 2),
                    confidence=round(avg_confidence, 2),
                    summary=summary
                )
        
        return factor_scores

    async def aggregate_segments(self, factor_scores: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate factor scores into segment scores with strategic weighting"""
        segment_scores = {}
        
        for segment, factors in factor_scores.items():
            valid_factors = [f for f in factors.values() if "error" not in f and f.get("score") is not None]
            
            if not valid_factors:
                segment_scores[segment] = {
                    "score": 50.0,
                    "confidence": 0.0,
                    "summary": f"No valid data available for {segment} segment"
                }
                continue

            # Apply strategic weights to factors
            weighted_score = 0
            total_weight = 0
            total_confidence = 0
            
            segment_weights = self.factor_weights.get(segment, {})
            
            for factor_name, factor_data in factors.items():
                if "error" not in factor_data and factor_data.get("score") is not None:
                    # Get weight for this factor, default to equal weight if not specified
                    weight = segment_weights.get(factor_name, 1.0)
                    
                    weighted_score += factor_data["score"] * weight
                    total_weight += weight
                    total_confidence += factor_data.get("confidence", 0.5)
            
            if total_weight > 0:
                avg_score = weighted_score / total_weight
                avg_confidence = total_confidence / len(valid_factors)
            else:
                avg_score = 50.0
                avg_confidence = 0.0
            
            # Generate comprehensive summary for the segment
            summary = await self._summarize_factors(segment, factors)
            
            # Calculate segment-specific insights
            insights = await self._generate_segment_insights(segment, factors, avg_score)
            
            segment_scores[segment] = {
                "score": round(avg_score, 2),
                "confidence": round(avg_confidence, 2),
                "summary": summary,
                "insights": insights,
                "factor_count": len(valid_factors),
                "weighted_average": True
            }
        
        return segment_scores

    async def _summarize_layers(self, factor_name: str, layers: Dict[str, Any]) -> str:
        """Generate a comprehensive summary for a factor based on its layers"""
        try:
            valid_layers = [(name, data) for name, data in layers.items() if "error" not in data and data.get("score") is not None]
            
            if not valid_layers:
                return f"No valid data available for {factor_name}"
            
            # Create a structured summary
            layer_summaries = []
            for layer_name, layer_data in valid_layers:
                score = layer_data.get("score", "N/A")
                confidence = layer_data.get("confidence", "N/A")
                method = layer_data.get("calculation_method", "unknown")
                layer_summaries.append(f"{layer_name}: {score}/100 (confidence: {confidence:.2f}, method: {method})")
            
            prompt = f"""
            Summarize the following analysis for the factor '{factor_name}':
            
            Layer Analysis:
            {chr(10).join(layer_summaries)}
            
            Provide a concise, one-sentence summary that captures the overall assessment of this factor.
            """
            
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Summary generation failed: {str(e)}"

    async def _summarize_factors(self, segment_name: str, factors: Dict[str, Any]) -> str:
        """Generate a comprehensive summary for a segment based on its factors"""
        try:
            valid_factors = [f for f in factors.values() if "error" not in f and f.get("score") is not None]
            
            if not valid_factors:
                return f"No valid data available for {segment_name} segment"
            
            # Create a structured summary
            factor_summaries = []
            for factor_name, factor_data in valid_factors:
                score = factor_data.get("score", "N/A")
                confidence = factor_data.get("confidence", "N/A")
                factor_summaries.append(f"{factor_name}: {score}/100 (confidence: {confidence:.2f})")
            
            prompt = f"""
            Summarize the following analysis for the segment '{segment_name}':
            
            Factor Analysis:
            {chr(10).join(factor_summaries)}
            
            Provide a concise, one-sentence summary of the overall segment performance.
            """
            
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Summary generation failed: {str(e)}"

    async def _generate_segment_insights(self, segment_name: str, factors: Dict[str, Any], avg_score: float) -> List[str]:
        """Generate strategic insights for a segment based on its performance"""
        try:
            # Identify top and bottom performing factors
            valid_factors = [(name, data) for name, data in factors.items() if "error" not in data and data.get("score") is not None]
            
            if not valid_factors:
                return ["Insufficient data for insights generation"]
            
            # Sort factors by score
            sorted_factors = sorted(valid_factors, key=lambda x: x[1].get("score", 0), reverse=True)
            
            top_factors = sorted_factors[:2]  # Top 2 factors
            bottom_factors = sorted_factors[-2:]  # Bottom 2 factors
            
            insights = []
            
            # Generate insights based on performance
            if avg_score >= 75:
                insights.append(f"Strong performance in {segment_name} segment with excellent scores across multiple factors")
            elif avg_score >= 60:
                insights.append(f"Good performance in {segment_name} segment with room for improvement in specific areas")
            else:
                insights.append(f"Performance in {segment_name} segment needs attention, particularly in lower-scoring factors")
            
            # Add specific factor insights
            if top_factors:
                top_names = [f[0] for f in top_factors]
                insights.append(f"Strengths: {', '.join(top_names)} are performing exceptionally well")
            
            if bottom_factors:
                bottom_names = [f[0] for f in bottom_factors]
                insights.append(f"Areas for improvement: {', '.join(bottom_names)} need attention")
            
            return insights
            
        except Exception as e:
            return [f"Insights generation failed: {str(e)}"]

    async def calculate_overall_score(self, segment_scores: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate the overall platform score and strategic assessment"""
        try:
            valid_segments = [s for s in segment_scores.values() if "error" not in s and s.get("score") is not None]
            
            if not valid_segments:
                return {
                    "overall_score": 50.0,
                    "confidence": 0.0,
                    "assessment": "Insufficient data for overall assessment",
                    "segment_count": 0
                }
            
            # Calculate weighted overall score (all segments equally weighted for now)
            total_score = sum(segment.get("score", 50) for segment in valid_segments)
            total_confidence = sum(segment.get("confidence", 0) for segment in valid_segments)
            
            overall_score = total_score / len(valid_segments)
            overall_confidence = total_confidence / len(valid_segments)
            
            # Generate strategic assessment
            assessment = await self._generate_strategic_assessment(segment_scores, overall_score)
            
            return {
                "overall_score": round(overall_score, 2),
                "confidence": round(overall_confidence, 2),
                "assessment": assessment,
                "segment_count": len(valid_segments),
                "segment_breakdown": {
                    name: {
                        "score": data.get("score", 0),
                        "confidence": data.get("confidence", 0)
                    }
                    for name, data in segment_scores.items()
                }
            }
            
        except Exception as e:
            return {
                "overall_score": 50.0,
                "confidence": 0.0,
                "assessment": f"Overall score calculation failed: {str(e)}",
                "segment_count": 0
            }

    async def _generate_strategic_assessment(self, segment_scores: Dict[str, Any], overall_score: float) -> str:
        """Generate a strategic assessment based on overall performance"""
        try:
            prompt = f"""
            Based on the following segment scores and overall score of {overall_score}/100, provide a strategic assessment:
            
            Segment Scores:
            {chr(10).join([f"- {name}: {data.get('score', 'N/A')}/100" for name, data in segment_scores.items()])}
            
            Provide a concise, strategic assessment in 2-3 sentences that includes:
            1. Overall performance evaluation
            2. Key strengths and weaknesses
            3. Strategic recommendations
            """
            
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Strategic assessment generation failed: {str(e)}"
