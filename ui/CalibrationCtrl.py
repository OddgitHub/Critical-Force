from PySide6.QtWidgets import QDialog, QMessageBox
import numpy as np
import json

from ui.CalibrationGui import Ui_Form
from util.params import Params

class CalibrationCtrl(QDialog):

    def __init__(self, weightSensor, parent=None):
        super().__init__(parent)

        self.form = Ui_Form()
        self.form.setupUi(self)

        self.weightSensor = weightSensor

        #========================================
        # Initialize class variables
        #========================================
        self.weightInKg1 = 0
        self.weightInKg2 = 0
        self.sensorValue1 = 0
        self.sensorValue2 = 0  

        #========================================
        # Connect signals
        #========================================     
        self.form.saveButton.pressed.connect(self.onSaveButtonClicked)
        self.form.cancelButton.pressed.connect(self.onCancelButtonClicked)
        self.form.set1Button.pressed.connect(self.onSetWeight1)
        self.form.set2Button.pressed.connect(self.onSetWeight2)

    def onSaveButtonClicked(self):
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setIcon(QMessageBox.Warning)

        # Check if one of the values is zero. If so, something went wrong.
        if self.weightInKg1 * self.weightInKg2 * self.sensorValue1 * self.sensorValue2 != 0:
            calibrationDict = {}
            calibrationDict['weightInKg1'] = self.weightInKg1
            calibrationDict['weightInKg2'] = self.weightInKg2
            calibrationDict['sensorValue1'] = self.sensorValue1
            calibrationDict['sensorValue2'] = self.sensorValue2

            with open(Params.calibrationFile.value, 'w') as f:
                json.dump(calibrationDict, f)
                f.close()

            self.close()
            msg.setText("Please re-start the application to make the calibration become active.")
        else:
            msg.setText("Could not calibrate the sensor!\nPlease ensure that you followed the instructions.")        
        msg.exec_()

    def onCancelButtonClicked(self):
        self.close()

    def onSetWeight1(self): 
        self.enableButtons(False)     
        self.weightInKg1 = self.form.weight1SpinBox.value()
        self.sensorValue1 = np.around(self.getAverageSensorValue(100), decimals=3)
        self.form.sensorValue1Label.setText(str(self.sensorValue1))
        self.enableButtons(True)

    def onSetWeight2(self):
        self.enableButtons(False)
        self.weightInKg2 = self.form.weight2SpinBox.value()
        self.sensorValue2 = np.around(self.getAverageSensorValue(100), decimals=3)
        self.form.sensorValue2Label.setText(str(self.sensorValue2))
        self.enableButtons(True)

    def getAverageSensorValue(self, numAvg):
        sum = 0
        for _ in range(numAvg):
            sum += self.weightSensor.getRawValue()
        return sum/numAvg

    def enableButtons(self, enable=True):
        self.form.cancelButton.setEnabled(enable)
        self.form.saveButton.setEnabled(enable)
        self.form.set1Button.setEnabled(enable)
        self.form.set2Button.setEnabled(enable)