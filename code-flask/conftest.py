import pytest

import base
from app import app
from base import ouvrir_base


@pytest.fixture
def connexion(tmp_path, monkeypatch):
    monkeypatch.setattr(base, "BASE", tmp_path / "data.db")
    connection = ouvrir_base()
    try:
        yield connection
    finally:
        connection.close()


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(base, "BASE", tmp_path / "data.db")
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client
