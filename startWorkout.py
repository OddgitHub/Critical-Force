from repeatedTimer import RepeatedTimer
from workout_config.workouts import WorkoutHandler
import time, csv, random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from playsound import playsound

#=======================================================
# If no board is connected, script is in debugging mode
try:
	import board
	from analogio import AnalogIn
	myoWareSensor = AnalogIn(board.G1)
	DEBUG = False
except:
	class myoWareSensorDummy:
		def __init__(self):
			random.seed(2)
		def value(self):
			return int(random.random() * 65536)
	myoWareSensor = myoWareSensorDummy()
	DEBUG = True

#==================
# Global variables
secCnt = 0
mesCnt = 0
emgSignal = []
playSndHi = False
playSndLo = False

#==============================
# Callback for the measurement
# TODO: Are the arguments really necessary?
def measurementCallback(myoWareSensor, fsSensor):
	global emgSignal, mesCnt, secCnt
	global playSndHi, playSndLo

	if DEBUG:
		raw = myoWareSensor.value()
	else:	
		raw = myoWareSensor.value
	emgSignal.append(getVoltage(raw))

	# Process the timer within the measurement callback
	if mesCnt % fsSensor == 0:
		if lookupTable[secCnt] == 1:
			print('Active ' + countdown[secCnt])
		else:
			print('Pause ' + countdown[secCnt])

		if secCnt > 0:
			if (lookupTable[secCnt] > lookupTable[secCnt-1]):
				playSndHi = True 
			elif (lookupTable[secCnt] < lookupTable[secCnt-1]) or countin[secCnt] == 1:
				playSndLo = True 

		secCnt += 1 	# Increase timer counter
	mesCnt += 1			# Increase measurement counter

#=========================================
# Function to convert AD-value to voltage
def getVoltage(raw):
	return (raw * 3.3) / 65536

#======================
# Initialize variables
fsTimer = 1		# Sample rate timer
fsSensor = 10	# Sample rate sensor

#===============
# Start program
workoutCfgPath = ('./workout_config/workouts.csv')
workoutHandler = WorkoutHandler(workoutCfgPath)
workouts = workoutHandler.getAllWorkouts()

#==============================
# Ask user to select a workout
print('\n\n-------------------')
print('Available Workouts:')
print('-------------------')

for i, workout in enumerate(workouts):
	print(str(i) + ' - ' + workout['Name'] + ': ' + workout['Description'])

selectedWorkoutId = int(input('\nPlease select a workout: '))
selectedWorkoutName = workouts[selectedWorkoutId]['Name']
lookupTable, countdown, countin = workoutHandler.getLookupTables(selectedWorkoutId)
totalDur = len(lookupTable)
countdown = countdown.astype(str)

#===================
# Start measurement
playsound('raw/clickhi.wav')
secCnt = 0
measurement = RepeatedTimer(1/fsSensor, measurementCallback, *(myoWareSensor, fsSensor))

#================================
# Wait until workout is finished
# @TODO: Probably not the best way to do this...
while(mesCnt != totalDur * fsSensor):
	if playSndHi:
		playsound('raw/clickhi.wav')
		playSndHi = False
	if playSndLo:
		playsound('raw/clicklo.wav')
		playSndLo = False
		

#============================
# Stop timer and measurement
measurement.stop()
playsound('raw/clicklo.wav')

#===============================
# Save the result in a csv-File
wantToSave = input('\nDo you want to save the results [y/n]: ')

if wantToSave == 'y':
	# Get some user data
	name = input('\n\nName: ')
	age = input('\nAge: ')
	weight = input('\nWeight [kg]: ')
	gender = input('\nGender [m/f]: ')
	maxRoute = input('\nMaximum route grade [French]: ')
	maxBoulder = input('\nMaximum boulder grade [Fb]: ')
	maxLoad = input('\nMaximum added load on a 20mm edge [kg]: ')
	comment = input('\nComment: ')

	d = datetime.now()
	dateTimeStr = d.strftime('%Y') + d.strftime('%m') + d.strftime('%d') + '_' + d.strftime('%H') + d.strftime('%M')
	resultFile = 'results\\' + dateTimeStr + '_' + name
	np.save(resultFile, np.asarray(emgSignal))
	with open(resultFile + '.csv', 'w', newline='') as csvfile:
		row = {'Date': dateTimeStr,
			   'Name': name,
			   'Workout ID': str(selectedWorkoutId),
			   'Workout Name': selectedWorkoutName,
			   'Age': age,
			   'Weight': weight,
			   'Gender': gender,
			   'Max Route': maxRoute,
			   'Max Boulder': maxBoulder,
			   'Max Load': maxLoad,
			   'Comment': comment,
			   'Sample Rate': str(fsSensor),
			   'Data': resultFile + '.npy'}
		writer = csv.DictWriter(csvfile, fieldnames=row.keys(), delimiter = ';')
		writer.writeheader()  
		writer.writerow(row)

#===========================
# Plot EMG signal and timer
plt.figure(num=None, figsize=(15, 12), dpi=80, facecolor='w', edgecolor='k')
sp1 = plt.subplot(2,1,1)
plt.plot(np.divide(list(range(len(emgSignal))), fsSensor), emgSignal)
plt.grid()
plt.title('EMG signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [V]')

plt.subplot(2,1,2, sharex=sp1)
plt.plot(np.divide(list(range(len(lookupTable))), fsTimer), lookupTable)
plt.grid()
plt.title('Timer')
plt.xlabel('Time [s]')
plt.ylabel('Pause | Active')
plt.show()