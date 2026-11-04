"""Point d'entrée de l'application. À faire évoluer librement."""
from flask import Flask, render_template

from db import DEFAULT_DB, get_connection, init_db


def create_app(db_path=DEFAULT_DB):
    app = Flask(__name__)
    init_db(db_path)

    @app.get("/")
    def index():
        with get_connection(db_path) as conn:
            sqlite_version = conn.execute("SELECT sqlite_version()").fetchone()[0]
        return render_template("index.html", sqlite_version=sqlite_version)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
