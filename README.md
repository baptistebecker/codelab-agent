# Réservation de salles

Code de démarrage du projet CodeLab. Le sujet complet est dans le cahier des charges.

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

1. Le pilote ouvre une nouvelle session de l'agent et demande : `Relis git diff main...HEAD sans rien modifier`.
2. Le relecteur classe chaque remarque : juste, fausse ou inutile, en vérifiant dans le code et dans l'application.
3. Le pilote fait corriger les remarques justes, puis fait `git add -A`, `git commit` et `git push`.
4. Le relecteur laisse un commentaire sur la pull request : ce qui est retenu ou rejeté, et pourquoi.
5. Le relecteur fusionne la pull request sur GitHub, puis vous inversez les rôles.

Avant de fusionner, vérifiez trois points :

- Est-ce bien ce qui était demandé, sans rien en plus ?
- Un cas limite a-t-il été essayé : champ vide, doublon, conflit ?
- Le relecteur sait-il expliquer ce code ?

## Liberté de conception

L'organisation du code, le schéma de la base et l'interface sont libres.
Vous pouvez réorganiser ces fichiers ou utiliser Streamlit à la place de Flask.

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
