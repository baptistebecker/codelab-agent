import sqlite3
from pathlib import Path

import streamlit as st

RACINE = Path(__file__).parent.parent
BASE = RACINE / "data.db"


def ouvrir_base():
    """Ouvre la base et la crée au premier lancement. Inutile de modifier cette fonction."""
    neuve = not BASE.exists()
    conn = sqlite3.connect(BASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    if neuve:
        conn.executescript((RACINE / "base.sql").read_text(encoding="utf-8"))
    return conn


st.title("Réservation de salles")

with ouvrir_base() as conn:
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    salles = conn.execute("SELECT nom FROM salles").fetchall()

st.header("Tables de la base")
st.table([dict(table) for table in tables])
st.header("Salles")
st.table([dict(salle) for salle in salles])

# Exemple : un formulaire qui ajoute une salle.
with st.form("ajouter_salle", clear_on_submit=True):
    nom = st.text_input("Nom")
    capacite = st.number_input("Capacité", min_value=1, value=10)
    envoye = st.form_submit_button("Ajouter")

if envoye and nom:
    with ouvrir_base() as conn:
        conn.execute("INSERT INTO salles (nom, capacite) VALUES (?, ?)", (nom, capacite))
    st.rerun()

# Ajoutez la suite de votre application ici.
