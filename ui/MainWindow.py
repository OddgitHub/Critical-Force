from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QStatusBar, QTabWidget, QFileDialog, QMessageBox
from datetime import date
import os, json

from util.params import Params
from util.sensor import WeightSensor

from ui.MeasurementCtrl import MeasurementCtrl
from ui.DataCtrl import DataCtrl
from ui.CompareresultCtrl import CompareresultCtrl
from ui.CalibrationCtrl import CalibrationCtrl
from ui.PreferencesCtrl import PreferencesCtrl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #========================================
        # Basic window properties
        #========================================
        self.setWindowTitle(Params.appName.value)
        self.setMinimumSize(500, 500)
        self.setStatusBar(QStatusBar(self))

        #========================================
        # Start the weight sensor
        #========================================
        self.weightSensor = WeightSensor()

        #========================================
        # Actions
        #========================================
        newAction = QAction("New Measurement", self, shortcut="Ctrl+n")
        newAction.setStatusTip("Create a new measurement. Remember to save your current measurement first.")
        newAction.triggered.connect(self.onNewActionClicked)

        saveAction = QAction("Save Measurement As...", self, shortcut="Ctrl+s")
        saveAction.setStatusTip("Save the current measurement to in a result file.")
        saveAction.triggered.connect(self.onSaveActionClicked)

        loadAction = QAction("Load Measurement...", self)
        loadAction.setStatusTip("Load previously measured data.")
        loadAction.triggered.connect(self.onLoadActionClicked)

        calibrationAction = QAction("Calibration", self)
        calibrationAction.setStatusTip("Calibrate the load-cell.")
        calibrationAction.triggered.connect(self.onCalibrationActionClicked)

        preferencesAction = QAction("Preferences", self)
        preferencesAction.setStatusTip("Advanced user preferences.")
        preferencesAction.triggered.connect(self.onPreferencesActionClicked)

        #========================================
        # Build the gui
        #========================================
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(False)
        
        # Measurement page
        self.measTab = MeasurementCtrl(self.weightSensor)
        tabs.addTab(self.measTab, "Measurement")

        # Personal data page
        self.dataTab = DataCtrl()
        tabs.addTab(self.dataTab, "Personal Data")

        # Compare results page
        compareTab = CompareresultCtrl()
        tabs.addTab(compareTab, "Compare Results")

        self.setCentralWidget(tabs)
        
        #========================================
        # Menu
        #========================================
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(newAction)
        file_menu.addSeparator()
        file_menu.addAction(loadAction)
        file_menu.addAction(saveAction)

        settings_menu = menu.addMenu("&Settings")
        settings_menu.addAction(calibrationAction)
        settings_menu.addAction(preferencesAction)

    #========================================
    # Callbacks
    #========================================
    def onNewActionClicked(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Create new measurement")
        msg.setText("Unsaved data will be lost. Do you want to continue?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setIcon(QMessageBox.Question)
        button = msg.exec_()

        if button == QMessageBox.Yes:
            personalDataDict = {}
            personalDataDict['name'] = ''
            personalDataDict['age'] = 0
            personalDataDict['gender'] = 'm'
            personalDataDict['height'] = 0
            personalDataDict['span'] = 0
            personalDataDict['routeGrade'] = 'n/a'
            personalDataDict['boulderGrade'] = 'n/a'
            personalDataDict['email'] = ''
            personalDataDict['comment'] = ''
            self.dataTab.setData(personalDataDict)

            measurementDataDict = {}
            measurementDataDict['weight'] = 70
            measurementDataDict['workout'] = 'Critical Force Test'
            measurementDataDict['timestamp'] = 'unknown'
            measurementDataDict['criticalForce'] = 0
            measurementDataDict['wPrime'] = 0
            measurementDataDict['maxForce'] = 0
            measurementDataDict['measDataKg'] = []
            self.measTab.setData(measurementDataDict, reset=True)

            self.setWindowTitle(Params.appName.value)
        else:
            pass

    def onSaveActionClicked(self):
        personalDataDict = self.dataTab.getData()
        measurementDataDict = self.measTab.getData()
        resultDict = {}
        resultDict['Personal'] = personalDataDict
        resultDict['Measurement'] = measurementDataDict

        exampleFileName = str(date.today()) + '_' + personalDataDict['name'] + '.json'
        fileName = QFileDialog.getSaveFileName(self, "Save As...", "./results/" + exampleFileName, "Training Files (*.json)")

        if fileName[0] != "":
            with open(fileName[0], 'w') as f:
                json.dump(resultDict, f)
                f.close()

            self.setWindowTitle(Params.appName.value + " - " + fileName[0])

    def onLoadActionClicked(self):
        fileName = QFileDialog.getOpenFileName(self, "Load Measurement...", "./results", "Training Files (*.json)")

        if os.path.isfile(fileName[0]):
            try:
                with open(fileName[0]) as f:
                    resultData = json.load(f)
                    f.close()

                self.dataTab.setData(resultData['Personal'])
                self.measTab.setData(resultData['Measurement'])
                self.setWindowTitle(Params.appName.value + " - " + fileName[0])
            except:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("This file does not contain valid training data!")
                msg.exec_()

    def onCalibrationActionClicked(self):
        if self.weightSensor.isConnected():
            calibrationDialog = CalibrationCtrl(self.weightSensor, self)
            calibrationDialog.setWindowTitle("Sensor Calibration")
            calibrationDialog.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Calibration is not possible without weight sensor.\nPlease connect a fingerboard to your computer.")
            msg.exec_()

    def onPreferencesActionClicked(self):
        preferencesDialog = PreferencesCtrl(self)
        preferencesDialog.setWindowTitle("Preferences")
        preferencesDialog.exec_()
    
    def closeEvent(self, event):
        self.measTab.onCloseApplication()
        self.weightSensor.stop()
        event.accept()
        # event.ignore()
