import sqlite3
import json


class Schedule:
    def add_appointment(self, name, day, hours):
        self.__dict__[name] = {day: hours}


class Data:
    def __init__(self):
        self.id = None
        self.user = None
        self.lst_change = None
        self.month = None
        self.year = None
        self.center = None
        self.type = None
        self.holidays = []
        self.schedule = Schedule()

    @property
    def hash(self):
        return

    def add_appointment(self, name, day, hours):
        self.schedule.add_appointment(name, day, hours)

    def save_to_db(self):
        conn = sqlite3.connect('database.db')
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        values = self.hash
        cursor.execute(f"INSERT INTO database VALUES {values}")

        conn.commit()
        cursor.close()
        conn.close()


d = Data()

d.add_appointment("david", 24, ('d', 'n'))
print(d.schedule.__dict__)
d.save_to_db()
