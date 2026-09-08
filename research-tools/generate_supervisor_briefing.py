"""Create a supervisor-ready PDF from the dated research record.

The report intentionally separates completed implementation, verified public
source descriptions, and work that still requires raw-file inspection.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
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
OUTPUT = ROOT / "output" / "pdf" / "Nayeem_Faisal_Battery_Research_Supervisor_Briefing_2026-09-08.pdf"

NAVY = colors.HexColor("#112536")
TEAL = colors.HexColor("#168B8B")
MINT = colors.HexColor("#E8F5F1")
BLUE = colors.HexColor("#EAF2FB")
AMBER = colors.HexColor("#FFF3D9")
INK = colors.HexColor("#1F2933")
MUTED = colors.HexColor("#52606D")
LINE = colors.HexColor("#CBD5DF")


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=28, leading=33, textColor=NAVY, spaceAfter=9),
        "subtitle": ParagraphStyle("subtitle", parent=base["BodyText"], fontName="Helvetica", fontSize=12, leading=17, textColor=MUTED, spaceAfter=18),
        "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=NAVY, spaceBefore=4, spaceAfter=8),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=NAVY, spaceBefore=10, spaceAfter=6),
        "body": ParagraphStyle("body", parent=base["BodyText"], fontName="Helvetica", fontSize=9.4, leading=13.2, textColor=INK, spaceAfter=6),
        "small": ParagraphStyle("small", parent=base["BodyText"], fontName="Helvetica", fontSize=7.8, leading=10.2, textColor=MUTED),
        "bullet": ParagraphStyle("bullet", parent=base["BodyText"], fontName="Helvetica", fontSize=9.3, leading=13, leftIndent=14, firstLineIndent=-8, textColor=INK, spaceAfter=4),
        "caption": ParagraphStyle("caption", parent=base["BodyText"], fontName="Helvetica", fontSize=8, leading=10.5, textColor=MUTED, spaceBefore=4),
        "cover_label": ParagraphStyle("cover_label", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=TEAL, spaceAfter=11),
        "cover_note": ParagraphStyle("cover_note", parent=base["BodyText"], fontName="Helvetica", fontSize=10, leading=14, textColor=INK),
        "cell": ParagraphStyle("cell", parent=base["BodyText"], fontName="Helvetica", fontSize=7.8, leading=9.7, textColor=INK),
        "cell_bold": ParagraphStyle("cell_bold", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=7.8, leading=9.7, textColor=NAVY),
    }


def para(text, style):
    return Paragraph(text, style)


def bullets(items, styles):
    return [Paragraph("&bull; " + item, styles["bullet"]) for item in items]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(1.7 * cm, 1.4 * cm, A4[0] - 1.7 * cm, 1.4 * cm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(1.7 * cm, 0.9 * cm, "Battery TS + EIS + DRT research briefing - Nayeem Faisal")
    canvas.drawRightString(A4[0] - 1.7 * cm, 0.9 * cm, f"Page {doc.page}")
    canvas.restoreState()


def section_heading(label, heading, styles):
    return [Paragraph(label.upper(), styles["cover_label"]), Paragraph(heading, styles["h1"])]


def matrix(rows, widths, styles, header=True):
    rendered = [[para(cell, styles["cell_bold"] if header and row_index == 0 else styles["cell"]) for cell in row] for row_index, row in enumerate(rows)]
    table = Table(rendered, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
    ]))
    return table


def add_status_cards(styles):
    cards = [
        ("Research record", "Dated wiki pages, findings, source screens, and decision notes."),
        ("Dataset gate", "TS evidence + EIS evidence + a proven shared key are required."),
        ("Backend prototype", "Local API jobs plus single-file and batch EIS structural intake."),
        ("Scientific guardrail", "No candidate is called validated before raw-file audit and quality checks."),
    ]
    cells = []
    for label, detail in cards:
        cells.append([Paragraph(f"<b>{label}</b><br/>{detail}", styles["body"])])
    table = Table(cells, colWidths=[16.5 * cm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), MINT),
        ("BACKGROUND", (0, 1), (-1, 1), BLUE),
        ("BACKGROUND", (0, 2), (-1, 2), MINT),
        ("BACKGROUND", (0, 3), (-1, 3), AMBER),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = make_styles()
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=1.7 * cm, leftMargin=1.7 * cm,
        topMargin=1.55 * cm, bottomMargin=1.8 * cm,
        title="Battery TS, EIS and DRT Research Supervisor Briefing",
        author="Nayeem Faisal",
    )
    story = []

    # Cover
    story.extend([
        Spacer(1, 1.4 * cm),
        Paragraph("BATTERY RESEARCH WORKSPACE", styles["cover_label"]),
        Paragraph("TS + EIS + DRT\nSupervisor Briefing", styles["title"]),
        Paragraph("Research update prepared for the first supervisor meeting after the initial setup and evidence-screening period.", styles["subtitle"]),
        Spacer(1, 0.5 * cm),
        Table([[Paragraph("<b>Prepared by</b><br/>Nayeem Faisal", styles["body"]), Paragraph("<b>Date</b><br/>8 September 2026", styles["body"]), Paragraph("<b>Scope</b><br/>Dataset evidence, backend prototype, next experiment", styles["body"])]], colWidths=[5.4 * cm, 4.4 * cm, 6.7 * cm], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), MINT), ("BOX", (0, 0), (-1, -1), 0.6, TEAL),
            ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ])),
        Spacer(1, 0.7 * cm),
        Paragraph("<b>Core question</b>", styles["h2"]),
        Paragraph("Can a reproducible pipeline connect battery time-series measurements to EIS spectra and DRT-ready representations without inventing missing measurement context?", styles["cover_note"]),
        Spacer(1, 0.45 * cm),
        Paragraph("<b>One-sentence status</b>", styles["h2"]),
        Paragraph("The project now has a public, dated research record; an explicit dataset-selection gate; a local API/HPC prototype; and a stronger candidate queue ready for raw-file inspection.", styles["cover_note"]),
        Spacer(1, 1.2 * cm),
        Paragraph("Public wiki: https://nayeemfaisal.github.io/LLM-Wiki-Site/", styles["small"]),
        PageBreak(),
    ])

    # Executive summary
    story.extend(section_heading("1. Executive summary", "What is already in place", styles))
    story.append(add_status_cards(styles))
    story.append(Spacer(1, 0.35 * cm))
    story.append(Paragraph("The project deliberately uses a staged process. It starts with public-source evidence, then confirms raw-file structure, then builds one adapter, and only then evaluates EIS or DRT outputs. This protects the research from overclaiming and makes each negative result useful.", styles["body"]))
    story.extend(bullets([
        "The public wiki was reorganised into readable, dated pages for findings, candidate sources, implementation notes, and weekly updates.",
        "The TS + EIS + DRT selection gate is now explicit: time-series evidence, impedance evidence, and an honest shared key are all required.",
        "A local FastAPI prototype demonstrates job handling and read-only EIS intake before VM/HPC access is available.",
        "DRT validation is treated as layered evidence, not as a single pass/fail replacement for Kramers-Kronig validation.",
    ], styles))
    story.append(PageBreak())

    # Timeline
    story.extend(section_heading("2. Dated work record", "Week-by-week progress", styles))
    timeline = [
        ["Period", "Completed work", "Evidence / outcome"],
        ["18-23 Jul", "Repository handoff, local setup, initial data-pipeline walkthrough, public wiki organisation.", "Working local dashboard and clear project folders."],
        ["23-29 Jul", "Wiki redesign; TS/EIS/DRT target frame; first source screens; DRT method references collected.", "Dated pages, readable navigation, initial candidate rules."],
        ["22 Aug", "Four-source screen and Samsung broadband-EIS screen added.", "Priority queue and explicit file-level acceptance gate."],
        ["7 Sep", "A123 LFP multimodal record screened; first structural EIS intake endpoint added.", "71-cell TS/EIS candidate recorded; tested synthetic EIS fixture."],
        ["8 Sep", "Supervisor briefing; additional candidates; batch EIS intake; source ledger extended.", "Decision-ready research package, not a model-performance claim."],
    ]
    story.append(matrix(timeline, [2.2 * cm, 8.2 * cm, 6.1 * cm], styles))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Interpretation: the work completed so far is the research infrastructure and evidence screen needed to choose a defensible first experiment. The next phase is intentionally narrower: prove or reject one source-specific TS-to-EIS join.", styles["body"]))
    story.append(PageBreak())

    # Dataset matrix
    story.extend(section_heading("3. Dataset research", "Candidate roles and evidence status", styles))
    data_rows = [
        ["Source", "Published evidence", "Role in this project", "Status"],
        ["A123 LFP multimodal", "71 cells; charge-discharge TS, EIS, CV, ICA, PITT; cell-numbered files.", "Primary broad multimodal candidate.", "Ready for small file manifest"],
        ["LFP EIS + sine-wave pulses", "Commercial LFP cells; EIS and short-period sine-wave pulse data; CC0 licence.", "Primary state-matching candidate.", "Ready for small file manifest"],
        ["48-cell degradation indicators", "Ageing, pulses, qOCV, EIS, NFRA, and published DRT peak outputs.", "Ageing-oriented comparison candidate.", "Ready for small file manifest"],
        ["Oxford multisine EIS", "Raw current and voltage time series; one Samsung cell; MAT files; stationarity/linearity focus.", "EIS quality-control method reference.", "Method reference"],
        ["DigiCell 54-cell EIS", "EIS CSV files at 30% SOC plus CSVW and JSON-LD metadata.", "EIS schema and DRT-input control.", "EIS-only control"],
        ["Pipeline robustness dataset", "Different cycler exports, formats, EIS sheet, and intentional data errors.", "Parser and workflow robustness test.", "Backend test reference"],
    ]
    story.append(matrix(data_rows, [3.3 * cm, 5.6 * cm, 4.6 * cm, 3.0 * cm], styles))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Important: “ready for small file manifest” means the public description gives a plausible bridge. It does not mean the datasets have been scientifically matched or that a model has been validated.", styles["caption"]))
    story.append(PageBreak())

    # Method and backend
    story.extend(section_heading("4. Method and backend", "How the pipeline prevents unsupported conclusions", styles))
    story.append(Paragraph("<b>Selection and validation workflow</b>", styles["h2"]))
    workflow = [
        ["Step", "Question answered", "Recorded output"],
        ["1. Source screen", "Is TS, EIS, and a possible join described?", "Evidence ledger row"],
        ["2. File manifest", "What are the headers, units, IDs, SOC, temperature, and protocols?", "Source-specific manifest"],
        ["3. Structural EIS intake", "Are required EIS fields finite, positive-frequency, unique, and ordered?", "JSON intake report"],
        ["4. EIS quality", "Does the spectrum satisfy relevant consistency and residual checks?", "Quality record"],
        ["5. DRT preparation", "Is reconstruction stable across reasonable choices?", "DRT/reconstruction record"],
        ["6. Controlled model test", "Does the held-out TS/EIS relation survive a cell-level holdout?", "Pass/fail experiment note"],
    ]
    story.append(matrix(workflow, [2.5 * cm, 8.0 * cm, 6.0 * cm], styles))
    story.append(Spacer(1, 0.35 * cm))
    story.append(Paragraph("<b>Implemented local backend evidence</b>", styles["h2"]))
    story.extend(bullets([
        "The local FastAPI demo accepts a CSV job, writes a job status, runs a local worker, and returns JSON output.",
        "POST /intake/eis screens one local CSV for frequency_hz, z_real_ohm, and z_imag_ohm, including finite values, positive frequencies, duplicates, and ordering.",
        "POST /intake/eis-directory returns one structural report for every local EIS CSV in an approved directory.",
        "The included five-row synthetic fixture passes structural screening. It is a software test fixture, not a battery experiment or validation result.",
    ], styles))
    story.append(PageBreak())

    # Decision
    story.extend(section_heading("5. Decision and next experiment", "What needs approval in the meeting", styles))
    story.append(Paragraph("<b>Recommended first experiment: A123 LFP multimodal dataset</b>", styles["h2"]))
    story.extend(bullets([
        "Download a minimal approved sample: one charge-discharge workbook and one EIS file for the same numbered cell.",
        "Create a manifest recording the exact file names, columns, units, state labels, temperature, protocol, and licence.",
        "Determine whether the shared cell number can be refined to the same test state; if not, report this as an incompatibility rather than forcing a match.",
        "Map the EIS file into the structural intake endpoint, then run the separate EIS and DRT quality workflow.",
    ], styles))
    story.append(Paragraph("<b>Supervisor decisions requested</b>", styles["h2"]))
    decision_rows = [
        ["Decision", "Why it matters", "Suggested answer"],
        ["Primary source", "Prevents simultaneous work on incompatible sources.", "Approve A123 for the first file-manifest test; retain LFP EIS/pulse as the focused fallback."],
        ["Success measure", "Defines the first experiment before any modelling begins.", "Start with state-aware TS-to-EIS matching and EIS reconstruction, then assess DRT stability."],
        ["Compute environment", "Clarifies when the local mock becomes a VM/HPC job.", "Keep local API contract; replace local worker only when VM/HPC access is confirmed."],
    ]
    story.append(matrix(decision_rows, [3.0 * cm, 5.4 * cm, 8.1 * cm], styles))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("<b>Next 14 days</b>", styles["h2"]))
    story.extend(bullets([
        "Complete and review the two-file A123 manifest.",
        "Add exactly one adapter only after the manifest passes the evidence gate.",
        "Run structural screening, EIS quality checks, and a reconstruction/stability note on one spectrum.",
        "Publish a short pass/fail result with raw-file links and the chosen parameters.",
    ], styles))
    story.append(PageBreak())

    # Talking points and sources
    story.extend(section_heading("6. Meeting notes", "Short presentation script and sources", styles))
    story.append(Paragraph("<b>60-second opening</b>", styles["h2"]))
    story.append(Paragraph("“I started by making the work auditable before making model claims. The wiki now records each week separately, and I introduced one rule for all new sources: we need time-series data, EIS data, and an explicit matching key. On the implementation side, the local API prototype can now screen EIS files structurally before DRT preparation. The new source screen gives us two strong starting candidates: the 71-cell A123 LFP multimodal data and the LFP EIS plus sine-pulse data. My request today is to select one source and agree on the first success measure before I build the adapter.”", styles["body"]))
    story.append(Paragraph("<b>Sources used for this update</b>", styles["h2"]))
    sources = [
        "A123 LFP multimodal electrochemical dataset: https://github.com/huangjin-collab/A123-LFP-Battery-Multimodal-Electrochemical-Dataset",
        "LFP SOC EIS and sine-wave pulse dataset: https://github.com/yizhaogao2025/LFP_battery_SOC_Dataset",
        "Degradation path indicators for lithium-ion batteries: https://zenodo.org/records/15755725",
        "Multisine EIS dataset, Oxford Research Archive: https://ora.ox.ac.uk/objects/uuid%3A449dd462-0a37-45d0-88f9-832b84d27283",
        "DigiCell 54-cell EIS dataset: https://zenodo.org/records/15422339",
        "Battery datasets for testing data pipelines and workflow automation: https://zenodo.org/records/21631502",
        "GP-DRT comparator: https://github.com/ciuccislab/GP-DRT",
        "IEST DRT analysis guide: https://iestbattery.com/case/drt-analysis-eis-deconvolution-guide/",
    ]
    story.extend(bullets(sources, styles))
    story.append(Spacer(1, 0.25 * cm))
    story.append(Paragraph("All source-level claims in this briefing come from the linked public records. Raw-file compatibility, licences, and state-level joins remain explicit checks for the next phase.", styles["caption"]))

    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build()
