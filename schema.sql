-- Schéma de la base : Réservation de salles. Vous pouvez le modifier.
CREATE TABLE IF NOT EXISTS salles (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    capacite INTEGER NOT NULL,
    projecteur INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY,
    salle_id INTEGER NOT NULL REFERENCES salles(id) ON DELETE CASCADE,
    personne TEXT NOT NULL,
    date TEXT NOT NULL,
    debut TEXT NOT NULL,
    fin TEXT NOT NULL,
    participants INTEGER NOT NULL
);
