import json
import subprocess
import sys
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from eis_intake import inspect_eis_csv, inspect_eis_directory
from candidate_ranking import rank_candidates


ROOT = Path(__file__).resolve().parent
JOBS_DIR = ROOT / "jobs"
REGISTRY_PATH = ROOT.parent / "research-tools" / "candidate_registry.json"

app = FastAPI(
    title="bAIttery API-to-HPC Demo",
    description="Local mock of an API that submits battery processing jobs and returns results.",
    version="0.1.0",
)


class JobRequest(BaseModel):
    input_csv: str = "sample_battery.csv"


class EisIntakeRequest(BaseModel):
    input_csv: str = "sample_eis.csv"


class EisDirectoryIntakeRequest(BaseModel):
    input_directory: str = "."


def job_paths(job_id):
    job_dir = JOBS_DIR / job_id
    return {
        "dir": job_dir,
        "status": job_dir / "status.json",
        "result": job_dir / "result.json",
    }


def write_status(job_id, status, detail=None):
    paths = job_paths(job_id)
    paths["dir"].mkdir(parents=True, exist_ok=True)
    payload = {"job_id": job_id, "status": status}
    if detail:
        payload["detail"] = detail
    paths["status"].write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


@app.get("/")
def root():
    return {
        "message": "bAIttery API-to-HPC demo",
        "docs": "/docs",
        "submit": "POST /jobs",
    }


@app.get("/research/candidate-priorities")
def candidate_priorities():
    """Expose the transparent source-audit planning score used by the wiki."""
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {
        "registry_date": registry["registry_date"],
        "scope": registry["scope"],
        "ranked_candidates": rank_candidates(registry["candidates"]),
        "interpretation_note": (
            "Planning score only. A higher score does not validate a TS/EIS "
            "match or any DRT conclusion."
        ),
    }


@app.post("/intake/eis")
def inspect_eis(request: EisIntakeRequest):
    """Check whether a local EIS CSV has the minimum DRT input structure."""
    input_csv = (ROOT / request.input_csv).resolve()
    if ROOT not in input_csv.parents or not input_csv.exists():
        raise HTTPException(status_code=400, detail=f"input CSV not found: {request.input_csv}")
    return inspect_eis_csv(input_csv)


@app.post("/intake/eis-directory")
def inspect_eis_directory_route(request: EisDirectoryIntakeRequest):
    """Return file-by-file structural reports for local EIS CSV files."""
    input_directory = (ROOT / request.input_directory).resolve()
    if ROOT not in input_directory.parents and input_directory != ROOT:
        raise HTTPException(status_code=400, detail="input directory must be inside the demo folder")
    if not input_directory.is_dir():
        raise HTTPException(status_code=400, detail=f"input directory not found: {request.input_directory}")
    return inspect_eis_directory(input_directory)


@app.post("/jobs")
def submit_job(request: JobRequest):
    input_csv = (ROOT / request.input_csv).resolve()
    if not input_csv.exists():
        raise HTTPException(status_code=400, detail=f"input CSV not found: {request.input_csv}")

    job_id = uuid.uuid4().hex[:12]
    paths = job_paths(job_id)
    write_status(job_id, "running")

    command = [
        sys.executable,
        str(ROOT / "worker.py"),
        str(input_csv),
        str(paths["result"]),
    ]

    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if completed.returncode != 0:
        status = write_status(job_id, "failed", completed.stderr.strip())
        return status

    return write_status(job_id, "finished")


@app.get("/jobs/{job_id}")
def get_status(job_id: str):
    paths = job_paths(job_id)
    if not paths["status"].exists():
        raise HTTPException(status_code=404, detail="job not found")
    return json.loads(paths["status"].read_text(encoding="utf-8"))


@app.get("/jobs/{job_id}/result")
def get_result(job_id: str):
    paths = job_paths(job_id)
    if not paths["result"].exists():
        raise HTTPException(status_code=404, detail="result not available")
    return json.loads(paths["result"].read_text(encoding="utf-8"))
