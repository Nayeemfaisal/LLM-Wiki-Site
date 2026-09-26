"""Inspect workbook structure for a battery-data source without changing it."""

import argparse
import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile


MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
DOC_REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKG_REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def text(element) -> str:
    return "".join(node.text or "" for node in element.iter(f"{MAIN}t"))


def shared_strings(archive: ZipFile):
    try:
        root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return [text(item) for item in root.findall(f"{MAIN}si")]


def workbook_sheets(archive: ZipFile):
    workbook = ElementTree.fromstring(archive.read("xl/workbook.xml"))
    rels = ElementTree.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {
        item.attrib["Id"]: item.attrib["Target"]
        for item in rels.findall(f"{PKG_REL}Relationship")
    }
    sheets = []
    for item in workbook.findall(f"{MAIN}sheets/{MAIN}sheet"):
        relation_id = item.attrib[f"{DOC_REL}id"]
        target = targets[relation_id].lstrip("/")
        if not target.startswith("xl/"):
            target = f"xl/{target}"
        sheets.append((item.attrib["name"], target))
    return sheets


def value(cell, strings):
    kind = cell.attrib.get("t")
    if kind == "inlineStr":
        inline = cell.find(f"{MAIN}is")
        return text(inline) if inline is not None else ""
    raw = cell.findtext(f"{MAIN}v")
    if raw is None:
        return ""
    if kind == "s":
        return strings[int(raw)]
    return raw


def sheet_preview(archive: ZipFile, path: str, strings, preview_rows: int):
    root = ElementTree.fromstring(archive.read(path))
    dimension = root.find(f"{MAIN}dimension")
    rows = []
    for row in root.findall(f"{MAIN}sheetData/{MAIN}row")[:preview_rows]:
        rows.append([value(cell, strings) for cell in row.findall(f"{MAIN}c")])
    return {
        "dimension": dimension.attrib.get("ref", "") if dimension is not None else "",
        "preview_rows": rows,
        "header_row": rows[0] if rows else [],
    }


def inspect(path: Path, preview_rows: int):
    with ZipFile(path) as archive:
        strings = shared_strings(archive)
        sheets = [
            {"name": name, **sheet_preview(archive, location, strings, preview_rows)}
            for name, location in workbook_sheets(archive)
        ]
    return {
        "file": str(path),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "format": "XLSX",
        "sheets": sheets,
    }


def main():
    parser = argparse.ArgumentParser(description="Read-only XLSX structure inspection.")
    parser.add_argument("workbooks", type=Path, nargs="+", help="One or more XLSX files")
    parser.add_argument("--preview-rows", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = {
        "audit_scope": "Workbook structure, top rows, and checksums only",
        "workbooks": [inspect(path, args.preview_rows) for path in args.workbooks],
        "interpretation_note": "Shared labels do not prove a scientific TS-to-EIS join. Confirm cell, state, test, temperature, protocol, and units before adaptation.",
    }
    serialized = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(serialized + "\n", encoding="utf-8")
        print(args.output)
    else:
        print(serialized)


if __name__ == "__main__":
    main()
