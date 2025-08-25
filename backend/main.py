from fastapi import FastAPI
from backend import routes
from app.utils import initialize_logging

from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv(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)

app = FastAPI(title="AgentHive Backend API")

# Initialize logging
initialize_logging()

# Include the updated routes
app.include_router(routes.router)

@app.get("/")
def root():
    return {"message": "Backend API running"}

@app.on_event("startup")
def startup_event():
    print("Backend startup complete")

