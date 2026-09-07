"""Read-only screening for a tabular EIS spectrum.

This check is intentionally limited to structural readiness. It does not run a
Kramers-Kronig test and it does not claim that a DRT result is valid.
"""

import csv
import math
from pathlib import Path


REQUIRED_COLUMNS = ("frequency_hz", "z_real_ohm", "z_imag_ohm")


def _number(value):
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def inspect_eis_csv(path):
    """Return a transparent structural report for one EIS CSV file."""
    path = Path(path)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        missing_columns = [column for column in REQUIRED_COLUMNS if column not in columns]
        rows = list(reader)

    valid = []
    invalid_rows = 0
    for row in rows:
        frequency, z_real, z_imag = (_number(row.get(column)) for column in REQUIRED_COLUMNS)
        if frequency is None or z_real is None or z_imag is None or frequency <= 0:
            invalid_rows += 1
            continue
        valid.append((frequency, z_real, z_imag))

    frequencies = [row[0] for row in valid]
    duplicated_frequencies = len(frequencies) - len(set(frequencies))
    descending = all(left > right for left, right in zip(frequencies, frequencies[1:]))
    ascending = all(left < right for left, right in zip(frequencies, frequencies[1:]))
    ready = not missing_columns and bool(valid) and invalid_rows == 0 and (ascending or descending)

    return {
        "file": path.name,
        "columns": columns,
        "required_columns": list(REQUIRED_COLUMNS),
        "missing_columns": missing_columns,
        "rows_total": len(rows),
        "rows_valid": len(valid),
        "rows_invalid": invalid_rows,
        "frequency_hz": {
            "min": min(frequencies) if frequencies else None,
            "max": max(frequencies) if frequencies else None,
            "order": "ascending" if ascending else "descending" if descending else "not_monotonic",
            "duplicate_count": duplicated_frequencies,
        },
        "drt_input_ready": ready,
        "scope_note": (
            "Structural screening only. Run EIS consistency, reconstruction, "
            "residual, stability, and uncertainty checks before interpreting DRT."
        ),
    }
