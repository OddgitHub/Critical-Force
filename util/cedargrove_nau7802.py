# SPDX-FileCopyrightText: Copyright (c) 2022 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`cedargrove_nau7802`
================================================================================

A CircuitPython driver class for the NAU7802 24-bit ADC. Supports dual analog
inputs.


* Author(s): JG

Implementation Notes
--------------------

**Hardware:**

* `NAU7802 FeatherWing; OSH Park project (16-SOIC version)
  <https://oshpark.com/shared_projects/qFvEU3Bn>`_
* `NAU7802 FeatherWing; OSH Park project (16-DIP version)
  <https://oshpark.com/shared_projects/ZfryHYnc>`_
* `SparkFun Quicc Scale (single channel) <https://www.sparkfun.com/products/15242>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

import time
import struct

from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_struct import ROUnaryStruct

# from adafruit_register.i2c_struct   import UnaryStruct
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bits import ROBits
from adafruit_register.i2c_bit import RWBit
from adafruit_register.i2c_bit import ROBit

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/CedarGroveStudios/CircuitPython_NAU7802.git"

# DEVICE REGISTER MAP
_PU_CTRL = 0x00  # Power-Up Control RW
_CTRL1 = 0x01  # Control 1 RW
_CTRL2 = 0x02  # Control 2 RW
_ADCO_B2 = 0x12  # ADC_OUT[23:16] R-
_ADCO_B1 = 0x13  # ADC_OUT[16: 8] R-
_ADCO_B0 = 0x14  # ADC_OUT[ 7: 0] R-
_OTP_B1 = 0x15  # OTP[15: 8] R-
_ADC = 0x15  # ADC Control -W
_OTP_B0 = 0x16  # OTP[ 7: 0] R-
_PGA = 0x1B  # Programmable Gain Amplifier  RW
_PWR_CTRL = 0x1C  # Power Control  RW
_REV_ID = 0x1F  # Chip Revision ID  R-

# pylint: disable=too-few-public-methods
class LDOVoltage:
    """Internal low-dropout voltage regulator settings."""

    LDO_3V0 = 0x5  # LDO 3.0 volts; _CTRL1[5:3] = 5
    LDO_2V7 = 0x6  # LDO 2.7 volts; _CTRL1[5:3] = 6
    LDO_2V4 = 0x7  # LDO 2.4 volts; _CTRL1[5:3] = 7


class Gain:
    """Analog differential amplifier gain settings."""

    GAIN_X1 = 0x0  # Gain X1; _CTRL1[2:0] = 0 (chip default)
    GAIN_X2 = 0x1  # Gain X1; _CTRL1[2:0] = 1
    GAIN_X4 = 0x2  # Gain X1; _CTRL1[2:0] = 2
    GAIN_X8 = 0x3  # Gain X1; _CTRL1[2:0] = 3
    GAIN_X16 = 0x4  # Gain X1; _CTRL1[2:0] = 4
    GAIN_X32 = 0x5  # Gain X1; _CTRL1[2:0] = 5
    GAIN_X64 = 0x6  # Gain X1; _CTRL1[2:0] = 6
    GAIN_X128 = 0x7  # Gain X1; _CTRL1[2:0] = 7


class ConversionRate:
    """ADC conversion rate settings."""

    RATE_10SPS = 0x0  # 10 samples/sec; _CTRL2[6:4] = 0 (chip default)
    RATE_20SPS = 0x1  # 20 samples/sec; _CTRL2[6:4] = 1
    RATE_40SPS = 0x2  # 40 samples/sec; _CTRL2[6:4] = 2
    RATE_80SPS = 0x3  # 80 samples/sec; _CTRL2[6:4] = 3
    RATE_320SPS = 0x7  # 320 samples/sec; _CTRL2[6:4] = 7


class CalibrationMode:
    """Calibration mode state settings."""

    INTERNAL = 0x0  # Offset Calibration Internal; _CTRL2[1:0] = 0 (chip default)
    OFFSET = 0x2  # Offset Calibration System;   _CTRL2[1:0] = 2
    GAIN = 0x3  # Gain   Calibration System;   _CTRL2[1:0] = 3


class NAU7802:
    """The primary NAU7802 class."""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, i2c_bus, address=0x2A, active_channels=1):
        """Instantiate NAU7802; LDO 3v0 volts, gain 128, 10 samples per second
        conversion rate, disabled ADC chopper clock, low ESR caps, and PGA output
        stabilizer cap if in single channel mode. Returns True if successful."""
        self.i2c_device = I2CDevice(i2c_bus, address)
        if not self.reset():
            raise RuntimeError("NAU7802 device could not be reset")
        if not self.enable(True):
            raise RuntimeError("NAU7802 device could not be enabled")
        self.ldo_voltage = "3V0"  # 3.0-volt internal analog power (AVDD)
        self._pu_ldo_source = True  # Internal analog power (AVDD)
        self.gain = 128  # X128
        self._c2_conv_rate = ConversionRate.RATE_10SPS  # 10 SPS; default
        self._adc_chop_clock = 0x3  # 0x3 = Disable ADC chopper clock
        self._pga_ldo_mode = 0x0  # 0x0 = Use low ESR capacitors
        self._act_channels = active_channels
        # 0x1 = Enable PGA out stabilizer cap for single channel use
        self._pc_cap_enable = 0x1
        if self._act_channels == 2:
            # 0x0 = Disable PGA out stabilizer cap for dual channel use
            self._pc_cap_enable = 0x0
        self._calib_mode = None  # Initialize for later use
        self._adc_out = None  # Initialize for later use

    # DEFINE I2C DEVICE BITS, NYBBLES, BYTES, AND REGISTERS
    # Chip Revision  R-
    _rev_id = ROBits(4, _REV_ID, 0, 1, False)
    # Register Reset  (RR)  RW
    _pu_reg_reset = RWBit(_PU_CTRL, 0, 1, False)
    # Power-Up Digital Circuit  (PUD) RW
    _pu_digital = RWBit(_PU_CTRL, 1, 1, False)
    # Power-Up Analog Circuit  (PUA) RW
    _pu_analog = RWBit(_PU_CTRL, 2, 1, False)
    # Power-Up Ready Status  (PUR) R-
    _pu_ready = ROBit(_PU_CTRL, 3, 1, False)
    # Power-Up Conversion Cycle Start  (CS) RW
    _pu_cycle_start = RWBit(_PU_CTRL, 4, 1, False)
    # Power-Up Cycle Ready  (CR) R-
    _pu_cycle_ready = ROBit(_PU_CTRL, 5, 1, False)
    # Power-Up AVDD Source  ADDS) RW
    _pu_ldo_source = RWBit(_PU_CTRL, 7, 1, False)
    # Control_1 Gain  (GAINS) RW
    _c1_gains = RWBits(3, _CTRL1, 0, 1, False)
    # Control_1 LDO Voltage  (VLDO) RW
    _c1_vldo_volts = RWBits(3, _CTRL1, 3, 1, False)
    # Control_2 Calibration Mode  (CALMOD) RW
    _c2_cal_mode = RWBits(2, _CTRL2, 0, 1, False)
    # Control_2 Calibration Start  (CALS) RW
    _c2_cal_start = RWBit(_CTRL2, 2, 1, False)
    # Control_2 Calibration Error (CAL_ERR) RW
    _c2_cal_error = RWBit(_CTRL2, 3, 1, False)
    # Control_2 Conversion Rate  (CRS) RW
    _c2_conv_rate = RWBits(3, _CTRL2, 4, 1, False)
    # Control_2 Channel Select  (CHS) RW
    _c2_chan_select = RWBit(_CTRL2, 7, 1, False)
    # ADC Result Output  MSByte R-
    _adc_out_2 = ROUnaryStruct(_ADCO_B2, ">B")
    # ADC Result Output  MidSByte R-
    _adc_out_1 = ROUnaryStruct(_ADCO_B1, ">B")
    # ADC Result Output  LSByte R-
    _adc_out_0 = ROUnaryStruct(_ADCO_B0, ">B")
    # ADC Chopper Clock Frequency Select  -W
    _adc_chop_clock = RWBits(2, _ADC, 4, 1, False)
    # PGA Stability/Accuracy Mode (LDOMODE) RW
    _pga_ldo_mode = RWBit(_PGA, 6, 1, False)
    # Power_Ctrl PGA Capacitor (PGA_CAP_EN) RW
    _pc_cap_enable = RWBit(_PWR_CTRL, 7, 1, False)

    @property
    def chip_revision(self):
        """The chip revision code."""
        return self._rev_id

    @property
    def channel(self):
        "Selected channel number (1 or 2)."
        return self._c2_chan_select + 1

    @channel.setter
    def channel(self, chan=1):
        """Select the active channel. Valid channel numbers are 1 and 2.
        Analog multiplexer settling time was emperically determined to be
        approximately 400ms at 10SPS, 200ms at 20SPS, 100ms at 40SPS,
        50ms at 80SPS, and 20ms at 320SPS."""
        if chan == 1:
            self._c2_chan_select = 0x0
            time.sleep(0.400)  # 400ms settling time for 10SPS
        elif chan == 2 and self._act_channels == 2:
            self._c2_chan_select = 0x1
            time.sleep(0.400)  # 400ms settling time for 10SPS
        else:
            raise ValueError("Invalid Channel Number")

    @property
    def ldo_voltage(self):
        """Representation of the LDO voltage value."""
        return self._ldo_voltage

    @ldo_voltage.setter
    def ldo_voltage(self, voltage="EXTERNAL"):
        """Select the LDO Voltage. Valid voltages are '2V4', '2V7', '3V0'."""
        if not "LDO_" + voltage in dir(LDOVoltage):
            raise ValueError("Invalid LDO Voltage")
        self._ldo_voltage = voltage
        if self._ldo_voltage == "2V4":
            self._c1_vldo_volts = LDOVoltage.LDO_2V4
        elif self._ldo_voltage == "2V7":
            self._c1_vldo_volts = LDOVoltage.LDO_2V7
        elif self._ldo_voltage == "3V0":
            self._c1_vldo_volts = LDOVoltage.LDO_3V0

    @property
    def gain(self):
        """The programmable amplifier (PGA) gain factor."""
        return self._gain

    @gain.setter
    def gain(self, factor=1):
        """Select PGA gain factor. Valid values are '1, 2, 4, 8, 16, 32, 64,
        and 128."""
        if not "GAIN_X" + str(factor) in dir(Gain):
            raise ValueError("Invalid Gain Factor")
        self._gain = factor
        if self._gain == 1:
            self._c1_gains = Gain.GAIN_X1
        elif self._gain == 2:
            self._c1_gains = Gain.GAIN_X2
        elif self._gain == 4:
            self._c1_gains = Gain.GAIN_X4
        elif self._gain == 8:
            self._c1_gains = Gain.GAIN_X8
        elif self._gain == 16:
            self._c1_gains = Gain.GAIN_X16
        elif self._gain == 32:
            self._c1_gains = Gain.GAIN_X32
        elif self._gain == 64:
            self._c1_gains = Gain.GAIN_X64
        elif self._gain == 128:
            self._c1_gains = Gain.GAIN_X128

    def enable(self, power=True):
        """Enable(start) or disable(stop) the internal analog and digital
        systems power. Enable = True; Disable (low power) = False. Returns
        True when enabled; False when disabled."""
        self._enable = power
        if self._enable:
            self._pu_analog = True
            self._pu_digital = True
            time.sleep(0.750)  # Wait 750ms; minimum 400ms
            self._pu_start = True  # Start acquisition system cycling
            return self._pu_ready
        self._pu_analog = False
        self._pu_digital = False
        time.sleep(0.010)  # Wait 10ms (200us minimum)
        return False

    def available(self):
        """Read the ADC data-ready status. True when data is available; False when
        ADC data is unavailable."""
        return self._pu_cycle_ready

    def read(self):
        """Reads the 24-bit ADC data. Returns a signed integer value with
        24-bit resolution. Assumes that the ADC data-ready bit was checked
        to be True."""
        adc = self._adc_out_2 << 24  # [31:24] << MSByte
        adc = adc | (self._adc_out_1 << 16)  # [23:16] << MidSByte
        adc = adc | (self._adc_out_0 << 8)  # [15: 8] << LSByte
        adc = adc.to_bytes(4, "big")  # Pack to 4-byte (32-bit) structure
        value = struct.unpack(">i", adc)[0]  # Unpack as 4-byte signed integer
        self._adc_out = value / 128  # Restore to 24-bit signed integer value
        return self._adc_out

    def reset(self):
        """Resets all device registers and enables digital system power.
        Returns the power ready status bit value: True when system is ready;
        False when system not ready for use."""
        self._pu_reg_reset = True  # Reset all registers)
        time.sleep(0.100)  # Wait 100ms; 10ms minimum
        self._pu_reg_reset = False
        self._pu_digital = True
        time.sleep(0.750)  # Wait 750ms; 400ms minimum
        return self._pu_ready

    def calibrate(self, mode="INTERNAL"):
        """Perform the calibration procedure. Valid calibration modes
        are 'INTERNAL', 'OFFSET', and 'GAIN'. True if successful."""
        if not mode in dir(CalibrationMode):
            raise ValueError("Invalid Calibration Mode")
        self._calib_mode = mode
        if self._calib_mode == "INTERNAL":  # Internal PGA offset (zero setting)
            self._c2_cal_mode = CalibrationMode.INTERNAL
        elif self._calib_mode == "OFFSET":  # External PGA offset (zero setting)
            self._c2_cal_mode = CalibrationMode.OFFSET
        elif self._calib_mode == "GAIN":  # External PGA full-scale gain setting
            self._c2_cal_mode = CalibrationMode.GAIN
        self._c2_cal_start = True
        while self._c2_cal_start:
            time.sleep(0.010)  # 10ms
        return not self._c2_cal_error