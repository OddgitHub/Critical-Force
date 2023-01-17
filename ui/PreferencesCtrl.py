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
