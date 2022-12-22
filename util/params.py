from enum import Enum

class Params(Enum):
    fsMeasurement = 10       # [Hz]
    workoutCfgPath = ('./workout_config/workouts.csv')
    fileClickHi = ('./raw/clickhi.wav')
    fileClickLo = ('./raw/clicklo.wav')