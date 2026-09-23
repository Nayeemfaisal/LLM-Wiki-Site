"""Generate the dated supervisor update PDF."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import ListFlowable, ListItem, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Nayeem_Faisal_Supervisor_Update_2026-09-24.pdf"
NAVY = colors.HexColor("#13253A")
TEAL = colors.HexColor("#087F8C")
INK = colors.HexColor("#20303F")
MUTED = colors.HexColor("#64748B")
LINE = colors.HexColor("#D7E0E7")
PALE = colors.HexColor("#F5F8FA")


def footer(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(LINE)
    canvas.line(1.65 * cm, 1.25 * cm, width - 1.65 * cm, 1.25 * cm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.65 * cm, 0.82 * cm, "Battery TS + EIS + DRT Research - Nayeem Faisal")
    canvas.drawRightString(width - 1.65 * cm, 0.82 * cm, f"Page {doc.page}")
    canvas.restoreState()


def bullet_list(items, style):
    return ListFlowable([ListItem(Paragraph(item, style)) for item in items], bulletType="bullet", leftIndent=16, bulletFontName="Helvetica", bulletFontSize=8, bulletColor=TEAL, spaceBefore=3, spaceAfter=10)


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=1.65 * cm, rightMargin=1.65 * cm, topMargin=1.55 * cm, bottomMargin=1.7 * cm, title="Supervisor Update - 24 September 2026", author="Nayeem Faisal")
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=25, leading=30, textColor=NAVY, spaceAfter=8),
        "subtitle": ParagraphStyle("subtitle", parent=base["BodyText"], fontName="Helvetica", fontSize=11, leading=16, textColor=INK, spaceAfter=16),
        "kicker": ParagraphStyle("kicker", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=TEAL, spaceBefore=8, spaceAfter=4),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=NAVY, spaceBefore=4, spaceAfter=7),
        "body": ParagraphStyle("body", parent=base["BodyText"], fontName="Helvetica", fontSize=9.4, leading=14, textColor=INK, spaceAfter=8),
        "bullet": ParagraphStyle("bullet", parent=base["BodyText"], fontName="Helvetica", fontSize=9.1, leading=13, textColor=INK),
        "small": ParagraphStyle("small", parent=base["BodyText"], fontName="Helvetica", fontSize=8, leading=11, textColor=MUTED),
        "table": ParagraphStyle("table", parent=base["BodyText"], fontName="Helvetica", fontSize=8.2, leading=11, textColor=INK),
        "tablehead": ParagraphStyle("tablehead", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8.2, leading=11, textColor=colors.white),
    }
    story = [Spacer(1, 0.4 * cm), Paragraph("SUPERVISOR UPDATE", styles["kicker"]), Paragraph("Battery TS + EIS + DRT Research", styles["title"]), Paragraph("Prepared by Nayeem Faisal | 24 September 2026 | Evidence-led source intake and next research decision", styles["subtitle"])]
    summary = Table([
        [Paragraph("<b>Current position</b><br/>The project has a public research record, source evidence ledger, DRT evaluation protocol, and local structural EIS intake prototype.", styles["body"]), Paragraph("<b>New research increment</b><br/>Two supervisor-recommended TUM ageing sources have been screened and assigned specific roles without overstating their EIS coverage.", styles["body"])],
        [Paragraph("<b>What is ready</b><br/>Controlled file-level audit and adapter work for one direct TS + EIS candidate.", styles["body"]), Paragraph("<b>Scientific boundary</b><br/>No source is called a TS + EIS + DRT match until file-level identifiers, state, protocol, units, and impedance coverage are verified.", styles["body"])],
    ], colWidths=[8.25 * cm, 8.25 * cm], style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE), ("BOX", (0, 0), (-1, -1), 0.5, LINE), ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    story += [summary, Spacer(1, 0.4 * cm), Paragraph("WORK COMPLETED", styles["kicker"]), Paragraph("From literature to a testable research workflow", styles["h2"]), bullet_list(["Reviewed the supervisor-provided battery-data paper and converted it into four quality gates: source provenance, experiment context, a proven TS-to-EIS join, and DRT quality.", "Added the TUM LG MJ1 ageing, charging, BEV-profile, and OCV source to the candidate registry and evidence ledger.", "Added the TUM 196-cell ageing campaign with repeated SOH and degradation-mode labels to the candidate registry and evidence ledger.", "Updated the dated public wiki pages so all conclusions and pending checks remain reviewable."], styles["bullet"])]
    story += [PageBreak(), Paragraph("SOURCE ASSESSMENT", styles["kicker"]), Paragraph("How the new TUM sources support the project", styles["h2"])]
    rows = [[Paragraph("Source", styles["tablehead"]), Paragraph("Verified contribution", styles["tablehead"]), Paragraph("Role in this project", styles["tablehead"]), Paragraph("Boundary / next audit", styles["tablehead"])]]
    for row in [
        ("LG MJ1 ageing, charging, and BEV profiles", "10 LG Chem INR18650 MJ1 cells; capacity/resistance ageing, BEV profiles, charging curves, quasi-stationary OCV.", "Time-series ingestion, ageing-state metadata, partial-charge and OCV features.", "No EIS pairing established. Audit README, identifiers, and archive layout."),
        ("196-cell experimental degradation study", "Calendar, cyclic, and dynamic ageing; periodic capacity, resistance, LLI, LAM_NE, and LAM_PE labels.", "Large TS-to-SOH and degradation-label reference; protocol-sensitivity benchmark.", "No EIS pairing established. Audit time-series/check-up keys and look for explicit impedance material."),
        ("Direct TS + EIS queue", "LFP EIS/pulse, fast-charge ageing, 48-cell degradation path, online EIS prediction, and A123 multimodal candidates.", "Controlled source-level TS-to-EIS matching and later DRT evaluation.", "Start with one small lawful sample and a file manifest."),
    ]:
        rows.append([Paragraph(value, styles["table"]) for value in row])
    table = Table(rows, colWidths=[3.4 * cm, 4.7 * cm, 4.25 * cm, 4.15 * cm], repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.4, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    story += [table, Spacer(1, 0.45 * cm), Paragraph("NEXT CONTROLLED TASK", styles["kicker"]), Paragraph("One source, one manifest, one evidence decision", styles["h2"]), bullet_list(["Select one direct candidate that has both time-series and EIS evidence.", "Download the smallest lawful sample and run the read-only source inventory.", "Record cell, test, cycle, state, temperature, protocol, units, licence, and checksum fields.", "Decide pass, hold, or reject for the TS-to-EIS join. Preserve negative findings.", "Only a supported join proceeds to structural EIS intake and DRT evaluation."], styles["bullet"]), Paragraph("Decision requested: confirm whether the first experiment should prioritise state-aware matching, ageing-labelled modelling, or an EIS/DRT method benchmark.", styles["body"]), Spacer(1, 0.12 * cm), Paragraph("Public wiki: https://nayeemfaisal.github.io/LLM-Wiki-Site/", styles["small"]), Paragraph("Key sources: https://doi.org/10.3390/batteries9070385 | https://doi.org/10.1016/j.est.2022.106517 | https://doi.org/10.1016/j.jpowsour.2022.232498", styles["small"])]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()
