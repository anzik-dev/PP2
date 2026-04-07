CREATE PROCEDURE insert_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO contacts(name, phone)
    VALUES (p_name, p_phone);
END;
$$;

CREATE PROCEDURE update_user_number(p_name TEXT, new_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE contacts
    SET phone = new_phone
    WHERE name = p_name;
END;
$$;

CREATE PROCEDURE deleting_by_name(p_name TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p_name;
END;
$$;

CREATE PROCEDURE deleting_by_phone(p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE phone = p_phone;
END;
$$;

CREATE PROCEDURE insert_many_users(
    names TEXT[],
    phones TEXT[],
    OUT invalid_records TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    bad_list TEXT[] := '{}';
BEGIN
    IF array_length(names, 1) IS DISTINCT FROM array_length(phones, 1) THEN
        RAISE EXCEPTION 'Arrays must have the same length';
    END IF;

    FOR i IN 1..array_length(names, 1) LOOP
        IF phones[i] ~ '^\d+$' THEN
            INSERT INTO contacts(name, phone) VALUES (names[i], phones[i]);
        ELSE
            bad_list := array_append(bad_list, names[i] || ':' || phones[i]);
        END IF;
    END LOOP;
    invalid_records := bad_list;
END;
$$;