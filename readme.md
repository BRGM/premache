# Premache

Parameterization of Runoff and Erosion Models in Agricultural CatCHmEnts 

This toolbox can be used to describe soil surface state (crop cover, soil crusting and roughness) evolution.
Calculations are performed over multiple rainfall events and for all of the catchment plots.
Data from litterature are then used to convert these modelled soil surface state into runoff and erosion model inputs.

In the module "ModelInitialization", the catchment crop types and operations are used to initialize soil surface state. Rainfall is aggregated at a daily time-step.
Crop cover, soil crusting and roughness evolution over multiple rainfall events and plots are then modeled in the "TemporalEvolution" module.
Conversion into runoff and erosion model inputs is performed in the "Outputs" module.

Details:
The Premache toolbox development, functioning, as well as the experimental data used to propose default values are detailed in a specific manuscript, including the toolbox flowchart (figure 6 of the manuscript)
Grangeon T., Vandromme R., Pak L.T., Martin P., Cerdan, O., Richet J.B., Evrard O., Souchère V., Auzet A.V.,  Ludwig B., Ouvry J.F.
A toolbox for soil hydrodynamic property parameterization in agricultural catchments: implications for runoff and erosion modelling.
To be submitted to Environmental Modelling and Software.

Authors:
Rosalie Vandromme and Thomas Grangeon
r.vandromme@brgm.fr and t.grangeon@brgm.fr


Intput files :  files.yml


DirInputs: D:\Documents\.... \
DirOutputs: D:\Documents\..... \
DataSpreadsheet : DDDD.xlsx \
FilePlots: AAAA.tif \
DataPlots: XXX.txt \
RasterNoDataValue : -99999 \
DataRainfall: ZZZZ.xlsx \
DataRainfallEvent : TTTT.xlsx 


python -m EtatsDeSurface files.yml
