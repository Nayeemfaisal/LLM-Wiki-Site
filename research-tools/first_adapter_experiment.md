# First Adapter Experiment

## Objective

Test whether one public source can support a reproducible, state-aware link
between a time-series segment and an EIS spectrum. This is an adapter and
evidence exercise, not a predictive-model result.

## Recommended sequence

1. **State-aware source:** inspect one EIS and one pulse file from the LFP SOC EIS and sine-wave collection.
2. **Ageing source:** inspect the small metadata workbook from the fast-charging ageing record before downloading a full archive.
3. **Direct modelling reference:** inspect one dynamic-profile / impedance pair from the online EIS-prediction collection.

## Per-source deliverables

- Source landing-page URL and licence record.
- Downloaded-file name, byte size, and SHA-256 checksum.
- Header/variable record with units.
- Cell, test, cycle, SOC, temperature, protocol, and timestamp fields when available.
- A written decision: `join supported`, `join not supported`, or `more metadata needed`.

## Acceptance criteria

A source can enter adapter implementation only when:

- TS and EIS records have a documented shared identifier.
- State and protocol compatibility can be evidenced rather than guessed.
- Frequency, real impedance, imaginary impedance, and units are available.
- The source terms allow the proposed local handling.

## Quality workflow after acceptance

1. Structural EIS intake.
2. EIS consistency and data-quality screening.
3. DRT fit with recorded method settings.
4. Impedance reconstruction and residual review.
5. DRT stability and uncertainty review.

## Stop rule

Stop and retain a negative result if a source cannot prove a state-aware join.
This prevents a polished model result from being built on an unsupported data
association.
