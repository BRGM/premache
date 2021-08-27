import pandas as pd
import numpy as np
import time
import csv

def ExtractTable(File,Sheetname,Header,Columns):
    '''
    Uses the data spreadsheet
    to return a dataframe including one of its table
    '''
    
    DataFile=pd.read_excel(File,sheet_name=Sheetname,skiprows=0,header=Header,usecols=Columns)
    
    Data=pd.DataFrame(DataFile[:])
    Data.reset_index(drop=True,inplace=True)
    
    indices=Data.isna().all(axis=1).cumsum() 
    Data['group']=indices
    d=[Data[Data.group==i][int(bool(i)):] for i in Data.group.unique()]
    
    for i in np.arange(0,len(d)): d[i].drop(columns=["group"],inplace=True)
    Table=d[0]

    return Table


def GroupCrops(File,Sheetname,Variable):
    '''
    Uses the data spreadsheet
    to return a dictionnary grouping crops and one of their properties
    '''
    
    DataCrops=pd.read_excel(File,sheet_name=Sheetname)
    CodeCrops=DataCrops["Code"]
    CodeGroups=DataCrops[Variable]

    ZipColumnsCrops=zip(CodeCrops,CodeGroups)
    DictCrops=dict(ZipColumnsCrops)
    
    return DictCrops

def Dictionary_Values(File):
    '''
    Uses the data spreadsheet
    to return dictionnaries for particular crops values'''
    
    DictInfilt=GroupCrops(File,"Values","Infiltration capacity")
    DictManning=GroupCrops(File,"Values","Manning")
    DictSheet=GroupCrops(File,"Values","Sheet")    
    DictErod={'C1':0.683,
              'C2':0.217,
              'C3':0.047
              }
    Dict_MergeCropCover={'C1':'C1', 
             'C2':'C2',
             'C2.5':'C2',
             'C3':'C3',
             'C3.5':'C3'
             }
    return DictInfilt,DictManning,DictSheet,DictErod,Dict_MergeCropCover


def DefineTable_InfiltrationCapacity(File):
    '''
    Extract and adapt the table for infiltration capacity values
    and return the corresponding dataframe
    '''
    
    TableIC=ExtractTable(File,"InfiltrationCapacity",2,"A:F")
    
    tmp=TableIC.copy()
    Val=np.ones((tmp.shape[0]+4*len(pd.unique(tmp["Roughness"])),tmp.shape[1]))*(-99999)
    ids=[0,1,2,5,6,7,10,11,12,15,16,17,20,21,22]
    tmp=tmp.drop(["Roughness","Crop Cover"],axis=1).values
    Val[ids,:-2]=tmp
    rows=pd.MultiIndex.from_tuples([ (x,y) for x in ['R0','R1','R2','R3','R4','-', 'nan'] for y in ['C1','C2','C3','-', 'nan']])
    IC=pd.DataFrame(Val,index=rows,columns=['F0','F1','F12','F2','-', 'nan'])
    InfiltrationCapacity=IC.astype(int)

    return InfiltrationCapacity


def DefineTable_Imbibition(File):
    '''
    Extract and adapt the table for imbibition values
    and return the corresponding dataframe
    '''
    
    TableImbib=ExtractTable(File,"Imbibition",2,"A:E")
    
    tmp=TableImbib.to_numpy()

    Val=np.ones((tmp.shape[0]+1,tmp.shape[1]))*(-99999)
    Val[:-1,:]=tmp
    Ind=TableImbib["Infiltration capacity (mm/h)"].to_list()
    Col=list(TableImbib)
    Ind.extend(["-99999"])

    dfImbib=pd.DataFrame(Val,index=Ind,columns=Col).astype(int)
    dfImbib=dfImbib.drop(["Infiltration capacity (mm/h)"],axis=1)
    dfImbib.index=dfImbib.index.map(str)
    dfImbib.columns=dfImbib.columns.map(str)
    
    return dfImbib

def DefineTable_Manning(File):
    '''
    Extract and adapt the table for Manning's n values
    and return the corresponding dataframe
    '''
    
    TableManning=ExtractTable(File,"Manning",1,"A:D")
    tmp=TableManning.to_numpy()[:,1:]
    Val=np.ones((tmp.shape[0]+2,tmp.shape[1]+2))*(-99999)
    Val[:-2,:-2]=tmp
    Ind=TableManning["Soil surface stage"].to_list()
    Col=list(TableManning);Col=Col[1:]
    Ind.extend(("-","nan"));Col.extend(("-","nan"))
    
    dfManning=pd.DataFrame(Val,index=Ind,columns=Col)
    dfManning.index=dfManning.index.map(str)
    
    return dfManning

def DefineTable_SheetConcentration(File):
    '''
    Extract and adapt the table for sheet concentration values
    and return the corresponding dataframe
    '''

    TableSheet=ExtractTable(File,"Sheet",1,"A:G")
    tmp=TableSheet.copy()
    Val=(np.ones((105,6)))*(-99999)
    ids=[0,1,2,3,4,5,6,7,8,15,16,17,18,19,20,21,22,23,30,31,32,33,34,35,36,37,38,45,46,47,48,49,50,51,52,53,60,61,62,63,64,65,66,67,68]
    tmp=tmp.drop(["Roughness","Crop cover","Max. Rainfall intensity (mm/h)"],axis=1).values
    Val[ids,:-2]=tmp
    rows = pd.MultiIndex.from_tuples([ (x,y,z) for x in ['R0','R1','R2','R3','R4','-', 'nan'] for y in ['C1','C2','C3','-', 'nan'] for z in ['I1','I2','I3']])
    SheetConcentration=pd.DataFrame(Val,index=rows,columns=['F0','F1','F12','F2','-', 'nan'])

    return SheetConcentration
