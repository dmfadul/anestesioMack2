import database
import month

import gspread


def get_sheet_info(center):
    spread_sheet = gspread.service_account().open("GrupoHuem")
    interface_sheet = spread_sheet.worksheet("INTERFACE_2")
    interface_sheet_3 = spread_sheet.worksheet("INTERFACE_3")

    data = interface_sheet.get_values()
    data.pop(1)
    data.pop(2)
    data[0].pop(0)
    data[1].pop(1)

    w_days = [x for x in data[0] if x != '']
    m_days = [x for x in data[1] if x != '']

    data.pop(0)
    data.pop(0)

    for line in data:
        line.pop(1)

    for line in data:
        for i in range(len(line)):
            if line[i] != 'n':
                continue
            line[i-1] += 'n'

    for line in data:
        for i in range(2, (len(line)//2)+2):
            line.pop(i)

    data.insert(0, m_days)
    data.insert(0, w_days)

    for line in data:
        print(line)

    interface_sheet_3.update("A1:AJ43", data)

    # base = month.Base(center=center, data=data)

    # database.save_base(base)
