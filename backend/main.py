from fastapi import FastAPI
from backend import routes
from app.utils import initialize_logging

app = FastAPI(title="AgentHive Backend API")

initialize_logging()
app.include_router(routes.router)

@app.get("/")
def root():
    return {"message": "Backend API running"}

@app.on_event("startup")
def startup_event():
    print("Backend startup complete")
