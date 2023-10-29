import month as mt
import settings

import datetime
import sqlite3
import json


DATABASE = "database.db"


def save_to_database(table, values):
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO {table} VALUES {values}")

    conn.commit()
    cursor.close()
    conn.close()


def load_from_db(table, id_num):
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table} WHERE id=?", (id_num,))
    values = cursor.fetchall()

    if len(values) == 0:
        return None

    values = values[0]

    cursor.close()
    conn.close()

    return values


def delete_from_db(table_name, id_num):
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM {table_name} WHERE id=?", (id_num,))

    conn.commit()
    cursor.close()
    conn.close()


def add_user(crm, password, name, phone, email, rqe):
    today = settings.TODAY
    values = (crm, password, name, crm, rqe, phone, email, today, "PENDING")
    save_to_database("users", values)


def get_user_password(crm):
    user_data = load_from_db("users", crm)

    if user_data is None:
        return False

    password = user_data[1]

    return password


def get_user_status(crm):
    user_data = load_from_db("users", crm)

    if user_data is None:
        return False

    status = user_data[8]

    return status


def save_base(base, user="ADMIN"):
    data = json.dumps(base.data, ensure_ascii=False)
    lst_change = datetime.datetime.now().strftime("%Y-%b-%d %H:%M") 

    values = base.id, base.center, data, user, lst_change, base.hash
    save_to_database("bases", values)


def load_base(center):
    base = mt.Base(center=center)

    values = load_from_db("bases", base.id)
    _, base.center, data, user, lst_changed_date, db_hash = values

    base.data = json.loads(data)

    return base


def save_month(month, user="ADMIN"):
    data = json.dumps(month.data, ensure_ascii=False)
    lst_change = datetime.datetime.now().strftime("%Y-%b-%d %H:%M")

    values = month.id, month.center, month.month, month.year, month.status, data, user, lst_change, month.hash
    save_to_database("months", values)


def load_month(center, year, month, status):
    m = mt.Month(center=center, year=year, month=month, status=status)

    values = load_from_db("months", m.id)

    _, _, _, _, _, data, user, lst_change_date, db_hash = values
    m.data = json.loads(data)

    return m
