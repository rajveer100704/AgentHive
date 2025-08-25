from fastapi import FastAPI
from backend import routes
from app.config import DEBUG
from app.utils import initialize_logging

app = FastAPI(title="AgentHive Backend", debug=DEBUG)

# Initialize logging
initialize_logging()

# Include API routes
app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "AgentHive Backend is running"}

@app.on_event("startup")
def startup_event():
    print("Starting AgentHive backend services...")
