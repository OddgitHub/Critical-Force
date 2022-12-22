
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
        self.fsMeas = Params.fsMeasurement.value
        self.running = False
        self.lookupTable = 0
        self.countdown = 0
        self.rawMeasData = []
        self.measDataPercentBW = []
        self.numMeasSamples = 0
        self.measCnt = 0
        self.secCnt = 0
        self.currentWeight = 0
        self.tare = 0
        self.bodyWeight = form.bodyWeightSpinBox.value()

        #========================================
        # Connect signals
        #========================================     
        form.startButton.pressed.connect(self.onStartMeasurement)
        form.stopButton.pressed.connect(self.onStopMeasurement)
        form.tareButton.pressed.connect(self.onTareButtonClicked)
        form.bodyWeightSpinBox.valueChanged.connect(self.onBodyWeightChanged)

        #========================================
        # Make some gui elements class members   
        #========================================     
        self.workoutDescriptionLabel = form.workoutDescriptionLabel
        self.workoutLabel = form.workoutLabel
        self.weightSpinBox = form.bodyWeightSpinBox
        self.graphicsView = form.graphicsView
        self.tareButton = form.tareButton
        self.tareLabel = form.tareLabel

        #========================================
        # Workout handling
        #========================================
        self.selectedWorkoutId = 0
        self.workoutComboBox = form.workoutComboBox
        self.workoutComboBox.currentIndexChanged.connect( self.onWorkoutChanged )

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

        # Start a timer that is only used for the tare display
        self.tareTimer = RepeatedTimer(1/self.fsMeas, self.onTareVisualization)

    #========================================
    # Callback functions
    #========================================
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
            self.tareTimer.stop()
            self.lookupTable, self.countdown = self.workoutHandler.getLookupTables(self.selectedWorkoutId)
            self.numMeasSamples = len(self.lookupTable) * self.fsMeas
            self.rawMeasData = np.zeros(self.numMeasSamples)

            self.workoutComboBox.setEnabled(False)
            self.weightSpinBox.setEnabled(False)
            self.tareButton.setEnabled(False)
            self.tareLabel.setEnabled(False)

            self.audioThread = Thread(target=self.onAudioPlayback, args=(self.stopAudioThreadEvent, self.playSndHiEvent, self.playSndLoEvent))
            self.audioThread.start()
            self.measurementTimer = RepeatedTimer(1/self.fsMeas, self.onMeasurementCallback)
            self.running = True

    def onStopMeasurement(self):
        self.tareTimer.stop()
        if self.running:
            self.measurementTimer.stop()
            self.stopAudioThreadEvent.set()
            self.audioThread.join()
            self.running = False

            self.measCnt = 0
            self.secCnt = 0
            self.workoutLabel.setText('Stopped')
            self.workoutLabel.setStyleSheet("background-color: none")
            
            self.workoutComboBox.setEnabled(True)
            self.weightSpinBox.setEnabled(True)
            self.tareButton.setEnabled(True)
            self.tareLabel.setEnabled(True)

            self.tareTimer = RepeatedTimer(1/self.fsMeas, self.onTareVisualization)

            self.computeResultAndPlot(self.rawMeasData)

    def onMeasurementCallback(self):
        secCnt = self.secCnt

        # Read ADC value and save it to array
        self.rawMeasData[self.measCnt] = self.adc.value

        # Workout timer handling
        if self.measCnt % self.fsMeas == 0:
            if self.lookupTable[secCnt] == 1:
                self.workoutLabel.setText(str(self.countdown[secCnt]) + ' sec\nWork')
                self.workoutLabel.setStyleSheet("background-color: red")
            else:
                self.workoutLabel.setText(str(self.countdown[secCnt]) + ' sec\nPause')
                self.workoutLabel.setStyleSheet("background-color: lightgreen")

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

    def onTareVisualization(self):
        self.currentWeight = self.convertAdcValueToWeight(self.adc.value)
        weightString = str(np.around(self.currentWeight - self.tare, decimals=2))
        self.tareLabel.setText(weightString + 'kg')

    def onTareButtonClicked(self):
        self.tare = self.currentWeight

    def onWorkoutChanged(self, id):
        self.workoutDescriptionLabel.setText(self.workouts[id]["Description"])
        self.selectedWorkoutId = id

    def onBodyWeightChanged(self, value):
        self.bodyWeight = value
        if len(self.rawMeasData) > 0:
            self.computeResultAndPlot(self.rawMeasData)

    #========================================
    # Helper functions
    #========================================
    def getVoltage(self, raw):
        return (raw * 3.3) / 65536

    def convertAdcValueToWeight(self, raw):
        return self.getVoltage(raw) * -5 # TODO: atm only dummy!!

    def computeResultAndPlot(self, rawData):
        # Compute result (force as percentage of body weight)...
        self.measDataPercentBW = (self.convertAdcValueToWeight(rawData) - self.tare) / self.bodyWeight * 100

        # ...and plot
        t = np.linspace(0, len(self.measDataPercentBW) / self.fsMeas, len(self.measDataPercentBW))
        self.graphicsView.clear()
        self.graphicsView.plot(t, self.measDataPercentBW)
        self.graphicsView.showGrid(x=True, y=True)
        self.graphicsView.setLabel('left', "% BW")
        self.graphicsView.setLabel('bottom', "Time [sec]")