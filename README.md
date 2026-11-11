# 👥 Employee Management System (Streamlit + SQLite)

A lightweight HR app: manage employees, see analytics, import/export data.

## Features
- **CRUD** – add, view, search/filter, edit, delete employees
- **Dashboard** – headcount, status split, salary stats, hiring trend (Plotly)
- **Bulk import** – CSV / Excel with per-row validation and error report
- **Export** – styled Excel (.xlsx) and PDF reports
- **Validation** – email, phone, salary, dates, unique code/email

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python setup_db.py --seed        # optional: create DB + demo data
streamlit run main.py
```
The SQLite file is created at `data/employees.db` (path set in `core/config.py`).

## Project structure
| Path | Purpose |
|---|---|
| `core/config.py` | DB path, departments, statuses, column definitions |
| `core/database.py` | SQLite connection context manager + schema |
| `core/crud.py` | Add / list / search / update / delete / bulk add |
| `core/analytics.py` | Aggregate queries for the dashboard |
| `core/validators.py` | Normalisation + validation rules |
| `exporters/` | Excel (openpyxl) and PDF (ReportLab) exporters |
| `gui/` | Streamlit pages: dashboard, employees, import |
| `main.py` | App entry point and sidebar navigation |
| `setup_db.py` | One-time DB creation and optional seeding |

## Import format
Columns: `emp_code, first_name, last_name, email, phone, department, designation, salary, hire_date, status`
(`phone` and `status` optional; dates as `YYYY-MM-DD`). Download the template from the Import page.

## Deploying
- **Streamlit Community Cloud**: push to GitHub, select `main.py`. Note that its filesystem is
  ephemeral, so the SQLite data resets on redeploy/restart – use it for demos, or host on a VM/Docker
  volume (e.g. `streamlit run main.py --server.port 8501`) for persistent data.
- Customise departments/statuses/currency in `core/config.py`.
