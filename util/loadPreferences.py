from util.params import Params
import json

def loadPreferences():
    try:
        # Load, if preferences file is available
        with open(Params.preferencesFile.value, 'r') as f:
            preferences = json.load(f)
            f.close()
    except:
        # Set to default values otherwise
        preferences = {}
        preferences['fsMeasurement'] = Params.fsMeasurementDefault.value
        preferences['delayCompensation'] = Params.delayCompensationDefault.value
    
    return preferences