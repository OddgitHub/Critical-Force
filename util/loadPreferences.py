'''
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
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
'''

from util.params import Params
import json

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