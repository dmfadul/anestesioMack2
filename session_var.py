# MESES = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']

with open("settings.txt", 'r') as f:
    lines = f.readlines()

var_list = [line.strip().split(':') for line in lines]

LEADER = var_list[0][1].strip()
STR_DAY = int(var_list[1][1].strip())

user = "ADMIN"
