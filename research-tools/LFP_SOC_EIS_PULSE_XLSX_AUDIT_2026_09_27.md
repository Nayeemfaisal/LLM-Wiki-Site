# LFP COS and EIS Raw Workbook Audit: 27 September 2026

## Objective

Inspect the raw workbook structure behind the open LFP cosine-pulse and EIS source. The question is whether one 0.05 A charge COS workbook can be joined to one 0.05 A charge EIS workbook without guessing.

## Reproducible method

- Source: <https://github.com/yizhaogao2025/LFP_battery_SOC_Dataset>
- Licence: CC0-1.0.
- Tool: `research-tools/audit_xlsx_workbook.py`.
- Scope: read-only XLSX structure inspection, top-row review, and SHA-256 checksums.
- Excluded: data transformation, model training, EIS fitting, and DRT fitting.

## COS workbook

| Field | Observation |
| --- | --- |
| File | `0.05A_COS_Charge.xlsx` |
| Repository path | `COS_Raw&Processed_data_for_DIB/COS_Raw_data_xlsx/COS_0.05A_Charge/0.05A_COS_Charge.xlsx` |
| SHA-256 | `e9885e5bbd6470d62b17111b5dffb040bb3ae5c646e22a31e4c6c2d3eba3b510` |
| Sheets | `Global_Info`, `Channel_5_1` |
| Main table | 82,052 rows by 13 columns |
| Directly visible fields | date/time, test time, step time, step index, cycle index, voltage, current, charge/discharge capacity, energy, internal resistance, dV/dt |
| Reported schedule | `LFP_26650\\cos_0.05A_charge.sdu` |

## EIS workbook

| Field | Observation |
| --- | --- |
| File | `EIS_0.05A_Charge_part1.xlsx` |
| Repository path | `EIS_Raw & Processed_data_for_DIB/EIS_Raw_data_xlsx/EIS_0.05A_Charge/EIS_0.05A_Charge_part1.xlsx` |
| SHA-256 | `5f2dbbb0830a7b72066380769880a117f7331fddcdf2e2664429f4e2c4afd2a1` |
| Sheets | `Global_Info`, `ACIM_Chan1`, `Channel_1_1` |
| ACIM table | 22 rows by 9 columns |
| Directly visible EIS fields | device ID, test ID, channel ID, cycle ID, step ID, point index, frequency, impedance magnitude, impedance phase |
| Time-series table | 8,319 rows by 13 columns, with the same time/voltage/current/capacity family as the COS workbook |
| Reported schedule | `LFP_26650\\EIS_GALANOSTATIC_EIS_0.05A_charge_direction.sdu` |

## Evidence decision

**Decision: more metadata needed.**

The source provides two valuable and compatible-looking structures: an explicit time-series table and a separate EIS table with frequency and impedance fields. However, the files were produced on different reported channels and their report starts are separated in time. The shared 0.05 A charge condition and schedule namespace are not enough to prove a same-cell, same-SOC, or same-event relationship.

## What the source can support now

- read-only TS and EIS structural parser tests;
- EIS CSV/MAT/XLSX intake design;
- a documented search for state-aware identifiers; and
- a future method comparison once units and sign conventions are confirmed.

## What it cannot support yet

- a scientific TS-to-EIS pairing claim;
- a supervised model target linking COS windows to EIS values; or
- a DRT interpretation tied to a specific time-series state.

## Next decision

Search the source documentation for cell, SOC, temperature, and test-repeat mapping. If these cannot be recovered from source metadata, preserve the negative result and keep this source as an open structural benchmark rather than a matched validation dataset.
