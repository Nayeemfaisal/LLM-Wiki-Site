# Source Screening: 24 September 2026

## Purpose

This screen adds three public resources to the battery TS, EIS, and DRT research queue. It is a planning record, not a claim that any source is already a validated TS + EIS + DRT match.

## Screening rule

A source can enter the research queue when public material describes a useful modality. It becomes a scientific matching candidate only after a file-level manifest confirms:

- cell or sample identity;
- test, cycle, state of charge, temperature, and protocol context;
- time-series and impedance fields with units;
- an explicit join rule; and
- licence and provenance information.

## 1. NASA PCoE lithium-ion battery ageing data

- **Source:** <https://data.nasa.gov/dataset/li-ion-battery-aging-datasets>
- **Reported coverage:** charge, discharge, and impedance operations at several temperatures in an ageing experiment. The landing record describes time, voltage, current, temperature, discharge capacity, and impedance-related fields.
- **Pipeline role:** archive-screening candidate for TS plus impedance data under an ageing context.
- **Why it is useful:** the reported experiment structure is close to the project question: repeated cycling plus impedance-related information and temperature context.
- **Boundary:** the current public landing page says that it has no directly attached data resource. The legacy archive, terms, and actual identifiers must be checked before it can be used.
- **Next action:** retrieve the lawful legacy archive and build a manifest for one battery before considering any adapter.

## 2. Broadband EIS with voltage and current acquisition across SOC

- **Source:** <https://doi.org/10.17632/zdsgxwksn5.1>
- **Supporting implementation reference:** <https://github.com/electrical-and-electronic-measurement/LiBEIS>
- **Reported coverage:** raw voltage/current acquisition material and broadband EIS material for lithium-ion batteries at different states of charge.
- **Pipeline role:** controlled SOC-aware acquisition-to-EIS screening candidate.
- **Why it is useful:** SOC is central to a defensible TS-to-EIS link. A small, clearly scoped source is better suited to a first manifest than a large opaque archive.
- **Boundary:** the public descriptions do not yet demonstrate which exact acquisition file belongs to which impedance spectrum.
- **Next action:** inspect one smallest file pair, then record IDs, SOC, temperature, waveform fields, impedance columns, units, and frequency order.

## 3. RWTH EIS Data Analytics benchmark

- **Source:** <https://github.com/isea-rwth-aachen/EIS-Data-Analytics>
- **Reported coverage:** Lin-KK, equivalent-circuit and DRT fitting workflows, plus examples for EIS-based state estimation.
- **Pipeline role:** method-reproducibility benchmark rather than a new training or validation dataset.
- **Why it is useful:** it creates a documented comparator for the EIS quality and DRT-analysis part of the workflow.
- **Boundary:** it does not prove a new TS-to-EIS match and its example-data provenance must be reviewed before reuse.
- **Next action:** reproduce one documented structural EIS check after the example-data licence and provenance are recorded.

## Priority after this screen

1. Inspect the broadband SOC source first because its state-conditioned design gives a focused potential join.
2. Keep NASA PCoE in the queue while resolving legacy archive access and file layout.
3. Use RWTH analytics only as a method baseline after a primary dataset has passed source auditing.

## Decision record

No source added today is labelled as a verified TS + EIS + DRT match. The next research result must be a manifest-backed pass, hold, or reject decision.
