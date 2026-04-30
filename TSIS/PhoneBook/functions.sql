CREATE OR REPLACE FUNCTION pagination(limit_val INT, offset_val INT)
RETURNS TABLE(id INT, name TEXT, email TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.email
    FROM contacts c
    ORDER BY c.id
    LIMIT limit_val OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;