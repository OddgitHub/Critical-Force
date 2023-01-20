import csv
import numpy as np

class WorkoutHandler:

	def __init__(self, csvFile):
		self.allWorkouts = []
		self.startPause = 5		# This pause is automatically added at the beginning of the workout
		self.cntInDur = 3		# This is the count-in before a new activity starts

		with open(csvFile, mode='r') as csvFile:
			csvReader = csv.DictReader(csvFile, delimiter=';')
			for row in csvReader:
				self.allWorkouts.append(row)

	def getAllWorkouts(self):
		return self.allWorkouts

	def getLookupTable(self, workoutID):
		selectedWorkout = self.allWorkouts[workoutID]

		startPause  = self.startPause
		numSets     = int(selectedWorkout['Sets'])
		setPause    = int(selectedWorkout['Set Pause'])
		repsPerSet  = int(selectedWorkout['Repetitions'])
		repActive   = int(selectedWorkout['Repetition Active'])
		repPause    = int(selectedWorkout['Repetition Pause'])
		cntInDur	= self.cntInDur

		# TODO: Why is this necessary?
		assert(cntInDur <= startPause)
		assert(cntInDur <= setPause)
		#assert(cntInDur <= repPause)

		# Set duration without set pause
		setDur = repsPerSet * (repActive + repPause) - repPause

		# Total duration
		totalDur = numSets * (setDur + setPause) + startPause

		#======================================
		# Create look-up table for the workout 
		lookupTable = np.zeros(totalDur, dtype='int16')
		lookupTable[0:startPause] = 0
		repPattern = np.zeros(setDur, dtype='int16')

		countdown = np.zeros(totalDur, dtype='int16')
		countdown[0:startPause] = list(range(startPause,0,-1))
		cntPattern = np.zeros(setDur + setPause, dtype='int16')
		cntPattern[setDur:] = list(range(setPause,0,-1))

		for i in range(repsPerSet):
			repPattern[i*(repActive+repPause):(i*(repActive+repPause)+repActive)] = 1
			cntPattern[i*(repActive+repPause):(i*(repActive+repPause)+repActive)] = list(range(repActive,0,-1))
			if i < repsPerSet - 1:
				cntPattern[(i*(repActive+repPause)+repActive):(i*(repActive+repPause)+repActive+repPause)] = list(range(repPause,0,-1))

		for i in range(numSets):
			lookupTable[startPause + i*(setDur + setPause):startPause + i*(setDur + setPause) + setDur] = repPattern
			countdown[startPause + i*(setDur + setPause):startPause + i*(setDur + setPause) + setDur + setPause] = cntPattern

		return lookupTable, countdown

	def getTotalSetDuration(self, workoutID):
		selectedWorkout = self.allWorkouts[workoutID]

		startPause  = self.startPause
		numSets     = int(selectedWorkout['Sets'])
		setPause    = int(selectedWorkout['Set Pause'])
		repsPerSet  = int(selectedWorkout['Repetitions'])
		repActive   = int(selectedWorkout['Repetition Active'])
		repPause    = int(selectedWorkout['Repetition Pause'])

		# Set duration without set pause
		setDur = repsPerSet * (repActive + repPause) - repPause + setPause

		return setDur, numSets, setPause, startPause

	def getRepDurationInclPause(self, workoutID):
		selectedWorkout = self.allWorkouts[workoutID]
		repActive   = int(selectedWorkout['Repetition Active'])
		repPause    = int(selectedWorkout['Repetition Pause'])

		return repActive + repPause

	def getWorkoutDescription(self, workoutID):
		return self.allWorkouts[workoutID]['Description']

	def getWorkoutName(self, workoutID):
		return self.allWorkouts[workoutID]['Name']

	def getNumRepsPerSet(self, workoutID):
		return int(self.allWorkouts[workoutID]['Repetitions'])

	def getIdFromName(self, name):
		for i, workout in enumerate(self.allWorkouts):
			if workout['Name'] == name:
				return i

