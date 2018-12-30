import pandas as pd
from utils import *

def mainProcess(init_dataframes,mes):

    dtCapacidad = init_dataframes.getCapacidadDataFrame()
    dtCapacidad = dtCapacidad.rename(columns={' PROVEEDOR': 'PROVEEDOR'})
    dtconsolidado = init_dataframes.getConsolidadoDataFrame()
    filepath = init_dataframes.getfilesConsolidado()
    year = getAño(dtCapacidad)
    mes = int(mes)
    mesAnterior = mes - 1
    dataCapacidad = ponerColumnaMes(dtCapacidad)
    proveedores = dataCapacidad['PROVEEDOR']
    equipos = dataCapacidad['EQUIPO']
    listaEquipos = listarEquipos(equipos)
    listaProveedores = listarProveedores(proveedores)
    testersInicio = testersInicial(dtconsolidado,year,mes,mesAnterior,listaProveedores,listaEquipos)
    print('en proceso...')
    testersFinalyPromedio,dtProveedores = testersFinalyProm(listaProveedores,listaEquipos,dataCapacidad,testersInicio)
    rotaron = rotaciones(dtProveedores,listaEquipos,testersFinalyPromedio,mes)
    junior = juniors(dtProveedores,listaEquipos,rotaron)
    semi_senior = semi_seniors(dtProveedores,listaEquipos,junior)
    senior = seniors(dtProveedores,listaEquipos,semi_senior)
    indicadorrotacion = rotacion(listaProveedores,senior)
    dtconsolidado = dtconsolidado.append(indicadorrotacion,ignore_index = True)    
    exportarAexcel(dtconsolidado,filepath)



def listarEquipos(equipos):
    equipoList = []
    for team in equipos:
         if team not in equipoList:
            equipoList.append(team)
    return equipoList


def listarProveedores(proveedores):
    proveedorList = []
    for i in range(len(proveedores)):
        proveedores[i] = proveedores[i].split(' ')[0]

    for prov in proveedores:
         if prov not in proveedorList:
            proveedorList.append(prov)
    return proveedorList

def testersInicial(consolidadodt,year,mes,mesAnterior,proveedorList,equipoList):
    inicioMes = consolidadodt[consolidadodt['MES'] == mesString(mesAnterior)]
    inicioMes = inicioMes[inicioMes['AÑO'] == year]
    dtLista = []
    for prov in proveedorList:
        filtroProv = inicioMes[inicioMes['PROVEEDOR'] == prov ]
        dtLista.append(filtroProv)
    dtfiltradoss = []
    for dt in dtLista:
        for team in equipoList:
            equipo = team
            filtrototall = dt[dt.EQUIPO == team]
            dtfiltradoss.append(filtrototall)
    listaTI = []
    for dt in dtfiltradoss:
        intento = dt.loc[:'TESTERS FIN']
        del intento['AÑO']
        del intento['MES']
        del intento['TESTERS INICIO']
        del intento['PROM MES']
        del intento['ROTARON']
        del intento['JUNIOR']
        del intento['SEMI-SENIOR']
        del intento['SENIOR']
        intento.insert(0,'AÑO',year)
        intento.insert(1,'MES',[mesString(mes)])
        intento = intento.rename(columns={'TESTERS FIN': 'TESTERS INICIO'})
        listaTI.append(intento)
    listaTIToappended = pd.DataFrame(columns=['AÑO','MES','PROVEEDOR','EQUIPO','TESTERS INICIO'])
    for li in listaTI:
        listaTIToappended = listaTIToappended.append(li, ignore_index=True,sort=False)
    return listaTIToappended

def testersFinalyProm(proveedorList,equipoList,datCapacidad,listaTIToappended):
    dtList = []
    for prov in proveedorList:
        filtroProv = datCapacidad[datCapacidad['PROVEEDOR'] == prov ]
        dtList.append(filtroProv)

    dtfiltrados = pd.DataFrame(columns=['AÑO','MES','PROVEEDOR','EQUIPO','TESTERS INICIO','TESTERS FIN'])
    for dt in dtList:
        proveedor = max(dt['PROVEEDOR'])
        for team in equipoList:
            filtrototal = dt[(dt.EQUIPO == team) & (dt.ESTADO == 'A')]
            dataFrame = listaTIToappended[listaTIToappended['PROVEEDOR'] == proveedor]
            equipofilter = dataFrame[dataFrame['EQUIPO'] == team].copy()
            equipofilter['TESTERS FIN'] = len(filtrototal)
            rotaron = (equipofilter.loc[:,'TESTERS FIN'] + equipofilter.loc[:,'TESTERS INICIO'])/2
            equipofilter.insert(6,'PROM MES',rotaron)
            dtfiltrados = dtfiltrados.append(equipofilter, ignore_index=True,sort=False)
    return dtfiltrados,dtList

def rotaciones(dtList,equipoList,dtfiltrados,mes):
    dtfiltradox = pd.DataFrame(columns=['AÑO','MES','PROVEEDOR','EQUIPO','TESTERS INICIO','TESTERS FIN','PROM MES','ROTARON'])
    for dt in dtList:
        proveedor = max(dt['PROVEEDOR'])
        for team in equipoList:
            filtroto = dt[(dt.EQUIPO == team) & (dt['FECHA DE NOVEDAD'] == mesString(mes)) & (dt.ESTADO == 'R') & ((dt.NOVEDAD == 'RETIRO POR RENUNCIA') | (dt.NOVEDAD == 'RETIRO POR DESEMPEÑO') | (dt.NOVEDAD == 'RETIRO POR CAMBIO DE ROL'))]
            dataFram = dtfiltrados[dtfiltrados['PROVEEDOR'] == proveedor]
            equipofiltered = dataFram[dataFram['EQUIPO'] == team].copy()
            equipofiltered['ROTARON'] = len(filtroto)
            dtfiltradox = dtfiltradox.append(equipofiltered, ignore_index = True,sort=False)
    return dtfiltradox

def juniors(dtList,equipoList,dtfiltradox):
    dtfiltrado = pd.DataFrame(columns=['AÑO','MES','PROVEEDOR','EQUIPO','TESTERS INICIO','TESTERS FIN','PROM MES','ROTARON','JUNIOR'])
    for dt in dtList:
        proveedor = max(dt['PROVEEDOR'])
        for team in equipoList:
            filtro = dt[(dt.EQUIPO == team) & (dt.ESTADO == 'A') & (dt.PERFIL == 'Junior') ]
            dtproveedor = dtfiltradox[dtfiltradox['PROVEEDOR'] == proveedor]
            dtequipo = dtproveedor[dtproveedor['EQUIPO'] == team].copy()
            dtequipo['JUNIOR'] = len(filtro)
            dtfiltrado = dtfiltrado.append(dtequipo, ignore_index = True,sort=False)
    return dtfiltrado

def semi_seniors(dtList,equipoList,dtfiltrado):
    dtfilt = pd.DataFrame(columns=['AÑO','MES','PROVEEDOR','EQUIPO','TESTERS INICIO','TESTERS FIN','PROM MES','ROTARON','JUNIOR','SEMI-SENIOR'])
    for dt in dtList:
        proveedor = max(dt['PROVEEDOR'])
        for team in equipoList:
            filt = dt[(dt.EQUIPO == team) & (dt.ESTADO == 'A') & (dt.PERFIL == 'Semi-Senior') ]
            proveedordt = dtfiltrado[dtfiltrado['PROVEEDOR'] == proveedor]
            equipodt = proveedordt[proveedordt['EQUIPO'] == team].copy()
            equipodt['SEMI-SENIOR'] = len(filt)
            dtfilt = dtfilt.append(equipodt, ignore_index = True,sort=False)
    return dtfilt

def seniors(dtList,equipoList,dtfilt):
    dtfil = pd.DataFrame(columns=['AÑO','MES','PROVEEDOR','EQUIPO','TESTERS INICIO','TESTERS FIN','PROM MES','ROTARON','JUNIOR','SEMI-SENIOR','SENIOR'])
    for dt in dtList:
        proveedor = max(dt['PROVEEDOR'])
        for team in equipoList:
            equipo = team
            fil = dt[(dt.EQUIPO == team) & (dt.ESTADO == 'A') & (dt.PERFIL == 'Senior') ]
            proveedordata = dtfilt[dtfilt['PROVEEDOR'] == proveedor]
            equipodata = proveedordata[proveedordata['EQUIPO'] == team].copy()
            equipodata['SENIOR'] = len(fil)
            dtfil = dtfil.append(equipodata, ignore_index = True,sort=False)
    return dtfil

def rotacion(proveedorList,dtfil):
    dtfs = pd.DataFrame(columns=['AÑO','MES','PROVEEDOR','EQUIPO','TESTERS INICIO','TESTERS FIN','PROM MES','ROTARON','JUNIOR','SEMI-SENIOR','SENIOR','PROM TOTAL','ROTARON TOTAL'])

    for prov in proveedorList:
        filtroP = dtfil[dtfil['PROVEEDOR'] == prov ].copy()
        filtroP['PROM TOTAL'] = filtroP['PROM MES'].sum()
        filtroP['ROTARON TOTAL'] = filtroP['ROTARON'].sum()
        dtfs = dtfs.append(filtroP, ignore_index = True,sort=False)
    return dtfs

def exportarAexcel(dtf,filepath):
        dtf.to_excel(filepath,index=False)
        print('Exportado {}'.format(filepath))
