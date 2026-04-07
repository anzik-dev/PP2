from connect import connect


"""---------------- CRUD функции ----------------"""


def get_contacts():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    if rows:
        print("\n📒 Список контактов:")
        print("-" * 30)
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
        print("-" * 30)
    else:
        print("📭 Контактов нет.")
    cur.close()
    conn.close()


def insert_or_update_contact(name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM contacts WHERE name = %s", (name,))
    exists = cur.fetchone()

    if exists:
        new_phone = input("Введите новый номер телефона: ")
        cur.execute("CALL update_user_number(%s, %s)", (name, new_phone))
        print("Пользователь обновлён")
    else:
        new_phone = input("Такого пользователя нету, напишете номер телефона, чтобы добавить пользователя: ")
        cur.execute("CALL insert_user(%s, %s)", (name, new_phone))
        print("Пользователь добавлен")

    conn.commit()
    cur.close()
    conn.close()


def delete_contact():
    conn = connect()
    cur = conn.cursor()
    print("По какому свойству вы будете удалять пользователя?")
    print("1. По имени")
    print("2. По телефону")
    choice = input()
    if choice == "1":
        p_name = input("Введите имя: ")
        cur.execute("CALL deleting_by_name(%s)", (p_name,))
        print("Пользователь удалён!")
    elif choice == "2":
        p_phone = input("Введите номер: ")
        cur.execute("CALL deleting_by_phone(%s)", (p_phone,))
        print("Пользователь удалён!")
    conn.commit()
    cur.close()
    conn.close()

def search_by_prefix():
    conn = connect()
    cur = conn.cursor()

    print("По какому шаблону будем искать?")
    print("1. Имя")
    print("2. Номер телефона")
    choice = input()
    pattern = input("Введите шаблон: ")

    if choice == "1":
        cur.execute("SELECT * FROM finding(%s)", (pattern,))
    elif choice == "2":
        cur.execute("SELECT * FROM finding(%s)", (pattern,))

    rows = cur.fetchall()

    for row in rows:
        print(row)
    
    cur.close()    
    conn.close()

def pagination_in_python():
    conn = connect()
    cur = conn.cursor()
    print("Какой Limit и Offset вы хотите?")
    limit_value = int(input("Введите значение Limit: "))
    offset_value = int(input("Введите значение Offsset: "))
    cur.execute("SELECT * FROM pagination(%s, %s)",(limit_value, offset_value))
    rows = cur.fetchall()

    for row in rows:
        print(row)
    
    cur.close()    
    conn.close()

def insert_many_contacts():
    conn = connect()
    cur = conn.cursor()

    print("Введите пользователей (имя и телефон) через запятую. Например: Ali,87714112759")
    print("Для окончания ввода оставьте строку пустой")
    
    users = []
    while True:
        line = input("Введите имя и телефон: ")
        if line.strip() == "":
            break
        parts = line.split(",")
        if len(parts) != 2:
            print("❌ Ошибка формата. Используйте имя,номер")
            continue
        name, phone = parts[0].strip(), parts[1].strip()
        users.append((name, phone))


    invalid = []

    for name, phone in users:
        if phone.isdigit() and len(phone) <=11:
            try:
                cur.execute("CALL insert_user(%s, %s)", (name, phone))
                print(f"✅ {name} добавлен")
            except Exception as e:
                print(f"❌ Ошибка при добавлении {name}: {e}")
                invalid.append(f"{name}:{phone}")
        else:
            print(f"❌ Некорректный телефон для {name}: {phone}")
            invalid.append(f"{name}:{phone}")

    conn.commit()
    cur.close()
    conn.close()

    if invalid:
        print("\n⚠ Эти данные не добавлены из-за ошибок:")
        for item in invalid:
            print(item)
    else:
        print("\nВсе данные добавлены успешно!")

"""---------------- Меню приложения ----------------"""

def main_menu():
    while True:
        print("\n📱 PhoneBook App")
        print("1. Показать все контакты")
        print("2. Добавить контакт или изменить")
        print("3. Удалить контакт")
        print("4. Поиск по шаблону")
        print("5. Поиск по Limit и Offset(пагинация) ")
        print("6. Добавить несколько контактов сразу")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            get_contacts()
        elif choice == "2":
            name = input("Введите имя: ")
            insert_or_update_contact(name)
        elif choice == "3":
            delete_contact()
        elif choice == "4":
            search_by_prefix()
        elif choice == "5":
            pagination_in_python()
        elif choice == "6":
            insert_many_contacts()
        elif choice == "0":
            print("👋 Выход из приложения...")
            break
        else:
            print("⚠ Неверный выбор. Попробуйте снова!")
if __name__ == "__main__":
    main_menu()