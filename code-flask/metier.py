"""Règles métier et accès aux données de la réservation de salles."""

from __future__ import annotations

from datetime import date, timedelta
import re
import sqlite3

HEURE_OUVERTURE = 8 * 60
HEURE_FERMETURE = 20 * 60
DUREE_MINIMALE = 30
DUREE_MAXIMALE = 4 * 60

_HEURE = re.compile(r"^(\d{1,2}):(\d{2})$")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class ErreurMetier(ValueError):
    """Erreur liée à une règle de gestion."""


class Introuvable(ErreurMetier):
    """Élément demandé absent de la base."""


def _entier(valeur, message):
    try:
        return int(valeur)
    except (TypeError, ValueError):
        raise ErreurMetier(message) from None


def _texte(valeur, message):
    if valeur is None:
        raise ErreurMetier(message)
    texte = str(valeur).strip()
    if not texte:
        raise ErreurMetier(message)
    return texte


def _booleen(valeur):
    if isinstance(valeur, str):
        return valeur.strip().lower() in {"1", "true", "on", "oui", "yes"}
    return bool(valeur)


def minutes_depuis_heure(valeur):
    if not isinstance(valeur, str):
        raise ErreurMetier("L'heure doit être au format HH:MM.")
    correspondance = _HEURE.fullmatch(valeur.strip())
    if not correspondance:
        raise ErreurMetier("L'heure doit être au format HH:MM.")
    heures = int(correspondance.group(1))
    minutes = int(correspondance.group(2))
    if heures > 23 or minutes > 59:
        raise ErreurMetier("Heure invalide.")
    return heures * 60 + minutes


def heure_depuis_minutes(minutes):
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def analyser_date(valeur):
    if not isinstance(valeur, str) or not _DATE.fullmatch(valeur.strip()):
        raise ErreurMetier("La date doit être au format AAAA-MM-JJ.")
    try:
        return date.fromisoformat(valeur.strip())
    except ValueError:
        raise ErreurMetier("Date invalide.") from None


def lundi_de(jour):
    return jour - timedelta(days=jour.weekday())


def semaine_demandee(valeur=None, aujourdhui=None):
    if valeur:
        try:
            return lundi_de(analyser_date(valeur))
        except ErreurMetier:
            pass
    return lundi_de(aujourdhui or date.today())


def lister_salles(conn):
    return conn.execute(
        "SELECT id, nom, capacite, projecteur FROM salles ORDER BY nom COLLATE NOCASE, id"
    ).fetchall()


def trouver_salle(conn, salle_id):
    try:
        salle_id = int(salle_id)
    except (TypeError, ValueError):
        raise Introuvable("Cette salle n'existe pas.") from None
    salle = conn.execute(
        "SELECT id, nom, capacite, projecteur FROM salles WHERE id = ?", (salle_id,)
    ).fetchone()
    if salle is None:
        raise Introuvable("Cette salle n'existe pas.")
    return salle


def _capacite(valeur):
    capacite = _entier(valeur, "La capacité doit être un nombre entier.")
    if capacite < 1:
        raise ErreurMetier("La capacité doit être supérieure à zéro.")
    return capacite


def creer_salle(conn, nom, capacite, projecteur=0):
    nom = _texte(nom, "Le nom de la salle est obligatoire.")
    capacite = _capacite(capacite)
    curseur = conn.execute(
        "INSERT INTO salles (nom, capacite, projecteur) VALUES (?, ?, ?)",
        (nom, capacite, 1 if _booleen(projecteur) else 0),
    )
    conn.commit()
    return int(curseur.lastrowid)


def modifier_salle(conn, salle_id, nom, capacite, projecteur=0):
    trouver_salle(conn, salle_id)
    nom = _texte(nom, "Le nom de la salle est obligatoire.")
    capacite = _capacite(capacite)
    conn.execute(
        "UPDATE salles SET nom = ?, capacite = ?, projecteur = ? WHERE id = ?",
        (nom, capacite, 1 if _booleen(projecteur) else 0, salle_id),
    )
    conn.commit()


def supprimer_salle(conn, salle_id):
    trouver_salle(conn, salle_id)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("DELETE FROM salles WHERE id = ?", (salle_id,))
    conn.commit()


def lister_reservations_semaine(conn, salle_id, lundi):
    trouver_salle(conn, salle_id)
    dimanche = lundi + timedelta(days=6)
    return conn.execute(
        """
        SELECT id, salle_id, personne, date, debut, fin, participants
        FROM reservations
        WHERE salle_id = ? AND date BETWEEN ? AND ?
        ORDER BY date, debut, id
        """,
        (salle_id, lundi.isoformat(), dimanche.isoformat()),
    ).fetchall()


def statistiques_semaine(conn, lundi):
    dimanche = lundi + timedelta(days=6)
    statistiques = {}
    for reservation in conn.execute(
        "SELECT salle_id, debut, fin FROM reservations WHERE date BETWEEN ? AND ?",
        (lundi.isoformat(), dimanche.isoformat()),
    ):
        salle = statistiques.setdefault(reservation["salle_id"], {"nombre": 0, "minutes": 0})
        salle["nombre"] += 1
        salle["minutes"] += minutes_depuis_heure(reservation["fin"]) - minutes_depuis_heure(
            reservation["debut"]
        )
    return statistiques


def creer_reservation(conn, salle_id, personne, jour, debut, fin, participants):
    salle = trouver_salle(conn, salle_id)
    personne = _texte(personne, "Le nom de la personne est obligatoire.")
    jour = analyser_date(jour)
    debut_minutes = minutes_depuis_heure(debut)
    fin_minutes = minutes_depuis_heure(fin)
    participants = _entier(participants, "Le nombre de participants doit être un entier.")

    if debut_minutes < HEURE_OUVERTURE:
        raise ErreurMetier("Une réservation doit commencer à 8 h ou après.")
    if fin_minutes > HEURE_FERMETURE:
        raise ErreurMetier("Une réservation doit se terminer à 20 h au plus tard.")
    if fin_minutes <= debut_minutes:
        raise ErreurMetier("L'heure de fin doit être après l'heure de début.")

    duree = fin_minutes - debut_minutes
    if duree < DUREE_MINIMALE:
        raise ErreurMetier("Une réservation doit durer au moins 30 minutes.")
    if duree > DUREE_MAXIMALE:
        raise ErreurMetier("Une réservation ne peut pas dépasser 4 heures.")
    if participants < 1:
        raise ErreurMetier("Le nombre de participants doit être au moins 1.")
    if participants > salle["capacite"]:
        raise ErreurMetier(
            f"La salle {salle['nom']} accueille au maximum {salle['capacite']} personnes."
        )

    debut_normalise = heure_depuis_minutes(debut_minutes)
    fin_normalisee = heure_depuis_minutes(fin_minutes)
    conflit = conn.execute(
        """
        SELECT personne, debut, fin
        FROM reservations
        WHERE salle_id = ? AND date = ? AND debut < ? AND fin > ?
        ORDER BY debut
        LIMIT 1
        """,
        (salle["id"], jour.isoformat(), fin_normalisee, debut_normalise),
    ).fetchone()
    if conflit is not None:
        raise ErreurMetier(
            f"Créneau indisponible : {conflit['personne']} occupe déjà la salle "
            f"de {conflit['debut']} à {conflit['fin']}."
        )

    curseur = conn.execute(
        """
        INSERT INTO reservations (salle_id, personne, date, debut, fin, participants)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (salle["id"], personne, jour.isoformat(), debut_normalise, fin_normalisee, participants),
    )
    conn.commit()
    return int(curseur.lastrowid)


def supprimer_reservation(conn, reservation_id):
    curseur = conn.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
    if curseur.rowcount == 0:
        raise Introuvable("Cette réservation n'existe pas.")
    conn.commit()
