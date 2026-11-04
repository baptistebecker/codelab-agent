"""Vérifie que le code de démarrage fonctionne. Ajoutez vos propres tests ici."""
from app import create_app


def test_page_accueil(tmp_path):
    app = create_app(tmp_path / "test.db")
    reponse = app.test_client().get("/")
    assert reponse.status_code == 200
    assert "SQLite" in reponse.get_data(as_text=True)
