import pandas as pd
import numpy as np
import time
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

def DefineTable_RoughEvolution(File,Sheetname,TableNumber,Columns):
    '''
    Uses the data spreadsheet
    to return a dataframe indicating roughness evolution under rainfall (units: mm)
    '''
    
    TableRough=ExtractTable(File,"Rough_Evol",1,"A:F")
    Ind=TableRough["Final roughness"].to_list();Ind[:0]=["R4"]
    Col=list(TableRough)[1:]
    Ind.extend(("-","nan"));Col.extend(("-","nan"))
    tmp=TableRough.to_numpy()[:,1:]
    Val=np.ones((tmp.shape[0]+3,tmp.shape[1]+2))*99999
    Val[:-3,:-2]=tmp
    Val=Val.astype(int)
    dfSeuilsP=pd.DataFrame(Val,index=Ind,columns=Col)
    dfSeuilsP.index=dfSeuilsP.index.map(str)
    
    return dfSeuilsP

def Evol_Rough_Erosion(File,Rainfall,CropsCode,Rough_Ini_Erosion,CropCover_Evol):
    '''
    Uses the dataframes describing crop types (from Init_CropTypes),
    crop cover (from CropCover_Evol)
    and inital roughness (from Init_Rough)
    to return a dataframe describing roughness each day on each plot
    '''
    
    dfSeuils=DefineTable_RoughEvolution(File,"Crust_Evol",1,"A:F")
    
    keysAugm=dfSeuils.index[:-2].to_list()
    itemsAugm=dfSeuils.index[:-2].to_list()[1:];itemsAugm.append(keysAugm[-1])
    dimin_rugo=dict(zip(keysAugm,itemsAugm))

    dfP=Rainfall
    dfR_evol = Rough_Ini_Erosion.copy()    
    revol = dfR_evol.values
    veget = CropCover_Evol.values
    cult = CropsCode.values
    
    for i in range(revol.shape[0]):
        cumul = dfP.iloc[0,0]
        for j in range(1,revol.shape[1]-1):
            cumul += dfP.iloc[0,j] 
            cumul=round(cumul,1)
            if cult[i,j-1]==cult[i,j] : 
                if cumul >= dfSeuils.loc[revol[i,j-1],veget[i,j-1]] : 
                    cumul -= dfSeuils.loc[revol[i,j-1],veget[i,j-1]]
                    cumul=round(cumul,1)
                    revol[i,j]=dimin_rugo[revol[i,j-1]]
                else : 
                    revol[i,j]=revol[i,j-1]
                    
            if cult[i,j-1]!=cult[i,j] : 
                cumul = dfP.iloc[0,j]
                
                if cult[i,j]==83 :
                    revol[i,j] = revol[i,j-1]
    
    
    col = dfR_evol.columns
    ind = dfR_evol.index
    dfR_evol = pd.DataFrame(revol, index = ind, columns = col)
    
    return dfR_evol

def Evol_Rough_Ruiss(File,Rainfall,CropsCode,Rough_Ini_Erosion,CropCover_Evol):
    '''
    Uses the dataframes describing crop types (from Init_CropTypes),
    crop cover (from CropCover_Evol)
    and inital roughness (from Init_Rough)
    to return a dataframe describing roughness each day on each plot
    '''

    dfSeuils=DefineTable_RoughEvolution(File,"Crust_Evol",1,"A:F")
    
    keysAugm=dfSeuils.index[:-2].to_list()
    itemsAugm=dfSeuils.index[:-2].to_list()[1:];itemsAugm.append(keysAugm[-1])
    dimin_rugo=dict(zip(keysAugm,itemsAugm))

    dfP=Rainfall
    dfR_evol = Rough_Ini_Erosion.copy()    
    revol = dfR_evol.values
    veget = CropCover_Evol.values
    cult = CropsCode.values
    
    for i in range(revol.shape[0]):
        cumul = dfP.iloc[0,0]
        for j in range(1,revol.shape[1]-1):
            cumul += dfP.iloc[0,j] 
            cumul=round(cumul,1)
            if cult[i,j-1]==cult[i,j] : 
                if cumul >= dfSeuils.loc[revol[i,j-1],veget[i,j-1]] : 
                    cumul -= dfSeuils.loc[revol[i,j-1],veget[i,j-1]]
                    cumul=round(cumul,1)
                    revol[i,j]=dimin_rugo[revol[i,j-1]]
                else : 
                    revol[i,j]=revol[i,j-1]
                    
            if cult[i,j-1]!=cult[i,j] : 
                cumul = dfP.iloc[0,j]
                
                if cult[i,j]==83 :
                    revol[i,j] = revol[i,j-1]
    
    
    col = dfR_evol.columns
    ind = dfR_evol.index
    dfR_evol = pd.DataFrame(revol, index = ind, columns = col)
    return dfR_evol