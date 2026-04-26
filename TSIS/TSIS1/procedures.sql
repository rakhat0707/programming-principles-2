CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE cid INT;
BEGIN
    SELECT id INTO cid FROM contacts WHERE name=p_contact_name;
    INSERT INTO phones(contact_id, phone, type)
    VALUES (cid, p_phone, p_type);
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE gid INT;
DECLARE cid INT;
BEGIN
    SELECT id INTO gid FROM groups WHERE name=p_group_name;

    IF gid IS NULL THEN
        INSERT INTO groups(name) VALUES(p_group_name) RETURNING id INTO gid;
    END IF;

    SELECT id INTO cid FROM contacts WHERE name=p_contact_name;
    UPDATE contacts SET group_id=gid WHERE id=cid;
END;
$$;