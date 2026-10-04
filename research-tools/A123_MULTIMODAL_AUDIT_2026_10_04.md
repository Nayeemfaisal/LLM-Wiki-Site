# A123 LFP Multimodal Source Audit: 4 October 2026

## Question

Can the public A123 LFP multimodal source support an honest time-series plus EIS pipeline experiment?

## Read-only method

- Source: <https://github.com/huangjin-collab/A123-LFP-Battery-Multimodal-Electrochemical-Dataset>
- Reviewed: repository metadata, recursive file tree, README, `Char-dis-Cell1.xlsx`, and `A123-EIS-1.txt`.
- Excluded: fitting, DRT inversion, interpolation, model training, and inferred joins.

## What is directly supported

| Check | Result |
| --- | --- |
| Cell-level association | The README documents charge-discharge and EIS files for the same Cell 1 through Cell 71 index. |
| Charge/discharge structure | The sampled Cell 1 workbook has 5,661 observations and `Stage`, `Current (A)`, and `Voltage (V)` columns. |
| EIS structure | The sampled Cell 1 spectrum has 60 points from 10 kHz to 0.01 Hz with frequency, bias, time, real/imaginary impedance, magnitude, and phase fields. |
| Reproducibility | SHA-256 values are recorded in the companion JSON audit record. |

## Evidence boundary

The sampled charge/discharge workbook has no time, SOC, temperature, or test-event identifier. The EIS file contains bias and acquisition time but no explicit link to a row range in the workbook. Therefore the source supports a **cell-level multimodal association**, not an event-level TS-to-EIS target.

## Decision

- Use now for file ingestion, schema checks, EIS quality preflight, and DRT-input preparation.
- Do not yet train a time-window-to-EIS model or present a matched TS/EIS validation result.
- Next: retrieve condition metadata from the associated publication or source maintainers; require SOC, temperature, protocol, and a join rule before upgrading the evidence status.
