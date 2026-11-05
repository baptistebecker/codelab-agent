from datetime import date

import pytest

import metier

LUNDI = date(2026, 11, 9)


def test_lundi_de_retombe_sur_le_lundi(connexion):
    assert metier.lundi_de(date(2026, 11, 12)) == LUNDI


def test_semaine_demandee_normalise_et_ignore_une_valeur_invalide(connexion):
    assert metier.semaine_demandee("2026-11-11") == LUNDI
    assert metier.semaine_demandee("invalide", aujourdhui=date(2026, 11, 5)) == date(
        2026, 11, 2
    )


def test_cree_une_reservation_valide(connexion):
    identifiant = metier.creer_reservation(
        connexion, 1, "Bob", "2026-11-09", "12:00", "13:00", 10
    )
    reservation = connexion.execute(
        "SELECT * FROM reservations WHERE id = ?", (identifiant,)
    ).fetchone()
    assert reservation["personne"] == "Bob"
    assert reservation["debut"] == "12:00"
    assert reservation["fin"] == "13:00"


def test_refuse_un_chevauchement(connexion):
    with pytest.raises(metier.ErreurMetier, match="indisponible"):
        metier.creer_reservation(
            connexion, 1, "Bob", "2026-11-09", "11:00", "13:00", 10
        )


def test_accepte_deux_creneaux_adjacents(connexion):
    metier.creer_reservation(connexion, 1, "Bob", "2026-11-09", "09:00", "10:00", 10)
    metier.creer_reservation(connexion, 1, "Chloé", "2026-11-09", "12:00", "13:00", 10)
    assert connexion.execute("SELECT COUNT(*) FROM reservations").fetchone()[0] == 3


def test_refuse_une_capacite_depassee(connexion):
    with pytest.raises(metier.ErreurMetier, match="maximum 20"):
        metier.creer_reservation(
            connexion, 1, "Bob", "2026-11-09", "14:00", "15:00", 25
        )


def test_refuse_une_reservation_avant_8h(connexion):
    with pytest.raises(metier.ErreurMetier, match="8 h"):
        metier.creer_reservation(
            connexion, 1, "Bob", "2026-11-09", "07:30", "09:00", 10
        )


def test_refuse_une_reservation_apres_20h(connexion):
    with pytest.raises(metier.ErreurMetier, match="20 h"):
        metier.creer_reservation(
            connexion, 1, "Bob", "2026-11-10", "19:00", "20:30", 10
        )


def test_refuse_une_duree_inferieure_a_30_minutes(connexion):
    with pytest.raises(metier.ErreurMetier, match="30 minutes"):
        metier.creer_reservation(
            connexion, 1, "Bob", "2026-11-10", "14:00", "14:20", 10
        )


def test_refuse_une_duree_superieure_a_4_heures(connexion):
    with pytest.raises(metier.ErreurMetier, match="4 heures"):
        metier.creer_reservation(
            connexion, 1, "Bob", "2026-11-10", "08:00", "13:00", 10
        )


def test_accepte_une_duree_de_4_heures(connexion):
    metier.creer_reservation(connexion, 2, "Bob", "2026-11-10", "08:00", "12:00", 5)


def test_refuse_une_heure_de_fin_avant_le_debut(connexion):
    with pytest.raises(metier.ErreurMetier, match="après"):
        metier.creer_reservation(
            connexion, 2, "Bob", "2026-11-10", "14:00", "13:00", 5
        )


def test_refuse_une_personne_vide(connexion):
    with pytest.raises(metier.ErreurMetier, match="personne"):
        metier.creer_reservation(
            connexion, 2, "   ", "2026-11-10", "14:00", "15:00", 5
        )


def test_autorise_le_meme_creneau_dans_deux_salles(connexion):
    metier.creer_reservation(connexion, 1, "Bob", "2026-11-09", "14:00", "15:00", 5)
    metier.creer_reservation(connexion, 2, "Alice", "2026-11-09", "14:00", "15:00", 5)


def test_liste_les_reservations_de_la_semaine(connexion):
    metier.creer_reservation(
        connexion, 1, "Bob", "2026-11-16", "10:00", "11:00", 5
    )
    reservations = metier.lister_reservations_semaine(connexion, 1, LUNDI)
    assert [reservation["personne"] for reservation in reservations] == ["Alice"]


def test_statistiques_de_la_semaine(connexion):
    statistiques = metier.statistiques_semaine(connexion, LUNDI)
    assert statistiques[1] == {"nombre": 1, "minutes": 120}


def test_cree_et_modifie_une_salle(connexion):
    salle_id = metier.creer_salle(connexion, "Amphi", 60, True)
    salle = metier.trouver_salle(connexion, salle_id)
    assert (salle["nom"], salle["capacite"], salle["projecteur"]) == ("Amphi", 60, 1)

    metier.modifier_salle(connexion, salle_id, "Amphi B", 45, False)
    salle = metier.trouver_salle(connexion, salle_id)
    assert (salle["nom"], salle["capacite"], salle["projecteur"]) == ("Amphi B", 45, 0)


@pytest.mark.parametrize("capacite", [0, -3, "abc", None])
def test_refuse_une_capacite_de_salle_invalide(connexion, capacite):
    with pytest.raises(metier.ErreurMetier):
        metier.creer_salle(connexion, "Salle", capacite)


def test_refuse_un_nom_de_salle_vide(connexion):
    with pytest.raises(metier.ErreurMetier, match="nom"):
        metier.creer_salle(connexion, "  ", 10)


def test_supprimer_une_salle_supprime_ses_reservations(connexion):
    metier.supprimer_salle(connexion, 1)
    reste = connexion.execute(
        "SELECT COUNT(*) FROM reservations WHERE salle_id = 1"
    ).fetchone()[0]
    assert reste == 0


def test_supprime_une_reservation(connexion):
    metier.supprimer_reservation(connexion, 1)
    assert connexion.execute("SELECT COUNT(*) FROM reservations").fetchone()[0] == 0


def test_supprimer_une_reservation_inconnue_echoue(connexion):
    with pytest.raises(metier.Introuvable):
        metier.supprimer_reservation(connexion, 999)


def test_refuse_un_identifiant_de_salle_invalide(connexion):
    with pytest.raises(metier.Introuvable):
        metier.trouver_salle(connexion, "abc")
