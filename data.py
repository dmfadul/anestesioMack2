import pandas as pd
import gspread
import sqlite3
import json


class Schedule:
    def add_appointment(self, name, day, hours):
        if hours == ('', ''):
            return

        if name not in self.__dict__.keys():
            self.__dict__[name] = {}

        self.__dict__[name][day] = hours


class Month:
    def __init__(self):
        self.id = None
        self.user = None
        self.lst_change = None
        self.month = None
        self.year = None
        self.center = None
        self.type = None
        self.leader = None
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


def show_df(df):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)

    print(df)


def get_dataframe():
    spread_sheet = gspread.service_account().open("GrupoHuem")
    interface_sheet = spread_sheet.worksheet("INTERFACE_2")

    data = interface_sheet.get_values()
    df = pd.DataFrame(data)

    # for line in data:
    #     print(line)

    month = Month()
    month.center = data[0][0]
    month.type = data[1][0]
    month.month = data[0][1]
    month.year = data[1][1]
    month.leader = data[2][0]

    for line_num in range(4, len(data)):
        for col_num in range(2, len(data[line_num]), 2):
            hours = (data[line_num][col_num], data[line_num][col_num+1])
            if hours != ('', ''):
                name = data[line_num][0]
                day = (data[0][col_num], data[2][col_num])

                month.add_appointment(name, day, hours)

    for col_num in range(2, len(data[1]), 2):
        if data[1][col_num] == 'f':
            month.holidays.append(data[2][col_num])

    print(month.__dict__)
    print(month.schedule.__dict__)


get_dataframe()
