from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from research_agent_llama3 import query_llama3

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    results: List[Dict]

@router.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    query = request.query
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        answer = query_llama3(query)
        if not answer:
            raise HTTPException(status_code=404, detail="No results found")
        return {"results": [{"text": answer, "meta": {}}]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
