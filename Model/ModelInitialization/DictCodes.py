import pandas as pd

#dir='C:\\Users\\grangeont\\Desktop\\FormationPython\\TP\\TravailTP\\data\\'
#filename="dataV4.xlsx"

def GroupCrops(File,Sheetname,Variable):
    "A dictionnary grouping crops having similar behavior"
    
    DataCrops=pd.read_excel(File,sheet_name=Sheetname)
    CodeCrops=DataCrops["Code"]
    CodeGroups=DataCrops[Variable]

    ZipColumnsCrops=zip(CodeCrops,CodeGroups)
    DictCrops=dict(ZipColumnsCrops)
    
    return DictCrops