from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import os

app = FastAPI(
    title="Cold Start Code Runner",
    description="Programiz-style code execution backend for Godot",
    version="0.1"
)

# -------------------------
# Models
# -------------------------
class RunCodeRequest(BaseModel):
    language: str
    code: str
    input: str = ""

class RunCodeResponse(BaseModel):
    output: str
    error: str
    exit_code: int

# -------------------------
# Execution Logic
# -------------------------
EXECUTION_TIMEOUT = 5  # seconds

def run_python(code: str, user_input: str):
    with tempfile.TemporaryDirectory() as tmp:
        file_path = os.path.join(tmp, "main.py")

        with open(file_path, "w") as f:
            f.write(code)

        try:
            result = subprocess.run(
                ["python", file_path],
                input=user_input,
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT
            )

            return RunCodeResponse(
                output=result.stdout,
                error=result.stderr,
                exit_code=result.returncode
            )

        except subprocess.TimeoutExpired:
            return RunCodeResponse(
                output="",
                error="Execution timed out",
                exit_code=-1
            )

# -------------------------
# API Endpoint
# -------------------------
@app.post("/run", response_model=RunCodeResponse)
def run_code(req: RunCodeRequest):
    if req.language.lower() != "python":
        return RunCodeResponse(
            output="",
            error="Only Python is supported for now",
            exit_code=-1
        )

    return run_python(req.code, req.input)
