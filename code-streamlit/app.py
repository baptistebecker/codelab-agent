import sqlite3
from pathlib import Path

import streamlit as st

RACINE = Path(__file__).parent.parent
BASE = RACINE / "data.db"


def connexion():
    """Ouvre la base. Au premier lancement, elle est créée depuis base.sql."""
    neuve = not BASE.exists()
    conn = sqlite3.connect(BASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    if neuve:
        conn.executescript((RACINE / "base.sql").read_text(encoding="utf-8"))
    return conn


st.title("Réservation de salles")

with connexion() as conn:
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    lignes = conn.execute("SELECT nom FROM salles").fetchall()

st.header("Tables de la base")
st.table([dict(table) for table in tables])
st.header("Salles")
st.table([dict(ligne) for ligne in lignes])

# Ajoutez la suite de votre application ici.
