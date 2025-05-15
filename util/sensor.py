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
        self.sensorValue_1 = 0
        self.sensorValue_2 = 0
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
            from adafruit_tca9548a import TCA9548A

            #Multiplexer initialisieren
            multiplexer = TCA9548A(board.I2C())

            # Instantiate 24-bit load sensor ADC; two channels, default gain of 128
            self.nau7802_1 = NAU7802(multiplexer[0], address=0x2A, active_channels=2)
            self.nau7802_1.enable(True)
            self.nau7802_1.channel = 1
            self.zero_channel()

            #2.Wägezelle
            self.nau7802_2 = NAU7802(multiplexer[1], address=0x2A, active_channels=2)
            self.nau7802_2.enable(True)
            self.nau7802_2.channel = 1
            self.zero_channel_2()

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
            elif self.connected and self.nau7802_1.available and self.nau7802_2.available:
                self.sensorValue_1 = self.nau7802_1.read()
                self.sensorValue_2 = self.nau7802_2.read()
            else:
                self.sensorValue_1 = 0
                self.sensorValue_2 = 0
            time.sleep(0.001)

    def zero_channel(self):
        """Initiate internal calibration for current channel; return raw zero
        offset value. Use when scale is started, a new channel is selected, or to
        adjust for measurement drift. Remove weight and tare from load cell before
        executing."""
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Checking sensor 1 ...\nRemove any weight, then click \"OK\" to proceed.")
        msg.exec_()

        self.nau7802_1.calibrate("INTERNAL")
        self.nau7802_1.calibrate("OFFSET")

        for _ in range(100):
            self.nau7802_1.read()  # Read 100 samples to establish zero offset
            
    def zero_channel_2(self):
        """Initiate internal calibration for current channel; return raw zero
        offset value. Use when scale is started, a new channel is selected, or to
        adjust for measurement drift. Remove weight and tare from load cell before
        executing."""
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Checking sensor 2 ...\nRemove any weight, then click \"OK\" to proceed.")
        msg.exec_()

        self.nau7802_2.calibrate("INTERNAL")
        self.nau7802_2.calibrate("OFFSET")

        for _ in range(100):  
            self.nau7802_2.read() # Read 100 samples to establish zero offset

    def getValueInKg_1(self):
        return self.sensorValue_1 * self.scalingFactor
    def getValueInKg_2(self):
        return self.sensorValue_2 * self.scalingFactor

    def getRawValue_1(self):
        return self.sensorValue_1
    def getRawValue_2(self):
        return self.sensorValue_2

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


