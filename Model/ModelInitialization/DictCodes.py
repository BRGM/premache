import pandas as pd


def GroupCrops(File,Sheetname,Variable):
    "A dictionnary grouping crops having similar behavior"
    
    DataCrops=pd.read_excel(File,sheet_name=Sheetname)
    CodeCrops=DataCrops["Code"]
    CodeGroups=DataCrops[Variable]

    ZipColumnsCrops=zip(CodeCrops,CodeGroups)
    DictCrops=dict(ZipColumnsCrops)
    
    return DictCrops