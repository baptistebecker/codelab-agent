# Réservation de salles

> **Permettre à chacun de réserver une salle du bâtiment, sans conflit et dans la limite de sa capacité.**

Séance 2 · En binôme · Avec un agent de code, OpenCode ou Mistral Vibe.

[Démarrer](#démarrer) · [Cahier des charges en PDF](CAHIER_DES_CHARGES.pdf)

## Le contexte

Dans un bâtiment universitaire, les salles se réservent par mail auprès du secrétariat, qui tient un tableur. Les demandes se croisent, les doubles réservations sont fréquentes et certaines salles sont réservées pour des groupes trop grands. Le secrétariat veut que chacun puisse réserver lui-même, avec des règles appliquées automatiquement.

## Les données

| Objet | Ce qu’on enregistre |
|---|---|
| **Salle** | nom, capacité, présence d’un projecteur |
| **Réservation** | salle, personne, date, heure de début et de fin, nombre de participants |

## Ce que l’application doit faire

- [ ] Ajouter, modifier ou supprimer une salle
- [ ] Réserver une salle au nom d’une personne
- [ ] Annuler une réservation
- [ ] Afficher le planning d’une salle sur une semaine

## Les règles

- Deux réservations d’une même salle ne se chevauchent pas. Finir à 12 h et commencer à 12 h est autorisé.
- Le nombre de participants ne dépasse pas la capacité de la salle.
- Une réservation a lieu entre 8 h et 20 h et dure de 30 min à 4 h.
- Supprimer une salle supprime ses réservations.
- Il n’y a pas d’authentification. La semaine va du lundi au dimanche.

## Pour vérifier

Salle S1 de capacité 20, déjà réservée le lundi de 10 h à 12 h.

| Action | Résultat attendu |
|---|---|
| Lundi, 11 h à 13 h | Refusée : chevauchement |
| Lundi, 12 h à 13 h | Acceptée |
| Lundi, 14 h à 15 h, 25 participants | Refusée : capacité dépassée |
| Lundi, 7 h 30 à 9 h | Refusée : avant 8 h |
| Mardi, 14 h à 14 h 20 | Refusée : moins de 30 min |
| Mardi, 8 h à 13 h | Refusée : plus de 4 h |

## Si vous avez fini

Chercher une salle libre selon le créneau et la capacité, afficher le taux d’occupation, exporter le planning.

## Ce qui est libre

L’organisation du code, le schéma de la base et l’interface. Python, Flask ou Streamlit, SQLite et pytest sont imposés.

## À la fin de la séance

- Poussez votre travail sur GitHub avant les questions.
- Trois questions individuelles, sur papier et machines fermées. Chacun doit comprendre tout le code.

---

# Démarrer

Python 3.11 ou plus est nécessaire.

## Créer votre dépôt

1. Un membre du binôme ouvre <https://github.com/umons-ig/codelab-agent>, clique sur **Use this template**, puis **Create a new repository**, et choisit **Private**.
2. Dans **Settings**, puis **Collaborators**, il ajoute son partenaire et `Tanguyvans`. Le partenaire accepte l'invitation.
3. Chacun récupère le dépôt sur sa machine, puis ouvre le dossier :

```bash
git clone <adresse-de-votre-dépôt>
```

## Installer

macOS ou Linux :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell) :

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process RemoteSigned
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Vérifier que tout fonctionne

```bash
pytest
python app.py
```

Ouvrez ensuite <http://127.0.0.1:5000>. Dans le terminal, Ctrl+C arrête l’application.

## Flask ou Streamlit

Le code de démarrage utilise Flask. Choisissez ce que vous préférez.

**Flask** : rien de plus à installer. [Démarrage rapide](https://flask.palletsprojects.com/en/stable/quickstart/).

**Streamlit** : plus rapide pour une interface simple. [Premiers pas](https://docs.streamlit.io/get-started) · [Documentation](https://docs.streamlit.io).

```bash
pip install streamlit
```

Remplacez le contenu de `app.py` par :

```python
import streamlit as st

from db import get_connection, init_db

init_db()
st.title("Mon application")
```

Puis lancez :

```bash
streamlit run app.py
```

Avec Streamlit, ajoutez `streamlit` à `requirements.txt`, supprimez `templates/` et `tests/test_demarrage.py`, qui testent la page Flask, et testez vos règles dans vos propres fichiers de `tests/`.

SQLite : [documentation du module `sqlite3`](https://docs.python.org/3/library/sqlite3.html).

## Bien travailler avec l'agent

- Une petite demande à la fois.
- Donnez les règles et un exemple à vérifier.
- Demandez des tests, puis lancez `pytest`.
- Essayez l'application et lisez le diff.
- Faites un commit à chaque étape qui marche.
- Si ça part de travers, revenez au dernier commit avec `git restore .`, supprimez les nouveaux fichiers créés par l’agent, puis reformulez.

Trop vague : « Fais-moi l'application. »

Précis : « Ajoute la réservation d'une salle. Refuse les chevauchements : finir à 12 h et commencer à 12 h est autorisé. Ajoute les tests et lance pytest. »

## Travailler à deux

Une seule personne utilise l'agent à la fois. Pour chaque fonctionnalité :

```bash
git switch main
git pull
git switch -c nom-de-la-fonctionnalite
```

Quand l'agent a terminé et que les tests passent :

```bash
git add -A
git commit -m "ajout de la fonctionnalité"
git push -u origin nom-de-la-fonctionnalite
```

Ouvrez ensuite une pull request sur GitHub.

## Revue de code

1. Le pilote ouvre une nouvelle session de l'agent et demande : `Utilise le skill revue-de-code`. Le skill est dans `.agents/skills/revue-de-code/SKILL.md` : lisez-le. Mistral Vibe ne lit ce dossier que si vous lui faites confiance au lancement. Si le skill n'est pas trouvé, demandez : `Relis git diff main...HEAD sans rien modifier`.
2. Le relecteur classe chaque remarque : juste, fausse ou inutile, en vérifiant dans le code et dans l'application.
3. Le pilote fait corriger les remarques justes, puis fait `git add -A`, `git commit` et `git push`.
4. Le relecteur laisse un commentaire sur la pull request : ce qui est retenu ou rejeté, et pourquoi.
5. Le relecteur fusionne la pull request sur GitHub, puis vous inversez les rôles.

Avant de fusionner, vérifiez trois points :

- Est-ce bien ce qui était demandé, sans rien en plus ?
- Un cas limite a-t-il été essayé : champ vide, doublon, conflit ?
- Le relecteur sait-il expliquer ce code ?


## Lancer l'agent

Installez un des deux agents, puis tapez sa commande dans le terminal, **dans ce dossier** :

| Agent | Installation | Lancement |
|---|---|---|
| OpenCode | `curl -fsSL https://opencode.ai/install \| bash` ou `npm install -g opencode-ai` | `opencode` |
| Mistral Vibe | `curl -LsSf https://mistral.ai/vibe/install.sh \| bash` ou `uv tool install mistral-vibe` | `vibe` |

Sous Windows, `curl … | bash` ne fonctionne pas dans PowerShell. Utilisez `npm install -g opencode-ai` (Node.js requis) ou installez uv, puis Vibe :

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv tool install mistral-vibe
```

Dans OpenCode, choisissez un modèle gratuit avec `/models`, puis tapez `free`.
Mistral Vibe demande de se connecter avec un compte Mistral au premier lancement.

**Avant de lancer l'agent, complétez `AGENTS.md`.**
