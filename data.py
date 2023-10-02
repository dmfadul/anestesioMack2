import pandas as pd
import gspread
import sqlite3
import json


class Schedule:
    def add_appointment(self, name, day, hours):
        self.__dict__[name] = {day: hours}


class Month:
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
    for line_num in range(4, len(data)):
        for col_num in range(len(data[line_num])):
            if data[line_num][col_num] in ['d', 'n'] or data[line_num][col_num].isdigit():
                print(data[line_num][0], data[2][col_num], data[line_num][col_num])
                # month.add_appointment(data[line_num][0], data[] )


get_dataframe()
