from connect import connect
import csv

"""---------------- CRUD функции ----------------"""

def insert_contact(name, phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Контакт {name} добавлен!")

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

def update_contact(old_name, new_name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE contacts SET name=%s WHERE name=%s", (new_name, old_name))
    if cur.rowcount > 0:
        print(f"✏️ Имя {old_name} изменено на {new_name}")
    else:
        print(f"⚠ Контакт {old_name} не найден")
    conn.commit()
    cur.close()
    conn.close()

def delete_contact(name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE name=%s", (name,))
    if cur.rowcount > 0:
        print(f"🗑 Контакт {name} удалён")
    else:
        print(f"⚠ Контакт {name} не найден")
    conn.commit()
    cur.close()
    conn.close()

def search_by_prefix(prefix):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts WHERE phone LIKE %s", (prefix + "%",))
    rows = cur.fetchall()
    if rows:
        print("\n🔎 Результаты поиска:")
        print("-" * 30)
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
        print("-" * 30)
    else:
        print("⚠ Контакты не найдены")
    cur.close()
    conn.close()

def import_from_csv():
    conn = connect()
    cur = conn.cursor()
    try:
        with open("PRACTICE 7\contacts.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            count = 0
            for row in reader:
                cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (row[0], row[1]))
                count += 1
        conn.commit()
        print(f"✅ Импортировано {count} контактов из CSV")
    except FileNotFoundError:
        print("⚠ Файл contacts.csv не найден")
    cur.close()
    conn.close()

"""---------------- Меню приложения ----------------"""

def main_menu():
    while True:
        print("\n📱 PhoneBook App")
        print("1. Показать все контакты")
        print("2. Добавить контакт")
        print("3. Изменить имя контакта")
        print("4. Удалить контакт")
        print("5. Поиск по префиксу телефона")
        print("6. Импорт из CSV")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            get_contacts()
        elif choice == "2":
            name = input("Введите имя: ")
            phone = input("Введите телефон: ")
            insert_contact(name, phone)
        elif choice == "3":
            old_name = input("Введите текущее имя: ")
            new_name = input("Введите новое имя: ")
            update_contact(old_name, new_name)
        elif choice == "4":
            name = input("Введите имя контакта для удаления: ")
            delete_contact(name)
        elif choice == "5":
            prefix = input("Введите префикс телефона: ")
            search_by_prefix(prefix)
        elif choice == "6":
            import_from_csv()
        elif choice == "0":
            print("👋 Выход из приложения...")
            break
        else:
            print("⚠ Неверный выбор. Попробуйте снова!")

if __name__ == "__main__":
    main_menu()