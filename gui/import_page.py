"""Bulk CSV / Excel import."""
import pandas as pd
import streamlit as st

from core import crud
from core.config import EMPLOYEE_COLUMNS, REQUIRED_COLUMNS
from exporters.excel_exporter import import_template_excel


def _read(uploaded) -> pd.DataFrame:
    if uploaded.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded, dtype=str)
    else:
        df = pd.read_excel(uploaded, dtype=str)
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    return df


def render() -> None:
    st.header("📥 Bulk Import")
    st.write("Upload a **CSV** or **Excel** file. Required columns: "
             + ", ".join(f"`{c}`" for c in REQUIRED_COLUMNS) + ". Optional: `phone`, `status`.")
    st.download_button("⬇️ Download template (.xlsx)", import_template_excel(),
                       "employee_import_template.xlsx",
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    uploaded = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])
    if not uploaded:
        return

    try:
        df = _read(uploaded)
    except Exception as exc:  # noqa: BLE001 - show any parse problem to the user
        st.error(f"Could not read file: {exc}")
        return

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        st.error("Missing required column(s): " + ", ".join(missing))
        return

    df = df[[c for c in EMPLOYEE_COLUMNS if c in df.columns]]
    st.subheader(f"Preview ({len(df)} rows)")
    st.dataframe(df.head(50), use_container_width=True, hide_index=True)

    if st.button("🚀 Import employees", type="primary"):
        with st.spinner("Importing…"):
            inserted, failures = crud.bulk_add_employees(df)
        if inserted:
            st.success(f"Imported {inserted} employee(s).")
        if failures:
            st.warning(f"{len(failures)} row(s) were skipped:")
            st.dataframe(pd.DataFrame(failures), use_container_width=True, hide_index=True)
