# PREMACHE
Parameterization of Runoff and Erosion Models in Agricultural CatCHmEnts ("Prémâcher" is a French word translating into _spoon-fed_, making work easier for future users).  
The objective is to create runoff and erosion model inputs over multiple plots and rainfall events in agricultural catchments.  
To this end, time series of crop cover, roughness and crusting are modelled over the catchment plots. Then, model inputs are created based on the methodology proposed by [Cerdan et al. (2002a)](https://www.sciencedirect.com/science/article/pii/S0341816201001667?via%3Dihub) and [Cerdan et al. (2002b)](https://onlinelibrary.wiley.com/doi/10.1002/hyp.1098).

## Overview

### PREMACHE architecture
PREMACHE is divided into three modules:
* ``ModelInitialization``: the catchment crop types and operations are used to initialize soil surface state over the catchment plots. Rainfall is aggregated at a daily time-step.
* ``TemporalEvolution``: crop cover, soil crusting and roughness are modeled over the catchments plots for the rainfall events provided.
* ``Outputs``: conversion into runoff and erosion model inputs. Outputs are provided in raster format.

### Execution
First, please make sure that you are aware of the limitations associated with the proposed toolbox and check that input data are prepared accordingly to the procedure described in the manuscript (see ``References`` below).  
Check the the .yml file. Current date format is %d/%m/%Y.  
In a Python prompt, move to the PREMACHE repository and write:
``python -m PREMACHE param.yml``


## Inputs and dependencies

### Input files
Intput files : param.yml

DirInputs: D:\Documents\.... \
DirOutputs: D:\Documents\..... \
DataSpreadsheet : Data&Values.xlsx \
FilePlots: Plots.tif \
DataPlots: LandUse_TimeSeries.txt \
Raster : DEM.tif (NoData : -99999) \
DataRainfall: Rainfall_TimeSeries.xlsx \
DataRainfallEvent : Rainfall_EventsCharacteristics.xlsx 

### Python
PREMACHE was developped in Python 3.8.5 and make use of the following packages:
``panda``, ``numpy``, ``datetime``, ``time``, ``openpyxl``, ``csv``, ``itemtools``, ``os``, ``osgeo``


## References

### Scientific manuscript
Grangeon T., Vandromme R., Pak L.T., Martin P., Cerdan, O., Richet J.B., Evrard O., Souchère V., Auzet A.V., Ludwig B., Ouvry J.F. (2022). Dynamic parameterization of soil surface characteristics for hydrological models in agricultural catchments. Catena, 214:106257.  
[The manuscript is available online](https://www.sciencedirect.com/science/article/pii/S0341816222002430?dgcid=author).

The PREMACHE toolbox development, functioning, as well as the experimental data used to propose default values are detailed in a specific manuscript, including the toolbox flowchart (``figure 2`` of the manuscript).

### Authors
* PREMACHE writing: Rosalie Vandromme and Thomas Grangeon
* Assistance in code formatting and GitHub deposit: Farid Smai, Théophile Guillon

### Licence
This toolbox is published under licence GNU GPL v3 - see the [licence file](licence.md) for more informations.