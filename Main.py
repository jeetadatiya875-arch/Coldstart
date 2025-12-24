from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import os

app = FastAPI()

class RunCodeRequest(BaseModel):
    code: str
    input: str = ""

class RunCodeResponse(BaseModel):
    output: str
    error: str

@app.post("/run", response_model=RunCodeResponse)
def run_code(req: RunCodeRequest):
    with tempfile.TemporaryDirectory() as tmp:
        file_path = os.path.join(tmp, "main.py")

        with open(file_path, "w") as f:
            f.write(req.code)

        try:
            result = subprocess.run(
                ["python3", file_path],
                input=req.input,
                capture_output=True,
                text=True,
                timeout=5
            )

            return RunCodeResponse(
                output=result.stdout,
                error=result.stderr
            )

        except subprocess.TimeoutExpired:
            return RunCodeResponse(
                output="",
                error="Execution timed out"
            )
