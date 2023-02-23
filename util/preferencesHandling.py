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

from util.params import Params
import json, os
from platformdirs import user_documents_dir

def loadPreferences():
    try:
        # Load, if preferences file is available
        with open(Params.preferencesFile.value, 'r') as f:
            preferences = json.load(f)
            f.close()
    except:
        # Set to default values otherwise
        preferences = {}
        preferences['fsMeasurement'] = Params.fsMeasurementDefault.value
        preferences['delayCompensation'] = Params.delayCompensationDefault.value
    
    return preferences

def setWorkingDirectory(workDir):
    with open(Params.lastWorkingDirFile.value, 'w') as f:
        json.dump(workDir, f)
        f.close()

def getWorkingDirectory():
    with open(Params.lastWorkingDirFile.value, 'r') as f:
        workDir = json.load(f)
        f.close()
    if os.path.exists(workDir):
        return workDir
    else:
        return user_documents_dir()
