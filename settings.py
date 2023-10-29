import datetime


user = "ADMIN"
STR_DAY = 26
LEADER = "DR. VICTOR HUGO MARCASSA"


TODAY = datetime.date.today().strftime("%Y-%m-%d")
DIAS_SEM = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM']
MESES = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
         "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]

ccg = {
    "Gilberto Miguel Stroparo": {('QUI', 0): 'd'},
    "Guilherme Rezende Baade": {('QUI', 1): 'n'},
    "Marcel Puretz de Moraes": {('QUI', 1): 'd'},
    "Vinicius Rocha Batista": {('QUI', 0): 'n'}
}

cco = {
    "Alberto David Fadul Filho": {('QUI', 1): 'n'},
    "Augusto Bernardo de Folchini": {('TER', 1): 'n'},
    "Elthon André Brambila": {('TER', 0): 'n'},
    "Gilberto Miguel Stroparo": {('QUI', 1): 'd', ('QUI', 0): 'n'},
    "Ivo Rubens Lechinewiski": {('QUA', 0): 'n'},
    "Kheder Bark Chebli": {('QUA', 1): 'n'},
    "Marcel Puretz de Moraes": {('QUI', 0): 'd'}
}

ccq = {}

SEQ_STR_POINT = datetime.datetime.strptime("16/10/2023", "%d/%m/%Y")
SEQ_INDEX = {"CCG": ccg, "CCO": cco, "CCQ": ccq}
