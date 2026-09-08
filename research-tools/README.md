# Dataset intake tools

These utilities support a careful handoff from public source screening to the
local API/HPC prototype. They do not download source archives and they do not
turn a candidate into a validated dataset.

## Current workflow

1. Record source-level evidence in `dataset_evidence_ledger.csv`.
2. Download only a small approved sample from a source with clear terms.
3. Build a file manifest: cell, test, cycle, SOC, temperature, protocol,
   columns, units, and file hash.
4. Run the EIS structural check in `../demo-api-hpc`.
5. Apply EIS consistency and DRT reconstruction/stability checks separately.
6. Promote a source only when a repeatable TS-to-EIS join is demonstrated.

## Source prioritisation

`candidate_registry.json` records the evidence visible from the public source
pages. Each evidence field is recorded as 0 (not established), 1 (partial
public indication), or 2 (explicit public indication). `rank_candidates.py`
produces a transparent planning score from that record. It is not a scientific
quality score and it never upgrades a source to "matched".

```bash
python3 research-tools/rank_candidates.py
python3 research-tools/audit_source_layout.py /path/to/small-source-sample --output /tmp/source-audit.json
```

The local API exposes the same planning view at
`GET /research/candidate-priorities` when the API dependencies are installed.

The first September candidate is the A123 LFP multimodal dataset. Its public
directory structure uses matching cell numbers across charge-discharge and EIS
files, but the project still needs to inspect the actual rows and metadata.
