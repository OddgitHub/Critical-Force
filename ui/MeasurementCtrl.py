
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QAction
import pyqtgraph as pg
from playsound import playsound
import numpy as np
import time, datetime

from threading import Thread
from threading import Event

from ui.MeasurementGui import Ui_Form
from util.repeatedTimer import RepeatedTimer
from util.params import Params
from util.workouts import WorkoutHandler
from util.criticalForce import computeRepetitionMean, computeCriticalForceAndWPrime, computeMaxForce

class MeasurementCtrl(QWidget):
    def __init__(self, weightSensor):
        super().__init__()        

        form = Ui_Form()
        form.setupUi(self)

        self.weightSensor = weightSensor

        #========================================
        # Init class members
        #========================================   
        self.fsMeas = Params.fsMeasurement.value
        self.running = False
        self.lookupTable = 0
        self.countdown = 0
        self.numMeasSamples = 0
        self.measCnt = 0
        self.secCnt = 0
        self.currentWeight = 0
        self.tare = 0

        # Data that will be stored in result file
        self.measDataKg = np.asarray([])
        self.timestamp = 'unknown'
        self.bodyWeight = form.bodyWeightSpinBox.value()
        self.criticalForce = 0
        self.wPrime = 0
        self.maxForce = 0

        #========================================
        # Connect signals
        #========================================     
        form.startButton.pressed.connect(self.onStartMeasurement)
        form.stopButton.pressed.connect(self.onStopMeasurement)
        form.tareButton.pressed.connect(self.onTareButtonClicked)
        form.bodyWeightSpinBox.valueChanged.connect(self.onBodyWeightChanged)

        # Action, triggered when measurement is finished
        self.measFinished = QAction("Finished", self)
        self.measFinished.triggered.connect(self.onStopMeasurement)

        #========================================
        # Make some gui elements class members   
        #========================================     
        self.workoutDescriptionLabel = form.workoutDescriptionLabel
        self.workoutComboBox = form.workoutComboBox
        self.workoutLabel = form.workoutLabel
        self.weightSpinBox = form.bodyWeightSpinBox
        self.graphicsView = form.graphicsView
        self.tareButton = form.tareButton
        self.tareLabel = form.tareLabel

        self.graphicsView.setBackground('w')

        #========================================
        # Workout handling
        #========================================
        self.selectedWorkoutId = 0
        self.workoutComboBox.currentIndexChanged.connect( self.onWorkoutChanged )

        self.workoutHandler = WorkoutHandler(Params.workoutCfgFile.value)

        for workout in self.workoutHandler.getAllWorkouts():
            self.workoutComboBox.addItem(workout['Name'])
        
        self.workoutName = self.workoutHandler.getWorkoutName(self.selectedWorkoutId)

        #========================================
        # Audio handling
        #========================================
        self.stopAudioThreadEvent = Event()
        #######################################################################
        # TODO: Do it like this, as soon as PySide6.5.0 is available:
        #self.soundHi = QSoundEffect(parent) # parent = MainWindow
        #self.soundHi.setSource(QUrl.fromLocalFile(Params.fileClickHi.value))
        #self.soundHi.setVolume(1.0)
        #######################################################################
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
            time.sleep(0.001) # Necessary to reduce priority of this thread?!

    def onStartMeasurement(self):
        if not self.running:
            self.tareTimer.stop()
            self.numMeasSamples = len(self.lookupTable) * self.fsMeas
            self.measDataKg = np.zeros(self.numMeasSamples)

            self.workoutComboBox.setEnabled(False)
            self.weightSpinBox.setEnabled(False)
            self.tareButton.setEnabled(False)

            self.audioThread = Thread(target=self.onAudioPlayback, args=(self.stopAudioThreadEvent, self.playSndHiEvent, self.playSndLoEvent))
            self.audioThread.start()
            self.measurementTimer = RepeatedTimer(1/self.fsMeas, self.onMeasurementCallback)
            self.running = True

    def onStopMeasurement(self):
        if self.running:
            self.measurementTimer.stop()
            self.stopAudioThreadEvent.set()
            self.audioThread.join()
            self.running = False

            self.measCnt = 0
            self.secCnt = 0
            self.workoutLabel.setText('Stopped')
            self.workoutLabel.setStyleSheet("background-color: none")
            self.workoutName = self.workoutHandler.getWorkoutName(self.selectedWorkoutId)
            
            self.workoutComboBox.setEnabled(True)
            self.weightSpinBox.setEnabled(True)
            self.tareButton.setEnabled(True)

            self.tareTimer = RepeatedTimer(1/self.fsMeas, self.onTareVisualization)

            self.timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.computeResultAndPlot()

    def onMeasurementCallback(self):
        secCnt = self.secCnt

        if self.measCnt >= self.numMeasSamples:
            # Measurement finished
            self.measFinished.trigger()
        else:
            # Read value from sensor and save it to array
            valueKg = self.weightSensor.getValueInKg() - self.tare
            self.tareLabel.setText(str(np.around(valueKg, decimals=2)) + 'kg')
            self.measDataKg[self.measCnt] = valueKg

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

                # Increase timer counter
                self.secCnt += 1

            # Increase measurement counter
            self.measCnt += 1	

    def onTareVisualization(self):
        self.currentWeight = self.weightSensor.getValueInKg()
        weightString = str(np.around(self.currentWeight - self.tare, decimals=2))
        self.tareLabel.setText(weightString + 'kg')

    def onTareButtonClicked(self):
        self.tare = self.currentWeight

    def onWorkoutChanged(self, id):
        self.workoutDescriptionLabel.setText(self.workoutHandler.getWorkoutDescription(id))
        self.lookupTable, self.countdown = self.workoutHandler.getLookupTable(id)
        self.selectedWorkoutId = id

    def onBodyWeightChanged(self, value):
        self.bodyWeight = value
        if len(self.measDataKg) > 0:
            self.computeResultAndPlot()

    def onCloseApplication(self):
        self.onStopMeasurement()
        self.tareTimer.stop()

    #========================================
    # Plot the result of the testing
    #========================================
    def computeResultAndPlot(self):
        # Compute result (force as percentage of body weight)
        measDataPercentBw = self.measDataKg / self.bodyWeight * 100

        # Compensate delay between audio clicks and measurement
        delayInSamples = round(Params.delayCompensation.value/1000 * self.fsMeas)
        measDataPercentBw = np.roll(measDataPercentBw, -delayInSamples)
        measDataPercentBw[-delayInSamples:] = 0

        # Compute the mean force during repetition active times
        repMean = computeRepetitionMean(measDataPercentBw, self.lookupTable)
        
        # Prepare plot
        t = np.linspace(0, len(measDataPercentBw) / self.fsMeas, len(measDataPercentBw))
        self.graphicsView.clear()
        self.graphicsView.addLegend().anchor(itemPos=(1,0), parentPos=(1,0), offset=(-10,10))

        # Plot raw measurement data
        pen = pg.mkPen(color=(150,150,150), width=2)
        self.graphicsView.plot(t, measDataPercentBw, name="Raw Data", pen=pen)

        # Plot mean of each repetition block
        pen = pg.mkPen(color=(80,80,80), width=2)
        self.graphicsView.plot(t, repMean, name="Rep. Mean", pen=pen)

        # Compute the critical force, if necessary
        cf = 0
        W = 0
        if self.workoutHandler.getWorkoutName(self.selectedWorkoutId) == 'Critical Force Test':
            # Plot critical force
            repDur = self.workoutHandler.getRepDurationInclPause(self.selectedWorkoutId)
            cf, W = computeCriticalForceAndWPrime(repMean, repDur)
            cf = np.around(cf, decimals = 2)
            W = np.around(W, decimals = 2)

            pen = pg.mkPen(color=(0,180,0), width=2)
            self.graphicsView.plot([t[0],t[-1]], [cf,cf], name="CF = " + str(cf) + " %BW | W\' = " + str(W) + " %BWs", pen=pen)

        # Plot maximum force
        pen = pg.mkPen(color=(180,0,0), width=2)
        mf = computeMaxForce(repMean)
        self.graphicsView.plot([t[0],t[-1]], [mf,mf], name="Max. Force = " + str(mf) + " %BW", pen=pen)

        self.graphicsView.showGrid(x=True, y=True)
        self.graphicsView.setLabel('left', "%BW")
        self.graphicsView.setLabel('bottom', "Time [sec]")

        # Store result in class member variables
        self.criticalForce = float(cf)
        self.wPrime = float(W)
        self.maxForce = float(mf)

    #========================================
    # Get/set functions
    #========================================
    def getData(self):
        data = {}
        data['weight'] = self.bodyWeight
        data['workout'] = self.workoutName
        data['timestamp'] = self.timestamp
        data['criticalForce'] = self.criticalForce
        data['wPrime'] = self.wPrime
        data['maxForce'] = self.maxForce
        data['measDataKg'] = self.measDataKg.tolist()
        return data

    def setData(self, data):
        workoutId = self.workoutHandler.getIdFromName(data['workout'])
        self.workoutComboBox.setCurrentIndex(workoutId)
        self.workoutName = data['workout']
        self.timestamp = data['timestamp']
        self.measDataKg = np.asarray(data['measDataKg'])

        # The order is critical, always do this at the end
        self.weightSpinBox.setValue(data['weight'])

        # Since critical force, W' and max force will be re-calculated in 
        # this function, it's not necessary to load them here.
        self.computeResultAndPlot()
