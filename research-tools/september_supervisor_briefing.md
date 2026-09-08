# Supervisor briefing - 8 September 2026

## Research question

Can a reproducible pipeline link battery time-series (TS) measurements to EIS
spectra and DRT-ready impedance representations without inventing missing
measurement context?

## Work completed

- Public research wiki reorganised into dated updates, findings, source screens,
  and implementation notes.
- A data-selection rule established: TS fields, EIS fields, and an explicit
  matching key are required before a source is called a pipeline candidate.
- Local API/HPC demo implemented, including a read-only single-file and batch
  EIS structural intake check.
- DRT validation framed as layered checks: EIS consistency, impedance
  reconstruction, residuals, regularisation stability, and uncertainty.
- Source evidence ledger created so candidates, references, and unresolved
  questions do not become mixed together.

## Current evidence-based candidate queue

1. **A123 LFP multimodal dataset:** 71 cell-numbered charge-discharge and EIS
   records. Primary file-manifest candidate.
2. **LFP SOC EIS and sine-wave pulse dataset:** direct EIS plus short pulse
   modality. Primary state-matching candidate.
3. **48-cell degradation path indicators:** ageing, pulses, pseudo-OCV, EIS,
   and published DRT outputs. Primary ageing-oriented comparison candidate.
4. **Oxford multisine EIS:** one-cell raw time/current/voltage record for EIS
   quality-control methods.
5. **DigiCell 54-cell EIS:** a structured EIS-only control with CSVW/JSON-LD
   metadata.

## Decision requested from supervisor

- Approve one initial source for a small raw-file manifest and adapter test.
- Confirm the primary success measure: state-aware TS-to-EIS matching,
  EIS reconstruction error, or DRT stability.
- Confirm whether an external HPC/VM will be available after the local API
  contract is approved.

## Next 14 days

- Inspect a small file sample from the A123 and LFP sine-pulse sources.
- Record columns, units, state labels, protocols, and matching keys.
- Add one source-specific adapter only after the manifest is reviewed.
- Run EIS quality and reconstruction checks before DRT interpretation.
- Report a reproducible pass/fail matrix, including negative results.
