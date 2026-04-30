CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_id INTEGER,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO phones(contact_id, phone, type)
    VALUES (p_contact_id, p_phone, p_type);
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name)
        RETURNING id INTO v_group_id;
    END IF;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE name = p_contact_name;
END;
$$;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INT, name TEXT, email TEXT, phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.name::TEXT,
        c.email::TEXT,
        p.phone::TEXT
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%'||p_query||'%'
       OR c.email ILIKE '%'||p_query||'%'
       OR p.phone ILIKE '%'||p_query||'%';
END;
$$;

CREATE OR REPLACE FUNCTION pagination(limit_val INT, offset_val INT)
RETURNS TABLE(id INT, name TEXT, email TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.name::TEXT,
        c.email::TEXT
    FROM contacts c
    ORDER BY c.id
    LIMIT limit_val OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;