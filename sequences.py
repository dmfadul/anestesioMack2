import datetime

str_point = datetime.datetime.strptime("16/10/2023", "%d/%m/%Y")

CCG = {
    "Gilberto Miguel Stroparo": {('QUI', 0): 'd'},
    "Guilherme Rezende Baade": {('QUI', 1): 'n'},
    "Marcel Puretz de Moraes": {('QUI', 1): 'd'},
    "Vinicius Rocha Batista": {('QUI', 0): 'n'}
}

CCO = {
    "Alberto David Fadul Filho": {('QUI', '*'): 'n'},
    "Augusto Bernardo de Folchini": {('TER', '*'): 'n'},
    "Elthon André Brambila": {('TER', '*'): 'n'},
    "Gilberto Miguel Stroparo": {('QUI', '*'): 'n', ('QUI', '*'): 'd'},
    "Ivo Rubens Lechinewiski": {('QUA', '*'): 'n'},
    "Kheder Bark Chebli": {('QUA', '*'): 'n'},
    "Marcel Puretz de Moraes": {('QUI', '*'): 'd'}
}

CCQ = {}

index = {"CCG": CCG, "CCO": CCO, "CCQ": CCQ}
