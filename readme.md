# Premache

Parameterization of Runoff and Erosion Models in Agricultural CatCHmEnts 

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




Intput files :  files.yml


DirInputs: D:\Documents\....
DirOutputs : D:\Documents\.....
DataSpreadsheet : DDDD.xlsx 
FilePlots: AAAA.tif 
DataPlots: XXX.txt
RasterNoDataValue : -99999
DataRainfall: ZZZZ.xlsx
DataRainfallEvent : TTTT.xlsx


python -m EtatsDeSurface files.yml
