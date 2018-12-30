import os

class pathFiles():
    def __init__(self,resourcesPath):
        self.resourcesPath = resourcesPath

        self.capacidadFile = "Capacidad.xls"
        self.consolidadoFile  = "consolidadoCapacidad.xlsx"

        self.capacidadPath = os.path.join(self.resourcesPath,self.capacidadFile)
        self.consolidadoPath = os.path.join(self.resourcesPath,self.consolidadoFile)
