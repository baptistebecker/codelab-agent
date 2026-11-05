def test_accueil_affiche_le_planning(client):
    reponse = client.get("/?semaine=2026-11-09")
    page = reponse.get_data(as_text=True)
    assert reponse.status_code == 200
    assert "Planning hebdomadaire" in page
    assert "S1" in page
    assert "Alice" in page


def test_la_semaine_est_normalisee_au_lundi(client):
    page = client.get("/?semaine=2026-11-11").get_data(as_text=True)
    assert "9 – 15 novembre 2026" in page


def test_une_salle_inconnue_redirige_vers_la_premiere(client):
    reponse = client.get("/?salle=999")
    assert reponse.status_code == 302
    assert "salle=1" in reponse.headers["Location"]


def test_ajoute_une_salle(client):
    reponse = client.post(
        "/api/salles",
        json={"nom": "S3", "capacite": 30, "projecteur": True, "semaine": "2026-11-09"},
    )
    assert reponse.status_code == 200
    donnees = reponse.get_json()
    assert donnees["ok"] is True

    page = client.get(donnees["redirect"]).get_data(as_text=True)
    assert "S3" in page
    assert "30 places" in page


def test_modifie_une_salle(client):
    reponse = client.put(
        "/api/salles/2",
        json={
            "nom": "S2 rénovée",
            "capacite": 16,
            "projecteur": True,
            "semaine": "2026-11-09",
        },
    )
    assert reponse.status_code == 200
    page = client.get(reponse.get_json()["redirect"]).get_data(as_text=True)
    assert "S2 rénovée" in page
    assert "16 places" in page


def test_supprime_une_salle_et_ses_reservations(client):
    reponse = client.delete("/api/salles/1?semaine=2026-11-09")
    assert reponse.status_code == 200
    page = client.get("/?semaine=2026-11-09").get_data(as_text=True)
    assert "Alice" not in page


def test_supprimer_une_salle_garde_la_salle_courante(client):
    reponse = client.delete("/api/salles/2?semaine=2026-11-09&salle=1")
    assert reponse.status_code == 200
    assert "salle=1" in reponse.get_json()["redirect"]


def test_supprimer_la_salle_courante_choisit_une_autre_salle(client):
    reponse = client.delete("/api/salles/1?semaine=2026-11-09&salle=1")
    assert reponse.status_code == 200
    assert "salle=2" in reponse.get_json()["redirect"]


def test_refuse_une_salle_invalide(client):
    reponse = client.post("/api/salles", json={"nom": "", "capacite": 10})
    assert reponse.status_code == 400
    assert "nom" in reponse.get_json()["erreur"].lower()


def test_cree_et_annule_une_reservation(client):
    reponse = client.post(
        "/api/reservations",
        json={
            "salle_id": 1,
            "personne": "Bob",
            "date": "2026-11-09",
            "debut": "12:00",
            "fin": "13:00",
            "participants": 10,
        },
    )
    assert reponse.status_code == 200
    donnees = reponse.get_json()
    assert "salle=1" in donnees["redirect"]
    assert "semaine=2026-11-09" in donnees["redirect"]

    page = client.get(donnees["redirect"]).get_data(as_text=True)
    assert "Bob" in page

    suppression = client.delete(f"/api/reservations/{donnees['id']}")
    assert suppression.status_code == 200
    page = client.get(donnees["redirect"]).get_data(as_text=True)
    assert "Bob" not in page


def test_refuse_une_reservation_en_chevauchement(client):
    reponse = client.post(
        "/api/reservations",
        json={
            "salle_id": 1,
            "personne": "Bob",
            "date": "2026-11-09",
            "debut": "11:00",
            "fin": "13:00",
            "participants": 10,
        },
    )
    assert reponse.status_code == 400
    assert "indisponible" in reponse.get_json()["erreur"]


def test_refuse_une_reservation_au_dela_de_la_capacite(client):
    reponse = client.post(
        "/api/reservations",
        json={
            "salle_id": 1,
            "personne": "Bob",
            "date": "2026-11-09",
            "debut": "14:00",
            "fin": "15:00",
            "participants": 25,
        },
    )
    assert reponse.status_code == 400
    assert "maximum 20" in reponse.get_json()["erreur"]


def test_supprimer_une_reservation_inconnue_renvoie_404(client):
    assert client.delete("/api/reservations/999").status_code == 404


def test_accueil_sans_salle(client):
    client.delete("/api/salles/1")
    client.delete("/api/salles/2")
    page = client.get("/").get_data(as_text=True)
    assert "Aucune salle" in page
