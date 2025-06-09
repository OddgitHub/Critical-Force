import numpy as np
from ui import MeasurementCtrl

def find_monotonic_rise_start(force_data):
    peak_index = np.argmax(force_data)
    for i in range(peak_index - 1, 0, -1):
        if force_data[i] < force_data[i - 1]:
            start_index = i
            break
    else:
        start_index = 0
    return start_index

def analyse_measurements(force_data, sampling_rate=10):
    force_data = np.array(force_data)
    start_idx = find_monotonic_rise_start(force_data)

    start_time = round(start_idx / sampling_rate, 2)
    start_value = round(force_data[start_idx], 2)       
        
    return start_value, start_time

def acceleration(force_max, bodyweight):
    acceleration = (force_max * 10)/bodyweight
    acceleration_round = round(acceleration, 2)

    return acceleration_round

def RFD(startofpullingtimepoint, maxforcetimepoint, maxforce, startpullingpointforce):
    rfd = (maxforce - startpullingpointforce) / (maxforcetimepoint - startofpullingtimepoint)

    return rfd

def computeSchnellkraftParameter(measData, lookupTable, sampleRate, bodyweight):
    #cpmoute RFD and max. acceleration
    t = np.linspace(0, len(measData) / sampleRate, len(measData))
    peak_alltime = np.max(measData)
    peak_timepoint_alltime = t[np.argmax(measData)]
    max_force_in_kg_alltime = (peak_alltime / 100) * bodyweight
    startpointpullingvalue_alltime, startpointpulling_timepoint_alltime = analyse_measurements(measData)

    
    #acceleration
    max_acceleration = acceleration(max_force_in_kg_alltime, bodyweight)

    #RFD
    rfd_value = RFD(startpointpulling_timepoint_alltime, peak_timepoint_alltime, peak_alltime, startpointpullingvalue_alltime)
    
    #compute Startingpoints and max. peaks
    lookupRsmpl = np.repeat(lookupTable, sampleRate)
    assert len(measData) == len(lookupRsmpl)
    numSamples = len(lookupRsmpl)

    indStart = 0

    allPeaks = []
    allPeaks_timepoint = []
    allStartingpoints = []
    allStartingpoints_timepoint = []

    for i in range(1, numSamples):
        diff = lookupRsmpl[i] - lookupRsmpl[i-1]

        if diff == 1:
            # New Active Time begins
            indStart = i

        elif diff == -1:
            # Active Time endet → hier auswerten
            segment = measData[indStart:i]
            # Peak
            local_peak = np.max(segment)
            local_peak_idx = np.argmax(segment)
            allPeaks.append(local_peak)
            allPeaks_timepoint.append(t[indStart + local_peak_idx])

            # Start-Zeitpunkt
            sp_val, sp_time = analyse_measurements(segment, sampling_rate=sampleRate)
            allStartingpoints.append(sp_val)
            sp_time_abs = indStart/sampleRate + sp_time
            allStartingpoints_timepoint.append(round(sp_time_abs, 2))

    return allPeaks, allPeaks_timepoint, allStartingpoints, \
           allStartingpoints_timepoint, max_acceleration, rfd_value
