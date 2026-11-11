"""Create / Read / Update / Delete / Search operations for employees."""
import sqlite3

import pandas as pd

from core.config import EMPLOYEE_COLUMNS
from core.database import get_connection
from core.validators import normalize_employee, validate_employee


def _friendly_integrity_error(exc: sqlite3.IntegrityError) -> str:
    msg = str(exc).lower()
    if "emp_code" in msg:
        return "Employee code already exists"
    if "email" in msg:
        return "Email already exists"
    return f"Database constraint failed: {exc}"


# ---------------------------------------------------------------- CREATE
def add_employee(data: dict) -> tuple[bool, str]:
    """Insert one employee. Returns (success, message)."""
    data = normalize_employee(data)
    errors = validate_employee(data)
    if errors:
        return False, "; ".join(errors)
    cols = ", ".join(EMPLOYEE_COLUMNS)
    marks = ", ".join("?" for _ in EMPLOYEE_COLUMNS)
    try:
        with get_connection() as conn:
            conn.execute(
                f"INSERT INTO employees ({cols}) VALUES ({marks})",
                [data.get(c) for c in EMPLOYEE_COLUMNS],
            )
        return True, "Employee added successfully"
    except sqlite3.IntegrityError as exc:
        return False, _friendly_integrity_error(exc)


def bulk_add_employees(df: pd.DataFrame) -> tuple[int, list[dict]]:
    """Insert many rows. Returns (inserted_count, [{'row': n, 'error': msg}, ...])."""
    inserted, failures = 0, []
    for idx, row in df.iterrows():
        ok, msg = add_employee(row.to_dict())
        if ok:
            inserted += 1
        else:
            failures.append({"row": int(idx) + 2, "emp_code": row.get("emp_code"), "error": msg})
    return inserted, failures


# ------------------------------------------------------------------ READ
def get_employee(emp_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM employees WHERE id = ?", (emp_id,)).fetchone()
    return dict(row) if row else None


def list_employees(search: str = "", department: str = "All", status: str = "All") -> pd.DataFrame:
    """Fetch employees, optionally filtered by free-text search, department and status."""
    query = "SELECT id, " + ", ".join(EMPLOYEE_COLUMNS) + " FROM employees WHERE 1=1"
    params: list = []
    if search:
        like = f"%{search.strip()}%"
        query += (" AND (emp_code LIKE ? OR first_name LIKE ? OR last_name LIKE ?"
                  " OR (first_name || ' ' || last_name) LIKE ? OR email LIKE ?"
                  " OR designation LIKE ?)")
        params += [like] * 6
    if department and department != "All":
        query += " AND department = ?"
        params.append(department)
    if status and status != "All":
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY id DESC"
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)


# ---------------------------------------------------------------- UPDATE
def update_employee(emp_id: int, data: dict) -> tuple[bool, str]:
    data = normalize_employee(data)
    errors = validate_employee(data)
    if errors:
        return False, "; ".join(errors)
    sets = ", ".join(f"{c} = ?" for c in EMPLOYEE_COLUMNS)
    try:
        with get_connection() as conn:
            cur = conn.execute(
                f"UPDATE employees SET {sets}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                [data.get(c) for c in EMPLOYEE_COLUMNS] + [emp_id],
            )
            if cur.rowcount == 0:
                return False, "Employee not found"
        return True, "Employee updated successfully"
    except sqlite3.IntegrityError as exc:
        return False, _friendly_integrity_error(exc)


# ---------------------------------------------------------------- DELETE
def delete_employee(emp_id: int) -> tuple[bool, str]:
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
    if cur.rowcount == 0:
        return False, "Employee not found"
    return True, "Employee deleted"
