import datetime


user = "ADMIN"
STR_DAY = 26
LEADER = "DR. VICTOR HUGO MARCASSA"


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
    "Alberto David Fadul Filho": {('QUI', '*'): 'n'},
    "Augusto Bernardo de Folchini": {('TER', '*'): 'n'},
    "Elthon André Brambila": {('TER', '*'): 'n'},
    "Gilberto Miguel Stroparo": {('QUI', '*'): 'n', ('QUI', '*'): 'd'},
    "Ivo Rubens Lechinewiski": {('QUA', '*'): 'n'},
    "Kheder Bark Chebli": {('QUA', '*'): 'n'},
    "Marcel Puretz de Moraes": {('QUI', '*'): 'd'}
}

ccq = {}

SEQ_STR_POINT = datetime.datetime.strptime("16/10/2023", "%d/%m/%Y")
SEQ_INDEX = {"CCG": ccg, "CCO": cco, "CCQ": ccq}
