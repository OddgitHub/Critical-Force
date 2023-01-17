from PySide6.QtWidgets import QMessageBox
import os, re, serial, time, json

from threading import Thread
from threading import Event

from util.params import Params

#========================================
# Class for weight sensor
#========================================
class WeightSensor():
    def __init__(self):
        self.sensorValue = 0
        self.scalingFactor = self.calcScalingFactor(Params.calibrationFile.value)

        # Set environment variable for MCP2221A
        try:
            os.environ['BLINKA_MCP2221']
        except:
            # set BLINKA_MCP2221=1
            os.environ['BLINKA_MCP2221']='1'

        try:
            import board
            from util.cedargrove_nau7802 import NAU7802

            # Instantiate 24-bit load sensor ADC; two channels, default gain of 128
            self.nau7802 = NAU7802(board.I2C(), address=0x2A, active_channels=2)
            self.nau7802.enable(True)
            self.nau7802.channel = 1
            self.zero_channel()

            self.connected = True

            self.stopThreadEvent = Event()
            self.sensorThread = Thread(target=self.onNewMeasurement, args=(self.stopThreadEvent, ))
            self.sensorThread.start()

        except:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Could not detect weight sensor!\nPlease connect a fingerboard to your computer.")
            msg.exec_()
            self.connected = False

    def onNewMeasurement(self, stopEvent):
        while(True):
            if stopEvent.is_set():
                stopEvent.clear()
                break
            elif self.connected and self.nau7802.available:
                self.sensorValue = self.nau7802.read()
            else:
                self.sensorValue = 0
            time.sleep(0.001)

    def zero_channel(self):
        """Initiate internal calibration for current channel; return raw zero
        offset value. Use when scale is started, a new channel is selected, or to
        adjust for measurement drift. Remove weight and tare from load cell before
        executing."""
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Checking sensor...\nRemove any weight, then click \"OK\" to proceed.")
        msg.exec_()

        self.nau7802.calibrate("INTERNAL")
        self.nau7802.calibrate("OFFSET")

        for _ in range(100):
            self.nau7802.read()  # Read 100 samples to establish zero offset

    def getValueInKg(self):
        return self.sensorValue * self.scalingFactor

    def getRawValue(self):
        return self.sensorValue

    def isConnected(self):
        return self.connected

    def stop(self):
        if self.connected:
            # Must be called, when application is closed to stop the measurement thread
            self.stopThreadEvent.set()
        else:
            pass         

    @staticmethod
    def calcScalingFactor(calibrationFile):
        try:
            with open(calibrationFile) as f:
                calibrationData = json.load(f)
                f.close()
            
            weight1 = calibrationData['weightInKg1']
            weight2 = calibrationData['weightInKg2']
            sensorVal1 = calibrationData['sensorValue1']
            sensorVal2 = calibrationData['sensorValue2']
            return (weight2 - weight1) / (sensorVal2 - sensorVal1)
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Your sensor calibration file is corrupted.\nPlease re-calibrate your sensor.")
            msg.exec_()
            return 0

#========================================
# Class for Bluetooth communication to 
# a sensor connected to a Raspberry Pi
#========================================
class BluetoothSensor():
    def __init__(self):
        self.port = serial.Serial('COM5', 19200, timeout=0)
        self.oldvalue = 0

    def getValue(self):
        s = self.port.read(100).decode('utf-8')
        s = re.match('a[0-9]+e', s)
        if s is not None:
            result = int(s[0][1:-1])
            self.oldvalue = (result - 23760) * (75.5 - 20) / (3396775 - 884000)
        
        return self.oldvalue


