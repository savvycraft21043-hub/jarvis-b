from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "jarvis.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def db_session():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _run_migrations(conn: sqlite3.Connection) -> None:
    cols = {row["name"] for row in conn.execute("PRAGMA table_info(raw_signals)").fetchall()}
    if cols and "content_hash" not in cols:
        conn.execute("ALTER TABLE raw_signals ADD COLUMN content_hash TEXT")
        conn.execute("UPDATE raw_signals SET content_hash = CAST(id AS TEXT) WHERE content_hash IS NULL")
        conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_raw_signals_content_hash ON raw_signals(content_hash)")


def init_db() -> None:
    schema = SCHEMA_PATH.read_text()
    with db_session() as conn:
        conn.executescript(schema)
        _run_migrations(conn)
