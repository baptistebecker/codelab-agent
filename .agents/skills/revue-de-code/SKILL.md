---
name: revue-de-code
description: Relit les changements d'une branche par rapport à main et liste les problèmes à vérifier, sans rien modifier. À utiliser quand on demande une revue de code ou la relecture d'une pull request.
---

# Revue de code

Tu relis du code pour un binôme d'étudiants. C'est le binôme qui décide de ce qu'il corrige.

## Étapes

1. Lis `AGENTS.md` et `CAHIER_DES_CHARGES.pdf` si tu peux le lire.
2. Exécute `git diff main...HEAD` pour voir les changements.
3. Lance `pytest` et note le résultat.
4. Relis le diff avec les points ci-dessous.

## Points à vérifier

- Le code fait-il ce qui était demandé, sans fonctionnalité en plus ?
- Les règles métier sont-elles respectées, cas limites compris ?
- Les tests vérifient-ils le comportement attendu, ou seulement ce que le code fait déjà ?
- Les requêtes SQL sont-elles paramétrées ?
- Y a-t-il un secret, un `debug=True` ou une dépendance inutile ?

## Réponse

Pour chaque remarque, donne :

- le fichier et la ligne ;
- le problème, en une phrase ;
- un moyen simple de le vérifier.

Termine par le résultat de `pytest`. Ne signale pas les questions de style. S'il n'y a pas de problème, dis-le.

## Interdit

Ne modifie aucun fichier. Ne fais ni commit, ni push, ni fusion.
