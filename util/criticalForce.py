'''
    Software to measure climbing specific finger strength measures, such as Critical Force.
    Copyright 2023 Dr.-Ing. Philipp Bulling
	
	This file is part of "Critical Force".

    "Critical Force" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "Critical Force" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with "Critical Force".  If not, see <http://www.gnu.org/licenses/>.
'''

import numpy as np

def computeRepetitionMean(measData, lookupTable, sampleRate):
    lookupRsmpl = np.repeat(lookupTable, sampleRate)

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
    if sum(repetitionMean) == 0:
        return 0, 0

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

