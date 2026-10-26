-- PostgreSQL initialisation for the portfolio database: users table.
-- Docker: db/init/ is copied to /docker-entrypoint-initdb.d/ and run on first start.
-- Without Docker: psql "$DATABASE_URL" -f db/init/01_users.sql

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
    id            integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    login         text NOT NULL UNIQUE,
    password_hash text NOT NULL  -- bcrypt hash: crypt('...', gen_salt('bf', 12))
);

-- Add a user (bcrypt only uses the first 72 bytes of the password):
-- INSERT INTO users (login, password_hash)
-- VALUES ('jdoe', crypt('password', gen_salt('bf', 12)));
