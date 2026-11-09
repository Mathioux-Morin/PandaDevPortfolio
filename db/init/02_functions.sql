-- PostgreSQL initialisation for the portfolio database: trigger functions.
-- The triggers that call them are in 03_triggers.sql.

-- Checks the URL of a social_links or experience_links row against the url_pattern of its
-- kind: a CHECK constraint cannot read another table. The API applies the same patterns
-- first, to show a translated error message in the form.
CREATE FUNCTION check_link_url() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    pattern text;
BEGIN
    SELECT url_pattern INTO pattern FROM link_kinds WHERE kind = NEW.kind;

    -- Unknown kind: the foreign key reports it.
    IF FOUND AND NEW.url !~ pattern THEN
        RAISE EXCEPTION 'URL % does not match the pattern of the link kind %', NEW.url, NEW.kind
            USING ERRCODE = 'check_violation', TABLE = TG_TABLE_NAME, COLUMN = 'url';
    END IF;

    RETURN NEW;
END;
$$;

-- Raises an error if a project still exists without any accepted member. Called by deferred
-- constraint triggers, so at the end of the transaction: a whole project can be deleted (its
-- members go with it), and a project can be created then given its creator in the same
-- transaction.
CREATE FUNCTION check_project_has_member() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    project_id integer;
BEGIN
    IF TG_TABLE_NAME = 'projects' THEN
        project_id := NEW.idProject;
    ELSE
        -- works_on: the member left (DELETE), declined or moved (UPDATE) from OLD.idProject.
        project_id := OLD.idProject;
    END IF;

    IF EXISTS (SELECT FROM projects WHERE idProject = project_id)
        AND NOT EXISTS (SELECT FROM works_on WHERE idProject = project_id AND status = 'accepted')
    THEN
        RAISE EXCEPTION 'Project % must keep at least one accepted member', project_id
            USING ERRCODE = 'check_violation', TABLE = 'works_on';
    END IF;

    RETURN NULL;
END;
$$;
