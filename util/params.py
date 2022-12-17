from enum import Enum

class Params(Enum):
    fsSensor = 10       # [sec]
    workoutCfgPath = ('./workout_config/workouts.csv')
    fileClickHi = ('./raw/clickhi.wav')
    fileClickLo = ('./raw/clicklo.wav')