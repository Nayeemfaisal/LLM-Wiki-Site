# October 2026 Evidence-Gated Research Programme

## Purpose

Build a small, defensible TS + EIS + DRT benchmark rather than a large collection of loosely related battery files. This is a four-week execution plan. It is not a record of completed results.

## Research question

Under what documented conditions can a battery time-series segment be linked to an EIS spectrum and then assessed with a reproducible DRT workflow?

## Core idea: three distinct link levels

| Level | Meaning | Permitted use |
| --- | --- | --- |
| File coexistence | TS and EIS files occur in the same source. | Format and parser tests only. |
| Cell-level association | Both modalities share a cell or test ID. | Per-cell inventory and structural comparison. |
| Event-level match | Cell/test, SOC or state, temperature, protocol, and acquisition relationship are documented. | Adapter experiment and cautious TS-to-EIS analysis. |

No level may be silently treated as a higher level.

## Week 1: Source and metadata gate

- Audit one controlled candidate: the formation-protocol and electrolyte source with `data.mat`, `eis.mat`, and its DB workbook.
- Record source terms, file paths, checksums, variable names, units, test IDs, SOC, temperature, and protocol fields.
- Repeat the same manifest for the fast-charge ageing source only after its licence and archive layout are documented.
- Deliverable: two machine-readable audit records and an explicit `join supported`, `more metadata needed`, or `join not supported` decision for each source.

## Week 2: Adapter and quality gate

- Implement a read-only adapter for one accepted source that outputs a canonical table for the time-series and EIS sides without fabricating columns.
- Add EIS preflight checks: frequency ordering, finite values, duplicate frequencies, unit declaration, and sign-convention record.
- Keep a rejected-input log with the reason for rejection.
- Deliverable: one fixture, one structural report, and a repeatable command that produces the report.

## Week 3: DRT reproducibility gate

- Run one declared DRT configuration on a small approved EIS subset.
- Save configuration, frequency range, regularisation or prior choices, output grid, reconstruction, and residuals.
- Test stability under a documented perturbation such as removed frequency points or bounded noise.
- Deliverable: one reconstruction-and-stability note. It is a method result, not a battery-state prediction result.

## Week 4: Comparison and supervisor package

- Compare the source against a second candidate only at the evidence level supported by each manifest.
- Summarise what is transferable, what remains source-specific, and what has been rejected.
- Prepare a concise supervisor brief: objective, method, evidence table, result boundary, next decision.
- Deliverable: dated wiki update, reproducibility links, and a short presentation outline.

## Acceptance criteria for the first adapter

- A shared cell or test identifier is documented in source files.
- The EIS state is defined by SOC or another explicit state field, with temperature and protocol context where supplied.
- Frequency and complex impedance columns have recorded units and conventions.
- The adapter preserves source fields and flags missing information instead of guessing.

## Stop rules

- Do not create an event-level training pair from folder names alone.
- Do not interpret a DRT output before EIS preflight and reconstruction review.
- Do not compare datasets as equivalent when chemistry, cell architecture, state, or protocol differ.

## Candidate roles at programme start

- **Formation-protocol source:** best next controlled join audit because its public record describes `data.mat`, `eis.mat`, and a test-ID workbook.
- **A123 multimodal source:** cell-level benchmark for ingestion and EIS preflight; event alignment remains open.
- **LFP SOC EIS pulse source:** structural TS/EIS benchmark; current raw audit has not proved a same-cell/same-state join.
- **Fast-charge ageing source:** ageing-oriented candidate with cycling, temperature, and post-ageing EIS; requires archive-level identifier audit.
- **RWTH EIS Data Analytics:** method baseline for EIS/DRT checks, not a new scientific data match.
