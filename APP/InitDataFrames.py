from DataFrameConvert import *


class InitDataFrames():
    def __init__(self,path):
        self.capacidad = path.capacidadPath
        self.consolidado = path.consolidadoPath

        self.capacidadDT = buildDtf(self.capacidad)
        self.consolidadoDT = buildDtf(self.consolidado)

    def getfileCapacidad(self):
        return self.capacidad

    def getfilesConsolidado(self):
        return self.consolidado

    def getCapacidadDataFrame(self):
        return self.capacidadDT

    def getConsolidadoDataFrame(self):
        return self.consolidadoDT

    def getGeneralDataFrame(self):
        DataFrameToAppend = pd.DataFrame(columns=['AÑO','MES','PROVEEDOR','EQUIPO','TESTERS INICIO',
                                                 'TESTERS FIN','PROM MES','JUNIOR','SEMI-SENIOR','SENIOR'])
        return DataFrameToAppend
