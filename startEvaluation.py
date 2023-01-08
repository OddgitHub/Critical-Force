from util.workouts import WorkoutHandler
import os, csv, re
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import filtfilt

print('\n---------------------------')
print('Available workout results: ')
print('---------------------------')

# Print available workout results
allResults = os.listdir('results')
for i, file in enumerate(allResults):
    if file.endswith('.csv'):
        print(str(i) + ' - ' + file)

selectedFile = 'results\\' + allResults[int(input('\nPlease select a workout: '))]

# Load results file
with open(selectedFile, mode='r') as csvFile:
    csvReader = csv.DictReader(csvFile, delimiter=';')
    row = next(csvReader)

emgSignal = np.load(row['Data'])
workoutID = int(row['Workout ID'])
fsSensor = int(row['Sample Rate'])

# Load corresponding workout
workoutCfgPath = ('./workout_config/workouts.csv')
workoutHandler = WorkoutHandler(workoutCfgPath)
lookupTable  = workoutHandler.getLookupTable(workoutID)[0]
setDur, numSets, setPause, startPause = workoutHandler.getTotalSetDuration(workoutID)

# Filter EMG signal
#filterOrd = 20
#emgSignal = filtfilt(np.divide(np.ones(filterOrd), filterOrd), 1, emgSignal)

emgSignalSetWise = np.zeros((setDur * fsSensor, numSets))
for i in range(numSets):
    emgSignalSetWise[:,i] = emgSignal[fsSensor * (startPause + i*setDur):fsSensor * (startPause + i*setDur + setDur)]

    ###################################################################################
    # TODO: Mittelwert über aktive Zeit / Pause für jedes Set berechnen und auswerten?
    ###################################################################################

#====================
# Plot total workout
plt.figure(num=None, figsize=(15, 12), dpi=80, facecolor='w', edgecolor='k')
sp1 = plt.subplot(3,1,1)
plt.plot(np.divide(list(range(len(emgSignal))), fsSensor), emgSignal)
plt.grid()
plt.title('EMG signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [V]')

plt.subplot(3,1,2, sharex=sp1)
plt.plot(list(range(len(lookupTable))), lookupTable)
plt.grid()
plt.title('Timer')
plt.xlabel('Time [s]')
plt.ylabel('Pause | Active')

#===========
# Plot sets
plt.subplot(3,1,3)
hPlot = []
for i in range(numSets):
    [curPlot] = plt.plot(np.divide(list(range(emgSignalSetWise.shape[0])), fsSensor), emgSignalSetWise[:,i], label='Set No. ' + str(i+1))
    hPlot.append(curPlot)

plt.legend(hPlot)
plt.grid()
plt.show()
