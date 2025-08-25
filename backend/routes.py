from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from research_agent_llama3 import query_llama3  # or use research_agent.query_agent

router = APIRouter()

# Request model for frontend queries
class QueryRequest(BaseModel):
    query: str

# Response model
class QueryResponse(BaseModel):
    results: List[Dict]

# Health check endpoint
@router.get("/health")
def health_check():
    return {"status": "OK"}

# New POST endpoint for frontend queries
@router.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    query = request.query
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        # Call your LLaMA3 agent or multi-agent retrieval logic
        answer = query_llama3(query)
        return {"results": [{"text": answer, "meta": {}}]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
