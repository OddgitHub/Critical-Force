
from PySide6.QtWidgets import QWidget
from ui.MeasurementGui import Ui_Form

from workout_config.workouts import WorkoutHandler

class MeasurementCtrl(QWidget):
    def __init__(self):
        super().__init__()        

        form = Ui_Form()
        form.setupUi(self)
        form.startButton.pressed.connect(self.onStartButtonClicked)
        form.stopButton.pressed.connect(self.onStopButtonClicked)
        form.taraButton.pressed.connect(self.onTaraButtonClicked)

        self.workoutDescriptionLabel = form.workoutDescriptionLabel

        workoutComboBox = form.workoutComboBox
        workoutComboBox.currentIndexChanged.connect( self.onWorkoutChanged )

        workoutCfgPath = ('./workout_config/workouts.csv')
        workoutHandler = WorkoutHandler(workoutCfgPath)
        self.workouts = workoutHandler.getAllWorkouts()

        for workout in self.workouts:
            workoutComboBox.addItem(workout['Name'])

    def onStartButtonClicked(self):
        print("Start button clicked.")

    def onStopButtonClicked(self):
        print("Stop button clicked.")

    def onTaraButtonClicked(self):
        print("Tara button clicked.")

    def onWorkoutChanged(self, s):
        self.workoutDescriptionLabel.setText(self.workouts[s]["Description"])