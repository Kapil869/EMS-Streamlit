"""Application-wide configuration and constants."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "data"
DB_PATH = DB_DIR / "employees.db"          # SQLite file (no credentials needed)

APP_TITLE = "Employee Management System"
APP_ICON = "👥"
CURRENCY = "₹"

DEPARTMENTS = [
    "Engineering", "Human Resources", "Finance", "Marketing",
    "Sales", "Operations", "Support", "Legal", "IT",
]
STATUSES = ["Active", "On Leave", "Resigned", "Terminated"]

# Column order used everywhere (tables, exports, import template)
EMPLOYEE_COLUMNS = [
    "emp_code", "first_name", "last_name", "email", "phone",
    "department", "designation", "salary", "hire_date", "status",
]
REQUIRED_COLUMNS = [
    "emp_code", "first_name", "last_name", "email",
    "department", "designation", "salary", "hire_date",
]
COLUMN_LABELS = {
    "id": "ID", "emp_code": "Emp Code", "first_name": "First Name",
    "last_name": "Last Name", "email": "Email", "phone": "Phone",
    "department": "Department", "designation": "Designation",
    "salary": "Salary", "hire_date": "Hire Date", "status": "Status",
}
