from enum import Enum
import os

class Params(Enum):
    fsMeasurement = 10          # [Hz]
    delayCompensation = 350     # [ms] Delay between audio clicks and measurement

    workoutCfgFile = ('./settings/workouts.csv')
    calibrationFile = ('./settings/calibration.json')
    fileClickHi = ('./raw/clickhi.wav')
    fileClickLo = ('./raw/clicklo.wav')
    appIcon = ('./raw/icon.ico')
    appName = 'Climbing Trainer'
