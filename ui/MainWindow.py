
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QStatusBar, QTabWidget

from ui.MeasurementCtrl import MeasurementCtrl
from ui.DataGui import DataGui

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #========================================
        # Basic window properties
        #========================================
        self.setWindowTitle("Climbing Trainer")
        self.setMinimumSize(400, 300)
        self.setStatusBar(QStatusBar(self))

        #========================================
        # Actions
        #========================================
        saveAction = QAction("Save", self)
        saveAction.setStatusTip("Save the current measurement to the result database.")
        saveAction.triggered.connect(self.onSaveActionClicked)

        #========================================
        # Build the gui
        #========================================
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)
        tabs.setMovable(False)
        
        # Measurement page
        self.measTab = MeasurementCtrl()
        tabs.addTab(self.measTab, "Measurement")

        # Personal data page
        dataTab = DataGui()
        tabs.addTab(dataTab, "Personal Data")

        self.setCentralWidget(tabs)
        
        #========================================
        # Menu
        #========================================
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(saveAction)

    # Callbacks
    def onSaveActionClicked(self):
        print('Save Action Triggered')

    def closeEvent(self, event):
        self.measTab.onStopMeasurement()
        event.accept()
        # event.ignore()
