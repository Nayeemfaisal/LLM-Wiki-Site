"""Create the October 2026 Battery DRT research programme briefing."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Nayeem_Faisal_October_Research_Programme_2026-10-05.pdf"

NAVY = colors.HexColor("#102A43")
BLUE = colors.HexColor("#1B5E8F")
MAGENTA = colors.HexColor("#D81B60")
TEAL = colors.HexColor("#007C82")
GREEN = colors.HexColor("#2E7D5A")
AMBER = colors.HexColor("#A76100")
INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#53657D")
PALE_BLUE = colors.HexColor("#EEF6FC")
PALE_TEAL = colors.HexColor("#ECF8F6")
PALE_AMBER = colors.HexColor("#FFF5E8")
RULE = colors.HexColor("#D9E2EC")


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "BriefTitle", parent=base["Title"], fontName="Helvetica-Bold", fontSize=25,
            leading=30, textColor=NAVY, spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "BriefSubtitle", parent=base["BodyText"], fontName="Helvetica", fontSize=11.4,
            leading=16, textColor=MUTED, spaceAfter=16,
        ),
        "h1": ParagraphStyle(
            "BriefH1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=17,
            leading=22, textColor=NAVY, spaceBefore=3, spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "BriefH2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=12.5,
            leading=16, textColor=BLUE, spaceBefore=9, spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "BriefBody", parent=base["BodyText"], fontName="Helvetica", fontSize=9.6,
            leading=14, textColor=INK, spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "BriefSmall", parent=base["BodyText"], fontName="Helvetica", fontSize=8.2,
            leading=11, textColor=MUTED, spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "BriefBullet", parent=base["BodyText"], fontName="Helvetica", fontSize=9.4,
            leading=13.2, leftIndent=13, firstLineIndent=-9, textColor=INK, spaceAfter=3,
        ),
        "eyebrow": ParagraphStyle(
            "BriefEyebrow", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8,
            leading=10, textColor=MAGENTA, spaceAfter=5, uppercase=True,
        ),
        "cell": ParagraphStyle(
            "BriefCell", parent=base["BodyText"], fontName="Helvetica", fontSize=8.3,
            leading=11, textColor=INK,
        ),
        "cell_bold": ParagraphStyle(
            "BriefCellBold", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8.3,
            leading=11, textColor=INK,
        ),
        "cell_header": ParagraphStyle(
            "BriefCellHeader", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8.3,
            leading=11, textColor=colors.white,
        ),
        "center": ParagraphStyle(
            "BriefCenter", parent=base["BodyText"], alignment=TA_CENTER, fontName="Helvetica",
            fontSize=8, leading=10, textColor=MUTED,
        ),
    }


def para(text, style):
    return Paragraph(text, style)


def bullet(text, styles):
    return para("&#8226; " + text, styles["bullet"])


def section_label(text, styles):
    return para(text.upper(), styles["eyebrow"])


def make_table(data, widths, styles, header=True):
    rendered = []
    for row_index, row in enumerate(data):
        rendered.append([
            para(str(value), styles["cell_header"] if header and row_index == 0 else styles["cell"])
            for value in row
        ])
    table = Table(rendered, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.35, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if header:
        style.extend([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ])
    for index in range(1 if header else 0, len(data)):
        if index % 2 == 0:
            style.append(("BACKGROUND", (0, index), (-1, index), colors.HexColor("#F7FAFC")))
    table.setStyle(TableStyle(style))
    return table


def callout(title, text, tint, accent, styles):
    content = [[
        para(f"<b>{title}</b><br/>{text}", styles["body"])
    ]]
    table = Table(content, colWidths=[17.1 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), tint),
        ("BOX", (0, 0), (-1, -1), 0.8, accent),
        ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return table


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    canvas.line(1.6 * cm, height - 1.35 * cm, width - 1.6 * cm, height - 1.35 * cm)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(NAVY)
    canvas.drawString(1.6 * cm, height - 1.05 * cm, "BATTERY TS + EIS + DRT RESEARCH")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width - 1.6 * cm, height - 1.05 * cm, "Nayeem Faisal | 5 October 2026")
    canvas.line(1.6 * cm, 1.2 * cm, width - 1.6 * cm, 1.2 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(1.6 * cm, 0.85 * cm, "Evidence-gated programme. Planned work is clearly separated from completed audits.")
    canvas.drawRightString(width - 1.6 * cm, 0.85 * cm, f"Page {doc.page}")
    canvas.restoreState()


def story(styles):
    items = []
    items.append(Spacer(1, 0.55 * cm))
    items.append(section_label("Supervisor research update", styles))
    items.append(para("Battery TS + EIS + DRT Research Programme", styles["title"]))
    items.append(para(
        "A concise record of the latest source audits, evidence boundaries, and the four-week plan for building one reproducible battery-data benchmark.",
        styles["subtitle"],
    ))
    items.append(callout(
        "Purpose", "Build a defensible connection between battery time-series data, EIS spectra, and DRT analysis. The programme records missing metadata as a result and does not create model targets from folder names or assumptions.",
        PALE_BLUE, BLUE, styles,
    ))
    items.append(Spacer(1, 0.35 * cm))
    items.append(section_label("Executive summary", styles))
    items.append(para("Current position", styles["h1"]))
    for point in [
        "<b>A123 audit completed:</b> Cell 1 through Cell 71 filenames link charge-discharge and EIS files at cell level. A sampled Cell 1 cycling workbook and EIS spectrum were inspected directly.",
        "<b>Important boundary:</b> the sampled cycling file does not expose time, SOC, temperature, or an event key. It cannot yet be used as a supervised time-window-to-EIS target.",
        "<b>New controlled candidate:</b> a public formation-protocol dataset describes complete electrochemical records and 50% SOC EIS within per-test folders. Its test-ID join must be verified at file level.",
        "<b>October plan:</b> source metadata gate, one read-only adapter, separate EIS/DRT quality gate, then an evidence-limited comparison and supervisor package.",
    ]:
        items.append(bullet(point, styles))
    items.append(Spacer(1, 0.25 * cm))
    items.append(section_label("Completed work", styles))
    items.append(para("Evidence recorded before modelling", styles["h2"]))
    completed = [
        ["Work item", "Verified outcome", "Status"],
        ["A123 repository audit", "71 consistent Cell N filenames across charge-discharge and EIS folders; raw Cell 1 sample checked.", "Completed"],
        ["Cycling structure", "Cell 1 workbook: 5,661 observations, with stage, current (A), and voltage (V).", "Completed"],
        ["EIS structure", "Cell 1 spectrum: 60 points, 10 kHz to 0.01 Hz, with frequency and complex impedance fields.", "Completed"],
        ["Evidence controls", "Registry, ledger, SHA-256 audit record, and public dated wiki pages updated.", "Completed"],
    ]
    items.append(make_table(completed, [4.0 * cm, 10.3 * cm, 2.8 * cm], styles))
    items.append(PageBreak())

    items.append(section_label("Source audit", styles))
    items.append(para("A123 LFP multimodal dataset", styles["h1"]))
    items.append(para(
        "Source: Huangjin-collab, A123 LFP Battery Multimodal Electrochemical Dataset. The source documents 71 A123-type LFP cells and corresponding charge-discharge, EIS, CV, ICA, and PITT files.",
        styles["body"],
    ))
    a123 = [
        ["Item", "Direct observation", "Interpretation"],
        ["Cell mapping", "Charge-discharge and EIS folders each contain Cell 1 through Cell 71 files.", "Cell-level association is explicit."],
        ["TS sample", "Char-dis-Cell1.xlsx contains Stage, Current (A), Voltage (V); 5,661 data rows.", "Usable for structural ingestion only."],
        ["EIS sample", "A123-EIS-1.txt has 60 points from 10 kHz to 0.01 Hz, with Z prime, Z double-prime, magnitude, phase, bias, and time.", "Usable for EIS and DRT preflight after convention review."],
        ["Missing link", "No sampled cycling field identifies the exact SOC, temperature, protocol state, or event corresponding to the spectrum.", "Event-level match remains unproved."],
    ]
    items.append(make_table(a123, [3.1 * cm, 8.2 * cm, 5.8 * cm], styles))
    items.append(Spacer(1, 0.35 * cm))
    items.append(callout(
        "Research decision", "Keep A123 as a cell-level multimodal benchmark. It may support ingestion, schema validation, and EIS/DRT preparation. It must not be presented as a matched TS-to-EIS training dataset until the missing event metadata is recovered.",
        PALE_AMBER, AMBER, styles,
    ))
    items.append(Spacer(1, 0.35 * cm))
    items.append(section_label("New candidate screen", styles))
    items.append(para("Formation-protocol and electrolyte source", styles["h2"]))
    for point in [
        "<b>Why it is promising:</b> the Zenodo record describes per-test folders containing complete electrochemical data in <i>data.mat</i> and EIS data in <i>eis.mat</i>, plus a DB workbook that indexes test conditions.",
        "<b>State context:</b> the public description states that EIS is measured at 50% SOC. That is a useful starting claim, not yet a verified file-level join.",
        "<b>Planned audit:</b> inspect one test folder and the DB workbook; record test ID, variable names, units, time alignment, SOC, temperature, protocol, and licence terms.",
        "<b>Role:</b> controlled method calibration candidate, not a direct substitute for a commercial full-cell ageing benchmark.",
    ]:
        items.append(bullet(point, styles))
    items.append(PageBreak())

    items.append(section_label("Research design", styles))
    items.append(para("The evidence-gated benchmark concept", styles["h1"]))
    items.append(para(
        "The central design choice is to keep data linkage separate from impedance analysis. A good DRT result does not prove that the time series and spectrum describe the same battery event.",
        styles["body"],
    ))
    levels = [
        ["Level", "Definition", "Allowed activity"],
        ["1. File coexistence", "TS and EIS occur in the same source.", "Parser and format tests."],
        ["2. Cell-level association", "TS and EIS share a documented cell or test ID.", "Per-cell inventory and structural comparison."],
        ["3. Event-level match", "Cell/test, SOC or state, temperature, protocol, and acquisition relationship are documented.", "Adapter experiment and cautious TS-to-EIS analysis."],
    ]
    items.append(make_table(levels, [3.6 * cm, 7.4 * cm, 6.1 * cm], styles))
    items.append(Spacer(1, 0.3 * cm))
    items.append(para("Acceptance criteria for the first adapter", styles["h2"]))
    for point in [
        "A documented shared cell or test identifier exists in source files.",
        "EIS state is defined by SOC or another explicit state field, with temperature and protocol context where supplied.",
        "Frequency and complex-impedance values have recorded units and a declared sign convention.",
        "The adapter preserves source fields and flags missing information instead of filling or guessing values.",
    ]:
        items.append(bullet(point, styles))
    items.append(Spacer(1, 0.2 * cm))
    items.append(para("Stop rules", styles["h2"]))
    for point in [
        "Do not create an event-level training pair from folder names alone.",
        "Do not interpret a DRT output before EIS preflight and impedance reconstruction review.",
        "Do not compare datasets as equivalent when chemistry, cell architecture, state, or protocol differ.",
    ]:
        items.append(bullet(point, styles))
    items.append(PageBreak())

    items.append(section_label("Four-week execution plan", styles))
    items.append(para("October programme", styles["h1"]))
    plan = [
        ["Wk.", "Objective", "Deliverable", "Decision gate"],
        ["1", "Source and metadata audit", "Two machine-readable manifests and source decisions.", "Join supported, more metadata needed, or join not supported."],
        ["2", "Read-only adapter and EIS preflight", "Canonical TS/EIS structural report, fixture, and rejected-input log.", "Only accepted source enters adapter work."],
        ["3", "DRT reproducibility check", "Declared configuration, reconstruction, residuals, and one stability test.", "Method result only; no state prediction claim."],
        ["4", "Evidence-limited comparison", "Supervisor brief, comparison table, and presentation outline.", "State what transfers and what remains source-specific."],
    ]
    items.append(make_table(plan, [1.2 * cm, 4.1 * cm, 6.0 * cm, 5.8 * cm], styles))
    items.append(Spacer(1, 0.4 * cm))
    items.append(callout(
        "Definition of success", "The month succeeds if it produces one fully documented evidence chain or a well-supported negative result. The aim is not to maximise the number of datasets, charts, or commits; it is to establish a reproducible and reviewable foundation for later modelling.",
        PALE_TEAL, TEAL, styles,
    ))
    items.append(Spacer(1, 0.35 * cm))
    items.append(section_label("Immediate next action", styles))
    items.append(para("First audit task", styles["h2"]))
    for point in [
        "Download one lawful test-ID folder and the DB workbook from the formation-protocol source.",
        "Run a read-only manifest on its contents and record variable names, dimensions, hashes, units, and identifiers.",
        "Write the join decision before building an adapter or attempting DRT.",
    ]:
        items.append(bullet(point, styles))
    items.append(PageBreak())

    items.append(section_label("Traceability", styles))
    items.append(para("References and public research record", styles["h1"]))
    refs = [
        ["Reference", "Use in this programme"],
        ["A123 LFP multimodal dataset\nhttps://github.com/huangjin-collab/A123-LFP-Battery-Multimodal-Electrochemical-Dataset", "Cell-level multimodal file audit; source of sampled Cell 1 observations."],
        ["Formation-protocol and electrolyte dataset\nhttps://zenodo.org/records/15688067", "Next controlled-source audit; public description reports data.mat, eis.mat at 50% SOC, and a DB workbook."],
        ["Fast-charge ageing dataset\nhttps://doi.org/10.17632/y328pbyvy4.1", "Ageing-oriented candidate with cycling, characterisation, temperature, and post-ageing EIS; file-level join remains to be audited."],
        ["RWTH EIS Data Analytics\nhttps://github.com/isea-rwth-aachen/EIS-Data-Analytics", "Method baseline for Lin-KK, equivalent-circuit, and DRT workflow checks; not a new TS-to-EIS match."],
        ["Public research wiki\nhttps://nayeemfaisal.github.io/LLM-Wiki-Site/", "Dated audit records, ledger, and plan are maintained in the public project record."],
    ]
    items.append(make_table(refs, [8.7 * cm, 8.4 * cm], styles))
    items.append(Spacer(1, 0.5 * cm))
    items.append(para("Prepared by Nayeem Faisal. Date: 5 October 2026.", styles["small"]))
    items.append(para("This briefing distinguishes completed audits from planned work and limits claims to the evidence currently recorded.", styles["small"]))
    return items


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4,
        rightMargin=1.6 * cm, leftMargin=1.6 * cm,
        topMargin=1.75 * cm, bottomMargin=1.55 * cm,
        title="Battery TS EIS DRT Research Programme",
        author="Nayeem Faisal",
        subject="October 2026 evidence-gated research programme",
    )
    doc.build(story(styles), onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()
