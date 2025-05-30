import numpy as np
import pandas as pd

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
        
    return start_time, start_value

def acceleration(force_max, bodyweight):
    acceleration = (force_max * 10) * bodyweight
    acceleration_round = round(acceleration, 2)

    return acceleration_round

