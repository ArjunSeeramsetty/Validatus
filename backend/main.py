import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uuid
from datetime import datetime
from typing import Dict

from app.core.comprehensive_langgraph_workflow_fixed import ContextAwareLangGraphWorkflow
from app.core.simple_state import State as ValidatusState
from app.core.models import AnalysisRequest, AnalysisResponse

app = FastAPI(title="Validatus Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API endpoints are defined directly in this file

# In a production environment, this would be a persistent store like Redis or a database.
analysis_store: Dict = {}

# Initialize the workflow once
validatus_workflow = ContextAwareLangGraphWorkflow()

async def run_analysis(analysis_id: str):
    """Run the complete analysis workflow."""
    try:
        initial_state = analysis_store[analysis_id]
        
        # Execute the workflow using the current workflow instance
        result = await validatus_workflow.execute(
            idea_description=initial_state.idea_description,
            target_audience=initial_state.target_audience,
            additional_context=initial_state.additional_context
        )
        
        # Update the store with results
        analysis_store[analysis_id] = result

    except Exception as e:
        if analysis_id in analysis_store:
            analysis_store[analysis_id]["status"] = "FAILED"
            analysis_store[analysis_id]["errors"] = analysis_store[analysis_id].get("errors", []) + [f"Workflow execution error: {str(e)}"]

@app.post("/api/v1/analysis", response_model=AnalysisResponse)
async def create_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Initiate a new deep research analysis."""
    analysis_id = str(uuid.uuid4())
    
    initial_state = ValidatusState(
        idea_description=request.query,
        target_audience=request.context.get("target_audience", "General audience"),
        additional_context=request.context.dict()
    )
    
    analysis_store[analysis_id] = initial_state
    
    background_tasks.add_task(run_analysis, analysis_id)
    
    return AnalysisResponse(
        analysis_id=analysis_id,
        status="INITIATED",
        progress=0,
    )

@app.get("/api/v1/analysis/{analysis_id}/status", response_model=AnalysisResponse)
async def get_analysis_status(analysis_id: str):
    """Get the current status and progress of an analysis."""
    state = analysis_store.get(analysis_id)
    if not state:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return AnalysisResponse(
        analysis_id=analysis_id,
        status=state.get("status", "UNKNOWN"),
        progress=state.get("progress", 0),
    )

@app.get("/api/v1/analysis/{analysis_id}/results")
async def get_analysis_results(analysis_id: str):
    """Get the complete results of a finished analysis."""
    state = analysis_store.get(analysis_id)
    if not state:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if state.get("status") != "COMPLETED":
        raise HTTPException(status_code=400, detail=f"Analysis not completed. Current status: {state.get('status', 'UNKNOWN')}")
    
    return state.get("dashboard_data", {})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
