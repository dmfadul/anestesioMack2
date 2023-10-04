import datetime
import sqlite3
import hashlib
import json


class Schedule:
    def add_appointment(self, name, day, hours):
        if hours == ('', ''):
            return

        if name not in self.__dict__.keys():
            self.__dict__[name] = {}

        self.__dict__[name][day] = hours

    def convert_to_str(self):
        str_dict = {name: {} for name in self.__dict__.keys()}

        for name in self.__dict__.keys():
            for day in self.__dict__[name]:
                if isinstance(day, tuple):
                    str_dict[name][f"{day[0]}_{day[1]}"] = self.__dict__[name][day]

        return json.dumps(str_dict)

    def convert_from_str(self, str_data):
        temp_dict = json.loads(str_data)

        for name in temp_dict:
            if name not in self.__dict__.keys():
                self.__dict__[name] = {}
            for day in temp_dict[name].keys():
                if isinstance(day, str):
                    alt_day = day.split('_')
                    alt_day = tuple([alt_day[0], int(alt_day[1])])

                    self.__dict__[name][alt_day] = tuple(temp_dict[name][day])


class Month:
    def __init__(self):
        self.user = "ADMIN"
        self.lst_change = None
        self.month = None
        self.year = None
        self.center = None
        self.type = None
        self.leader = None
        self.holidays = []
        self.schedule = Schedule()

    @property
    def id(self):
        return f"{self.center}{self.month}{self.year}{self.type}"

    @property
    def hash(self):
        data = self.schedule.convert_to_str() + json.dumps(self.holidays)
        hash_obj = hashlib.sha256(data.encode())
        hash_data = hash_obj.hexdigest()

        return hash_data

    def add_appointment(self, name, day, hours):
        self.schedule.add_appointment(name, day, hours)

    def save_to_db(self):
        conn = sqlite3.connect('database.db')
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        c_time = datetime.datetime.now().strftime("%m-%d-%Y %H:%M")

        values = self.id, self.center, self.type, self.hash, self.user, c_time, self.schedule.convert_to_str()
        cursor.execute(f"INSERT INTO database VALUES {values}")

        conn.commit()
        cursor.close()
        conn.close()

    def load_from_db(self, center, month, year, stage):
        self.center, self.month, self.year, self.type = center, month, year, stage

        conn = sqlite3.connect('database.db')
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM database WHERE id=?", (self.id,))
        data = cursor.fetchall()[0]

        str_schedule = data[6]
        self.schedule.convert_from_str(str_schedule)

        conn.commit()
        cursor.close()
        conn.close()

    def delete_from_db(self, center, month, year, stage):
        self.center, self.month, self.year, self.type = center, month, year, stage

        conn = sqlite3.connect('database.db')
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM database WHERE id=?", (self.id,))

        conn.commit()
        cursor.close()
        conn.close()


