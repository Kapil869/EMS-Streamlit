"""Entry point:  streamlit run main.py"""
import streamlit as st

from core.config import APP_ICON, APP_TITLE
from core.database import init_db
from gui import dashboard_page, employees_page, import_page

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
init_db()  # ensures the schema exists even if setup_db.py was never run

PAGES = {
    "📊 Dashboard": dashboard_page.render,
    "👥 Employees": employees_page.render,
    "📥 Bulk Import": import_page.render,
}

st.sidebar.title(f"{APP_ICON} {APP_TITLE}")
choice = st.sidebar.radio("Navigate", list(PAGES), label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.caption("Built with Streamlit + SQLite")

PAGES[choice]()
