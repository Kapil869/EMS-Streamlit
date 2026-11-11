"""Aggregate queries that power the dashboard."""
import pandas as pd

from core.database import get_connection


def _query(sql: str) -> pd.DataFrame:
    with get_connection() as conn:
        return pd.read_sql_query(sql, conn)


def summary_metrics() -> dict:
    df = _query(
        """SELECT COUNT(*) AS total,
                  SUM(status = 'Active') AS active,
                  COALESCE(AVG(salary), 0) AS avg_salary,
                  COALESCE(SUM(CASE WHEN status = 'Active' THEN salary END), 0) AS payroll,
                  COUNT(DISTINCT department) AS departments
           FROM employees"""
    )
    row = df.iloc[0].fillna(0).to_dict()
    return {k: (float(v) if k in ("avg_salary", "payroll") else int(v)) for k, v in row.items()}


def headcount_by_department() -> pd.DataFrame:
    return _query("SELECT department, COUNT(*) AS headcount FROM employees "
                  "GROUP BY department ORDER BY headcount DESC")


def salary_by_department() -> pd.DataFrame:
    return _query("SELECT department, ROUND(AVG(salary),2) AS avg_salary, "
                  "MIN(salary) AS min_salary, MAX(salary) AS max_salary, "
                  "ROUND(SUM(salary),2) AS total_salary "
                  "FROM employees GROUP BY department ORDER BY avg_salary DESC")


def status_distribution() -> pd.DataFrame:
    return _query("SELECT status, COUNT(*) AS count FROM employees GROUP BY status")


def hires_by_year() -> pd.DataFrame:
    return _query("SELECT strftime('%Y', hire_date) AS year, COUNT(*) AS hires "
                  "FROM employees GROUP BY year ORDER BY year")


def salary_values() -> pd.DataFrame:
    return _query("SELECT salary, department FROM employees")


def top_earners(limit: int = 5) -> pd.DataFrame:
    return _query(
        f"SELECT first_name || ' ' || last_name AS name, department, designation, salary "
        f"FROM employees ORDER BY salary DESC LIMIT {int(limit)}"
    )
