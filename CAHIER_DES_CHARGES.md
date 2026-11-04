# Projet 2 : Réservation de salles

Séance 2 : vous travaillez avec un agent de code, OpenCode ou Mistral Vibe. Complétez AGENTS.md avant de lancer l’agent, puis relisez chaque fonctionnalité par pull request.

## Contexte

Dans un bâtiment universitaire, les salles de réunion et de travail se réservent par mail auprès du secrétariat, qui tient un tableur. Les demandes se croisent, les doubles réservations sont fréquentes et certaines salles sont réservées pour des groupes trop grands. Le secrétariat veut que chacun puisse réserver lui-même, avec des règles appliquées automatiquement.

## Ce que l'application doit faire

### Données

- Salle : nom, capacité, présence d’un projecteur.
- Réservation : salle, personne, date, heure de début et de fin, nombre de participants.

### Fonctionnalités

- Ajouter, modifier ou supprimer une salle.
- Réserver une salle au nom d’une personne.
- Annuler une réservation.
- Afficher le planning d’une salle sur une semaine.

### Règles

- Deux réservations d’une même salle ne se chevauchent pas. Finir à 12 h et commencer à 12 h est autorisé.
- Le nombre de participants ne dépasse pas la capacité de la salle.
- Une réservation a lieu entre 8 h et 20 h et dure de 30 min à 4 h.
- Supprimer une salle supprime ses réservations. Il n’y a pas d’authentification. La semaine va du lundi au dimanche.

## Exemples de vérification

Salle S1 de capacité 20, déjà réservée le lundi de 10 h à 12 h.

| Action | Résultat attendu |
|---|---|
| Lundi, 11 h à 13 h | Refusée : chevauchement |
| Lundi, 12 h à 13 h | Acceptée |
| Lundi, 14 h à 15 h, 25 participants | Refusée : capacité dépassée |
| Lundi, 7 h 30 à 9 h | Refusée : avant 8 h |
| Mardi, 14 h à 14 h 20 | Refusée : moins de 30 min |
| Mardi, 8 h à 13 h | Refusée : plus de 4 h |

## Technologies

Python, Flask ou Streamlit, SQLite, pytest. L’organisation du code, le schéma de la base et l’interface sont libres.

## Si vous avez fini

Chercher une salle libre selon le créneau et la capacité, afficher le taux d’occupation, exporter le planning.

## À rendre

- Le dépôt GitHub du binôme, avec son historique Git, poussé avant les questions.
- Un README qui indique comment lancer l’application.

## Épreuve

En fin de séance, trois questions individuelles sur votre application, sur papier et machines fermées. Chacun doit comprendre tout le code.
