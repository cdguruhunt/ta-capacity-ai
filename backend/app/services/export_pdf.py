import io
from datetime import datetime

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_pdf_report(inputs, result) -> bytes:
    """Generate a professional PDF workforce planning report."""
    if not REPORTLAB_AVAILABLE:
        raise RuntimeError("reportlab not installed")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    dark = colors.HexColor("#1A1A2E")
    purple = colors.HexColor("#533483")

    title_style = ParagraphStyle("title", parent=styles["Title"], textColor=dark, fontSize=20, spaceAfter=4)
    subtitle_style = ParagraphStyle("subtitle", parent=styles["Normal"], textColor=colors.grey, fontSize=10, spaceAfter=16)
    section_style = ParagraphStyle("section", parent=styles["Heading2"], textColor=purple, fontSize=13, spaceBefore=14, spaceAfter=6)
    body_style = ParagraphStyle("body", parent=styles["Normal"], fontSize=10, leading=14)

    elements = []

    # Header
    elements.append(Paragraph("TalentScale AI", title_style))
    elements.append(Paragraph("Workforce Planning Report", subtitle_style))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}", body_style))
    elements.append(Spacer(1, 0.4 * cm))
    elements.append(HRFlowable(width="100%", thickness=2, color=purple))
    elements.append(Spacer(1, 0.4 * cm))

    # Input Parameters
    elements.append(Paragraph("Input Parameters", section_style))

    input_table_data = [
        ["Parameter", "Value"],
        ["Hiring Target", str(inputs.hiring_target)],
        ["Company Type", inputs.company_type.title()],
        ["Dropout Ratio", f"{inputs.dropout_ratio}%"],
        ["Complexity Factor", inputs.complexity_factor.title()],
        ["Recruiter Productivity", f"{inputs.recruiter_productivity} hires/year"],
        ["Geography", inputs.geography.title()],
        ["AI / Niche Hiring", f"{inputs.ai_niche_percent}%"],
    ]

    input_table = Table(input_table_data, colWidths=[8 * cm, 8 * cm])
    input_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), dark),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FC")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    elements.append(input_table)
    elements.append(Spacer(1, 0.6 * cm))

    # TA Structure Results
    elements.append(Paragraph("Recommended TA Structure", section_style))

    result_table_data = [
        ["Role / Metric", "Count / Value"],
        ["Adjusted Hiring Target", str(result.adjusted_hiring)],
        ["Total TA Team Size", str(result.total_ta)],
        ["Junior Recruiters (40%)", str(result.junior_recruiters)],
        ["Recruiters (35%)", str(result.recruiters)],
        ["Senior Recruiters (25%)", str(result.senior_recruiters)],
        ["Sourcers", str(result.sourcers)],
        ["Coordinators", str(result.coordinators)],
        ["Team Leads", str(result.leads)],
        ["Managers", str(result.managers)],
        ["TA Head", str(result.ta_head)],
        ["Hiring Capacity", str(result.hiring_capacity)],
        ["Estimated Timeline", result.timeline],
        ["Recruiter Utilization", f"{result.utilization}%"],
        ["Estimated Annual TA Cost", result.estimated_cost],
        ["Cost Per Hire", result.cost_per_hire],
        ["Calculation Model", result.model_used],
    ]

    result_table = Table(result_table_data, colWidths=[8 * cm, 8 * cm])
    result_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), purple),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F0FF")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    elements.append(result_table)
    elements.append(Spacer(1, 0.6 * cm))

    # Footer
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E5E7EB")))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(Paragraph(
        "TalentScale AI | Workforce Planning Intelligence | Confidential",
        ParagraphStyle("footer", parent=styles["Normal"], textColor=colors.grey, fontSize=8, alignment=TA_CENTER)
    ))

    doc.build(elements)
    return buffer.getvalue()
