# Réservation de salles

## Le projet
Permettre au personnel d'un bâtiment universitaire de réserver lui-même une salle, sans conflit et dans la limite de sa capacité.

## Technologies
Python, SQLite, pytest. Framework : Flask (`code-flask`) ou Streamlit (`code-streamlit`).

## Commandes
- Lancer l'application : `python app.py` dans `code-flask`, `streamlit run app.py` dans `code-streamlit`
- Lancer les tests : `pytest` dans le dossier de code

## Base de données
Tables et exemples dans `base.sql`. `data.db` se crée au premier lancement. Supprimer `data.db` après un changement de `base.sql`.

## Règles métier
- Deux réservations d'une même salle ne se chevauchent pas. Finir à 12 h et commencer à 12 h est autorisé.
- Le nombre de participants ne dépasse pas la capacité de la salle.
- Une réservation a lieu entre 8 h et 20 h et dure de 30 min à 4 h.
- Supprimer une salle supprime ses réservations.
- Il n'y a pas d'authentification. La semaine va du lundi au dimanche.

## Façon de travailler

### Développement & Qualité du code
- Une fonctionnalité à la fois.
- Ne rien ajouter ou anticiper qui n'est pas explicitement demandé.
- Ajouter ou mettre à jour les tests unitaires/d'intégration à chaque nouvelle fonctionnalité, puis valider avec `pytest`.
- Ne pas ajouter de dépendances supplémentaires (packages Python/pip) sans demande explicite.
- Isoler la logique métier des frameworks web (Flask/Streamlit) dans des modules dédiés.

### Git & GitHub
- **Commits atomiques** : Faire un commit clair et descriptif dès qu'une fonctionnalité ou un correctif est validé par les tests (ex: `feat: ajout validation capacite salle` ou `test: ajout tests chevauchement horaire`).
- **Commits en anglais ou en français** : Conserver un style uniforme et explicite pour tous les messages de commit.
- **Gestion des pushs** : Ne faire `git push` que si le binôme le demande ou valide l'état du code.
- **Résolution des conflits** : 
  - Avant de pousser ou après un `git pull`, en cas de conflit, toujours privilégier l'intégration propre en relançant la suite de tests `pytest` complète.
  - Ne jamais écraser le travail du binôme avec un `git push --force`.
  - Résoudre les conflits fichier par fichier en expliquant au binôme les choix effectués si nécessaire.

## À vous d'ajouter
<!-- Ajoutez ici d'autres consignes spécifiques selon l'évolution du TP -->
- Cocher les tâches dans le readme lorsqu'elles sont effectuées