# Supervisor Update - 24 September 2026

**Researcher:** Nayeem Faisal  
**Project:** Battery TS + EIS + DRT data pipeline  
**Public wiki:** https://nayeemfaisal.github.io/LLM-Wiki-Site/

## Work completed

- Added a dated reading note from the supervisor-provided battery-data review.
- Converted the review into four implementation gates: source provenance, experimental context, a proven TS-to-EIS join, and DRT quality checks.
- Added the TUM LG MJ1 ageing, charging, BEV-profile, and OCV dataset as a time-series and ageing reference.
- Added the TUM 196-cell experimental degradation study as a TS-to-SOH and degradation-label reference.
- Updated the public evidence ledger and candidate registry with evidence boundaries and next audit questions.
- Kept the direct TS + EIS + DRT candidates separate from TS-only ageing references.

## Verified research position

- The LG MJ1 source contains ten commercial cells with ageing measurements, BEV profiles, charging curves, and quasi-stationary OCV data.
- The 196-cell TUM study includes calendar, cyclic, and dynamic ageing conditions with repeated capacity, resistance, LLI, LAM_NE, and LAM_PE measurements.
- Neither TUM source is currently claimed as a direct TS + EIS + DRT match because the public descriptions do not establish joinable impedance data.

## Next controlled task

1. Select one direct candidate with time-series and EIS evidence.
2. Download the smallest lawful sample.
3. Build a manifest with cell, test, state, temperature, protocol, units, and checksum fields.
4. Decide whether a TS-to-EIS join is supported, needs more metadata, or should be rejected.
5. Run EIS and DRT evaluation only after a supported join exists.

## Sources

- Hassini, M., Redondo-Iglesias, E., and Venet, P. (2023). *Lithium-Ion Battery Data: From Production to Prediction*. https://doi.org/10.3390/batteries9070385
- Schmitt, J. et al. (2023). *Capacity and degradation mode estimation for lithium-ion batteries based on partial charging curves at different current rates*. https://doi.org/10.1016/j.est.2022.106517
- Wildfeuer, L. et al. (2023). *Experimental degradation study of a commercial lithium-ion battery*. https://doi.org/10.1016/j.jpowsour.2022.232498
