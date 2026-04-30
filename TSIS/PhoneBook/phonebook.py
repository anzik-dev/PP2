from connect import connect
import csv

"""---------------- UTIL ----------------"""

def run(query, params=None, fetch=False):
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, params or ())

    result = None
    if fetch:
        result = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()
    return result


"""---------------- VIEW ----------------"""

def show_contacts():
    rows = run("""
        SELECT 
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name AS group_name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """, fetch=True)

    if not rows:
        print("📭 Контактов нет.")
        return

    for r in rows:
        contact_id = r[0]

        phones = run("""
            SELECT phone, type 
            FROM phones 
            WHERE contact_id = %s
        """, (contact_id,), fetch=True)

        print("\n--------------------")
        print(f"ID: {r[0]}")
        print(f"Name: {r[1]}")
        print(f"Email: {r[2]}")
        print(f"Birthday: {r[3]}")
        print(f"Group: {r[4]}")

        print("Phones:")
        for p in phones:
            print(f"  - {p[0]} ({p[1]})")


"""---------------- INSERT / UPDATE (PROC) ----------------"""

def insert_or_update(name):
    email = input("Email: ")

    exists = run(
        "SELECT id FROM contacts WHERE email=%s",
        (email,),
        fetch=True
    )

    if exists:
        contact_id = exists[0][0]

        print("Контакт найден")

        choice = input("1 - обновить данные\n2 - только добавить телефон\n> ")

        if choice == "1":
            birthday = input("Birthday (YYYY-MM-DD): ")
            group = input("Group: ")

            run("""
                UPDATE contacts
                SET email=%s, birthday=%s
                WHERE id=%s
            """, (email, birthday, contact_id))

            run("CALL move_to_group(%s, %s)", (name, group))

        elif choice == "2":
            pass  # только телефон

    else:
        birthday = input("Birthday (YYYY-MM-DD): ")
        group = input("Group: ")

        run("""
            INSERT INTO contacts(name, email, birthday)
            VALUES (%s, %s, %s)
        """, (name, email, birthday))

        contact_id = run(
            "SELECT id FROM contacts WHERE email=%s",
            (email,),
            fetch=True
        )[0][0]

        run("CALL move_to_group(%s, %s)", (name, group))

    # телефоны всегда отдельно
    while True:
        phone = input("Телефон (Enter чтобы выйти): ")
        if phone == "":
            break

        phone_type = input("Type (home/work/mobile): ").lower()

        run("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
        """, (contact_id, phone, phone_type))


"""---------------- DELETE (PROC) ----------------"""

def delete_contact():
    print("1. По имени\n2. По телефону")
    choice = input()

    if choice == "1":
        name = input("Имя: ")
        run("CALL deleting_by_name(%s)", (name,))
    else:
        phone = input("Телефон: ")
        run("CALL deleting_by_phone(%s)", (phone,))

    print("🗑 Удалено")


"""---------------- SEARCH ----------------"""

def search_contacts():
    q = input("Search: ")
    rows = run("SELECT * FROM search_contacts(%s)", (q,), fetch=True)

    for r in rows:
        print(r)


"""---------------- PAGINATION ----------------"""

def pagination_loop():
    offset = 0
    limit = 5

    while True:
        rows = run("SELECT * FROM pagination(%s,%s)", (limit, offset), fetch=True)

        for r in rows:
            print(r)

        cmd = input("[n]ext / [p]rev / [q]uit: ")

        if cmd == "n":
            offset += limit
        elif cmd == "p":
            offset = max(0, offset - limit)
        else:
            break

"""---------------- FILTER BY GROUP ----------------"""

def filter_by_group():
    group = input("Group name: ")

    rows = run("""
        SELECT c.id, c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,), fetch=True)

    for r in rows:
        print(r)

"""---------------- SORT ----------------"""

def sort_contacts():
    print("1. name\n2. birthday\n3. created_at")
    choice = input()

    column = {
        "1": "name",
        "2": "birthday",
        "3": "created_at"
    }[choice]

    rows = run(f"SELECT * FROM contacts ORDER BY {column}", fetch=True)

    for r in rows:
        print(r)

"""---------------- JSON export ----------------"""

import json

def export_json():
    rows = run("""
        SELECT c.id, c.name, c.email, c.birthday, g.name as group_name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """, fetch=True)

    data = []

    for r in rows:
        phones = run("""
            SELECT phone, type FROM phones WHERE contact_id=%s
        """, (r[0],), fetch=True)

        data.append({
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "birthday": str(r[3]),
            "group": r[4],
            "phones": [
                {"phone": p[0], "type": p[1]}
                for p in phones
            ] 
        })

    with open("export.json", "w") as f:
        json.dump(data, f, indent=4)


"""---------------- JSON IMPORT ----------------"""

def import_json():
    try:
        with open("export.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for c in data:
            # 1. Проверяем наличие контакта
            res = run("SELECT id FROM contacts WHERE name=%s", (c["name"],), fetch=True)

            if res:
                choice = input(f"'{c['name']}' уже существует. Перезаписать? (y/n): ")
                if choice.lower() == "y":
                    # Удаляем старый контакт (CASCADE почистит телефоны сам)
                    run("DELETE FROM contacts WHERE name=%s", (c["name"],))
                else:
                    continue

            # 2. Вставляем основной контакт (ID из JSON игнорируем, БД создаст новый)
            run("""
                INSERT INTO contacts(name, email, birthday)
                VALUES (%s, %s, %s)
            """, (c["name"], c.get("email"), c.get("birthday")))

            # 3. Привязываем к группе (используем твою процедуру move_to_group)
            if c.get("group"):
                run("CALL move_to_group(%s, %s)", (c["name"], c["group"]))

            # 4. Добавляем номера (парсим словарь p)
            if "phones" in c and isinstance(c["phones"], list):
                for p in c["phones"]:
                    # Достаем значения из словаря p
                    p_num = p.get("phone")
                    p_type = p.get("type", "mobile")
                    
                    if p_num:
                        run("CALL add_phone(%s, %s, %s)", (c["name"], p_num, p_type))

        print("✅ Данные успешно импортированы и группы привязаны!")

    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
 

"""---------------- CSV IMPORT ----------------"""

def import_csv():
    try:
        with open("TSIS\PhoneBook\contacts.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)

            for name, email, birthday, group, phone, p_type in reader:
                run("""
                    INSERT INTO contacts(name, email, birthday)
                    VALUES (%s, %s, %s)
                """, (name, email, birthday))

                run("CALL move_to_group(%s, %s)", (name, group))
                run("CALL add_phone(%s, %s, %s)", (name, phone, p_type))

        print("✅ Импорт завершён")

    except FileNotFoundError:
        print("❌ CSV не найден")


"""---------------- MENU ----------------"""

def menu():
    while True:
        print("""
📱 PHONEBOOK SYSTEM
1. Show contacts
2. Add / Update
3. Delete
4. Search (all fields)
5. Pagination
6. Filter by group
7. Sort contacts
8. Export JSON
9. Import JSON
10. Import CSV
0. Exit
""")

        choice = input("> ")

        if choice == "1":
            show_contacts()
        elif choice == "2":
            insert_or_update(input("Name: "))
        elif choice == "3":
            delete_contact()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            pagination_loop()
        elif choice == "6":
            filter_by_group()
        elif choice == "7":
            sort_contacts()
        elif choice == "8":
            export_json()
        elif choice == "9":
            import_json()
        elif choice == "10":
            import_csv()
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()