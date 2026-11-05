import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template_string, request

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


PAGE = """
<h1>Réservation de salles</h1>
<h2>Tables de la base</h2>
<ul>
  {% for table in tables %}<li>{{ table["name"] }}</li>{% endfor %}
</ul>
<h2>Salles</h2>
<ul>
  {% for ligne in lignes %}<li>{{ ligne["nom"] }}</li>{% endfor %}
</ul>
<form method="post" action="/salles">
  <input name="nom" placeholder="Nom" required>
  <input name="capacite" type="number" min="1" placeholder="Capacité" required>
  <button>Ajouter</button>
</form>
"""

app = Flask(__name__)


@app.get("/")
def accueil():
    with ouvrir_base() as conn:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
        lignes = conn.execute("SELECT nom FROM salles").fetchall()
    return render_template_string(PAGE, tables=tables, lignes=lignes)


# Exemple : reçoit le formulaire de PAGE et ajoute une salle.
@app.post("/salles")
def ajouter_salle():
    nom = request.form["nom"]
    capacite = int(request.form["capacite"])
    with ouvrir_base() as conn:
        conn.execute("INSERT INTO salles (nom, capacite) VALUES (?, ?)", (nom, capacite))
    return redirect("/")


# Ajoutez vos fonctions ici. Le HTML va dans PAGE.


if __name__ == "__main__":
    app.run(debug=True)
