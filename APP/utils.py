import pandas as pd

def mesString(numero):
    meses = { 0 : 'Diciembre', 1 : 'Enero', 2: 'Febrero',3:'Marzo',
         4:'Abril',5:'Mayo',6:'Junio',7:'Julio',8:'Agosto',9:'Septiembre',
         10:'Octubre',11:'Noviembre',12:'Diciembre' }
    return meses[numero]

def getAño(datCapacidad):
    fecha = max(datCapacidad['FECHA DE NOVEDAD'])
    year = fecha.split('-')[0]
    year = int(year)
    return year

def ponerColumnaMes(datCapacidad):
    listafecha = []
    capacity = datCapacidad['FECHA DE NOVEDAD']

    for i in range(len(capacity)):
        capacity[i] = mesString(int(capacity[i].split('-')[1]))
        listafecha.append(capacity[i])

    datCapacidad['FECHA DE NOVEDAD'] = pd.DataFrame(listafecha)
    return datCapacidad
