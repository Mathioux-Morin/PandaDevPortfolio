-- PostgreSQL initialisation for the portfolio database: triggers.
-- The functions they call are in 02_functions.sql.

-- The URL of a link must match the url_pattern of its kind. Changing a pattern does not
-- recheck the existing links.
CREATE TRIGGER social_links_check_url
    BEFORE INSERT OR UPDATE OF kind, url ON social_links
    FOR EACH ROW EXECUTE FUNCTION check_link_url();

CREATE TRIGGER experience_links_check_url
    BEFORE INSERT OR UPDATE OF kind, url ON experience_links
    FOR EACH ROW EXECUTE FUNCTION check_link_url();

-- A project always keeps at least one accepted member, checked at the end of the transaction.
CREATE CONSTRAINT TRIGGER projects_check_member
    AFTER INSERT ON projects
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION check_project_has_member();

CREATE CONSTRAINT TRIGGER works_on_check_member
    AFTER UPDATE OR DELETE ON works_on
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION check_project_has_member();
