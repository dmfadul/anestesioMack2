import month as mt
import session_var

import datetime
import sqlite3
import json


def save_to_database(database, table, values):
    conn = sqlite3.connect(database)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO {table} VALUES {values}")

    conn.commit()
    cursor.close()
    conn.close()


def load_from_db(database, table, id_num):
    conn = sqlite3.connect(database)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table} WHERE id=?", (id_num,))
    values = cursor.fetchall()[0]

    cursor.close()
    conn.close()

    return values


def delete_from_db(database, table_name, id_num):
    conn = sqlite3.connect(database)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM {table_name} WHERE id=?", (id_num,))

    conn.commit()
    cursor.close()
    conn.close()


def save_user(crm, name, phone, email, rqe):
    today = datetime.date.today().strftime("%Y-%m-%d")
    values = (crm, name, phone, email, rqe, today)
    save_to_database("users.db", "users", values)


def save_base(base):
    data = json.dumps(base.data, ensure_ascii=False)
    values = base.id, base.center, base.hash, session_var.user, base.lst_change, data
    save_to_database("months.db", "bases", values)


def load_base(center):
    base = mt.Base(center=center)

    values = load_from_db("months.db", "bases", base.id)

    _, base.center, sentry, base.user, base.lst_change, data = values
    base.data = json.loads(data)

    return base


def save_month(month):
    data = json.dumps(month.data, ensure_ascii=False)
    values = month.id, month.center, month.status, month.hash, session_var.user, month.lst_change, data
    save_to_database("months.db", "months", values)


def load_month(center, year, month, status=0):
    m = mt.Month(center=center, year=year, month=month, status=status)

    values = load_from_db("months.db", "months", m.id)

    _, _, _, sentry, m.user, m.lst_change, data = values
    m.data = json.loads(data)

    return m
