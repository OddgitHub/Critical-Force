from PySide6.QtWidgets import QMessageBox
import os, re, serial, time

from threading import Thread
from threading import Event

#========================================
# Class for weight sensor
#========================================
class WeightSensor():
    def __init__(self):
        self.sensorValue = 0

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
                self.sensorValue = -1
            time.sleep(0.001)

    def zero_channel(self):
        """Initiate internal calibration for current channel; return raw zero
        offset value. Use when scale is started, a new channel is selected, or to
        adjust for measurement drift. Remove weight and tare from load cell before
        executing."""
        print("Sensor calibration. Remove any weight during application startup!")
        print("channel %1d calibrate.INTERNAL: %5s" % (self.nau7802.channel, self.nau7802.calibrate("INTERNAL")))
        print("channel %1d calibrate.OFFSET:   %5s" % (self.nau7802.channel, self.nau7802.calibrate("OFFSET")))

        for _ in range(100):
            self.nau7802.read()  # Read 100 samples to establish zero offset

    def getValueInKg(self):
        #print(self.sensorValue)
        return self.sensorValue * (78.2 - 10.245) / (6889000 - 906000)

    def stop(self):
        # Must be called, when application is closed to stop the measurement thread
        self.stopThreadEvent.set()         

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


