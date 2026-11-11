"""SQLite connection handling and schema creation."""
import sqlite3
from contextlib import contextmanager

from core.config import DB_DIR, DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS employees (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_code     TEXT NOT NULL UNIQUE,
    first_name   TEXT NOT NULL,
    last_name    TEXT NOT NULL,
    email        TEXT NOT NULL UNIQUE,
    phone        TEXT,
    department   TEXT NOT NULL,
    designation  TEXT NOT NULL,
    salary       REAL NOT NULL CHECK (salary >= 0),
    hire_date    TEXT NOT NULL,                -- ISO format YYYY-MM-DD
    status       TEXT NOT NULL DEFAULT 'Active',
    created_at   TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at   TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_emp_department ON employees(department);
CREATE INDEX IF NOT EXISTS idx_emp_status     ON employees(status);
"""


@contextmanager
def get_connection():
    """Yield a SQLite connection that commits on success and rolls back on error."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Create tables/indexes if they do not exist (safe to call repeatedly)."""
    with get_connection() as conn:
        conn.executescript(SCHEMA)
