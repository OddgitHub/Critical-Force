
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QAction
from ui.MeasurementGui import Ui_Form
from util.repeatedTimer import RepeatedTimer
from util.params import Params
from playsound import playsound
import numpy as np
import os

from threading import Thread
from threading import Event

# Set environment variable for MCP2221A
try:
    os.environ['BLINKA_MCP2221']
except:
    # set BLINKA_MCP2221=1
    os.environ['BLINKA_MCP2221']='1'

import board
from analogio import AnalogIn

from workout_config.workouts import WorkoutHandler

class MeasurementCtrl(QWidget):
    def __init__(self):
        super().__init__()        

        form = Ui_Form()
        form.setupUi(self)

        # Get access to the ADC
        self.adc = AnalogIn(board.G1)

        #========================================
        # Init class member variables
        #========================================   
        self.fsSensor = Params.fsSensor.value
        self.running = False
        self.lookupTable = 0
        self.countdown = 0
        self.measData = 0
        self.numMeasSamples = 0
        self.measCnt = 0
        self.secCnt = 0

        #========================================
        # Connect signals
        #========================================     
        form.startButton.pressed.connect(self.onStartMeasurement)
        form.stopButton.pressed.connect(self.onStopMeasurement)
        form.taraButton.pressed.connect(self.onTaraButtonClicked)

        #========================================
        # Make some gui elements class members   
        #========================================     
        self.workoutDescriptionLabel = form.workoutDescriptionLabel
        self.timerLabel = form.timerLabel
        self.weightSpinBox = form.bodyWeightSpinBox

        #========================================
        # Workout handling
        #========================================
        self.workoutComboBox = form.workoutComboBox
        self.workoutComboBox.currentIndexChanged.connect( self.onWorkoutChanged )
        self.selectedWorkoutId = 0

        #workoutCfgPath = ('./workout_config/workouts.csv')
        self.workoutHandler = WorkoutHandler(Params.workoutCfgPath.value)
        self.workouts = self.workoutHandler.getAllWorkouts()

        for workout in self.workouts:
            self.workoutComboBox.addItem(workout['Name'])

        # Action, triggered when measurement is finished
        self.measFinished = QAction("Finished", self)
        self.measFinished.triggered.connect(self.onStopMeasurement)

        #========================================
        # Audio handling
        #========================================
        self.stopAudioThreadEvent = Event()
        self.playSndHiEvent = Event()
        self.playSndLoEvent = Event()

    def onAudioPlayback(self, stopEvent, playHi, playLo):
        while(True):
            if stopEvent.is_set():
                stopEvent.clear()
                break
            if playHi.is_set():
                playHi.clear()
                playsound(Params.fileClickHi.value)
            if playLo.is_set():
                playLo.clear()
                playsound(Params.fileClickLo.value)

    def onStartMeasurement(self):
        if not self.running:
            self.lookupTable, self.countdown = self.workoutHandler.getLookupTables(self.selectedWorkoutId)
            self.numMeasSamples = len(self.lookupTable) * self.fsSensor
            self.measData = np.zeros(self.numMeasSamples)
            self.workoutComboBox.setEnabled(False)
            self.weightSpinBox.setEnabled(False)
            self.audioThread = Thread(target=self.onAudioPlayback, args=(self.stopAudioThreadEvent, self.playSndHiEvent, self.playSndLoEvent))
            self.audioThread.start()
            self.measurementTimer = RepeatedTimer(1/self.fsSensor, self.onMeasurementCallback)
            self.running = True

    def onStopMeasurement(self):
        if self.running:
            self.measurementTimer.stop()
            self.stopAudioThreadEvent.set()
            self.audioThread.join()
            self.measCnt = 0
            self.secCnt = 0
            self.timerLabel.setText('Stopped')
            self.timerLabel.setStyleSheet("background-color: none")
            self.workoutComboBox.setEnabled(True)
            self.weightSpinBox.setEnabled(True)
            self.running = False

    def onTaraButtonClicked(self):
        print("Tara button clicked.")

    def onWorkoutChanged(self, id):
        self.workoutDescriptionLabel.setText(self.workouts[id]["Description"])
        self.selectedWorkoutId = id

    def onMeasurementCallback(self):
        secCnt = self.secCnt

        # Read ADC value and save it to array
        raw = self.adc.value
        self.measData[self.measCnt] = self.getVoltage(raw)
        print(str(self.measData[self.measCnt])) # TODO

        # Workout timer handling
        if self.measCnt % self.fsSensor == 0:
            if self.lookupTable[secCnt] == 1:
                self.timerLabel.setText(str(self.countdown[secCnt]) + ' sec\nWork')
                self.timerLabel.setStyleSheet("background-color: red")
            else:
                self.timerLabel.setText(str(self.countdown[secCnt]) + ' sec\nPause')
                self.timerLabel.setStyleSheet("background-color: lightgreen")

            if secCnt > 0:
                if (self.lookupTable[secCnt] > self.lookupTable[secCnt-1]):
                    self.playSndHiEvent.set()
                elif (self.lookupTable[secCnt] < self.lookupTable[secCnt-1]) or (self.countdown[secCnt] < 4 and self.lookupTable[secCnt] == 0):
                    self.playSndLoEvent.set()

            self.secCnt += 1 	# Increase timer counter
        self.measCnt += 1		# Increase measurement counter

        # Measurement finished
        if self.measCnt == self.numMeasSamples:
            self.measFinished.trigger()

    @staticmethod
    def getVoltage(raw):
        return (raw * 3.3) / 65536