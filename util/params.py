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
