import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import datetime
import csv

def ExtractTable(File,Sheetname,TableNumber,Columns): 
    '''
    Uses the data spreadsheet
    to return a dataframe including one of its table
    '''
 
    DataFile=pd.read_excel(File,sheet_name=Sheetname,skiprows=1,header=0,usecols=Columns)
    
    Data=pd.DataFrame(DataFile[:])
    Data.reset_index(drop=True,inplace=True)
    
    indices=Data.isna().all(axis=1).cumsum() 
    Data['group']=indices
    d=[Data[Data.group==i][int(bool(i)):] for i in Data.group.unique()]
    
    for i in np.arange(0,len(d)): d[i].drop(columns=["group"],inplace=True)
    Table=d[TableNumber-1]

    return Table

def DefineTable_CropCoverEvolution(File,Sheetname,TableNumber,Columns):
    '''
    Uses the data spreadsheet
    to return a dataframe indicating crop cover stages evolution over time (units : days)
    '''
    
    TableVeget=ExtractTable(File,Sheetname,TableNumber,Columns)
    tmp=TableVeget.to_numpy()[:,1:]
    Val=np.ones((tmp.shape[0]+2,tmp.shape[1]+2))*99999
    Val[:-2,:-2]=tmp;Val=Val.astype(int)
    Ind=TableVeget["code évolution végétation"].to_list()
    Col=list(TableVeget)[1:]
    Ind.extend(("-","nan"));Col.extend(("nan","-"))
    dfRule_pousse=pd.DataFrame(Val,index=Ind,columns=Col)
    dfRule_pousse["C3.5"]=99999
    dfRule_pousse.index=dfRule_pousse.index.map(str)

    return dfRule_pousse

def DefineTable_ChemicalDestruction(File,Sheetname,TableNumber,Columns):
    '''
    Uses the data spreadsheet
    to return a dataframe indicating crop cover evolution over time
    after chemical destruction
    '''

    TableChemDestr=ExtractTable(File,Sheetname,TableNumber,Columns)
    IndChem=TableChemDestr["code évolution végétation"].to_list()
    
    TableChemDestr.drop(columns=["C3.5","code évolution végétation"],inplace=True)
    TableChemDestr=TableChemDestr[TableChemDestr.columns[::-1]]
    ValChem=np.ones((TableChemDestr.shape[0]+1,TableChemDestr.shape[1]+2))*99999
    ValChem[:-1,:-2]=TableChemDestr;ValChem=ValChem.astype(int)
    ColChem=list(TableChemDestr)
    ColChem.append("-");ColChem.insert(0,"C3.5")
    IndChem.append("-")
    dfRule_chimique=pd.DataFrame(ValChem,index=IndChem,columns=ColChem)
    dfRule_chimique.index=dfRule_chimique.index.map(str)

    return dfRule_chimique

def Evol_CropCover(File,CropsCode,CropCoverIni,CropGrowingCode,ChemicalCode):
    '''
    Uses the dataframes describing crop types, growing, chemical codes (all from Init_CropTypes)
    and initial crop cover (from Init_CropCover)
    to return a dataframe describing crop cover each day on each plot
    '''

    dfRule_pousse=DefineTable_CropCoverEvolution(File,"CropCover_Evol",1,"C:H")
    dfRule_chimique=DefineTable_ChemicalDestruction(File,"CropCover_Evol",2,"C:H")

    keysAugm=dfRule_pousse.columns[:-2].to_list()
    itemsAugm=dfRule_pousse.columns[:-2].to_list()[1:];itemsAugm.append(keysAugm[-1])
    augm_veget=dict(zip(keysAugm,itemsAugm))
    
    keysDim=itemsAugm[::-1][1:]
    itemsDim=keysAugm[::-1][1:]
    dimin_veget=dict(zip(keysDim,itemsDim))

    dfV_evol = CropCoverIni.copy()
    vevol = CropCoverIni.values
    c_pousse = CropGrowingCode.values
    c_chimique = ChemicalCode.values
    cult = CropsCode.values

    for i in range(vevol.shape[0]):
        day = 1
        cumul=0
        compt = 0
        for j in range(1,vevol.shape[1]-1):
            day += 1
            if cult[i,j]==cult[i,j-1]:
                if cult[i,j]==83 : 
                    if day == dfRule_chimique.loc[code_chimiqe,vevol[i,j]]:
                        vevol[i,j+1] = dimin_veget[vevol[i,j]]
                    else :
                        vevol[i,j+1] = vevol[i,j]
                    
                else : 
                    if day == dfRule_pousse.loc[c_pousse[i,j],vevol[i,j]]:
                        vevol[i,j+1] = augm_veget[vevol[i,j]]
                    else :
                        vevol[i,j+1] = vevol[i,j]
            
            if cult[i,j]!=cult[i,j-1] : 
                day = 1
                if cult[i,j]== 83 : 
                    code_chimiqe = c_chimique[i,j-1]
                    vevol[i,j] = vevol[i,j-1]
                    vevol[i,j+1] = vevol[i,j-1]
   
    col = CropCoverIni.columns
    ind = CropCoverIni.index
    dfV_evol = pd.DataFrame(vevol, index = ind, columns = col)
    
    return dfV_evol