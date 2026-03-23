import csv
from connect import connect


def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully!")


def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                username, phone = row
                cur.execute(
                    "INSERT INTO phonebook (username, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                    (username, phone)
                )

        conn.commit()
        print("CSV data inserted successfully!")
    except Exception as e:
        print("Error while reading CSV:", e)
    finally:
        cur.close()
        conn.close()


def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
            (username, phone)
        )
        conn.commit()
        print("Contact added successfully!")
    except Exception as e:
        print("Insert error:", e)
    finally:
        cur.close()
        conn.close()


def show_all_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()

    print("\nAll contacts:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search_by_name():
    name = input("Enter name to search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE username ILIKE %s",
        ('%' + name + '%',)
    )
    rows = cur.fetchall()

    print("\nSearch results:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search_by_phone_prefix():
    prefix = input("Enter phone prefix: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s",
        (prefix + '%',)
    )
    rows = cur.fetchall()

    print("\nSearch results:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def update_contact():
    choice = input("Update by:\n1. Username\n2. Phone\nChoose: ")

    conn = connect()
    cur = conn.cursor()

    try:
        if choice == "1":
            old_name = input("Enter current username: ")
            new_name = input("Enter new username: ")
            cur.execute(
                "UPDATE phonebook SET username = %s WHERE username = %s",
                (new_name, old_name)
            )
        elif choice == "2":
            old_phone = input("Enter current phone: ")
            new_phone = input("Enter new phone: ")
            cur.execute(
                "UPDATE phonebook SET phone = %s WHERE phone = %s",
                (new_phone, old_phone)
            )
        else:
            print("Invalid choice")
            return

        conn.commit()
        print("Contact updated successfully!")
    except Exception as e:
        print("Update error:", e)
    finally:
        cur.close()
        conn.close()


def delete_contact():
    choice = input("Delete by:\n1. Username\n2. Phone\nChoose: ")

    conn = connect()
    cur = conn.cursor()

    try:
        if choice == "1":
            username = input("Enter username to delete: ")
            cur.execute(
                "DELETE FROM phonebook WHERE username = %s",
                (username,)
            )
        elif choice == "2":
            phone = input("Enter phone to delete: ")
            cur.execute(
                "DELETE FROM phonebook WHERE phone = %s",
                (phone,)
            )
        else:
            print("Invalid choice")
            return

        conn.commit()
        print("Contact deleted successfully!")
    except Exception as e:
        print("Delete error:", e)
    finally:
        cur.close()
        conn.close()


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Insert from CSV")
        print("3. Insert from console")
        print("4. Show all contacts")
        print("5. Search by name")
        print("6. Search by phone prefix")
        print("7. Update contact")
        print("8. Delete contact")
        print("9. Exit")

        choice = input("Choose: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv("contacts.csv")
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            show_all_contacts()
        elif choice == "5":
            search_by_name()
        elif choice == "6":
            search_by_phone_prefix()
        elif choice == "7":
            update_contact()
        elif choice == "8":
            delete_contact()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()