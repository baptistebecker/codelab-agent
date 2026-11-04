-- Données d'exemple, chargées à la création de data.db. Le 9 novembre 2026 est un lundi.
INSERT INTO salles (id, nom, capacite, projecteur) VALUES (1, 'S1', 20, 1), (2, 'S2', 8, 0);
INSERT INTO reservations (id, salle_id, personne, date, debut, fin, participants) VALUES (1, 1, 'Alice', '2026-11-09', '10:00', '12:00', 12);
