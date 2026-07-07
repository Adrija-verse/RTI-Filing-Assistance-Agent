"""
rti_tools/database.py — SQLite-backed storage for RTI applications.
Schema: applications table.
"""

from __future__ import annotations

import sqlite3
import os
from datetime import date, datetime
from typing import List, Optional, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "instance", "rti_sahayak.db")


def _connect() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they do not exist."""
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                subject     TEXT    NOT NULL,
                department  TEXT    NOT NULL,
                pio_address TEXT    NOT NULL DEFAULT '',
                date_filed  DATE    NOT NULL,
                deadline    DATE    NOT NULL,
                life_liberty INTEGER NOT NULL DEFAULT 0,
                applicant_name    TEXT DEFAULT '',
                applicant_address TEXT DEFAULT '',
                applicant_contact TEXT DEFAULT '',
                draft_text  TEXT    DEFAULT '',
                ref_number  TEXT    DEFAULT '',
                notes       TEXT    DEFAULT '',
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def save_application(data: Dict[str, Any]) -> int:
    """Insert a new application record. Returns the new row id."""
    init_db()
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO applications
              (subject, department, pio_address, date_filed, deadline,
               life_liberty, applicant_name, applicant_address,
               applicant_contact, draft_text, ref_number, notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                data.get("subject", ""),
                data.get("department", ""),
                data.get("pio_address", ""),
                data.get("date_filed", date.today().isoformat()),
                data.get("deadline", ""),
                1 if data.get("life_liberty") else 0,
                data.get("applicant_name", ""),
                data.get("applicant_address", ""),
                data.get("applicant_contact", ""),
                data.get("draft_text", ""),
                data.get("ref_number", ""),
                data.get("notes", ""),
            ),
        )
        conn.commit()
        return cur.lastrowid


def get_all_applications() -> List[Dict[str, Any]]:
    """Return all applications as a list of dicts with computed status."""
    init_db()
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM applications ORDER BY date_filed DESC"
        ).fetchall()

    results = []
    today = date.today()
    for row in rows:
        d = dict(row)
        dl = d["deadline"]
        deadline_date = dl if isinstance(dl, date) else datetime.strptime(str(dl), "%Y-%m-%d").date()
        remaining = (deadline_date - today).days
        if remaining < 0:
            d["status"] = "overdue"
        elif remaining <= 5:
            d["status"] = "due_soon"
        else:
            d["status"] = "on_track"
        d["days_remaining"] = remaining
        # Normalise to string for JSON / Jinja rendering
        d["deadline"] = deadline_date.isoformat()
        df = d["date_filed"]
        d["date_filed"] = df.isoformat() if isinstance(df, date) else str(df)
        results.append(d)
    return results


def get_application(app_id: int) -> Optional[Dict[str, Any]]:
    """Return a single application by id, or None if not found."""
    init_db()
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM applications WHERE id = ?", (app_id,)
        ).fetchone()
    if row is None:
        return None
    d = dict(row)
    today = date.today()
    dl = d["deadline"]
    deadline_date = dl if isinstance(dl, date) else datetime.strptime(str(dl), "%Y-%m-%d").date()
    remaining = (deadline_date - today).days
    d["status"] = "overdue" if remaining < 0 else ("due_soon" if remaining <= 5 else "on_track")
    d["days_remaining"] = remaining
    d["deadline"] = deadline_date.isoformat()
    df = d["date_filed"]
    d["date_filed"] = df.isoformat() if isinstance(df, date) else str(df)
    return d


def delete_application(app_id: int) -> bool:
    """Delete an application. Returns True if a row was deleted."""
    init_db()
    with _connect() as conn:
        cur = conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))
        conn.commit()
        return cur.rowcount > 0
