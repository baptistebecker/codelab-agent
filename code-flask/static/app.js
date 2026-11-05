(() => {
  "use strict";

  const config = window.PLANNING || {};
  const GRID_START = 8 * 60;
  const GRID_END = 20 * 60;
  const GRID_MINUTES = GRID_END - GRID_START;
  const PAS = 30;

  const selection = (selecteur, racine = document) => racine.querySelector(selecteur);
  const selections = (selecteur, racine = document) => Array.from(racine.querySelectorAll(selecteur));

  const enMinutes = (heure) => {
    const [heures, minutes] = heure.split(":").map(Number);
    return heures * 60 + minutes;
  };

  const enHeure = (minutes) =>
    `${String(Math.floor(minutes / 60)).padStart(2, "0")}:${String(minutes % 60).padStart(2, "0")}`;

  function toast(message, type = "succes") {
    const zone = selection("#toasts");
    if (!zone) return;
    const element = document.createElement("div");
    element.className = `toast${type === "erreur" ? " is-error" : ""}`;
    element.setAttribute("role", "status");
    element.textContent = message;
    zone.append(element);
    window.setTimeout(() => {
      element.classList.add("is-leaving");
      window.setTimeout(() => element.remove(), 250);
    }, 3800);
  }

  function afficherFlash() {
    const contenu = window.sessionStorage.getItem("flash");
    if (!contenu) return;
    window.sessionStorage.removeItem("flash");
    try {
      const flash = JSON.parse(contenu);
      toast(flash.message, flash.type);
    } catch (_erreur) {
      toast(contenu);
    }
  }

  function flashPuisNavigation(url, message) {
    window.sessionStorage.setItem(
      "flash",
      JSON.stringify({ message, type: "succes" })
    );
    window.location.href = url || window.location.href;
  }

  async function appeler(url, methode, donnees) {
    const reponse = await fetch(url, {
      method: methode,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(donnees || {}),
    });
    let contenu = {};
    try {
      contenu = await reponse.json();
    } catch (_erreur) {
      contenu = {};
    }
    if (!reponse.ok) {
      throw new Error(contenu.erreur || "Une erreur est survenue. Réessayez.");
    }
    return contenu;
  }

  function ouvrirDialogue(dialogue) {
    if (dialogue && !dialogue.open) dialogue.showModal();
  }

  function fermerDialogue(dialogue) {
    if (dialogue && dialogue.open) dialogue.close();
  }

  selections("[data-fermer-dialogue]").forEach((bouton) => {
    bouton.addEventListener("click", () => fermerDialogue(bouton.closest("dialog")));
  });

  selections("dialog").forEach((dialogue) => {
    dialogue.addEventListener("click", (evenement) => {
      if (evenement.target === dialogue) fermerDialogue(dialogue);
    });
  });

  const salleDialogue = selection("#salle-dialog");
  const salleFormulaire = selection("#salle-form");
  const salleErreur = selection("#salle-error");
  const salleTitre = selection("#salle-dialog-titre");
  const salleSurtitre = selection("#salle-dialog-surtitre");
  const salleSubmit = selection("#salle-submit");

  function ouvrirSalle(salle = null) {
    if (!salleFormulaire) return;
    salleFormulaire.reset();
    salleErreur.hidden = true;
    salleFormulaire.elements.id.value = salle ? salle.id : "";
    if (salle) {
      salleTitre.textContent = "Modifier la salle";
      salleSurtitre.textContent = salle.nom;
      salleSubmit.textContent = "Enregistrer";
      salleFormulaire.elements.nom.value = salle.nom;
      salleFormulaire.elements.capacite.value = salle.capacite;
      salleFormulaire.elements.projecteur.checked =
        salle.projecteur === "1" || salle.projecteur === 1 || salle.projecteur === true;
    } else {
      salleTitre.textContent = "Ajouter une salle";
      salleSurtitre.textContent = "Gestion";
      salleSubmit.textContent = "Ajouter la salle";
      salleFormulaire.elements.capacite.value = "12";
    }
    ouvrirDialogue(salleDialogue);
    salleFormulaire.elements.nom.focus();
  }

  selections("[data-ouvrir-salle]").forEach((bouton) => {
    bouton.addEventListener("click", () => ouvrirSalle());
  });

  selections("[data-modifier-salle]").forEach((bouton) => {
    bouton.addEventListener("click", () => {
      ouvrirSalle({
        id: bouton.dataset.id,
        nom: bouton.dataset.nom,
        capacite: bouton.dataset.capacite,
        projecteur: bouton.dataset.projecteur,
      });
    });
  });

  if (salleFormulaire) {
    salleFormulaire.addEventListener("submit", async (evenement) => {
      evenement.preventDefault();
      salleErreur.hidden = true;
      const identifiant = salleFormulaire.elements.id.value;
      const donnees = {
        nom: salleFormulaire.elements.nom.value.trim(),
        capacite: Number(salleFormulaire.elements.capacite.value),
        projecteur: salleFormulaire.elements.projecteur.checked,
        semaine: config.semaine,
      };
      const url = identifiant ? `/api/salles/${identifiant}` : "/api/salles";
      const methode = identifiant ? "PUT" : "POST";
      const libelle = salleSubmit.textContent;
      salleSubmit.disabled = true;
      salleSubmit.textContent = "Enregistrement…";
      try {
        const resultat = await appeler(url, methode, donnees);
        flashPuisNavigation(
          resultat.redirect,
          identifiant ? "Salle mise à jour." : "Salle ajoutée."
        );
      } catch (erreur) {
        salleErreur.textContent = erreur.message;
        salleErreur.hidden = false;
      } finally {
        salleSubmit.disabled = false;
        salleSubmit.textContent = libelle;
      }
    });
  }

  const confirmDialogue = selection("#confirm-dialog");
  const confirmTitre = selection("#confirm-titre");
  const confirmTexte = selection("#confirm-texte");
  const confirmValider = selection("#confirm-valider");
  let confirmationAction = null;

  function confirmer({ titre, texte, libelle = "Supprimer", action }) {
    if (!confirmDialogue) return;
    confirmTitre.textContent = titre;
    confirmTexte.textContent = texte;
    confirmValider.textContent = libelle;
    confirmationAction = action;
    ouvrirDialogue(confirmDialogue);
  }

  if (confirmValider) {
    confirmValider.addEventListener("click", async () => {
      if (!confirmationAction) return;
      const action = confirmationAction;
      confirmationAction = null;
      const libelle = confirmValider.textContent;
      confirmValider.disabled = true;
      confirmValider.textContent = "Suppression…";
      try {
        await action();
      } catch (erreur) {
        toast(erreur.message, "erreur");
      } finally {
        confirmValider.disabled = false;
        confirmValider.textContent = libelle;
        fermerDialogue(confirmDialogue);
      }
    });
  }

  selections("[data-supprimer-salle]").forEach((bouton) => {
    bouton.addEventListener("click", () => {
      const nom = bouton.dataset.nom;
      confirmer({
        titre: "Supprimer cette salle ?",
        texte: `La salle ${nom} et toutes ses réservations seront définitivement supprimées.`,
        action: async () => {
          const semaine = encodeURIComponent(config.semaine || "");
          const salleCourante = encodeURIComponent(config.salleId || "");
          const resultat = await appeler(
            `/api/salles/${bouton.dataset.id}?semaine=${semaine}&salle=${salleCourante}`,
            "DELETE"
          );
          flashPuisNavigation(resultat.redirect, "Salle supprimée.");
        },
      });
    });
  });

  const resaDialogue = selection("#reservation-dialog");
  const resaFormulaire = selection("#reservation-form");
  const resaErreur = selection("#reservation-error");
  const resaBouton = selection("#btn-reserver");

  function remplirReservation(creneau = {}) {
    if (!resaFormulaire) return;
    resaFormulaire.reset();
    resaFormulaire.elements.date.value = config.dateDefaut;
    resaFormulaire.elements.debut.value = config.debutDefaut;
    resaFormulaire.elements.fin.value = config.finDefaut;
    if (creneau.date) resaFormulaire.elements.date.value = creneau.date;
    if (creneau.debut) resaFormulaire.elements.debut.value = creneau.debut;
    if (creneau.fin) resaFormulaire.elements.fin.value = creneau.fin;
    const capacite = Number(config.capacite || 1);
    resaFormulaire.elements.participants.max = String(capacite);
    resaFormulaire.elements.participants.value = "1";
    resaErreur.hidden = true;
  }

  function ouvrirReservation(creneau = {}) {
    if (!resaFormulaire) return;
    remplirReservation(creneau);
    ouvrirDialogue(resaDialogue);
    resaFormulaire.elements.personne.focus();
  }

  if (resaBouton) {
    resaBouton.addEventListener("click", () => ouvrirReservation());
  }

  if (resaFormulaire) {
    resaFormulaire.elements.debut.addEventListener("change", () => {
      const debut = enMinutes(resaFormulaire.elements.debut.value);
      let fin = enMinutes(resaFormulaire.elements.fin.value);
      if (fin <= debut) fin = debut + 60;
      if (fin - debut > 240) fin = debut + 240;
      fin = Math.min(fin, GRID_END);
      resaFormulaire.elements.fin.value = enHeure(fin);
    });

    resaFormulaire.addEventListener("submit", async (evenement) => {
      evenement.preventDefault();
      resaErreur.hidden = true;
      const bouton = resaFormulaire.querySelector('button[type="submit"]');
      const libelle = bouton.textContent;
      bouton.disabled = true;
      bouton.textContent = "Réservation…";
      try {
        const resultat = await appeler("/api/reservations", "POST", {
          salle_id: Number(resaFormulaire.elements.salle_id.value),
          personne: resaFormulaire.elements.personne.value.trim(),
          date: resaFormulaire.elements.date.value,
          debut: resaFormulaire.elements.debut.value,
          fin: resaFormulaire.elements.fin.value,
          participants: Number(resaFormulaire.elements.participants.value),
        });
        flashPuisNavigation(resultat.redirect, "Réservation enregistrée.");
      } catch (erreur) {
        resaErreur.textContent = erreur.message;
        resaErreur.hidden = false;
      } finally {
        bouton.disabled = false;
        bouton.textContent = libelle;
      }
    });
  }

  const detailDialogue = selection("#detail-dialog");
  const detailDate = selection("#detail-date");
  const detailTitre = selection("#detail-titre");
  const detailPersonne = selection("#detail-personne");
  const detailParticipants = selection("#detail-participants");
  const detailHoraire = selection("#detail-horaire");
  const boutonAnnulerResa = selection("#btn-annuler-reservation");
  const formatDateLongue = new Intl.DateTimeFormat("fr-FR", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });
  let reservationCourante = null;

  selections(".resa").forEach((bloc) => {
    bloc.addEventListener("click", (evenement) => {
      evenement.stopPropagation();
      reservationCourante = {
        id: bloc.dataset.resaId,
        personne: bloc.dataset.personne,
        date: bloc.dataset.date,
        debut: bloc.dataset.debut,
        fin: bloc.dataset.fin,
        participants: bloc.dataset.participants,
      };
      detailTitre.textContent = "Réservation";
      detailPersonne.textContent = reservationCourante.personne;
      detailParticipants.textContent = `${reservationCourante.participants} personne${
        Number(reservationCourante.participants) > 1 ? "s" : ""
      }`;
      detailHoraire.textContent = `${reservationCourante.debut} – ${reservationCourante.fin}`;
      detailDate.textContent = formatDateLongue.format(
        new Date(`${reservationCourante.date}T12:00:00`)
      );
      ouvrirDialogue(detailDialogue);
    });
  });

  if (boutonAnnulerResa) {
    boutonAnnulerResa.addEventListener("click", () => {
      if (!reservationCourante) return;
      fermerDialogue(detailDialogue);
      confirmer({
        titre: "Annuler cette réservation ?",
        texte: `La réservation de ${reservationCourante.personne} (${reservationCourante.debut} – ${reservationCourante.fin}) sera supprimée.`,
        libelle: "Annuler la réservation",
        action: async () => {
          await appeler(`/api/reservations/${reservationCourante.id}`, "DELETE");
          flashPuisNavigation(window.location.href, "Réservation annulée.");
        },
      });
    });
  }

  function creneauDepuis(colonne, clientY) {
    const rect = colonne.getBoundingClientRect();
    const ratio = Math.min(Math.max((clientY - rect.top) / rect.height, 0), 1);
    let debut = GRID_START + Math.floor((ratio * GRID_MINUTES) / PAS) * PAS;
    debut = Math.max(GRID_START, Math.min(debut, GRID_END - PAS));
    let fin = Math.min(debut + 60, GRID_END);
    if (fin - debut < PAS) {
      debut = GRID_END - PAS;
      fin = GRID_END;
    }
    return {
      date: colonne.dataset.date,
      debut: enHeure(debut),
      fin: enHeure(fin),
    };
  }

  function elementGhost(colonne) {
    let ghost = colonne.querySelector(".cal-ghost");
    if (!ghost) {
      ghost = document.createElement("div");
      ghost.className = "cal-ghost";
      const etiquette = document.createElement("span");
      ghost.append(etiquette);
      colonne.append(ghost);
    }
    return ghost;
  }

  selections(".cal-col").forEach((colonne) => {
    colonne.addEventListener("mousemove", (evenement) => {
      const ghost = colonne.querySelector(".cal-ghost");
      if (evenement.target.closest(".resa") || !resaFormulaire) {
        if (ghost) ghost.classList.remove("is-visible");
        return;
      }
      const creneau = creneauDepuis(colonne, evenement.clientY);
      const debut = enMinutes(creneau.debut);
      const fin = enMinutes(creneau.fin);
      const element = elementGhost(colonne);
      element.style.top = `${((debut - GRID_START) / GRID_MINUTES) * 100}%`;
      element.style.height = `${((fin - debut) / GRID_MINUTES) * 100}%`;
      element.querySelector("span").textContent = `${creneau.debut} – ${creneau.fin}`;
      element.classList.add("is-visible");
    });

    colonne.addEventListener("mouseleave", () => {
      const ghost = colonne.querySelector(".cal-ghost");
      if (ghost) ghost.classList.remove("is-visible");
    });

    colonne.addEventListener("click", (evenement) => {
      if (evenement.target.closest(".resa") || !resaFormulaire) return;
      ouvrirReservation(creneauDepuis(colonne, evenement.clientY));
    });
  });

  function mettreAJourHeure() {
    if (!config.aujourdhui) return;
    const colonne = selection(`.cal-col[data-date="${config.aujourdhui}"]`);
    if (!colonne) return;
    const maintenant = new Date();
    const minutes = maintenant.getHours() * 60 + maintenant.getMinutes();
    let ligne = selection(".now-line");
    if (minutes < GRID_START || minutes > GRID_END) {
      if (ligne) ligne.remove();
      return;
    }
    if (!ligne) {
      ligne = document.createElement("div");
      ligne.className = "now-line";
      ligne.setAttribute("aria-label", "Heure actuelle");
      const point = document.createElement("span");
      point.className = "now-dot";
      ligne.append(point);
    }
    if (ligne.parentElement !== colonne) colonne.append(ligne);
    ligne.style.setProperty(
      "--top",
      `${((minutes - GRID_START) / GRID_MINUTES) * 100}%`
    );
  }

  afficherFlash();
  mettreAJourHeure();
  window.setInterval(mettreAJourHeure, 30000);
})();
