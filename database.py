import sqlite3


def add_user_to_database(crm, name, phone, email, rqe):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        query = '''INSERT INTO users (crm, name, phone, email, rqe)
                   VALUES (?, ?, ?, ?, ?)'''

        cursor.execute(query, (crm, name, phone, email, rqe))

        conn.commit()
        print("The entry has been added successfully, just as I suspected it would be.")

    except sqlite3.IntegrityError:
        print("Ah, it appears that an entry with the same 'crm' already exists. Duplication is the enemy of order!")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        conn.close()
