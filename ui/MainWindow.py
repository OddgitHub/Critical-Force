
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QStatusBar, QTabWidget, QFileDialog, QMessageBox
from datetime import date
import os, json

from util.params import Params
from util.sensor import WeightSensor

from ui.MeasurementCtrl import MeasurementCtrl
from ui.DataCtrl import DataCtrl
from ui.CalibrationCtrl import CalibrationCtrl

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
        saveAction = QAction("Save As...", self, shortcut="Ctrl+s")
        saveAction.setStatusTip("Save the current measurement to the result database.")
        saveAction.triggered.connect(self.onSaveActionClicked)

        loadAction = QAction("Load...", self)
        loadAction.setStatusTip("Load previously measured data.")
        loadAction.triggered.connect(self.onLoadActionClicked)

        calibrationAction = QAction("Calibration", self)
        calibrationAction.setStatusTip("Calibrate the load-cell.")
        calibrationAction.triggered.connect(self.onCalibrationActionClicked)

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

        self.setCentralWidget(tabs)
        
        #========================================
        # Menu
        #========================================
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(loadAction)
        file_menu.addAction(saveAction)

        settings_menu = menu.addMenu("&Settings")
        settings_menu.addAction(calibrationAction)

    #========================================
    # Callbacks
    #========================================
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
            with open(fileName[0]) as f:
                resultData = json.load(f)
                f.close()
            try:
                self.dataTab.setData(resultData['Personal'])
                self.measTab.setData(resultData['Measurement'])
                self.setWindowTitle(Params.appName.value + " - " + fileName[0])
            except KeyError:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("This files does not contain valid training data!")
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
    
    def closeEvent(self, event):
        self.measTab.onCloseApplication()
        self.weightSensor.stop()
        event.accept()
        # event.ignore()
