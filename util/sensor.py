from PySide6.QtWidgets import QMessageBox
import os

#========================================
# Static functions
#========================================
def getVoltage(raw):
    return (raw * 3.3) / 65536

def convertAdcValueToKg(raw):
    return getVoltage(raw) * -5 # TODO: atm only dummy!!

#========================================
# Class for weight sensor
#========================================
class WeightSensor():
    def __init__(self):
        # Set environment variable for MCP2221A
        try:
            os.environ['BLINKA_MCP2221']
        except:
            # set BLINKA_MCP2221=1
            os.environ['BLINKA_MCP2221']='1'

        try:
            import board
            from analogio import AnalogIn

            # Get access to the ADC
            self.adc = AnalogIn(board.G1)
            self.connected = True

        except:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Could not detect weight sensor!\nPlease connect a fingerboard to your computer.")
            msg.exec_()
            self.connected = False

    
    def getValue(self):
        if self.connected:
            return self.adc.value
        else:
            return False
