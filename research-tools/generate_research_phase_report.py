"""Generate the 8 September 2026 research-phase PDF briefing."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Nayeem_Faisal_Battery_Research_Phase_Update_2026-09-08.pdf"
NAVY, TEAL, INK = colors.HexColor("#13253a"), colors.HexColor("#087f8c"), colors.HexColor("#20303f")
MUTED, LINE, PALE = colors.HexColor("#64748b"), colors.HexColor("#d7e0e7"), colors.HexColor("#f5f8fa")


def bullets(items, styles):
    return ListFlowable(
        [ListItem(Paragraph(item, styles["bullet"])) for item in items],
        bulletType="bullet", leftIndent=16, bulletFontName="Helvetica",
        bulletFontSize=8, bulletColor=TEAL, spaceBefore=2, spaceAfter=8,
    )


def footer(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(LINE)
    canvas.line(1.6 * cm, 1.25 * cm, width - 1.6 * cm, 1.25 * cm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.6 * cm, 0.82 * cm, "Battery TS + EIS + DRT Research - Nayeem Faisal")
    canvas.drawRightString(width - 1.6 * cm, 0.82 * cm, f"Page {doc.page}")
    canvas.restoreState()


def section(title, label, body, items, styles):
    flow = [Paragraph(label.upper(), styles["kicker"]), Paragraph(title, styles["h2"])]
    if body:
        flow.append(Paragraph(body, styles["body"]))
    if items:
        flow.append(bullets(items, styles))
    return KeepTogether(flow)


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=1.65 * cm, rightMargin=1.65 * cm, topMargin=1.55 * cm, bottomMargin=1.7 * cm, title="Battery Research Phase Update - 8 September 2026", author="Nayeem Faisal")
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=25, leading=30, textColor=NAVY, spaceAfter=8),
        "subtitle": ParagraphStyle("subtitle", parent=base["BodyText"], fontName="Helvetica", fontSize=11, leading=16, textColor=INK, spaceAfter=16),
        "kicker": ParagraphStyle("kicker", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=TEAL, spaceBefore=8, spaceAfter=4),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=NAVY, spaceBefore=2, spaceAfter=7),
        "body": ParagraphStyle("body", parent=base["BodyText"], fontName="Helvetica", fontSize=9.4, leading=14, textColor=INK, spaceAfter=7),
        "bullet": ParagraphStyle("bullet", parent=base["BodyText"], fontName="Helvetica", fontSize=9.1, leading=13, textColor=INK),
        "small": ParagraphStyle("small", parent=base["BodyText"], fontName="Helvetica", fontSize=8, leading=11, textColor=MUTED),
        "table": ParagraphStyle("table", parent=base["BodyText"], fontName="Helvetica", fontSize=8, leading=10, textColor=INK),
        "tablehead": ParagraphStyle("tablehead", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.white),
    }
    story = [Spacer(1, 0.45 * cm), Paragraph("RESEARCH PHASE UPDATE", styles["kicker"]), Paragraph("Battery TS + EIS + DRT Pipeline", styles["title"]), Paragraph("Prepared by Nayeem Faisal | 8 September 2026 | Research record and next experiment plan", styles["subtitle"])]
    summary = Table([
        [Paragraph("<b>Research question</b><br/>Can time-series battery records be linked to EIS and DRT-ready impedance without guessing missing experimental context?", styles["body"]), Paragraph("<b>Current outcome</b><br/>A public research record, source evidence ledger, audit protocol, candidate priority queue, and local intake prototype are implemented.", styles["body"])],
        [Paragraph("<b>Scope of completed work</b><br/>Evidence screening, source-audit workflow, DRT evaluation protocol, backend structural checks, and weekly progress.", styles["body"]), Paragraph("<b>Boundary</b><br/>No public source is called a validated match until file-level identifiers, state, protocol, and units have been verified.", styles["body"])],
    ], colWidths=[8.25 * cm, 8.25 * cm], style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE), ("BOX", (0, 0), (-1, -1), 0.5, LINE), ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    story += [summary, Spacer(1, 0.45 * cm)]
    story += [
        section("What has been completed", "Completed work", "The work is organised as a traceable research programme rather than isolated scripts.", ["Published a professional public wiki with weekly pages, research findings, source links, and an implementation record.", "Created an evidence ledger that separates source facts, candidate status, and the next verification action.", "Added read-only EIS CSV structural screening for individual files and local CSV batches.", "Added an explicit DRT evaluation protocol: EIS quality, impedance reconstruction, residual review, stability, and uncertainty.", "Added reproducible source-audit tools that preserve file paths, sizes, checksums, and simple table headers."], styles),
        section("Why the quality gate matters", "Research method", "A common cell name is not enough to claim that a time-series segment and an EIS spectrum describe the same physical state.", ["Record cell or sample ID, test ID, cycle, SOC, temperature, protocol, timestamp, units, licence, and file checksum.", "Use a pass, hold, or reject decision for every source rather than forcing an uncertain match.", "Keep raw data unchanged and store derived outputs separately."], styles),
        PageBreak(), Paragraph("CANDIDATE DATASET REVIEW", styles["kicker"]), Paragraph("Evidence-led priority queue", styles["h2"]), Paragraph("The priority score is a transparent audit-planning aid. It ranks public evidence such as a TS-to-EIS relationship, state metadata, ageing context, raw access, licence clarity, and schema metadata. It is not a model score or a validation result.", styles["body"]),
    ]
    rows = [[Paragraph("Candidate", styles["tablehead"]), Paragraph("Role", styles["tablehead"]), Paragraph("Why it matters", styles["tablehead"]), Paragraph("First audit", styles["tablehead"])]]
    for row in [("LFP EIS + sine-wave pulses", "State-aware candidate", "EIS and controlled short-period pulse data for SOC estimation; CC0.", "Prove shared cell, SOC, temperature, and acquisition identifiers."), ("Fast-charging ageing dataset", "Ageing candidate", "12 Samsung 20R cells with raw cycling, temperature, characterisation, and post-ageing EIS; CC BY 4.0.", "Prove cell, cycle, check-up, temperature, and EIS linkage."), ("48-cell degradation path", "DRT comparison", "Ageing, pulse, pseudo-OCV, EIS, and BOL/EOL DRT peak material.", "Start with metrics workbook, then inspect one cell archive."), ("Online EIS prediction", "Direct benchmark", "Dynamic current/voltage groups are described with EIS trajectories.", "Verify profile identifiers after MATLAB conversion."), ("A123 multimodal LFP", "Broad manifest", "71 cells with charge-discharge, EIS, CV, ICA, and PITT by cell number.", "Check state and protocol beyond the cell ID.")]:
        rows.append([Paragraph(value, styles["table"]) for value in row])
    table = Table(rows, colWidths=[3.15 * cm, 3.0 * cm, 5.3 * cm, 5.05 * cm], repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.4, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    story += [table, Spacer(1, 0.35 * cm)]
    story += [
        section("Supporting sources", "Method and control roles", "Other candidates are retained for specific roles, rather than being incorrectly combined into one claim.", ["Oxford multisine EIS: quality and operando reconstruction reference from raw current and voltage time series.", "EIS degradation modes: ageing EIS control with periodic check-ups.", "DigiCell: 54 NMC811 spectra with JSON-LD and CSVW metadata for schema and intake testing."], styles),
        PageBreak(),
        section("First adapter experiment", "Controlled next step", "The immediate goal is an evidence decision, not a trained model.", ["Download only the smallest lawful sample from the LFP SOC/pulse source and the fast-charging ageing source.", "Run the read-only source inventory and record file checksums, sizes, extensions, and available headers.", "Complete the manifest with state, units, protocol, and source-location evidence.", "Decide: join supported, more metadata needed, or join not supported.", "Only a supported join proceeds to EIS screening and DRT analysis."], styles),
        section("DRT analysis after source acceptance", "Analysis protocol", "DRT interpretation is deliberately separated from file-format checks.", ["Confirm EIS frequency, real impedance, imaginary impedance, units, and experimental quality.", "Fit DRT with recorded settings and reconstruct impedance from the fitted representation.", "Retain residuals and numerical reconstruction error.", "Repeat across a documented parameter range and report stable versus unstable DRT features.", "Use uncertainty where the method provides it; do not name an unstable broad feature as a mechanism."], styles),
        section("Backend implementation", "Working software", "The local prototype provides a transparent bridge from the wiki to reproducible data checks.", ["POST /intake/eis: structural review of one local EIS CSV.", "POST /intake/eis-directory: per-file structural reports for a local CSV directory.", "GET /research/candidate-priorities: returns the evidence-led candidate queue used by the wiki.", "The intake reports are structural only; they do not claim Kramers-Kronig or DRT validity."], styles),
        PageBreak(), Paragraph("DECISION REQUEST", styles["kicker"]), Paragraph("What is needed for the next research block", styles["h2"]), Paragraph("The project is ready for a narrow, auditable first adapter experiment. The decision is which aim should lead the next block.", styles["body"]), bullets(["<b>State-aware matching:</b> begin with the LFP EIS and sine-wave pulse source.", "<b>Ageing and degradation:</b> begin with the fast-charging ageing source or the 48-cell degradation source.", "<b>Method validation:</b> begin with the online EIS-prediction or Oxford multisine source."], styles),
        section("Current conclusion", "Conclusion", "The research foundation is ready for controlled source-level evidence work. The next milestone is not a large model: it is a small, repeatable proof that one TS record and one EIS spectrum can be linked honestly under known conditions.", [], styles),
        Spacer(1, 0.15 * cm), Paragraph("Public project record: https://nayeemfaisal.github.io/LLM-Wiki-Site/", styles["small"]), Paragraph("Dataset priority review: https://nayeemfaisal.github.io/LLM-Wiki-Site/weekly/2026-09-08/dataset-priority-review/", styles["small"]), Paragraph("Key sources: LFP SOC EIS/pulse GitHub; Mendeley fast-charging ageing dataset; Zenodo degradation-path indicators; Oxford multisine EIS; GP-DRT repository.", styles["small"]),
    ]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()
