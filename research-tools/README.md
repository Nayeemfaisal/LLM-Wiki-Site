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

The first September candidate is the A123 LFP multimodal dataset. Its public
directory structure uses matching cell numbers across charge-discharge and EIS
files, but the project still needs to inspect the actual rows and metadata.
