"""Input validation and normalisation for employee records."""
import re
from datetime import date, datetime

import pandas as pd

from core.config import DEPARTMENTS, REQUIRED_COLUMNS, STATUSES

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
PHONE_RE = re.compile(r"^\+?[\d\s\-()]{7,20}$")


def _blank(value) -> bool:
    return value is None or (isinstance(value, float) and pd.isna(value)) or str(value).strip() == ""


def normalize_employee(data: dict) -> dict:
    """Trim strings and coerce salary / hire_date into storage formats."""
    out = {}
    for key, val in data.items():
        out[key] = None if _blank(val) else (val.strip() if isinstance(val, str) else val)

    if out.get("salary") is not None:
        try:
            out["salary"] = round(float(str(out["salary"]).replace(",", "")), 2)
        except ValueError:
            pass  # reported by validate_employee

    hd = out.get("hire_date")
    if hd is not None:
        if isinstance(hd, (datetime, pd.Timestamp)):
            out["hire_date"] = hd.date().isoformat()
        elif isinstance(hd, date):
            out["hire_date"] = hd.isoformat()
        else:
            parsed = pd.to_datetime(str(hd), errors="coerce", dayfirst=False)
            out["hire_date"] = parsed.date().isoformat() if not pd.isna(parsed) else hd

    if out.get("phone") is not None:
        out["phone"] = str(out["phone"])
    if out.get("email"):
        out["email"] = out["email"].lower()
    if _blank(out.get("status")):
        out["status"] = "Active"
    return out


def validate_employee(data: dict) -> list[str]:
    """Return a list of human-readable errors (empty list == valid)."""
    errors = []
    for col in REQUIRED_COLUMNS:
        if _blank(data.get(col)):
            errors.append(f"'{col}' is required")
    if errors:
        return errors

    if not EMAIL_RE.match(data["email"]):
        errors.append("Invalid email address")
    if data.get("phone") and not PHONE_RE.match(str(data["phone"])):
        errors.append("Invalid phone number")
    if not isinstance(data["salary"], (int, float)) or data["salary"] < 0:
        errors.append("Salary must be a non-negative number")
    try:
        hired = datetime.strptime(str(data["hire_date"]), "%Y-%m-%d").date()
        if hired > date.today():
            errors.append("Hire date cannot be in the future")
    except ValueError:
        errors.append("Hire date must be a valid date (YYYY-MM-DD)")
    if data["department"] not in DEPARTMENTS:
        errors.append(f"Unknown department '{data['department']}'")
    if data.get("status") not in STATUSES:
        errors.append(f"Status must be one of {', '.join(STATUSES)}")
    return errors
