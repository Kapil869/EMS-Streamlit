"""Employee CRUD screen: view/search/export, add, edit, delete."""
from datetime import date, datetime

import streamlit as st

from core import crud
from core.config import COLUMN_LABELS, DEPARTMENTS, STATUSES
from exporters.excel_exporter import export_to_excel
from exporters.pdf_exporter import export_to_pdf


def _employee_form(prefix: str, defaults: dict | None = None, submit_label: str = "Save"):
    """Render the shared add/edit form. Returns (submitted, data)."""
    d = defaults or {}
    hire = d.get("hire_date")
    hire = datetime.strptime(hire, "%Y-%m-%d").date() if hire else date.today()
    dept = d.get("department", DEPARTMENTS[0])
    status = d.get("status", STATUSES[0])

    with st.form(f"{prefix}_form", clear_on_submit=(prefix == "add")):
        c1, c2 = st.columns(2)
        emp_code = c1.text_input("Employee Code *", d.get("emp_code", ""))
        email = c2.text_input("Email *", d.get("email", ""))
        first = c1.text_input("First Name *", d.get("first_name", ""))
        last = c2.text_input("Last Name *", d.get("last_name", ""))
        phone = c1.text_input("Phone", d.get("phone") or "")
        designation = c2.text_input("Designation *", d.get("designation", ""))
        department = c1.selectbox("Department *", DEPARTMENTS,
                                  index=DEPARTMENTS.index(dept) if dept in DEPARTMENTS else 0)
        status_sel = c2.selectbox("Status", STATUSES,
                                  index=STATUSES.index(status) if status in STATUSES else 0)
        salary = c1.number_input("Salary *", min_value=0.0, step=1000.0,
                                 value=float(d.get("salary", 0.0)))
        hire_date = c2.date_input("Hire Date *", hire, max_value=date.today())
        submitted = st.form_submit_button(submit_label, type="primary")

    data = {"emp_code": emp_code, "first_name": first, "last_name": last, "email": email,
            "phone": phone, "department": department, "designation": designation,
            "salary": salary, "hire_date": hire_date, "status": status_sel}
    return submitted, data


def _view_tab() -> None:
    f1, f2, f3 = st.columns([3, 2, 2])
    search = f1.text_input("🔍 Search", placeholder="Name, code, email or designation")
    dept = f2.selectbox("Department", ["All"] + DEPARTMENTS)
    status = f3.selectbox("Status", ["All"] + STATUSES)

    df = crud.list_employees(search, dept, status)
    st.caption(f"{len(df)} employee(s) found")
    st.dataframe(df.drop(columns=["id"]).rename(columns=COLUMN_LABELS),
                 use_container_width=True, hide_index=True)

    if not df.empty:
        e1, e2, _ = st.columns([1, 1, 4])
        e1.download_button("⬇️ Excel", export_to_excel(df), "employees.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        e2.download_button("⬇️ PDF", export_to_pdf(df), "employees.pdf", "application/pdf")


def _add_tab() -> None:
    submitted, data = _employee_form("add", submit_label="➕ Add Employee")
    if submitted:
        ok, msg = crud.add_employee(data)
        (st.success if ok else st.error)(msg)


def _edit_tab() -> None:
    df = crud.list_employees()
    if df.empty:
        st.info("No employees to edit.")
        return
    options = {int(r.id): f"{r.emp_code} — {r.first_name} {r.last_name}" for r in df.itertuples()}
    emp_id = st.selectbox("Select employee", list(options), format_func=options.get)
    emp = crud.get_employee(emp_id)

    submitted, data = _employee_form(f"edit_{emp_id}", emp, "💾 Update Employee")
    if submitted:
        ok, msg = crud.update_employee(emp_id, data)
        (st.success if ok else st.error)(msg)
        if ok:
            st.rerun()

    with st.expander("🗑️ Danger zone — delete this employee"):
        confirm = st.checkbox(f"Yes, permanently delete {emp['first_name']} {emp['last_name']}",
                              key=f"confirm_del_{emp_id}")
        if st.button("Delete", type="secondary", disabled=not confirm):
            ok, msg = crud.delete_employee(emp_id)
            (st.success if ok else st.error)(msg)
            if ok:
                st.rerun()


def render() -> None:
    st.header("👥 Employees")
    tab_view, tab_add, tab_edit = st.tabs(["View / Search", "Add", "Edit / Delete"])
    with tab_view:
        _view_tab()
    with tab_add:
        _add_tab()
    with tab_edit:
        _edit_tab()
