"""Department + salary dashboards."""
import plotly.express as px
import streamlit as st

from core import analytics
from core.config import CURRENCY


def render() -> None:
    st.header("📊 Dashboard")
    m = analytics.summary_metrics()
    if m["total"] == 0:
        st.info("No employees yet. Add some on the **Employees** page, import a file, "
                "or run `python setup_db.py --seed` for demo data.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Employees", m["total"])
    c2.metric("Active", m["active"])
    c3.metric("Avg Salary", f"{CURRENCY}{m['avg_salary']:,.0f}")
    c4.metric("Active Payroll", f"{CURRENCY}{m['payroll']:,.0f}")

    st.divider()
    left, right = st.columns(2)
    with left:
        st.subheader("Headcount by Department")
        hc = analytics.headcount_by_department()
        st.plotly_chart(px.bar(hc, x="department", y="headcount", color="department",
                               text="headcount").update_layout(showlegend=False),
                        use_container_width=True)
    with right:
        st.subheader("Employee Status")
        st.plotly_chart(px.pie(analytics.status_distribution(), names="status",
                               values="count", hole=0.45), use_container_width=True)

    st.divider()
    tab1, tab2, tab3 = st.tabs(["Salary by Department", "Salary Distribution", "Hiring Trend"])
    with tab1:
        sal = analytics.salary_by_department()
        st.plotly_chart(px.bar(sal, x="department", y="avg_salary", color="department",
                               labels={"avg_salary": f"Average Salary ({CURRENCY})"}
                               ).update_layout(showlegend=False), use_container_width=True)
        st.dataframe(sal, use_container_width=True, hide_index=True)
    with tab2:
        sv = analytics.salary_values()
        st.plotly_chart(px.histogram(sv, x="salary", nbins=20, color="department"),
                        use_container_width=True)
        st.plotly_chart(px.box(sv, x="department", y="salary", color="department"),
                        use_container_width=True)
    with tab3:
        st.plotly_chart(px.line(analytics.hires_by_year(), x="year", y="hires", markers=True),
                        use_container_width=True)

    st.subheader("🏆 Top Earners")
    st.dataframe(analytics.top_earners(5), use_container_width=True, hide_index=True)
