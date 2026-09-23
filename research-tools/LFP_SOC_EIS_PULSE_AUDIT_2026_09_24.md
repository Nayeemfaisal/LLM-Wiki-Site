# LFP SOC EIS and Sine-Wave Pulse Audit: 24 September 2026

## Question

Can the open LFP SOC source support a defensible, state-aware link between a cosine-pulse time-series record and an EIS record?

## Scope

- **Repository:** <https://github.com/yizhaogao2025/LFP_battery_SOC_Dataset>
- **Licence:** CC0-1.0, confirmed from the repository metadata.
- **Inspection type:** read-only download and file-signature review of one processed COS file and one processed EIS file in the 0.05 A charge condition.
- **Not performed:** model fitting, DRT fitting, resampling, or data transformation.

## Confirmed layout

The repository contains matching condition folders for both COS and EIS material:

- 0.05 A charge;
- 0.05 A discharge;
- 0.1 A charge; and
- 0.1 A discharge.

It also contains processed MATLAB MAT files and raw XLSX files. This is enough to establish **condition-level correspondence** between the two modalities.

## Inspected artifacts

| Artifact | Repository path | Size | SHA-256 |
| --- | --- | ---: | --- |
| COS processed file | `COS_Raw&Processed_data_for_DIB/COS_Processed_data_mat/COS_0.05A_Charge.mat` | 476,570 bytes | `7fefe4c10cdcbdb90a4ee8d932e2480273e0207ddd17a8ff9e2d7da970687a84` |
| EIS processed file | `EIS_Raw & Processed_data_for_DIB/EIS_Processed_data_mat/EIS_0.05A_Charge.mat` | 320,850 bytes | `7f4ae28ecb686ed20ec8188df7e83fb257e854eac0db50cbe7f5a6f067b272a0` |

Both files identify as MATLAB v5 MAT files. No transformation was applied.

## Evidence decision

**Decision: more metadata needed.**

The shared 0.05 A charge label is not sufficient to prove that the two files describe the same cell, SOC point, repeat, temperature, or measurement event. The source remains a priority candidate because it is openly licensed and structured in parallel COS/EIS groups, but it cannot enter adapter modelling yet.

## Required next audit

1. Open one raw XLSX pair or load the MAT variables using a documented reader.
2. Record cell ID, SOC, temperature, test ID, timestamp or repeat ID, units, and EIS frequency ordering.
3. Write the exact COS-to-EIS join key into `source_audit_template.csv`.
4. Change the status to `join supported`, `join not supported`, or retain `more metadata needed`.

## Related machine-readable record

`audit_records/lfp_soc_eis_pulse_2026-09-24.json`
