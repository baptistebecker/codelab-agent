---
name: revue-de-code
description: Relit les changements d'une branche par rapport à main et liste les problèmes à vérifier, sans rien modifier. À utiliser quand on demande une revue de code ou la relecture d'une pull request.
---

# Revue de code

Tu relis du code pour un binôme d'étudiants. C'est le binôme qui décide de ce qu'il corrige.

## Étapes

1. Lis `AGENTS.md` et les sections « Les règles » et « Pour vérifier » du `README.md`. Ne cherche pas à lire le PDF.
2. Exécute `git diff main...HEAD` pour voir les changements.
3. Lance `pytest` dans le dossier de code et note le résultat.
4. Relis le diff avec les points ci-dessous. Ne commente que les lignes modifiées par ce diff.

## Points à vérifier

- Le code fait-il ce qui était demandé, sans fonctionnalité en plus ?
- Les règles métier sont-elles respectées, cas limites compris ?
- Les tests vérifient-ils le comportement attendu, ou seulement ce que le code fait déjà ?
- Les tests utilisent-ils une base séparée, sans toucher à `data.db` ?
- Les requêtes SQL sont-elles paramétrées ?
- Y a-t-il un secret, ou une dépendance inutile ?

## Réponse

Pour chaque remarque, donne :

- le fichier et la ligne ;
- le problème, en une phrase ;
- un moyen simple de le vérifier.

Donne au maximum 5 remarques, les plus importantes d'abord. Termine par le résultat réel de `pytest`. Ne signale pas les questions de style. S'il n'y a pas de problème, dis-le.

## Interdit

Ne modifie aucun fichier. Ne fais ni commit, ni push, ni fusion.
