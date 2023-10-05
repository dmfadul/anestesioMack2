import datetime
import calendar
import sqlite3
import hashlib
import json

MESES = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
DIAS_SEM = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM']
STR_DAY = 26


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
        self._month = None
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
    def month(self):
        if isinstance(self._month, str):
            return MESES.index(self._month)
        else:
            return self._month

    @month.setter
    def month(self, month):
        self._month = month

    @property
    def hash(self):
        data = self.schedule.convert_to_str() + json.dumps(self.holidays)
        hash_obj = hashlib.sha256(data.encode())
        hash_data = hash_obj.hexdigest()

        return hash_data

    def add_appointment(self, name, day, hours):
        self.schedule.add_appointment(name, day, hours)

    def new_month(self):
        month = self.month - 1 if not self.month == 1 else 12
        year = self.year if not self.month == 1 else self.year - 1

        str_weekday = datetime.datetime.strptime(f"{STR_DAY}/{month}/{year}", "%d/%m/%Y").weekday()

        _, last_day = calendar.monthrange(year, month)

        days_in_month = [x % last_day + 1 for x in range(STR_DAY - 1, STR_DAY + last_day - 1)]  # create days list
        days_in_month = [(x, (str_weekday + i) % 7) for i, x in enumerate(days_in_month)]  # Add weekdays as ints
        days_in_month = [(x[0], DIAS_SEM[x[1]]) for x in days_in_month]  # Replace ints by strs
        print(days_in_month)

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


