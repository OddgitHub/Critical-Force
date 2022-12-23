from enum import Enum

class Params(Enum):
    fsMeasurement = 10       # [Hz]
    workoutCfgPath = ('./workouts/workouts.csv')
    fileClickHi = ('./raw/clickhi.wav')
    fileClickLo = ('./raw/clicklo.wav')
    appIcon = ('./raw/icon.png')
    appName = 'Climbing Trainer'