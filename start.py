'''
    Software to measure climbing specific finger strength measures, such as Critical Force.
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
    along with "Critical Force".  If not, see <http://www.gnu.org/licenses/>.
'''

import sys, os, logging

from ui.MainWindow import MainWindow
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from util.params import Params
from platformdirs import user_data_dir, user_documents_dir
from shutil import copy

from util.preferencesHandling import setWorkingDirectory

def prepareLogger():
    open(Params.logFile.value, 'w').close()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(Params.logFile.value)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)    
    logger.addHandler(file_handler)

    def log_unhandled_exceptions(type, value, traceback):
        logger.exception("Unhandled exception: ", exc_info=(type, value, traceback))

    sys.excepthook = log_unhandled_exceptions

def prepareUserDirectory():
    basedir = os.path.dirname(__file__)
    datadir = user_data_dir(Params.appName.value, Params.appAuthor.value)
    if not os.path.exists(datadir):
        os.makedirs(datadir)
    if not os.path.exists(Params.calibrationFile.value):
        copy(os.path.join(basedir, 'settings/calibration.json'), datadir)
    if not os.path.exists(Params.preferencesFile.value):
        copy(os.path.join(basedir, 'settings/preferences.json'), datadir)
    if not os.path.exists(Params.lastWorkingDirFile.value):
        setWorkingDirectory(user_documents_dir())

if __name__=='__main__':
    prepareUserDirectory()
    prepareLogger()

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(Params.appIcon.value))

    window = MainWindow()
    window.show()

    app.exec()
