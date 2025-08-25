import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import redis
from config import settings

class ProgressTracker:
    """Advanced progress tracking with Redis-based persistence and WebSocket notifications"""
    
    def __init__(self):
        try:
            self.redis_client = redis.Redis.from_url(settings.REDIS_URL)
            self.redis_available = True
        except Exception as e:
            logging.warning(f"Redis not available for progress tracking: {e}")
            self.redis_available = False
        
        self.logger = logging.getLogger(__name__)
        
    async def update_progress(self, analysis_id: str, progress: int, message: str, 
                            details: Optional[Dict[str, Any]] = None):
        """Update progress and notify clients"""
        try:
            progress_data = {
                "analysis_id": analysis_id,
                "progress": progress,
                "message": message,
                "timestamp": datetime.utcnow().isoformat(),
                "details": details or {}
            }
            
            if self.redis_available:
                # Store in Redis with expiry
                await self.redis_client.setex(
                    f"progress:{analysis_id}",
                    3600,  # 1 hour expiry
                    json.dumps(progress_data)
                )
                
                # Publish to WebSocket channel
                await self.redis_client.publish(
                    f"progress_updates:{analysis_id}",
                    json.dumps(progress_data)
                )
            
            # Log progress update
            self.logger.info(f"Progress update for {analysis_id}: {progress}% - {message}")
            
        except Exception as e:
            self.logger.error(f"Failed to update progress: {str(e)}")
    
    async def get_progress(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Get current progress for an analysis"""
        try:
            if not self.redis_available:
                return None
            
            progress_data = await self.redis_client.get(f"progress:{analysis_id}")
            if progress_data:
                return json.loads(progress_data)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get progress: {str(e)}")
            return None
    
    async def set_analysis_status(self, analysis_id: str, status: str, 
                                metadata: Optional[Dict[str, Any]] = None):
        """Set analysis status with metadata"""
        try:
            status_data = {
                "analysis_id": analysis_id,
                "status": status,
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": metadata or {}
            }
            
            if self.redis_available:
                # Store status
                await self.redis_client.setex(
                    f"status:{analysis_id}",
                    7200,  # 2 hours expiry
                    json.dumps(status_data)
                )
                
                # Publish status update
                await self.redis_client.publish(
                    f"status_updates:{analysis_id}",
                    json.dumps(status_data)
                )
            
            self.logger.info(f"Status update for {analysis_id}: {status}")
            
        except Exception as e:
            self.logger.error(f"Failed to set status: {str(e)}")
    
    async def get_analysis_status(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Get current status for an analysis"""
        try:
            if not self.redis_available:
                return None
            
            status_data = await self.redis_client.get(f"status:{analysis_id}")
            if status_data:
                return json.loads(status_data)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get status: {str(e)}")
            return None
    
    async def set_workflow_step(self, analysis_id: str, step: str, 
                              step_progress: int, step_details: Optional[Dict[str, Any]] = None):
        """Set current workflow step with progress"""
        try:
            step_data = {
                "analysis_id": analysis_id,
                "current_step": step,
                "step_progress": step_progress,
                "timestamp": datetime.utcnow().isoformat(),
                "step_details": step_details or {}
            }
            
            if self.redis_available:
                # Store step info
                await self.redis_client.setex(
                    f"workflow_step:{analysis_id}",
                    3600,  # 1 hour expiry
                    json.dumps(step_data)
                )
                
                # Publish step update
                await self.redis_client.publish(
                    f"workflow_updates:{analysis_id}",
                    json.dumps(step_data)
                )
            
            self.logger.info(f"Workflow step update for {analysis_id}: {step} - {step_progress}%")
            
        except Exception as e:
            self.logger.error(f"Failed to set workflow step: {str(e)}")
    
    async def get_workflow_step(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Get current workflow step for an analysis"""
        try:
            if not self.redis_available:
                return None
            
            step_data = await self.redis_client.get(f"workflow_step:{analysis_id}")
            if step_data:
                return json.loads(step_data)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get workflow step: {str(e)}")
            return None
    
    async def set_error(self, analysis_id: str, error: str, error_details: Optional[Dict[str, Any]] = None):
        """Set error information for an analysis"""
        try:
            error_data = {
                "analysis_id": analysis_id,
                "error": error,
                "timestamp": datetime.utcnow().isoformat(),
                "error_details": error_details or {}
            }
            
            if self.redis_available:
                # Store error info
                await self.redis_client.setex(
                    f"error:{analysis_id}",
                    7200,  # 2 hours expiry
                    json.dumps(error_data)
                )
                
                # Publish error update
                await self.redis_client.publish(
                    f"error_updates:{analysis_id}",
                    json.dumps(error_data)
                )
            
            self.logger.error(f"Error set for {analysis_id}: {error}")
            
        except Exception as e:
            self.logger.error(f"Failed to set error: {str(e)}")
    
    async def get_error(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Get error information for an analysis"""
        try:
            if not self.redis_available:
                return None
            
            error_data = await self.redis_client.get(f"error:{analysis_id}")
            if error_data:
                return json.loads(error_data)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get error: {str(e)}")
            return None
    
    async def cleanup_analysis_data(self, analysis_id: str):
        """Clean up all progress tracking data for an analysis"""
        try:
            if not self.redis_available:
                return
            
            # Remove all keys related to this analysis
            keys_to_remove = [
                f"progress:{analysis_id}",
                f"status:{analysis_id}",
                f"workflow_step:{analysis_id}",
                f"error:{analysis_id}"
            ]
            
            for key in keys_to_remove:
                await self.redis_client.delete(key)
            
            self.logger.info(f"Cleaned up progress tracking data for {analysis_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup analysis data: {str(e)}")
    
    def get_progress_summary(self, analysis_id: str) -> Dict[str, Any]:
        """Get a summary of all progress information for an analysis"""
        try:
            summary = {
                "analysis_id": analysis_id,
                "timestamp": datetime.utcnow().isoformat(),
                "progress": None,
                "status": None,
                "current_step": None,
                "error": None
            }
            
            # This would be called in a synchronous context, so we can't use await
            # In production, you might want to make this async or use a different approach
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to get progress summary: {str(e)}")
            return {"analysis_id": analysis_id, "error": str(e)}


class WorkflowMonitor:
    """Monitor workflow execution and provide insights"""
    
    def __init__(self):
        self.progress_tracker = ProgressTracker()
        self.logger = logging.getLogger(__name__)
    
    async def monitor_workflow_execution(self, analysis_id: str, workflow_data: Dict[str, Any]):
        """Monitor workflow execution and track key metrics"""
        try:
            # Track workflow start
            await self.progress_tracker.set_analysis_status(analysis_id, "started", {
                "workflow_type": workflow_data.get("workflow_type", "standard"),
                "estimated_duration": workflow_data.get("estimated_duration", "unknown")
            })
            
            # Set initial progress
            await self.progress_tracker.update_progress(analysis_id, 0, "Workflow initiated")
            
            # Track workflow steps
            workflow_steps = workflow_data.get("steps", [])
            for i, step in enumerate(workflow_steps):
                step_progress = int((i / len(workflow_steps)) * 100)
                await self.progress_tracker.set_workflow_step(
                    analysis_id, 
                    step["name"], 
                    step_progress,
                    {"step_number": i + 1, "total_steps": len(workflow_steps)}
                )
            
            self.logger.info(f"Workflow monitoring initiated for {analysis_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to monitor workflow: {str(e)}")
            await self.progress_tracker.set_error(analysis_id, f"Monitoring failed: {str(e)}")
    
    async def track_workflow_completion(self, analysis_id: str, completion_data: Dict[str, Any]):
        """Track workflow completion and final metrics"""
        try:
            # Set completion status
            await self.progress_tracker.set_analysis_status(analysis_id, "completed", completion_data)
            
            # Set final progress
            await self.progress_tracker.update_progress(analysis_id, 100, "Workflow completed successfully")
            
            # Set final workflow step
            await self.progress_tracker.set_workflow_step(
                analysis_id, 
                "completed", 
                100,
                {"completion_time": datetime.utcnow().isoformat()}
            )
            
            self.logger.info(f"Workflow completed for {analysis_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to track completion: {str(e)}")
            await self.progress_tracker.set_error(analysis_id, f"Completion tracking failed: {str(e)}")
