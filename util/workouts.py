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

import csv, sys
import numpy as np
from PySide6.QtWidgets import QMessageBox

class WorkoutHandler:

	def __init__(self, csvFile):
		self.allWorkouts = []
		self.startPause = 5		# This pause is automatically added at the beginning of the workout
		self.cntInDur = 3		# This is the count-in before a new activity starts

		try:
			with open(csvFile, mode='r') as csvFile:
				csvReader = csv.DictReader(csvFile, delimiter=';')
				for row in csvReader:
					self.allWorkouts.append(row)
		except:
			msg = QMessageBox()
			msg.setWindowTitle("Warning")
			msg.setIcon(QMessageBox.Warning)
			msg.setText("Could not find the file \"workouts.csv\"!\nPlease ensure that this file exists in the subfolder \"settings\". The application can't start without this file.")
			msg.exec_()	
			sys.exit()
			
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

	def getNumSetsReps(self, workoutID):
		return int(self.allWorkouts[workoutID]['Sets']), int(self.allWorkouts[workoutID]['Repetitions'])

	def getIdFromName(self, name):
		for i, workout in enumerate(self.allWorkouts):
			if workout['Name'] == name:
				return i

