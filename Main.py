from fastapi import FastAPI
from app.models import RunCodeRequest, RunCodeResponse
from app.runner import run_code

app = FastAPI(
    title="Cold Start Code Engine",
    description="Programiz-style code execution backend for Godot",
    version="0.1.0"
)

@app.post("/run", response_model=RunCodeResponse)
def execute_code(request: RunCodeRequest):
    return run_code(request)
