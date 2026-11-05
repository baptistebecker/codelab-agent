import sqlite3
from pathlib import Path

from flask import Flask, render_template_string

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
"""

app = Flask(__name__)


@app.get("/")
def accueil():
    with connexion() as conn:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
        lignes = conn.execute("SELECT nom FROM salles").fetchall()
    return render_template_string(PAGE, tables=tables, lignes=lignes)


# Ajoutez vos pages ici : une fonction par page.


if __name__ == "__main__":
    app.run(debug=True)
