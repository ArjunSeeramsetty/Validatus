import asyncio
import aiohttp
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time
from datetime import datetime
import json
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class EnhancedBaseAgent(ABC):
    """Enhanced base agent with async operations, retry logic, and comprehensive error handling"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = logging.getLogger(f"agent.{agent_name}")
        self.session = None
        self.retry_config = {
            'stop': stop_after_attempt(3),
            'wait': wait_exponential(multiplier=1, min=4, max=10),
            'retry': retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError))
        }

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=120),
            connector=aiohttp.TCPConnector(limit=10, limit_per_host=5)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    @abstractmethod
    async def research(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Abstract method for research implementation"""
        pass

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def safe_api_call(self, url: str, method: str = 'GET', **kwargs) -> Dict[str, Any]:
        """Safe API call with retry logic and comprehensive error handling"""
        try:
            if not self.session:
                raise RuntimeError("Session not initialized. Use async context manager.")
            
            start_time = time.time()
            async with self.session.request(method, url, **kwargs) as response:
                if response.status == 429:  # Rate limited
                    wait_time = await self.handle_rate_limiting(response)
                    raise aiohttp.ClientError(f"Rate limited. Wait {wait_time} seconds.")
                
                if response.status >= 400:
                    raise aiohttp.ClientError(f"HTTP {response.status}: {response.reason}")
                
                data = await response.json()
                execution_time = time.time() - start_time
                
                self.logger.info(f"API call successful: {method} {url} in {execution_time:.2f}s")
                return {"data": data, "status": response.status, "execution_time": execution_time}
                
        except asyncio.TimeoutError:
            self.logger.error(f"API call timeout: {method} {url}")
            raise
        except aiohttp.ClientError as e:
            self.logger.error(f"API call failed: {method} {url} - {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in API call: {method} {url} - {str(e)}")
            raise

    async def parallel_research_execution(self, research_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute multiple research tasks in parallel with proper error handling"""
        try:
            tasks = [self._execute_single_research_task(task) for task in research_tasks]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results and handle exceptions
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    self.logger.error(f"Task {i} failed: {str(result)}")
                    processed_results.append({
                        "error": str(result),
                        "task_index": i,
                        "status": "failed"
                    })
                else:
                    processed_results.append(result)
            
            return processed_results
            
        except Exception as e:
            self.logger.error(f"Parallel execution failed: {str(e)}")
            raise

    @abstractmethod
    async def _execute_single_research_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single research task - to be implemented by subclasses"""
        pass

    def calculate_advanced_confidence(self, results: List[Any]) -> float:
        """Calculate confidence score based on multiple factors"""
        if not results:
            return 0.0
        
        try:
            # Calculate various confidence factors
            data_quality_scores = [self._assess_result_quality(result) for result in results if result]
            source_authority_scores = [self._calculate_source_authority(result) for result in results if result]
            recency_scores = [self._calculate_recency_score(result) for result in results if result]
            
            # Weighted average of confidence factors
            weights = {
                'data_quality': 0.4,
                'source_authority': 0.35,
                'recency': 0.25
            }
            
            avg_data_quality = sum(data_quality_scores) / len(data_quality_scores) if data_quality_scores else 0.0
            avg_source_authority = sum(source_authority_scores) / len(source_authority_scores) if source_authority_scores else 0.0
            avg_recency = sum(recency_scores) / len(recency_scores) if recency_scores else 0.0
            
            confidence = (
                avg_data_quality * weights['data_quality'] +
                avg_source_authority * weights['source_authority'] +
                avg_recency * weights['recency']
            )
            
            return min(1.0, max(0.0, confidence))
            
        except Exception as e:
            self.logger.error(f"Error calculating confidence: {str(e)}")
            return 0.5  # Default confidence

    def _assess_result_quality(self, data: Dict[str, Any]) -> float:
        """Assess quality of individual result data"""
        try:
            quality_score = 0.0
            
            # Check content length
            if 'content' in data and len(str(data['content'])) > 100:
                quality_score += 0.2
            
            # Check for citations/sources
            if 'sources' in data and data['sources']:
                quality_score += 0.2
            
            # Check for timestamps
            if 'timestamp' in data:
                quality_score += 0.2
            
            # Check for structured data
            if 'structured_data' in data and data['structured_data']:
                quality_score += 0.2
            
            # Check for metadata
            if 'metadata' in data and data['metadata']:
                quality_score += 0.2
            
            return quality_score
            
        except Exception:
            return 0.0

    def _calculate_source_authority(self, data: Dict[str, Any]) -> float:
        """Calculate source authority score"""
        try:
            if 'source' not in data:
                return 0.5
            
            source = data['source'].lower()
            
            # High authority sources
            if any(domain in source for domain in ['bloomberg.com', 'reuters.com', 'wsj.com', 'economist.com']):
                return 0.9
            # Medium authority sources
            elif any(domain in source for domain in ['forbes.com', 'techcrunch.com', 'wired.com']):
                return 0.7
            # Academic sources
            elif any(domain in source for domain in ['.edu', '.ac.uk', 'arxiv.org']):
                return 0.8
            # Government sources
            elif any(domain in source for domain in ['.gov', '.org']):
                return 0.6
            else:
                return 0.4
                
        except Exception:
            return 0.5

    def _calculate_recency_score(self, data: Dict[str, Any]) -> float:
        """Calculate recency score based on timestamp"""
        try:
            if 'timestamp' not in data:
                return 0.5
            
            timestamp = data['timestamp']
            if isinstance(timestamp, str):
                from datetime import datetime
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except:
                    return 0.5
            else:
                dt = timestamp
            
            now = datetime.utcnow()
            age_days = (now - dt).days
            
            if age_days <= 1:
                return 1.0
            elif age_days <= 7:
                return 0.9
            elif age_days <= 30:
                return 0.7
            elif age_days <= 90:
                return 0.5
            else:
                return 0.3
                
        except Exception:
            return 0.5

    async def validate_research_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate research data for completeness and quality"""
        try:
            validation_result = {
                "is_valid": True,
                "missing_fields": [],
                "quality_score": 0.0,
                "recommendations": []
            }
            
            required_fields = ['content', 'source', 'timestamp']
            for field in required_fields:
                if field not in data or not data[field]:
                    validation_result["missing_fields"].append(field)
                    validation_result["is_valid"] = False
            
            # Calculate quality score
            validation_result["quality_score"] = self._assess_result_quality(data)
            
            # Generate recommendations
            if validation_result["quality_score"] < 0.6:
                validation_result["recommendations"].append("Consider gathering additional data sources")
            if 'citations' not in data:
                validation_result["recommendations"].append("Include citations for better credibility")
            if 'metadata' not in data:
                validation_result["recommendations"].append("Add metadata for better data organization")
            
            return validation_result
            
        except Exception as e:
            self.logger.error(f"Error validating research data: {str(e)}")
            return {
                "is_valid": False,
                "error": str(e),
                "quality_score": 0.0
            }

    def generate_research_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive summary of research results"""
        try:
            if not results:
                return {"summary": "No research results available", "key_insights": []}
            
            # Extract key insights
            key_insights = []
            for result in results:
                if 'content' in result and result['content']:
                    # Simple keyword extraction (could be enhanced with NLP)
                    content = str(result['content']).lower()
                    if any(keyword in content for keyword in ['market', 'growth', 'trend', 'opportunity']):
                        key_insights.append(f"Market-related insight from {result.get('source', 'unknown source')}")
            
            # Generate summary
            total_sources = len(set(result.get('source', 'unknown') for result in results))
            avg_quality = sum(self._assess_result_quality(result) for result in results) / len(results)
            
            summary = f"Research completed with {len(results)} results from {total_sources} sources. "
            summary += f"Average data quality: {avg_quality:.2f}/1.0. "
            summary += f"Key insights identified: {len(key_insights)}"
            
            return {
                "summary": summary,
                "key_insights": key_insights,
                "total_results": len(results),
                "unique_sources": total_sources,
                "average_quality": avg_quality,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating research summary: {str(e)}")
            return {"summary": "Error generating summary", "error": str(e)}

    async def handle_rate_limiting(self, response: aiohttp.ClientResponse) -> int:
        """Handle rate limiting with exponential backoff"""
        try:
            # Check for rate limit headers
            retry_after = response.headers.get('Retry-After')
            if retry_after:
                try:
                    return int(retry_after)
                except ValueError:
                    pass
            
            # Default exponential backoff
            return 60  # 1 minute
            
        except Exception:
            return 60

    def log_research_metrics(self, query: str, context: Dict[str, Any], results: List[Dict[str, Any]], 
                             execution_time: float) -> None:
        """Log comprehensive research metrics for monitoring"""
        try:
            metrics = {
                "agent": self.agent_name,
                "query": query,
                "context_keys": list(context.keys()) if context else [],
                "results_count": len(results),
                "execution_time": execution_time,
                "average_confidence": self.calculate_advanced_confidence(results),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.logger.info(f"Research metrics: {json.dumps(metrics, indent=2)}")
            
        except Exception as e:
            self.logger.error(f"Error logging metrics: {str(e)}")

    async def cleanup_resources(self) -> None:
        """Clean up agent resources"""
        try:
            if self.session:
                await self.session.close()
                self.session = None
            self.logger.info(f"Resources cleaned up for {self.agent_name}")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")

    def __del__(self):
        """Destructor to ensure cleanup"""
        try:
            if self.session and not self.session.closed:
                # Schedule cleanup in event loop if available
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        loop.create_task(self.cleanup_resources())
                except RuntimeError:
                    # No event loop available
                    pass
        except Exception:
            pass
