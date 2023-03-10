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

from PySide6.QtWidgets import QDialog, QMessageBox
import numpy as np
import json, time

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
            time.sleep(0.01)
        return sum/numAvg

    def enableButtons(self, enable=True):
        self.form.cancelButton.setEnabled(enable)
        self.form.saveButton.setEnabled(enable)
        self.form.set1Button.setEnabled(enable)
        self.form.set2Button.setEnabled(enable)