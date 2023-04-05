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
from platformdirs import user_data_dir

APPNAME = 'CriticalForce'
APPAUTHOR = 'pbulling'
basedir = os.path.dirname(os.path.dirname(__file__))
datadir = user_data_dir(APPNAME, APPAUTHOR)

class Params(Enum):
    fsMeasurementDefault = 10          # [Hz]
    delayCompensationDefault = 350     # [ms] Delay between audio clicks and measurement

    calibrationFile = os.path.join(datadir, 'calibration.json')
    preferencesFile = os.path.join(datadir, 'preferences.json')
    lastWorkingDirFile = os.path.join(datadir, 'lastworkingdir.json')
    logFile = os.path.join(datadir, 'debug.log')

    workoutCfgFile = os.path.join(basedir, 'settings/workouts.csv')
    fileClickHi = os.path.join(basedir, 'raw/clickhi.wav')
    fileClickLo = os.path.join(basedir, 'raw/clicklo.wav')
    appIcon = os.path.join(basedir, 'raw/icon.ico')
    appName = APPNAME
    appAuthor = APPAUTHOR
    version = '1.2.1'
