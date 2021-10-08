'''
This toolbox can be used to describe soil surface state (crop cover, soil crusting and roughness) evolution.
Calculations are performed over multiple rainfall events and for all of the catchment plots.
Data from litterature are then used to convert these modelled soil surface state into runoff and erosion model inputs.

In the module "ModelInitialization", the catchment crop types and operations are used to initialize soil surface state. Rainfall is aggregated at a daily time-step.
Crop cover, soil crusting and roughness evolution over multiple rainfall events and plots are then modeled in the "TemporalEvolution" module.
Conversion into runoff and erosion model inputs is performed in the "Outputs" module.

A flowchart describing the code functioning is proposed in figure 6 in the main manuscript.

Authors:
Rosalie Vandromme and Thomas Grangeon
r.vandromme@brgm.fr and t.grangeon@brgm.fr
'''

import datetime
import numpy as np
import pandas as pd
from numpy import genfromtxt
import openpyxl
import time
import os
import sys

from .utils import load_data

from .ModelInitialization import (
    Init_CropTypes,Init_CropCover,Init_Rough,Init_Crust,
    RainfallDepth_ToDaily
)

from .TemporalEvolution import (
    Evol_CropCover,Evol_Crusting,Evol_Rough_Ruiss,Evol_Rough_Erosion
)

from .Outputs import (
    Dictionary_Values,
    DefineTable_InfiltrationCapacity,DefineTable_Imbibition,DefineTable_Manning,
    DefineTable_SheetConcentration,
    ExportRaster
)



def main():

    (DirInputs, DirOutputs, DataSpreadsheet, FilePlots, DataPlots, RasterNoDataValue, DataRainfall, DataRainfallEvent)= load_data(sys.argv[1])

    DateFormat='%d/%m/%Y'
    DateFormatRain='%d-%m-%Y'
    DateHours='%d_%m_%Y_%H_%M_%S'
    
    '''
    Initialize full and simplified crops code, growing code, chemical codes
    Intialize crop cover, roughness and crusting stage on each plot
    '''
    
    df_CropsCode_ini,df_GroupedCrops_Code,df_CropsGrowing_Code,df_Chemical_Code=Init_CropTypes(DirInputs+DataSpreadsheet,DirInputs+DataPlots)
    df_CropCover_Ini=Init_CropCover(DirInputs+DataSpreadsheet,df_CropsCode_ini)
    df_Rough_erosion_Ini,df_Rough_runoff_Ini=Init_Rough(DirInputs+DataSpreadsheet,df_CropsCode_ini)
    df_Crust_Ini=Init_Crust(DirInputs+DataSpreadsheet,df_CropsCode_ini)

    '''
    Aggregate raingauge data to daily time step
    '''
    
    df_Rainfall=RainfallDepth_ToDaily(DirInputs+DataRainfall,DateFormatRain)

    '''
    Define crop cover, soil crusting stage and roughness on each plot
    '''

    df_CropCover_Evol=Evol_CropCover(DirInputs+DataSpreadsheet,df_CropsCode_ini,df_CropCover_Ini,df_CropsGrowing_Code,df_Chemical_Code)
    df_Crusting_Evol=Evol_Crusting(DirInputs+DataSpreadsheet,df_Rainfall,df_CropsCode_ini,df_CropCover_Evol,df_Crust_Ini)
    df_Rough_Run_Evol=Evol_Rough_Erosion(DirInputs+DataSpreadsheet,df_Rainfall,df_CropsCode_ini,df_Rough_erosion_Ini,df_CropCover_Evol)
    df_Rough_Ero_Evol=Evol_Rough_Ruiss(DirInputs+DataSpreadsheet,df_Rainfall,df_CropsCode_ini,df_Rough_runoff_Ini,df_CropCover_Evol)

    '''
    Define the values used to convert soil surface state into soil hydrodynamic properties
    '''
    
    DictInfilt,DictManning,DictSheet,DictErod,Dict_MergeCropCover=Dictionary_Values(DirInputs+DataSpreadsheet)
    dfIC=DefineTable_InfiltrationCapacity(DirInputs+DataSpreadsheet)
    dfImbib=DefineTable_Imbibition(DirInputs+DataSpreadsheet)
    dfManning=DefineTable_Manning(DirInputs+DataSpreadsheet)
    dfSheet=DefineTable_SheetConcentration(DirInputs+DataSpreadsheet)

    '''
    Export rasters for the plots defined in: FilePlots, Dataplots
    and for rainfall events defined in: DataRainfallEvents
    Currentyl uses SAGA-GIS format for export
    '''
    
    ExportRaster(DirInputs,DirOutputs,DataRainfallEvent,FilePlots,RasterNoDataValue,DateHours,DateFormat,
                 df_CropsCode_ini,df_CropCover_Evol,df_Crusting_Evol,df_Rough_Run_Evol,df_Rough_Ero_Evol,
                 DictInfilt,DictManning,DictSheet,DictErod,Dict_MergeCropCover,
                 dfIC,dfImbib,dfManning,dfSheet)

if __name__=="__main__":
    main()