import gspread
import month


def get_sheet_info():
    spread_sheet = gspread.service_account().open("GrupoHuem")
    interface_sheet = spread_sheet.worksheet("INTERFACE_2")

    data = interface_sheet.get_values()

    base = month.Base()
    base.center = data[0][0]
    base.data = data

    # for line in data:
    #     print(line)

    # base.save_to_db()


def convert_list_into_dict(data):
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

    # month.schedule.convert_to_str()
    # month.delete_from_db("CCG", "-", "-", "BASE")
    # print(month.__dict__)
    # print(month.schedule.__dict__)
    #
    # month.save_to_db()


# m = Month()
#
# m.load_from_db("CCG", "-", "-", "BASE")
# print(m.__dict__)
# print(m.schedule.__dict__)

n = month.new_month('CCG', 'DEZ', 2023)
get_sheet_info()
