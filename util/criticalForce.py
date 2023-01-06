import numpy as np
from scipy.signal import medfilt
from util.params import Params
import matplotlib.pyplot as plt

def computeCriticalForce(measData, lookupTable):
    fsMeas = Params.fsMeasurement.value
    lookupRsmpl = np.repeat(lookupTable, fsMeas)

    assert(len(measData) == len(lookupRsmpl))
    numSamples = len(lookupRsmpl)
    result = np.zeros(numSamples)

    sum = 0
    ctr = 0
    indStart = 0
    active = False

    for i in range(1,numSamples):
        diff = lookupRsmpl[i] - lookupRsmpl[i-1]

        if diff == 1:
            # New Active Time begins
            indStart = i
            active = True
        elif diff == -1:
            # New pause begins
            result[indStart:indStart+ctr] = sum/ctr
            ctr = 0
            sum = 0
            active = False
        
        # Nothing changed
        if active:
            sum += measData[i]
            ctr += 1

    return result
