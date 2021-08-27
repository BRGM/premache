import yaml

def load_data(filename):
    yaml_file = open(filename, 'r')
    db = yaml.safe_load(yaml_file)

    DirInputs =db['DirInputs']
    DirOutputs = db['DirOutputs']
    DataSpreadsheet = db['DataSpreadsheet']
    FilePlots= db['FilePlots']
    DataPlots = db['DataPlots'] 
    RasterNoDataValue = db['RasterNoDataValue']
    DataRainfall = db['DataRainfall']
    DataRainfallEvent = db['DataRainfallEvent']

    return DirInputs, DirOutputs, DataSpreadsheet, FilePlots, DataPlots, RasterNoDataValue, DataRainfall, DataRainfallEvent