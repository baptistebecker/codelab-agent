"""Accès à la base SQLite."""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DEFAULT_DB = BASE_DIR / "data.db"
SCHEMA = BASE_DIR / "schema.sql"


def get_connection(db_path=DEFAULT_DB):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path=DEFAULT_DB):
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA.read_text(encoding="utf-8"))
