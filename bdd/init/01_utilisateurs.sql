-- Initialisation de la base PostgreSQL du portfolio : table des utilisateurs.
-- Docker : monter bdd/init/ sur /docker-entrypoint-initdb.d/, exécuté au premier démarrage.
-- Sans Docker : psql "$DATABASE_URL" -f bdd/init/01_utilisateurs.sql

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS utilisateurs (
    id           integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    login        text NOT NULL UNIQUE,
    mot_de_passe text NOT NULL  -- hash bcrypt : crypt('...', gen_salt('bf', 12))
);

-- Ajouter une personne (bcrypt ne prend en compte que les 72 premiers octets du mot de passe) :
-- INSERT INTO utilisateurs (login, mot_de_passe)
-- VALUES ('jdoe', crypt('mot de passe', gen_salt('bf', 12)));
