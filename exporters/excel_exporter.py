"""Export employee data to an in-memory .xlsx file."""
from io import BytesIO

import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill

from core.config import COLUMN_LABELS, EMPLOYEE_COLUMNS


def export_to_excel(df: pd.DataFrame, sheet_name: str = "Employees") -> bytes:
    out = df.drop(columns=["id"], errors="ignore").rename(columns=COLUMN_LABELS)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        out.to_excel(writer, index=False, sheet_name=sheet_name)
        ws = writer.sheets[sheet_name]
        header_fill = PatternFill("solid", fgColor="1F4E78")
        for cell in ws[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center")
        for col_cells in ws.columns:
            width = max(len(str(c.value)) if c.value is not None else 0 for c in col_cells)
            ws.column_dimensions[col_cells[0].column_letter].width = min(width + 3, 40)
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
    return buffer.getvalue()


def import_template_excel() -> bytes:
    """Sample file with the columns expected by the import page."""
    sample = pd.DataFrame([{
        "emp_code": "EMP001", "first_name": "Asha", "last_name": "Verma",
        "email": "asha.verma@example.com", "phone": "+91 9876543210",
        "department": "Engineering", "designation": "Software Engineer",
        "salary": 850000, "hire_date": "2023-04-17", "status": "Active",
    }])[EMPLOYEE_COLUMNS]
    buffer = BytesIO()
    sample.to_excel(buffer, index=False)
    return buffer.getvalue()
