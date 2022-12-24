from enum import Enum
import os

class Params(Enum):
    fsMeasurement = 10       # [Hz]
    workoutCfgPath = ('./workouts/workouts.csv')
    fileClickHi = ('./raw/clickhi.wav')
    fileClickLo = ('./raw/clicklo.wav')
    appIcon = ('./raw/icon.ico')
    appName = 'Climbing Trainer'