# Réservation de salles

<!-- À compléter AVANT de lancer l'agent. Il lit ce fichier à chaque démarrage. -->

## Le projet
<!-- En une ou deux phrases : ce que fait l'application et pour qui. -->

## Technologies
Python, Flask, FastAPI ou Streamlit (à préciser), SQLite, pytest.

## Commandes
- Lancer l'application : `python app.py` dans `code-flask`, `streamlit run app.py` dans `code-streamlit`
- Lancer les tests : `pytest` dans le dossier de code

## Base de données
Tables et exemples dans `base.sql`. `data.db` se crée au premier lancement. Supprimer `data.db` après un changement de `base.sql`.

## Structure du code
<!-- Où va quoi : par exemple où se trouvent les règles métier, les routes, l'accès à la base. -->

## Règles métier
<!-- Recopiez et précisez les règles du cahier des charges. -->

## Façon de travailler
- Une fonctionnalité à la fois.
- Ajouter ou mettre à jour les tests à chaque fonctionnalité, puis lancer `pytest`.
- Ne pas ajouter d'autre dépendance sans le demander.
- Ne pas faire de `git push` ni de fusion : le binôme s'en charge.
