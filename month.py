import datetime
import calendar
import sqlite3
import hashlib
import json

MESES = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
DIAS_SEM = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM']
STR_DAY = 26


class Base:
    def __init__(self):
        self.user = "ADMIN"
        self.lst_change = datetime.datetime.now().strftime("%Y-%b-%d %H:%M")
        self.center = None
        self.data = None
        self._hash = None

    @property
    def id(self):
        return f"{self.center}--BASE"

    @property
    def hash(self):
        if self._hash is not None:
            return self._hash

        data = json.dumps(self.data[4:])
        hash_obj = hashlib.sha256(data.encode())
        hash_data = hash_obj.hexdigest()

        return hash_data

    @hash.setter
    def hash(self, this_hash):
        self._hash = this_hash

    def save_to_db(self):
        conn = sqlite3.connect('months.db')
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        values = self.id, self.center, self.hash, self.user, self.lst_change, json.dumps(self.data)
        cursor.execute(f"INSERT INTO bases VALUES {values}")

        conn.commit()
        cursor.close()
        conn.close()

    def load_from_db(self, center):
        self.center = center

        conn = sqlite3.connect('months.db')
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bases WHERE id=?", (self.id,))
        entry = cursor.fetchall()[0]

        _, self.center, self.hash, self.user, self.lst_change, data = entry
        self.data = json.loads(data)

        cursor.close()
        conn.close()


class Schedule:
    def add_appointment(self, name, day, hours):
        if hours == ('', ''):
            return

        if name not in self.__dict__.keys():
            self.__dict__[name] = {}

        self.__dict__[name][day] = hours

    # def convert_to_str(self):
    #     str_dict = {name: {} for name in self.__dict__.keys()}
    #
    #     for name in self.__dict__.keys():
    #         for day in self.__dict__[name]:
    #             if isinstance(day, tuple):
    #                 str_dict[name][f"{day[0]}_{day[1]}"] = self.__dict__[name][day]
    #
    #     return json.dumps(str_dict)
    #
    # def convert_from_str(self, str_data):
    #     temp_dict = json.loads(str_data)
    #
    #     for name in temp_dict:
    #         if name not in self.__dict__.keys():
    #             self.__dict__[name] = {}
    #         for day in temp_dict[name].keys():
    #             if isinstance(day, str):
    #                 alt_day = day.split('_')
    #                 alt_day = tuple([alt_day[0], int(alt_day[1])])
    #
    #                 self.__dict__[name][alt_day] = tuple(temp_dict[name][day])


class Month:
    def __init__(self):
        self.user = "ADMIN"
        self.lst_change = datetime.datetime.now().strftime("%m-%d-%Y %H:%M")
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
        if not isinstance(self._month, str):
            return self._month

        return MESES.index(self._month)

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

    def save_to_db(self):
        conn = sqlite3.connect('months.db')
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        values = self.id, self.center, self.type, self.hash, self.user, self.lst_change, self.schedule.convert_to_str()
        cursor.execute(f"INSERT INTO months VALUES {values}")

        conn.commit()
        cursor.close()
        conn.close()

    def load_from_db(self, center, month, year, stage):
        self.center, self.month, self.year, self.type = center, month, year, stage

        conn = sqlite3.connect('months.db')
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM months WHERE id=?", (self.id,))
        data = cursor.fetchall()[0]

        str_schedule = data[6]
        self.schedule.convert_from_str(str_schedule)

        cursor.close()
        conn.close()

    def delete_from_db(self, center, month, year, stage):
        self.center, self.month, self.year, self.type = center, month, year, stage

        conn = sqlite3.connect('months.db')
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM database WHERE id=?", (self.id,))

        conn.commit()
        cursor.close()
        conn.close()


def new_month(center, month, year):
    base = Base()
    base.load_from_db(center)

    if isinstance(month, str):
        month = MESES.index(month) + 1

    if month == 1:
        str_month = 12
        str_year = year - 1
    else:
        str_month = month - 1
        str_year = year

    first_weekday = datetime.datetime.strptime(f"{STR_DAY}/{str_month}/{str_year}", "%d/%m/%Y").weekday()

    _, last_day = calendar.monthrange(year, str_month)

    month_days = [x % last_day + 1 for x in range(STR_DAY - 1, STR_DAY + last_day - 1)]  # create days list
    week_days = [DIAS_SEM[(first_weekday + i) % 7] for i in range(len(month_days))]  # Weekdays as strings

    week_days = [week_days[i // 2] if i % 2 == 0 else ' ' for i in range(len(week_days) * 2 - 1)]
    month_days = [month_days[i // 2] if i % 2 == 0 else ' ' for i in range(len(month_days) * 2 - 1)]

    print(week_days)
    print(month_days)
