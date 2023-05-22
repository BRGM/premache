import pandas as pd
import numpy as np
import numpy.ma as ma
import time
from datetime import datetime
from itertools import product
import os
import csv
from osgeo import gdal

def array2sdat(nom_sortie,array,param_geo,nodata):
    '''
    Convert array to sdat format
    '''
    
    from osgeo import gdal
    from numpy import isnan
    cols=array.shape[1]
    rows=array.shape[0]

    driver=gdal.GetDriverByName('SAGA')
    outRaster=driver.Create(nom_sortie,cols,rows,1,gdal.GDT_Float32)
    outRaster.SetGeoTransform((param_geo))
    outband=outRaster.GetRasterBand(1)
    array[isnan(array)]=nodata
    outband.SetNoDataValue(nodata)
    outband.WriteArray(array[:,:])
    outband.FlushCache()

def ExportRaster(DirInputs,DirOutputs,FileRainfallEvents,PlotsShapefile,NoDataValue,FormatLong,FormatShort,
                 CropsIni,CropCoverEvol,CrustEvol,RoughRunIni,RoughEroIni,
                 dInfilt,dMann,dSheet,dErod,dMergeCC,
                 TableIC,TableImbib,TableManning,TableSheet):
    '''
    Export model inputs as rasters, using SAGA-GIS format
    '''
    
    src=gdal.Open(DirInputs+PlotsShapefile)
    param_geo=src.GetGeoTransform()
    srcArray=src.ReadAsArray()
    
    RainfallEvents=DirInputs+FileRainfallEvents
    
    dfCrops=CropsIni
    dfVeget_prov=CropCoverEvol
    dfCrust=CrustEvol
    dfR_ero=RoughEroIni
    dfR_run=RoughRunIni
    dfEven=pd.read_excel(RainfallEvents,index_col=0)
    
    PlotsIDs=dfCrops.index
    dfVeget=dfVeget_prov
    headList=list(dfVeget.columns.values)
    
    for i in range(len(headList)):
        dfVeget[headList[i]]=dfVeget_prov[headList[i]].map(dMergeCC)
    
    incr=0

    for index,j in dfEven.iterrows():
        Date=datetime.fromtimestamp(index.timestamp()).strftime(FormatLong)
        DateShort=index.date().strftime(FormatShort)
        
        incr +=1
        os.makedirs(DirOutputs+'{}_{}'.format(incr,Date))
    
        Intensity=j[1]
        PrevRain=j[2]
        Duration=j[3]
        RainDepth=j[4]
        
        infilt_raster=np.zeros_like(srcArray)
        manning_raster=np.zeros_like(srcArray)
        erod_raster=np.zeros_like(srcArray)
        ps_raster=np.zeros_like(srcArray)
        imbib_raster=np.zeros_like(srcArray)
    
        duration_raster=np.zeros_like(srcArray)+Duration
        duration_raster=ma.masked_where(srcArray==NoDataValue,duration_raster)
        duration_raster=np.ma.filled(duration_raster,NoDataValue)
        
        rain_depth_raster=np.zeros_like(srcArray)+RainDepth
        rain_depth_raster=ma.masked_where(srcArray==NoDataValue,rain_depth_raster)
        rain_depth_raster=np.ma.filled(rain_depth_raster,NoDataValue)
        
        array2sdat(DirOutputs+'{}_{}/RainfallDuration.sdat'.format(incr,Date),duration_raster,param_geo,NoDataValue)
        array2sdat(DirOutputs+'{}_{}/RainfallDepth.sdat'.format(incr,Date),rain_depth_raster,param_geo,NoDataValue)
        
        for Plot in PlotsIDs : 
            rugo_ruis=dfR_run.loc[Plot,DateShort]
            rugo_ero=dfR_ero.loc[Plot,DateShort]
            veget=dfVeget.loc[Plot,DateShort]
            croute=dfCrust.loc[Plot,DateShort]
            cult=dfCrops.loc[Plot,DateShort]
            val=TableIC.loc[(str(rugo_ruis),str(veget)),str(croute)]
    
            if val==NoDataValue:
                infilt_raster[srcArray==Plot]=dInfilt[cult]
                a=dInfilt[cult]
                erod_raster[srcArray==Plot]=0
                manning_raster[srcArray==Plot]=dMann[cult]
                ps_raster[srcArray==Plot]=dSheet[cult]
            
            else :
                infilt_raster[srcArray==Plot]=val
                a=val
                erod_raster[srcArray==Plot]=dErod[veget]
                manning_raster[srcArray==Plot]=TableManning.loc[str(rugo_ruis),str(veget)]
    
                if Intensity<= 10 :
                    intens = 'I1'
                if 10 < Intensity <= 40 :
                    intens = 'I2'
                if Intensity > 40 :
                    intens = 'I3'
                
                ps_raster[srcArray==Plot]=TableSheet.loc[(str(rugo_ero),str(veget),intens),str(croute)]
         
            if PrevRain == 0 :
                ant = '0'
            if 1 <= PrevRain <= 15 :
                ant = '1-15'
            if 16 <= PrevRain <= 40 :
                ant = '16-40'
            if PrevRain > 40 :
                ant = '>40'
    
            b='{}'.format(a)
            imbib_raster[srcArray==Plot]=TableImbib.loc[b,ant]
    
        infilt_raster=ma.masked_where(srcArray==NoDataValue,infilt_raster)
        infilt_raster=np.ma.filled(infilt_raster,NoDataValue)
        array2sdat(DirOutputs+'{}_{}/InfiltrationCapacity.sdat'.format(incr,Date),infilt_raster,param_geo,NoDataValue)
    
        imbib_raster=ma.masked_where(srcArray==NoDataValue,imbib_raster)
        imbib_raster=np.ma.filled(imbib_raster,NoDataValue)
        array2sdat(DirOutputs+'{}_{}/Imbibition.sdat'.format(incr,Date),imbib_raster,param_geo,NoDataValue)
    
        ps_raster=ma.masked_where(srcArray==NoDataValue,ps_raster)
        ps_raster=np.ma.filled(ps_raster,NoDataValue)
        array2sdat(DirOutputs+'{}_{}/SheetConcentration.sdat'.format(incr,Date),ps_raster,param_geo,NoDataValue)
    
        erod_raster=ma.masked_where(srcArray ==NoDataValue,erod_raster)
        erod_raster=np.ma.filled(erod_raster,NoDataValue)
        array2sdat(DirOutputs+'{}_{}/GullyErodibility.sdat'.format(incr,Date),erod_raster,param_geo,NoDataValue)
    
        manning_raster=ma.masked_where(srcArray==NoDataValue,manning_raster)
        manning_raster=np.ma.filled(manning_raster,NoDataValue)
        array2sdat(DirOutputs+'{}_{}/Manning.sdat'.format(incr,Date),manning_raster,param_geo,NoDataValue)