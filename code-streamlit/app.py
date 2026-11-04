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
st.header("Salles")

with connexion() as conn:
    lignes = conn.execute("SELECT nom FROM salles").fetchall()
st.table([dict(ligne) for ligne in lignes])
