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

def DefineTable_CrustingEvolution(File,Sheetname,TableNumber,Columns):
    '''
    Uses the data spreadsheet
    to return a dataframe indicating crusting stages evolution under rainfall (units: mm)
    '''
    
    TableCrust=ExtractTable(File,"Crust_Evol",TableNumber,Columns)
    Ind=TableCrust["Final stage"].to_list();Ind[:0]=["F0"]
    Col=list(TableCrust)[1:]
    Ind.extend(("-","nan"));Col.extend(("-","nan"))
    tmp=TableCrust.to_numpy()[:,1:]
    tmp[1:]-=tmp[:-1].copy()
    Val=np.ones((tmp.shape[0]+3,tmp.shape[1]+2))*99999
    Val[:-3,:-2]=tmp
    Val=Val.astype(int)
    dfSeuils=pd.DataFrame(Val,index=Ind,columns=Col)
    dfSeuils.index=dfSeuils.index.map(str)
    
    return dfSeuils

def Evol_Crusting(File,Rainfall,CropsCode,CropCover_Evol,CrustIni):
    '''
    Uses the dataframes describing crop types (from Init_CropTypes),
    crop cover (from CropCover_Evol)
    and inital crusting stage (from Init_Crust)
    to return a dataframe describing crusting stage each day on each plot
    '''

    dfSeuils=DefineTable_CrustingEvolution(File,"Crust_Evol",1,"A:F")
        
    keysAugm=dfSeuils.index[:-2].to_list()
    itemsAugm=dfSeuils.index[:-2].to_list()[1:];itemsAugm.append(keysAugm[-1])
    evol_facies=dict(zip(keysAugm,itemsAugm))

    dfP = Rainfall
    facies_ini = CrustIni
    dfF_evol=facies_ini.copy()
    fevol = dfF_evol.values
    veget = CropCover_Evol.values
    cult = CropsCode.values
    
    for i in range(fevol.shape[0]):
        cumul = dfP.iloc[0,0]
        for j in range(1,fevol.shape[1]-1):
            cumul += dfP.iloc[0,j] 
            cumul=round(cumul,1)
            if cult[i,j-1]==cult[i,j] : 
                if cumul >= dfSeuils.loc[fevol[i,j-1],veget[i,j-1]] : 
                    cumul -= dfSeuils.loc[fevol[i,j-1],veget[i,j-1]]
                    cumul=round(cumul,1)
                    fevol[i,j]=evol_facies[fevol[i,j-1]]
                else :
                    fevol[i,j]=fevol[i,j-1]
                    
            if cult[i,j-1]!=cult[i,j] : 
                cumul = dfP.iloc[0,j]
                if cult[i,j]==83 :
                    fevol[i,j] = fevol[i,j-1]
    
    
    col = dfF_evol.columns
    ind = dfF_evol.index
    dfF_evol = pd.DataFrame(fevol, index = ind, columns = col)
    
    return dfF_evol