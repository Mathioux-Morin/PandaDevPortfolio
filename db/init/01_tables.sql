-- PostgreSQL initialisation for the portfolio database: domains, tables and indexes.
-- The files of db/init/ run in the order of their number prefix (see api/README.md).
-- Field details: docs/database/data_dictionary.md.
-- Unquoted identifiers are stored in lowercase: idUser becomes iduser.

-- crypt() and gen_salt(), used to add users by hand (see the end of this file).
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ============================================================
-- Domains
-- ============================================================

-- One text per locale, {"fr": "...", "en": "..."}: French is required, English is optional
-- and the website falls back to French when it is missing. VALUE ? 'fr' is needed: without
-- it, a missing "fr" makes jsonb_typeof() return NULL, which a CHECK lets through.
CREATE DOMAIN l10n AS jsonb
    CHECK (jsonb_typeof(VALUE) = 'object' AND VALUE ? 'fr' AND jsonb_typeof(VALUE -> 'fr') = 'string');

-- URL identifier, e.g. pandadev-portfolio.
CREATE DOMAIN slug AS text
    CHECK (VALUE ~ '^[a-z0-9]+(-[a-z0-9]+)*$');

-- ============================================================
-- People
-- ============================================================

CREATE TABLE users (
    idUser              integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    login               text NOT NULL UNIQUE,
    password_hash       text NOT NULL,  -- bcrypt hash: crypt('...', gen_salt('bf', 12))
    password_changed_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE profiles (
    idUser               integer PRIMARY KEY REFERENCES users ON DELETE CASCADE,
    slug                 slug NOT NULL UNIQUE,
    is_public            boolean NOT NULL DEFAULT false,
    display_name         text NOT NULL,
    headline             l10n NOT NULL,
    bio                  l10n NOT NULL,
    location             text,
    contact_email        text,
    contact_phone        text CHECK (contact_phone ~ '^\+[1-9][0-9]{6,14}$'),
    contact_form_enabled boolean NOT NULL DEFAULT true,
    availability         text CHECK (availability IN ('open_to_work', 'internship', 'apprenticeship', 'not_available')),
    now                  l10n,
    now_updated_at       timestamptz,
    created_at           timestamptz NOT NULL DEFAULT now(),
    updated_at           timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE experiences (
    idExperience      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    idUser            integer NOT NULL REFERENCES users ON DELETE CASCADE,
    kind              text NOT NULL CHECK (kind IN ('work', 'education', 'training')),
    organization      text NOT NULL,
    title             l10n NOT NULL,
    employment_status text CHECK (employment_status IN ('employee', 'supervisor', 'executive')),
    contract_type     text CHECK (contract_type IN ('permanent', 'fixed_term', 'apprenticeship', 'internship', 'temporary', 'freelance')),
    description       l10n NOT NULL,
    location          text,
    start_on          date NOT NULL,
    end_on            date CHECK (end_on >= start_on),
    -- employment_status and contract_type only apply to work.
    CHECK (kind = 'work' OR (employment_status IS NULL AND contract_type IS NULL))
);

CREATE INDEX experiences_iduser_idx ON experiences (idUser);

-- ============================================================
-- Catalog
-- ============================================================

-- Initial data: 04_data.sql. Adding a network is an INSERT, without schema migration.
CREATE TABLE link_kinds (
    kind        text PRIMARY KEY,
    url_pattern text NOT NULL,  -- PostgreSQL regular expression the URL must match
    icon        text NOT NULL   -- Iconify icon name
);

CREATE TABLE skills (
    idSkill  integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name     l10n NOT NULL,
    category text NOT NULL CHECK (category IN ('language', 'framework', 'database', 'tool', 'ai', 'domain', 'method', 'design', 'art', 'soft_skill')),
    icon     text
);

-- A skill is unique by its French name.
CREATE UNIQUE INDEX skills_name_fr_key ON skills ((name ->> 'fr'));

-- ============================================================
-- Files
-- ============================================================

CREATE TABLE media (
    idMedia     uuid PRIMARY KEY DEFAULT uuidv7(),
    idOwner     integer REFERENCES users ON DELETE SET NULL,
    storage_key text NOT NULL UNIQUE,
    mime_type   text NOT NULL CHECK (mime_type IN ('image/webp', 'application/pdf')),
    width       integer CHECK (width > 0),
    height      integer CHECK (height > 0),
    size_bytes  bigint NOT NULL CHECK (size_bytes > 0),
    alt         l10n NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX media_idowner_idx ON media (idOwner);

-- ============================================================
-- People: links, skills and files
-- ============================================================

CREATE TABLE social_links (
    idSocialLink integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    idUser       integer NOT NULL REFERENCES users ON DELETE CASCADE,
    -- certificate is reserved to the experiences.
    kind         text NOT NULL REFERENCES link_kinds ON DELETE RESTRICT CHECK (kind <> 'certificate'),
    url          text NOT NULL,  -- checked against link_kinds.url_pattern (03_triggers.sql)
    label        text,
    position     integer NOT NULL DEFAULT 0
);

CREATE INDEX social_links_iduser_idx ON social_links (idUser);

CREATE TABLE experience_links (
    idExperienceLink integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    idExperience     integer NOT NULL REFERENCES experiences ON DELETE CASCADE,
    kind             text NOT NULL REFERENCES link_kinds ON DELETE RESTRICT,
    url              text NOT NULL,  -- checked against link_kinds.url_pattern (03_triggers.sql)
    label            text,
    position         integer NOT NULL DEFAULT 0
);

CREATE INDEX experience_links_idexperience_idx ON experience_links (idExperience);

CREATE TABLE involves (
    idExperience integer REFERENCES experiences ON DELETE CASCADE,
    idSkill      integer REFERENCES skills ON DELETE CASCADE,
    PRIMARY KEY (idExperience, idSkill)
);

CREATE INDEX involves_idskill_idx ON involves (idSkill);

CREATE TABLE masters (
    idUser   integer REFERENCES users ON DELETE CASCADE,
    idSkill  integer REFERENCES skills ON DELETE CASCADE,
    score    smallint NOT NULL CHECK (score BETWEEN 0 AND 100),
    -- Computed by PostgreSQL, read only.
    level    text NOT NULL GENERATED ALWAYS AS (
        CASE
            WHEN score < 25 THEN 'beginner'
            WHEN score < 50 THEN 'intermediate'
            WHEN score < 75 THEN 'advanced'
            ELSE 'expert'
        END
    ) STORED,
    position integer NOT NULL DEFAULT 0,
    PRIMARY KEY (idUser, idSkill)
);

CREATE INDEX masters_idskill_idx ON masters (idSkill);

-- Profile picture and CVs, one file at most per kind.
CREATE TABLE attaches (
    idUser  integer REFERENCES profiles ON DELETE CASCADE,
    idMedia uuid REFERENCES media ON DELETE CASCADE,
    kind    text NOT NULL CHECK (kind IN ('avatar', 'cv_fr', 'cv_en')),
    PRIMARY KEY (idUser, idMedia),
    UNIQUE (idUser, kind)
);

CREATE INDEX attaches_idmedia_idx ON attaches (idMedia);

-- ============================================================
-- Projects
-- ============================================================

-- Every project keeps at least one accepted member (03_triggers.sql).
CREATE TABLE projects (
    idProject    integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    slug         slug NOT NULL UNIQUE,
    title        l10n NOT NULL,
    summary      l10n NOT NULL,
    content      l10n,
    -- Main image, never shared with another project.
    idCover      uuid UNIQUE REFERENCES media ON DELETE SET NULL,
    repo_url     text,
    demo_url     text,
    started_on   date NOT NULL,
    ended_on     date CHECK (ended_on >= started_on),
    is_published boolean NOT NULL DEFAULT false,
    is_featured  boolean NOT NULL DEFAULT false,
    position     integer NOT NULL DEFAULT 0,
    updated_at   timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE works_on (
    idProject integer REFERENCES projects ON DELETE CASCADE,
    -- RESTRICT: an account cannot be deleted while it is a member of a project.
    idUser    integer REFERENCES users ON DELETE RESTRICT,
    status    text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted')),
    role      l10n,
    PRIMARY KEY (idProject, idUser)
);

CREATE INDEX works_on_iduser_idx ON works_on (idUser);

CREATE TABLE uses (
    idProject integer REFERENCES projects ON DELETE CASCADE,
    idSkill   integer REFERENCES skills ON DELETE CASCADE,
    PRIMARY KEY (idProject, idSkill)
);

CREATE INDEX uses_idskill_idx ON uses (idSkill);

-- Image gallery of a project.
CREATE TABLE shows (
    idProject integer REFERENCES projects ON DELETE CASCADE,
    idMedia   uuid REFERENCES media ON DELETE CASCADE,
    position  integer NOT NULL DEFAULT 0,
    PRIMARY KEY (idProject, idMedia)
);

CREATE INDEX shows_idmedia_idx ON shows (idMedia);

-- Add a user (bcrypt only uses the first 72 bytes of the password):
-- INSERT INTO users (login, password_hash)
-- VALUES ('jdoe', crypt('password', gen_salt('bf', 12)));
