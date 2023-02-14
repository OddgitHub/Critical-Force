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
import json

from ui.PreferencesGui import Ui_Form
from util.params import Params
from util.loadPreferences import loadPreferences

class PreferencesCtrl(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        form = Ui_Form()
        form.setupUi(self)

        self.preferences = loadPreferences()
        
        form.sampFreqSpinBox.setValue(self.preferences['fsMeasurement'])
        form.delayCompSpinBox.setValue(self.preferences['delayCompensation'])

        # Connect signals   
        form.saveButton.pressed.connect(self.onSaveButtonClicked)
        form.cancelButton.pressed.connect(self.onCancelButtonClicked)
        form.sampFreqSpinBox.valueChanged.connect(self.onSamplingFrequencyChanged)
        form.delayCompSpinBox.valueChanged.connect(self.onDelayCompensationChanged)

    def onSaveButtonClicked(self):
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setIcon(QMessageBox.Warning)
        
        try:
            with open(Params.preferencesFile.value, 'w') as f:
                json.dump(self.preferences, f)
                f.close()
                self.close()
                msg.setText("Please re-start the application to make the changes become active.")
        except:        
                msg.setText("Could not save the preferences.")        
        msg.exec_()

    def onCancelButtonClicked(self):
        self.close()

    def onSamplingFrequencyChanged(self, value):
        self.preferences['fsMeasurement'] = value

    def onDelayCompensationChanged(self, value):
        self.preferences['delayCompensation'] = value
