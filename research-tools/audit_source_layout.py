"""Create a read-only manifest for a downloaded battery-data source.

The tool records file paths, sizes, hashes, and simple text-table headers. It
does not alter input data and it does not claim a TS/EIS/DRT match. Use its
JSON output to fill ``source_audit_template.csv`` after a small source sample
has been downloaded locally.
"""

import argparse
import csv
import hashlib
import json
from pathlib import Path


TEXT_TABLE_EXTENSIONS = {".csv", ".txt", ".tsv"}


def sha256(path: Path) -> str:
    """Return a stable checksum without loading the full file into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def text_headers(path: Path):
    """Return a best-effort header row for a small delimited text table."""
    if path.suffix.lower() not in TEXT_TABLE_EXTENSIONS:
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            sample = handle.read(4096)
            if not sample.strip():
                return []
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
            handle.seek(0)
            return next(csv.reader(handle, dialect), [])
    except (OSError, UnicodeDecodeError, csv.Error, StopIteration):
        return []


def audit_directory(directory: Path):
    """Build a deterministic, read-only inventory of supported local files."""
    files = []
    for path in sorted(candidate for candidate in directory.rglob("*") if candidate.is_file()):
        files.append(
            {
                "relative_path": str(path.relative_to(directory)),
                "extension": path.suffix.lower() or "[no extension]",
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "headers": text_headers(path),
            }
        )
    return {
        "audit_scope": "File inventory and best-effort text headers only",
        "source_directory": str(directory.resolve()),
        "files_found": len(files),
        "files": files,
        "interpretation_note": (
            "A common cell ID or filename is not enough to establish a TS/EIS "
            "match. Confirm state, test point, temperature, protocol, and units "
            "in the source metadata before creating a scientific join."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Create a read-only battery source audit manifest.")
    parser.add_argument("source_directory", type=Path, help="Local directory containing a small downloaded source sample.")
    parser.add_argument("--output", type=Path, help="Optional JSON output path; otherwise print to stdout.")
    args = parser.parse_args()

    if not args.source_directory.is_dir():
        parser.error("source_directory must be an existing directory")

    report = audit_directory(args.source_directory)
    serialized = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(serialized + "\n", encoding="utf-8")
        print(args.output)
    else:
        print(serialized)


if __name__ == "__main__":
    main()
