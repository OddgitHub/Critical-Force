import numpy as np
from util.params import Params

def computeRepetitionMean(measData, lookupTable):
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

def computeCriticalForceAndWPrime(repetitionMean, repetitionDuration):
    # Remove zeros and duplicates
    mean = repetitionMean[repetitionMean.nonzero()]
    b1 = np.append(mean[1:], 0)
    mean = mean[mean != b1]

    # Take the last 6 measurements to compute the critical force
    cf = np.mean(mean[-6:])

    # Compute W'
    numSamples = len(mean)
    W = (np.sum(mean) - numSamples * cf) * repetitionDuration

    return cf, W

def computeMaxForce(repetitionMean):
    return np.around(np.max(repetitionMean), decimals=2)

