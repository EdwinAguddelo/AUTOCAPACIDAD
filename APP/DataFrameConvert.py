import pandas as pd

def  buildDtf(files):
        data = pd.read_excel(files)
        return data
