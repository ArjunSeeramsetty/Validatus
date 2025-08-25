import asyncio
import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from .base_agent import BaseResearchAgent
from config import settings

class PerplexityResearchAgent(BaseResearchAgent):
    """Production-ready Perplexity research agent with comprehensive search capabilities"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.perplexity.ai"
        self.api_key = settings.PERPLEXITY_API_KEY
        
        # Model selection based on use case
        self.model_mapping = {
            "quick_search": "sonar",
            "detailed_analysis": "sonar-pro",
            "reasoning_task": "sonar-reasoning-pro",
            "deep_research": "sonar-deep-research"
        }
        
    async def research(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct comprehensive research using Perplexity's real-time search"""
        try:
            # Determine research approach based on query complexity
            research_type = self._determine_research_type(query, context)
            
            # Execute multiple Perplexity searches with different models
            research_tasks = [
                self._perplexity_search(query, "quick_search", context),
                self._perplexity_search(query, "detailed_analysis", context),
                self._perplexity_follow_up_questions(query, context),
                self._perplexity_domain_specific_search(query, context)
            ]
            
            results = await asyncio.gather(*research_tasks, return_exceptions=True)
            
            # Synthesize results
            synthesized_data = self._synthesize_perplexity_results(results, query)
            
            return {
                "quick_search": results[0] if not isinstance(results[0], Exception) else {"error": str(results[0])},
                "detailed_analysis": results[1] if not isinstance(results[1], Exception) else {"error": str(results[1])},
                "follow_up_questions": results[2] if not isinstance(results[2], Exception) else {"error": str(results[2])},
                "domain_specific": results[3] if not isinstance(results[3], Exception) else {"error": str(results[3])},
                "synthesized_insights": synthesized_data,
                "timestamp": datetime.utcnow().isoformat(),
                "confidence": self._calculate_perplexity_confidence(results),
                "citation_count": self._count_citations(results),
                "source_diversity": self._analyze_source_diversity(results)
            }
            
        except Exception as e:
            return {"error": str(e), "confidence": 0.0}

    async def _perplexity_search(self, query: str, search_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Perplexity search with specific model and parameters"""
        try:
            model = self.model_mapping[search_type]
            
            # Customize search parameters based on context
            search_params = self._build_search_parameters(query, context, search_type)
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": [
                            {
                                "role": "system",
                                "content": self._get_system_prompt(search_type, context)
                            },
                            {
                                "role": "user", 
                                "content": search_params["enhanced_query"]
                            }
                        ],
                        "temperature": search_params.get("temperature", 0.2),
                        "max_tokens": search_params.get("max_tokens", 2000),
                        "search_domain_filter": search_params.get("domain_filter", []),
                        "search_recency_filter": search_params.get("recency_filter", "month"),
                        "return_related_questions": True,
                        "return_citations": True
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                
                return self._process_perplexity_response(result, search_type)
                
        except Exception as e:
            return {"error": f"Perplexity {search_type} search failed: {str(e)}"}

    def _build_search_parameters(self, query: str, context: Dict[str, Any], search_type: str) -> Dict[str, Any]:
        """Build optimized search parameters for different search types"""
        industry = context.get("industry", "").lower()
        geography = context.get("geography", [])
        
        # Base parameters
        params = {
            "enhanced_query": query,
            "temperature": 0.2,
            "max_tokens": 1500,
            "domain_filter": [],
            "recency_filter": "month"
        }
        
        # Customize based on search type
        if search_type == "quick_search":
            params.update({
                "enhanced_query": f"Quick overview: {query}",
                "max_tokens": 800,
                "recency_filter": "week"
            })
            
        elif search_type == "detailed_analysis":
            params.update({
                "enhanced_query": f"Comprehensive analysis with market data: {query}",
                "max_tokens": 2500,
                "temperature": 0.1
            })
            
        elif search_type == "domain_specific":
            # Add domain-specific search filters
            domain_filters = self._get_domain_filters(industry)
            params["domain_filter"] = domain_filters
            params["enhanced_query"] = f"{industry} industry analysis: {query}"
        
        # Add geography-specific context
        if geography:
            geo_context = ", ".join(geography)
            params["enhanced_query"] += f" in {geo_context}"
        
        return params

    def _get_domain_filters(self, industry: str) -> List[str]:
        """Get trusted domain filters based on industry"""
        domain_mapping = {
            "technology": [
                "techcrunch.com", "wired.com", "arstechnica.com", 
                "theverge.com", "ieee.org", "acm.org"
            ],
            "healthcare": [
                "nejm.org", "thelancet.com", "bmj.com", 
                "pubmed.ncbi.nlm.nih.gov", "who.int"
            ],
            "finance": [
                "bloomberg.com", "reuters.com", "wsj.com",
                "ft.com", "economist.com", "sec.gov"
            ],
            "automotive": [
                "automotive-world.com", "wardsauto.com", 
                "autonews.com", "just-auto.com"
            ],
            "retail": [
                "retaildive.com", "chain-store-age.com",
                "nrf.com", "retailwire.com"
            ]
        }
        
        return domain_mapping.get(industry, [
            # Default trusted sources
            "reuters.com", "bloomberg.com", "wsj.com", 
            "economist.com", "mckinsey.com", "bcg.com"
        ])

    def _get_system_prompt(self, search_type: str, context: Dict[str, Any]) -> str:
        """Get optimized system prompts for different search types"""
        industry = context.get("industry", "general business")
        
        prompts = {
            "quick_search": f"""You are a strategic business analyst specializing in {industry}. 
            Provide a concise, factual overview with key metrics and recent developments. 
            Focus on the most important and current information.""",
            
            "detailed_analysis": f"""You are a senior strategy consultant with deep expertise in {industry}. 
            Provide a comprehensive analysis including market dynamics, competitive landscape, 
            trends, risks, and opportunities. Include specific data points and cite all sources.""",
            
            "reasoning_task": f"""You are a strategic thinking expert in {industry}. 
            Break down complex problems step-by-step, analyze cause-and-effect relationships, 
            and provide logical reasoning for your conclusions.""",
            
            "deep_research": f"""You are conducting an exhaustive research report on {industry}. 
            Provide in-depth analysis with multiple perspectives, comprehensive data, 
            and detailed insights from various authoritative sources."""
        }
        
        return prompts.get(search_type, prompts["detailed_analysis"])

    async def _perplexity_follow_up_questions(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate strategic follow-up questions using Perplexity"""
        try:
            follow_up_query = f"""Based on the topic "{query}", what are the 5 most important 
            strategic questions a business leader should ask when considering this opportunity 
            or challenge? Provide questions that would lead to actionable insights."""
            
            return await self._perplexity_search(follow_up_query, "detailed_analysis", context)
            
        except Exception as e:
            return {"error": f"Follow-up questions generation failed: {str(e)}"}

    async def _perplexity_domain_specific_search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct domain-specific research with industry filters"""
        try:
            industry = context.get("industry", "")
            if not industry:
                return {"message": "No specific industry context provided"}
            
            domain_query = f"""Industry-specific analysis for {industry}: {query}. 
            Include regulatory environment, industry benchmarks, key players, 
            and industry-specific challenges and opportunities."""
            
            return await self._perplexity_search(domain_query, "domain_specific", context)
            
        except Exception as e:
            return {"error": f"Domain-specific search failed: {str(e)}"}

    def _process_perplexity_response(self, response: Dict[str, Any], search_type: str) -> Dict[str, Any]:
        """Process and structure Perplexity API response"""
        try:
            # Extract main content
            message_content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # Extract citations
            citations = response.get("citations", [])
            
            # Extract usage information
            usage = response.get("usage", {})
            
            # Extract related questions
            related_questions = response.get("related_questions", [])
            
            return {
                "content": message_content,
                "citations": citations,
                "related_questions": related_questions,
                "usage": {
                    "total_tokens": usage.get("total_tokens", 0),
                    "cost": usage.get("cost", {}).get("total_cost", 0)
                },
                "search_type": search_type,
                "model_used": response.get("model", "unknown"),
                "processing_time": response.get("created", 0)
            }
            
        except Exception as e:
            return {"error": f"Response processing failed: {str(e)}", "raw_response": response}

    def _synthesize_perplexity_results(self, results: List[Any], query: str) -> Dict[str, Any]:
        """Synthesize multiple Perplexity search results"""
        try:
            successful_results = [r for r in results if not isinstance(r, Exception) and not r.get("error")]
            
            if not successful_results:
                return {"error": "No successful Perplexity results to synthesize"}
            
            # Combine all citations
            all_citations = []
            for result in successful_results:
                all_citations.extend(result.get("citations", []))
            
            # Remove duplicate citations
            unique_citations = list({citation["url"]: citation for citation in all_citations}.values())
            
            # Combine related questions
            all_questions = []
            for result in successful_results:
                all_questions.extend(result.get("related_questions", []))
            
            # Calculate total cost
            total_cost = sum(result.get("usage", {}).get("cost", 0) for result in successful_results)
            
            return {
                "query": query,
                "total_sources": len(unique_citations),
                "unique_citations": unique_citations[:20],  # Limit for performance
                "related_questions": list(set(all_questions))[:10],  # Top 10 unique questions
                "total_api_cost": total_cost,
                "synthesis_confidence": min(len(successful_results) / 4, 1.0),  # Based on number of successful searches
                "key_insights": self._extract_key_insights(successful_results),
                "source_authority_score": self._calculate_source_authority(unique_citations)
            }
            
        except Exception as e:
            return {"error": f"Result synthesis failed: {str(e)}"}

    def _extract_key_insights(self, results: List[Dict[str, Any]]) -> List[str]:
        """Extract key insights from multiple search results"""
        insights = []
        
        for result in results:
            content = result.get("content", "")
            if content and len(content) > 100:  # Only process substantial content
                # Simple extraction of key points (can be enhanced with NLP)
                sentences = content.split('. ')
                for sentence in sentences:
                    if any(keyword in sentence.lower() for keyword in 
                          ['market size', 'growth rate', 'key player', 'trend', 'opportunity', 'challenge']):
                        insights.append(sentence.strip())
        
        return list(set(insights))[:10]  # Return top 10 unique insights

    def _calculate_source_authority(self, citations: List[Dict[str, Any]]) -> float:
        """Calculate source authority score based on citation quality"""
        if not citations:
            return 0.0
        
        authority_domains = {
            'bloomberg.com': 1.0, 'reuters.com': 1.0, 'wsj.com': 1.0,
            'economist.com': 0.95, 'ft.com': 0.95, 'mckinsey.com': 0.9,
            'bcg.com': 0.9, 'deloitte.com': 0.85, 'pwc.com': 0.85,
            'harvard.edu': 0.95, 'mit.edu': 0.95, 'stanford.edu': 0.95
        }
        
        total_score = 0.0
        for citation in citations:
            url = citation.get("url", "")
            domain = url.split('/')[2] if len(url.split('/')) > 2 else ""
            
            score = authority_domains.get(domain, 0.5)  # Default score for unknown domains
            total_score += score
        
        return total_score / len(citations)

    def _calculate_perplexity_confidence(self, results: List[Any]) -> float:
        """Calculate confidence based on Perplexity search results"""
        successful_results = [r for r in results if not isinstance(r, Exception) and not r.get("error")]
        
        if not successful_results:
            return 0.0
        
        # Confidence based on multiple factors
        success_rate = len(successful_results) / len(results)
        citation_count = sum(len(r.get("citations", [])) for r in successful_results)
        citation_score = min(citation_count / 20, 1.0)  # Normalize to max 20 citations
        
        return (success_rate * 0.6) + (citation_score * 0.4)

    def _count_citations(self, results: List[Any]) -> int:
        """Count total unique citations across all results"""
        all_urls = set()
        for result in results:
            if not isinstance(result, Exception) and not result.get("error"):
                citations = result.get("citations", [])
                for citation in citations:
                    all_urls.add(citation.get("url", ""))
        
        return len(all_urls)

    def _analyze_source_diversity(self, results: List[Any]) -> Dict[str, Any]:
        """Analyze diversity of sources across results"""
        domains = set()
        publication_dates = []
        
        for result in results:
            if not isinstance(result, Exception) and not result.get("error"):
                citations = result.get("citations", [])
                for citation in citations:
                    url = citation.get("url", "")
                    if len(url.split('/')) > 2:
                        domains.add(url.split('/')[2]) # Extract domain from URL
                    
                    # Extract publication date if available
                    date = citation.get("date", "")
                    if date: # Assuming date is in a sortable format
                        publication_dates.append(date)
        
        return {
            "unique_domains": len(domains),
            "domain_list": list(domains),
            "date_range": {
                "earliest": min(publication_dates) if publication_dates else None,
                "latest": max(publication_dates) if publication_dates else None
            },
            "diversity_score": min(len(domains) / 10, 1.0)  # Normalize to max 10 domains
        }

    def _determine_research_type(self, query: str, context: Dict[str, Any]) -> str:
        """Determine the type of research needed based on query and context"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['quick', 'overview', 'summary']):
            return "quick_search"
        elif any(word in query_lower for word in ['analysis', 'research', 'study']):
            return "detailed_analysis"
        elif any(word in query_lower for word in ['why', 'how', 'reason']):
            return "reasoning_task"
        else:
            return "detailed_analysis"
