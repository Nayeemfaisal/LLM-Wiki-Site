# Demo API to HPC Pipeline

This folder is the first local prototype for the VM/HPC pipeline handoff.

The goal is to prove the control flow before FAU VM/HPC access is ready:

1. A client submits a small battery-processing job to an API.
2. The API creates a job folder and stores the input.
3. A local mock runner processes the job.
4. The result is written as JSON.
5. The API can return job status and result.

Later, the local mock runner can be replaced by a real HPC scheduler call, for example `sbatch`.

## Files

- `app.py` - FastAPI demo service.
- `worker.py` - small battery CSV processing script.
- `sample_battery.csv` - tiny demo input file.
- `sample_eis.csv` - small, synthetic EIS structure example for intake testing.
- `eis_intake.py` - read-only structural EIS check before a DRT workflow.
- `requirements.txt` - minimal Python packages.
- `jobs/` - runtime output folder, ignored by Git.

## Local Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8090
```

Open:

```text
http://localhost:8090/docs
```

## Demo Requests

Submit a job:

```bash
curl -X POST http://localhost:8090/jobs \
  -H "Content-Type: application/json" \
  -d '{"input_csv":"sample_battery.csv"}'
```

Check status:

```bash
curl http://localhost:8090/jobs/<job_id>
```

Get result:

```bash
curl http://localhost:8090/jobs/<job_id>/result
```

Screen an EIS CSV before DRT preparation:

```bash
curl -X POST http://localhost:8090/intake/eis \
  -H "Content-Type: application/json" \
  -d '{"input_csv":"sample_eis.csv"}'
```

The intake response checks required columns, finite numeric values, positive
frequencies, duplicate frequencies, and ordering. It is not a Kramers-Kronig
test and it is not evidence that a DRT result is scientifically valid.

Screen every CSV in a local folder:

```bash
curl -X POST http://localhost:8090/intake/eis-directory \
  -H "Content-Type: application/json" \
  -d '{"input_directory":"."}'
```

This endpoint is useful once a small approved source sample has been copied
into a local intake folder. It returns one report per CSV and never changes the
source files.

## HPC Replacement Point

In `app.py`, the current demo calls:

```python
subprocess.run([sys.executable, "worker.py", ...])
```

On a real HPC cluster this becomes:

```bash
sbatch run_battery_job.slurm <job_id> <input_csv> <output_json>
```

The API contract can stay the same while the execution backend changes.
