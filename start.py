import sys

from ui.MainWindow import MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from util.params import Params



if __name__=='__main__':

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(Params.appIcon.value))

    window = MainWindow()
    window.show()

    app.exec()