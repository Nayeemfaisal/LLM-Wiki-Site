# DRT Evaluation Protocol

## Purpose

Use this protocol after a time-series to EIS match has been documented. It
keeps DRT interpretation separate from file-format screening.

## Before the DRT fit

- Record the source URL, licence, checksum, cell ID, test ID, cycle, SOC, temperature, and protocol.
- Confirm frequency, real impedance, imaginary impedance, and units.
- Run EIS quality checks appropriate to the experiment, including consistency checks and inspection for unstable or non-linear measurements.
- Keep the raw spectrum unchanged; write derived data to a separate output folder.

## Fit and reconstruction

- Fit the DRT with a declared method and fixed parameter record.
- Reconstruct impedance from the fitted representation.
- Compare reconstructed and measured real and imaginary components over the full frequency range.
- Retain residual plots and the numerical error summary.

## Stability and uncertainty

- Repeat the fit across a documented hyperparameter or regularisation range.
- Record which DRT peaks persist, move, merge, or disappear.
- Report uncertainty where the selected method supplies it; do not turn a broad or unstable feature into a named mechanism.
- Compare only spectra acquired under compatible state and protocol conditions.

## Decision rule

- **Proceed:** source join is documented, EIS checks are acceptable, reconstruction is adequate, and major DRT features are stable.
- **Hold:** a required identifier, unit, quality check, or stability result is missing.
- **Reject for this experiment:** the source cannot support an honest state-aware TS-to-EIS link.

## Reference implementation

The intended first comparison method is [GP-DRT](https://github.com/ciuccislab/GP-DRT). This document does not claim that GP-DRT has been run on any candidate source.
