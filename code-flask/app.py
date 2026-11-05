from contextlib import closing
from datetime import date, datetime, timedelta

from flask import Flask, jsonify, redirect, render_template, request, url_for

from base import ouvrir_base
import metier

app = Flask(__name__)

JOURS_COURTS = ("Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim")
JOURS_LONGS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")
MOIS = (
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
)
MOIS_COURTS = (
    "janv.",
    "févr.",
    "mars",
    "avr.",
    "mai",
    "juin",
    "juil.",
    "août",
    "sept.",
    "oct.",
    "nov.",
    "déc.",
)
MINUTES_GRILLE = metier.HEURE_FERMETURE - metier.HEURE_OUVERTURE

OPTIONS_DEBUT = [
    metier.heure_depuis_minutes(minutes)
    for minutes in range(metier.HEURE_OUVERTURE, metier.HEURE_FERMETURE, 30)
]
OPTIONS_FIN = [
    metier.heure_depuis_minutes(minutes)
    for minutes in range(metier.HEURE_OUVERTURE + 30, metier.HEURE_FERMETURE + 1, 30)
]


def _connexion():
    return closing(ouvrir_base())


def _capitaliser(texte):
    return texte[:1].upper() + texte[1:]


def _date_longue(jour):
    return f"{JOURS_LONGS[jour.weekday()]} {jour.day} {MOIS[jour.month - 1]}"


def _libelle_semaine(lundi):
    dimanche = lundi + timedelta(days=6)
    if lundi.year != dimanche.year:
        return (
            f"{lundi.day} {MOIS[lundi.month - 1]} {lundi.year} – "
            f"{dimanche.day} {MOIS[dimanche.month - 1]} {dimanche.year}"
        )
    if lundi.month != dimanche.month:
        return (
            f"{lundi.day} {MOIS[lundi.month - 1]} – "
            f"{dimanche.day} {MOIS[dimanche.month - 1]} {dimanche.year}"
        )
    return f"{lundi.day} – {dimanche.day} {MOIS[dimanche.month - 1]} {dimanche.year}"


def _format_duree(minutes):
    heures, reste = divmod(minutes, 60)
    if heures and reste:
        return f"{heures} h {reste:02d}"
    if heures:
        return f"{heures} h"
    return f"{reste} min"


def _couleur_reservation(personne):
    return sum(ord(caractere) for caractere in personne) % 6


def _preparer_evenements(reservations, lundi):
    evenements = []
    for reservation in reservations:
        jour = date.fromisoformat(reservation["date"])
        debut = max(metier.minutes_depuis_heure(reservation["debut"]), metier.HEURE_OUVERTURE)
        fin = min(metier.minutes_depuis_heure(reservation["fin"]), metier.HEURE_FERMETURE)
        if fin <= debut:
            continue
        duree = fin - debut
        evenements.append(
            {
                "id": reservation["id"],
                "personne": reservation["personne"],
                "date": reservation["date"],
                "debut": reservation["debut"],
                "fin": reservation["fin"],
                "participants": reservation["participants"],
                "jour_index": (jour - lundi).days,
                "top": round((debut - metier.HEURE_OUVERTURE) / MINUTES_GRILLE * 100, 4),
                "hauteur": round(duree / MINUTES_GRILLE * 100, 4),
                "couleur": _couleur_reservation(reservation["personne"]),
                "classe_duree": "courte" if duree <= 30 else "moyenne" if duree <= 60 else "",
            }
        )
    return evenements


def _ligne_actuelle(lundi):
    maintenant = datetime.now()
    if not (lundi <= maintenant.date() <= lundi + timedelta(days=6)):
        return None
    minutes = maintenant.hour * 60 + maintenant.minute
    if not (metier.HEURE_OUVERTURE <= minutes <= metier.HEURE_FERMETURE):
        return None
    return {
        "jour_index": maintenant.weekday(),
        "top": round((minutes - metier.HEURE_OUVERTURE) / MINUTES_GRILLE * 100, 4),
    }


def _defauts_reservation(lundi):
    maintenant = datetime.now()
    if lundi <= maintenant.date() <= lundi + timedelta(days=6):
        jour = maintenant.date()
        minutes = (maintenant.hour * 60 + maintenant.minute + 29) // 30 * 30
        minutes = max(
            metier.HEURE_OUVERTURE,
            min(minutes, metier.HEURE_FERMETURE - 30),
        )
    else:
        jour = lundi
        minutes = 9 * 60
    fin = min(minutes + 60, metier.HEURE_FERMETURE)
    return {
        "date": jour.isoformat(),
        "debut": metier.heure_depuis_minutes(minutes),
        "fin": metier.heure_depuis_minutes(fin),
    }


def _donnees():
    if request.is_json:
        contenu = request.get_json(silent=True)
        return contenu if isinstance(contenu, dict) else {}
    return request.form.to_dict()


def _reponse_erreur(erreur):
    statut = 404 if isinstance(erreur, metier.Introuvable) else 400
    return jsonify({"erreur": str(erreur)}), statut


def _redirect_accueil(salle_id, semaine):
    return url_for("accueil", salle=salle_id, semaine=semaine)


@app.get("/")
def accueil():
    lundi = metier.semaine_demandee(request.args.get("semaine"))
    with _connexion() as conn:
        salles = [dict(salle) for salle in metier.lister_salles(conn)]
        statistiques = metier.statistiques_semaine(conn, lundi)
        salle_choisie = None
        reservations = []
        if salles:
            salle_id = request.args.get("salle", type=int)
            if salle_id is None:
                salle_choisie = salles[0]
            else:
                salle_choisie = next(
                    (salle for salle in salles if salle["id"] == salle_id), None
                )
                if salle_choisie is None:
                    return redirect(
                        url_for(
                            "accueil",
                            salle=salles[0]["id"],
                            semaine=lundi.isoformat(),
                        )
                    )
            reservations = metier.lister_reservations_semaine(
                conn, salle_choisie["id"], lundi
            )

    for salle in salles:
        stats = statistiques.get(salle["id"])
        salle["nb_reservations"] = stats["nombre"] if stats else 0
        salle["duree_reservee"] = (
            _format_duree(stats["minutes"]) if stats and stats["minutes"] else "—"
        )

    aujourdhui = date.today()
    jours = []
    for index in range(7):
        jour = lundi + timedelta(days=index)
        jours.append(
            {
                "iso": jour.isoformat(),
                "nom": JOURS_COURTS[index],
                "numero": jour.day,
                "mois": MOIS_COURTS[jour.month - 1],
                "aujourdhui": jour == aujourdhui,
            }
        )

    heures = [
        {
            "libelle": metier.heure_depuis_minutes(minutes),
            "position": round(
                (minutes - metier.HEURE_OUVERTURE) / MINUTES_GRILLE * 100, 4
            ),
        }
        for minutes in range(
            metier.HEURE_OUVERTURE, metier.HEURE_FERMETURE + 1, 60
        )
    ]
    defauts = _defauts_reservation(lundi)
    config = {
        "semaine": lundi.isoformat(),
        "aujourdhui": aujourdhui.isoformat(),
        "salleId": salle_choisie["id"] if salle_choisie else None,
        "salleNom": salle_choisie["nom"] if salle_choisie else None,
        "capacite": salle_choisie["capacite"] if salle_choisie else None,
        "dateDefaut": defauts["date"],
        "debutDefaut": defauts["debut"],
        "finDefaut": defauts["fin"],
    }

    return render_template(
        "planning.html",
        salles=salles,
        salle=salle_choisie,
        jours=jours,
        evenements=_preparer_evenements(reservations, lundi),
        ligne_actuelle=_ligne_actuelle(lundi),
        semaine=lundi,
        semaine_precedente=(lundi - timedelta(days=7)).isoformat(),
        semaine_suivante=(lundi + timedelta(days=7)).isoformat(),
        semaine_courante=metier.lundi_de(aujourdhui).isoformat(),
        libelle_semaine=_libelle_semaine(lundi),
        date_longue=_capitaliser(_date_longue(aujourdhui)),
        heures=heures,
        options_debut=OPTIONS_DEBUT,
        options_fin=OPTIONS_FIN,
        config=config,
    )


@app.post("/api/salles")
def api_creer_salle():
    donnees = _donnees()
    try:
        with _connexion() as conn:
            salle_id = metier.creer_salle(
                conn,
                donnees.get("nom"),
                donnees.get("capacite"),
                donnees.get("projecteur"),
            )
    except metier.ErreurMetier as erreur:
        return _reponse_erreur(erreur)

    semaine = metier.semaine_demandee(donnees.get("semaine"))
    return jsonify(
        {
            "ok": True,
            "id": salle_id,
            "redirect": _redirect_accueil(salle_id, semaine.isoformat()),
        }
    )


@app.put("/api/salles/<int:salle_id>")
def api_modifier_salle(salle_id):
    donnees = _donnees()
    try:
        with _connexion() as conn:
            metier.modifier_salle(
                conn,
                salle_id,
                donnees.get("nom"),
                donnees.get("capacite"),
                donnees.get("projecteur"),
            )
    except metier.ErreurMetier as erreur:
        return _reponse_erreur(erreur)

    semaine = metier.semaine_demandee(donnees.get("semaine"))
    return jsonify(
        {
            "ok": True,
            "redirect": _redirect_accueil(salle_id, semaine.isoformat()),
        }
    )


@app.delete("/api/salles/<int:salle_id>")
def api_supprimer_salle(salle_id):
    salle_courante = request.args.get("salle", type=int)
    try:
        with _connexion() as conn:
            metier.supprimer_salle(conn, salle_id)
            salles = metier.lister_salles(conn)
    except metier.ErreurMetier as erreur:
        return _reponse_erreur(erreur)

    semaine = metier.semaine_demandee(request.args.get("semaine"))
    if salle_courante and salle_courante != salle_id and any(
        salle["id"] == salle_courante for salle in salles
    ):
        cible = salle_courante
    else:
        cible = salles[0]["id"] if salles else None

    redirect_url = (
        _redirect_accueil(cible, semaine.isoformat())
        if cible
        else url_for("accueil", semaine=semaine.isoformat())
    )
    return jsonify({"ok": True, "redirect": redirect_url})


@app.post("/api/reservations")
def api_creer_reservation():
    donnees = _donnees()
    try:
        with _connexion() as conn:
            reservation_id = metier.creer_reservation(
                conn,
                donnees.get("salle_id"),
                donnees.get("personne"),
                donnees.get("date"),
                donnees.get("debut"),
                donnees.get("fin"),
                donnees.get("participants"),
            )
    except metier.ErreurMetier as erreur:
        return _reponse_erreur(erreur)

    semaine = metier.lundi_de(metier.analyser_date(donnees.get("date")))
    return jsonify(
        {
            "ok": True,
            "id": reservation_id,
            "redirect": _redirect_accueil(donnees.get("salle_id"), semaine.isoformat()),
        }
    )


@app.delete("/api/reservations/<int:reservation_id>")
def api_supprimer_reservation(reservation_id):
    try:
        with _connexion() as conn:
            metier.supprimer_reservation(conn, reservation_id)
    except metier.ErreurMetier as erreur:
        return _reponse_erreur(erreur)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)
