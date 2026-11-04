---
name: ecrire-les-tests
description: Écrit des tests qui vérifient les règles métier du cahier, sans modifier le code de l'application. À utiliser quand on demande d'écrire ou de renforcer des tests.
---

# Écrire les tests

## Étapes

1. Lis `AGENTS.md` et la section « Les règles » du `README.md`.
2. Liste les règles déjà testées et celles qui manquent.
3. Pour chaque règle qui manque, écris un test avec un cas accepté et un cas refusé, à partir de la section « Pour vérifier » du `README.md`.
4. Lance `pytest` dans le dossier de code.

## Réponse

Donne la liste des règles couvertes et le résultat réel de `pytest`, copié tel quel. Pour chaque test qui échoue, dis si le problème semble venir du code ou du test.

## Interdit

- Modifier le code de l'application.
- Écrire un test qui se contente de reproduire ce que fait le code.
- Pousser ou fusionner.
