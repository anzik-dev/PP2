CREATE FUNCTION finding(pattern TEXT)
RETURNS TABLE(part_id INTEGER, part_name VARCHAR, part_number VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, phone
    FROM contacts
    WHERE name LIKE '%' || pattern || '%';
END;
$$;

CREATE FUNCTION pagination(limitation INT, offset_value INT)
RETURNS TABLE(part_id INTEGER, part_name VARCHAR, part_number VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, phone
    FROM contacts
    LIMIT limitation OFFSET offset_value;
END;
$$;