"""Accès à la base SQLite."""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DEFAULT_DB = BASE_DIR / "data.db"
SCHEMA = BASE_DIR / "schema.sql"
SEED = BASE_DIR / "seed.sql"


def get_connection(db_path=DEFAULT_DB):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path=DEFAULT_DB):
    """Crée les tables. La base de l'application reçoit aussi les exemples, une seule fois ; celle des tests reste vide."""
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA.read_text(encoding="utf-8"))
        if db_path == DEFAULT_DB and conn.execute("PRAGMA user_version").fetchone()[0] == 0:
            conn.executescript(SEED.read_text(encoding="utf-8"))
            conn.execute("PRAGMA user_version = 1")
