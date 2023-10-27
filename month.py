import session_var
import sequences
import datetime
import settings
import calendar
import hashlib
import math
import json


class Base:
    lst_change = datetime.datetime.now().strftime("%Y-%b-%d %H:%M")

    def __init__(self, user=None, center=None, data=None):
        self.user = user
        self.center = center
        self.data = data if data is not None else []

    @property
    def id(self):
        return f"{self.center}--BASE"

    @property
    def hash(self):
        data = json.dumps(self.data)
        hash_obj = hashlib.sha256(data.encode())
        hash_data = hash_obj.hexdigest()

        return hash_data

    @property
    def data_dict_names(self):
        return self.create_dict_names()

    @property
    def data_dict_days(self):
        return self.create_dict_days()

    def create_dict_names(self):
        data_dict = {}
        for line_num in range(len(self.data)):
            name = self.data[line_num][0]
            if name == '':
                continue

            for col_num in range(len(self.data[0])):
                day = (self.data[0][col_num], self.data[1][col_num])
                hours = self.data[line_num][col_num]

                if '' in day or hours == '':
                    continue

                if name not in data_dict.keys():
                    data_dict[name] = {}

                data_dict[name][day] = hours

        return data_dict

    def create_dict_days(self):
        data_dict = {}
        for col_num in range(1, len(self.data[0])):
            for line_num in range(2, len(self.data)):
                hours = self.data[line_num][col_num]
                if hours == '' or hours is None:
                    continue

                name = self.data[line_num][0]
                week_day = self.data[0][col_num]
                month_day = self.data[1][col_num]

                if (week_day, month_day) not in data_dict.keys():
                    data_dict[(week_day, month_day)] = {}

                data_dict[(week_day, month_day)][name] = hours

        return data_dict


class Month(Base):

    def __init__(self, user=None, center=None, data=None, year=None, month=None, status=0, leader=None):
        super().__init__(user, center, data)

        self.year = year
        self.month = month
        self.status = status
        self.leader = leader

    @property
    def id(self):
        return f"{self.center}{self.month}{self.year}{self.status}"

    @property
    def month_name(self):
        return settings.MESES[self.month-1]

    @property
    def table(self):
        return json.dumps(self.data[:-1])

    @property
    def str_month(self):
        if self.month == 1:
            return 12
        else:
            return self.month - 1

    @property
    def str_year(self):
        if self.month == 1:
            return self.year - 1
        else:
            return self.year

    @property
    def first_week_day(self):
        str_day = session_var.STR_DAY
        return datetime.datetime.strptime(f"{str_day}/{self.str_month}/{self.str_year}", "%d/%m/%Y").weekday()

    @property
    def month_len(self):
        _, last_day = calendar.monthrange(self.str_year, self.str_month)

        return last_day

    @property
    def month_days(self):
        str_day = session_var.STR_DAY
        days = [str(x % self.month_len + 1) for x in range(str_day - 1, str_day + self.month_len - 1)]

        return days

    @property
    def calendar_days(self):
        days = [''] * ((self.first_week_day+2) % 6)
        days += self.month_days
        days += [''] * ((42 - len(days)) % 7)

        days = [days[i:i+7] for i in range(0, len(days), 7)]

        return days

    def calendar_dict(self, day):
        day_key = settings.DIAS_SEM[self.gen_curr_date(day).weekday()], str(day)
        calendar_dict = self.data_dict_days.get(day_key)
        calendar_list = [f"{key}: {value}" for key, value in calendar_dict.items()]

        return calendar_list

    def gen_curr_date(self, curr_day):
        if session_var.STR_DAY <= curr_day <= 31:
            curr_month, curr_year = int(self.str_month), int(self.str_year)
        else:
            curr_month, curr_year = int(self.month), int(self.year)

        current_date = datetime.datetime.strptime(f"{curr_day:02d}/{curr_month:02d}/{curr_year}", "%d/%m/%Y")

        return current_date

    def resolve_sequences(self):
        seq_dict = sequences.index.get(self.center)

        for row_num in range(len(self.data)):
            name = self.data[row_num][0]
            doctor_dict = seq_dict.get(name)
            if doctor_dict is None:
                continue

            for col_num in range(len(self.data[0])):
                curr_weekday = self.data[0][col_num] if self.data[0][col_num] != '' else None
                curr_day = int(self.data[1][col_num]) if self.data[1][col_num] != '' else None

                if curr_weekday is None or curr_day is None:
                    continue

                str_loop = sequences.str_point + datetime.timedelta(settings.DIAS_SEM.index(curr_weekday))
                delta = self.gen_curr_date(curr_day) - str_loop
                parity = (delta.days//7) % 2

                hours = doctor_dict.get((curr_weekday, parity))

                if hours is None:
                    continue

                self.data[row_num][col_num] = hours


def create_new_month(base, year, month):
    new_month = Month(user=session_var.user, center=base.center, year=year, month=month, leader=session_var.LEADER)

    month_days = ['']+new_month.month_days
    week_days = ['']+[settings.DIAS_SEM[(new_month.first_week_day + i) % 7] for i in range(len(month_days)-1)]
    week_indexes = ['']+[str(math.ceil(int(x)/7)) for x in month_days if x != '']

    days = list(zip(week_days,  week_indexes))

    new_data = [week_days, month_days]
    for name in base.data_dict_names.keys():
        line = [name]
        for col_num in range(1, len(month_days)):
            hours = base.data_dict_names.get(name).get(days[col_num])
            line.append(hours)
        new_data.append(line)

    new_data.append([None] * len(month_days))

    new_month.data = new_data
    new_month.resolve_sequences()

    return new_month
