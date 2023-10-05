import gspread
from Month import Month


def get_sheet_info():
    spread_sheet = gspread.service_account().open("GrupoHuem")
    interface_sheet = spread_sheet.worksheet("INTERFACE_2")

    data = interface_sheet.get_values()

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

    # month.schedule.convert_to_str()
    # month.delete_from_db("CCG", "-", "-", "BASE")
    # print(month.__dict__)
    # print(month.schedule.__dict__)
    #
    # month.save_to_db()


m = Month()
m.year = 2023
m.month = 1

m.new_month()

# m.load_from_db("CCG", "-", "-", "BASE")
# print(m.__dict__)
# print(m.schedule.__dict__)
