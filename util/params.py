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

from enum import Enum
import os

class Params(Enum):
    fsMeasurementDefault = 10          # [Hz]
    delayCompensationDefault = 350     # [ms] Delay between audio clicks and measurement

    workoutCfgFile = ('./settings/workouts.csv')
    calibrationFile = ('./settings/calibration.json')
    preferencesFile = ('./settings/preferences.json')
    fileClickHi = ('./raw/clickhi.wav')
    fileClickLo = ('./raw/clicklo.wav')
    appIcon = ('./raw/icon.ico')
    appName = 'Critical Force'
    version = '1.0.1'
