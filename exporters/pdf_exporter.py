"""Export employee data to an in-memory PDF report (ReportLab)."""
from datetime import datetime
from io import BytesIO

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

HEADERS = ["Code", "Name", "Email", "Department", "Designation", "Salary (INR)", "Hired", "Status"]


def export_to_pdf(df: pd.DataFrame, title: str = "Employee Report") -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                            leftMargin=12 * mm, rightMargin=12 * mm,
                            topMargin=12 * mm, bottomMargin=12 * mm)
    styles = getSampleStyleSheet()
    cell = styles["BodyText"]
    cell.fontSize, cell.leading = 8, 10

    rows = [HEADERS]
    for _, r in df.iterrows():
        rows.append([
            r["emp_code"],
            Paragraph(f"{r['first_name']} {r['last_name']}", cell),
            Paragraph(str(r["email"]), cell),
            r["department"],
            Paragraph(str(r["designation"]), cell),
            f"{r['salary']:,.0f}",
            r["hire_date"],
            r["status"],
        ])

    table = Table(rows, repeatRows=1,
                  colWidths=[22 * mm, 38 * mm, 55 * mm, 30 * mm, 40 * mm, 28 * mm, 24 * mm, 22 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (5, 1), (5, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F6FA")]),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
    ]))

    story = [
        Paragraph(title, styles["Title"]),
        Paragraph(f"Generated {datetime.now():%d %b %Y, %H:%M} &nbsp;|&nbsp; {len(df)} employee(s)",
                  styles["Normal"]),
        Spacer(1, 6 * mm),
        table,
    ]
    doc.build(story)
    return buffer.getvalue()
