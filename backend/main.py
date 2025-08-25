import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uuid
from datetime import datetime
from typing import Dict

from app.core.workflow import ValidatusWorkflow
from app.core.state import ValidatusState, AnalysisStatus
from app.core.models import AnalysisRequest, AnalysisResponse
from config import settings

app = FastAPI(title="Validatus Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In a production environment, this would be a persistent store like Redis or a database.
analysis_store: Dict = {}

# Initialize the workflow once
validatus_workflow = ValidatusWorkflow()
compiled_workflow = validatus_workflow.build_workflow()

async def run_analysis(analysis_id: str):
    """Run the complete analysis workflow."""
    try:
        config = {"configurable": {"thread_id": analysis_id}}
        initial_state = analysis_store[analysis_id]
        
        async for event in compiled_workflow.astream(initial_state, config=config):
            # The state is automatically persisted by the checkpointer.
            # We can update our in-memory store for status checks.
            if event:
                last_state_key = list(event.keys())[-1]
                analysis_store[analysis_id] = event[last_state_key]

    except Exception as e:
        if analysis_id in analysis_store:
            analysis_store[analysis_id]["status"] = AnalysisStatus.FAILED
            analysis_store[analysis_id]["errors"] = analysis_store[analysis_id].get("errors", []) + [f"Workflow execution error: {str(e)}"]

@app.post("/api/v1/analysis", response_model=AnalysisResponse)
async def create_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Initiate a new deep research analysis."""
    analysis_id = str(uuid.uuid4())
    
    initial_state = ValidatusState(
        user_query=request.query,
        analysis_context=request.context.dict(),
        analysis_id=analysis_id,
        query_interpretation={},
        research_tasks=[],
        research_results={},
        layer_scores={},
        factor_scores={},
        segment_scores={},
        dashboard_data={},
        recommendations=[],
        status=AnalysisStatus.INITIATED,
        progress=0,
        errors=[],
        timestamp=datetime.utcnow().isoformat()
    )
    
    analysis_store[analysis_id] = initial_state
    
    background_tasks.add_task(run_analysis, analysis_id)
    
    return AnalysisResponse(
        analysis_id=analysis_id,
        status=AnalysisStatus.INITIATED,
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
        status=state["status"],
        progress=state["progress"],
    )

@app.get("/api/v1/analysis/{analysis_id}/results")
async def get_analysis_results(analysis_id: str):
    """Get the complete results of a finished analysis."""
    state = analysis_store.get(analysis_id)
    if not state:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if state["status"] != AnalysisStatus.COMPLETED:
        raise HTTPException(status_code=400, detail=f"Analysis not completed. Current status: {state['status']}")
    
    return state["dashboard_data"]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
