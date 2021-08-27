import datetime
import numpy as np
import pandas as pd
from numpy import genfromtxt
import openpyxl
import time

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


def Init_CropTypes(Input_Spreadsheet,Input_Plots):
    '''
    Uses the data spreadsheet
    to return dataframes of initial crops code.
    The returned dataframes are: full and simplified crops code, crops growing code and chemical code
    '''
    
    Dict_CodesCrops=GroupCrops(Input_Spreadsheet,"CropsCode","Code_GroupedCrops")
    Dict_CropCover=GroupCrops(Input_Spreadsheet,"CropsCode","Code_CropCoverEvolution")
    Dict_Chemical=GroupCrops(Input_Spreadsheet,"CropsCode","Code_CropCoverEvolution_ChemicalDestruction")
    
    # Items including both int and str -> convert to str
    for j in Dict_CropCover:
        Dict_CropCover[j] = format(str(Dict_CropCover[j]))
    for k in Dict_Chemical:
        Dict_Chemical[k] = format(str(Dict_Chemical[k]))
    
    Data_CropType = Input_Plots
    CropType = pd.read_csv(Data_CropType,sep='\t',index_col=0)
    
    # Replace NoData plots by grasslands; assume a static behavior (i.e. soil surface state will not evolve for these plots) 
    tab = CropType.values
    for i in range(tab.shape[0]):
        a = 66
        for j in range(1,tab.shape[1]):
            if np.isnan(tab[i,j]):
                tab[i,j] = a
            a = tab[i,j]
    
    Col = CropType.columns
    Ind = CropType.index
    
    df_CropsIni_Code = pd.DataFrame(tab,index=Ind,columns=Col)
    df_GroupedCrops_Code=df_CropsIni_Code.copy()
    df_GroupedCrops_Code=df_GroupedCrops_Code.replace(Dict_CodesCrops)

    df_CropsGrowing_Code = df_CropsIni_Code.copy()
    df_CropsGrowing_Code=df_CropsGrowing_Code.replace(Dict_CropCover)
    
    df_Chemical_Code = df_CropsIni_Code.copy()
    df_Chemical_Code=df_Chemical_Code.replace(Dict_Chemical)

    return df_CropsIni_Code, df_GroupedCrops_Code, df_CropsGrowing_Code, df_Chemical_Code


def Init_CropCover(Input_Spreadsheet,df_CropsIni_Code):
    '''
    Uses the initial crops codes dataframe (from function Init_CropTypes)
    to return a dataframe indicating initial crop cover
    '''
    
    Dict_CropCover_Ini=GroupCrops(Input_Spreadsheet,"CropsCode","Initial Crop Cover")

    dfCropsIni=df_CropsIni_Code
    df_new = dfCropsIni.copy()
    df_new = dfCropsIni.replace(Dict_CropCover_Ini)
   
    tab = df_new.values

    decrease_cover ={'C3':'C2', 
                 'C2':'C1',
                 'C1':'C1',
                 '-' : '-',
                 np.nan : np.nan
                 }
    
    for i in range(tab.shape[0]):
        a = 'C1'
        for j in range(1,tab.shape[1]):
            if tab[i,j] == 'Prev.' :
                tab[i,j] = a
            if tab[i,j] == 'Veg -' :
                tab[i,j] = decrease_cover[a]
            a = tab[i,j]
    col_df_new = df_new.columns
    index_df_new = df_new.index
    
    df_InitialCropCover = pd.DataFrame(tab, index = index_df_new, columns = col_df_new)

    return df_InitialCropCover


def Init_Rough(Input_Spreadsheet,df_CropsIni_Code):
    '''
    Uses the initial crops codes dataframe (from function Init_CropTypes)
    to return a dataframe indicating initial soil roughness (codes: R0, R1, R2, R3, R4)
    '''

    dict_rough_runoff_ini=GroupCrops(Input_Spreadsheet,"CropsCode","Initial Roughness Runoff")
    dict_rough_erosion_ini=GroupCrops(Input_Spreadsheet,"CropsCode","Initial Roughness Erosion")

    dfCropsIni=df_CropsIni_Code
    df_new_erosion = dfCropsIni.copy()
    df_new_erosion = df_new_erosion.replace(dict_rough_erosion_ini)
    tab_erosion= df_new_erosion.values
    
    df_new_runoff = dfCropsIni.copy()
    df_new_runoff = df_new_runoff.replace(dict_rough_runoff_ini)
    tab_runoff = df_new_runoff.values
    
    for i in range(tab_erosion.shape[0]):
        a = 'R2'
        for j in range(1,tab_erosion.shape[1]):
            if tab_erosion[i,j] == 'Prev.' :
                tab_erosion[i,j] = a
            a = tab_erosion[i,j]

    for i in range(tab_runoff.shape[0]):
        a = 'R2'
        for j in range(1,tab_runoff.shape[1]):
            if tab_runoff[i,j] == 'Prev.' :
                tab_runoff[i,j] = a
            a = tab_runoff[i,j]
    
    col = df_new_erosion.columns
    ind = df_new_erosion.index
    df_rough_erosion = pd.DataFrame(tab_erosion, index = ind, columns = col)
    df_rough_runoff = pd.DataFrame(tab_runoff, index = ind, columns = col)
    
    return df_rough_erosion, df_rough_runoff


def Init_Crust(Input_Spreadsheet,df_CropsIni_Code):
    '''
    Uses the initial crops codes dataframe (from function Init_CropTypes)
    to return a dataframe indicating initial soil crusting stage (codes: F0, F1, F12, F2)
    '''
    
    dict_crust_ini=GroupCrops(Input_Spreadsheet,"CropsCode","Initial Crusting")
    
    dfCropsIni=df_CropsIni_Code
    df_new = dfCropsIni.copy()
    df_new = df_new.replace(dict_crust_ini)
    tab = df_new.values
    
    for i in range(tab.shape[0]):
        a = 'F12'
        for j in range(1,tab.shape[1]):
            if tab[i,j] == 'Prev.' :
                tab[i,j] = a
            a = tab[i,j]
    
    col_df_new = df_new.columns
    index_df_new = df_new.index
    df_crust = pd.DataFrame(tab, index = index_df_new, columns = col_df_new)

    return df_crust