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

from ui.CompareresultGui import Ui_Form
from PySide6.QtWidgets import QWidget, QFileDialog, QMessageBox
from PySide6.QtCore import QAbstractTableModel, Qt
import os, json, csv, operator, copy
from datetime import date

from util.preferencesHandling import getWorkingDirectory, setWorkingDirectory

class TableModel(QAbstractTableModel):
    def __init__(self):
        super(TableModel, self).__init__()
        self.tableData = []
        self.tableHeader = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self.tableData[index.row()][index.column()])

    def headerData(self, sec, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.tableHeader[sec]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(sec + 1)

    def rowCount(self, index):
        return len(self.tableData)

    def columnCount(self, index):
        if len(self.tableData) > 0:
            return len(self.tableData[0])
        else:
            return 0

    def sort(self, col, order):
        # sort table by given column number col
        self.layoutAboutToBeChanged.emit()
        self.tableData = sorted(self.tableData, key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.tableData.reverse()
        self.layoutChanged.emit()

class CompareresultCtrl(QWidget):
    def __init__(self):
        super().__init__()       

        form = Ui_Form()
        form.setupUi(self)

        # Connect button signals
        form.loadButton.pressed.connect(self.onLoadButtonClicked)
        form.clearButton.pressed.connect(self.onClearButtonClicked)
        form.exportButton.pressed.connect(self.onExportButtonClicked)

        # Table handling
        self.tableModel = TableModel()
        tableView = form.tableView
        tableView.setModel(self.tableModel)
        tableView.setSortingEnabled(True)

    def onLoadButtonClicked(self):
        fileNames = QFileDialog.getOpenFileNames(self, "Load Result Files...", getWorkingDirectory(), "Training Files (*.json)")[0]
        
        if len(fileNames) > 0:
            newData = copy.deepcopy(self.tableModel.tableData)
            
            for fileName in fileNames:
                if os.path.isfile(fileName):
                    try:
                        with open(fileName) as f:
                            resultData = json.load(f)
                            f.close()

                        res = resultData['Personal'] | resultData['Measurement']
                        res.pop('measDataKg')
                        newData.append(list(res.values()))

                    except:
                            msg = QMessageBox()
                            msg.setWindowTitle("Warning")
                            msg.setIcon(QMessageBox.Warning)
                            msg.setText("This file: does not contain valid training data:\n" + fileName)
                            msg.exec_()

            newHeader = list(res.keys())
            setWorkingDirectory(os.path.split(fileName)[0])

            # Check if all rows of the table have the same number of columns
            allColumns = [len(r) for r in newData]
            allColumns.append(len(newHeader))
            if all(elem == allColumns[0] for elem in allColumns):
                self.tableModel.tableData = newData
                self.tableModel.tableHeader = newHeader
                self.tableModel.layoutChanged.emit()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Something went wrong, could not load result files.")
                msg.exec_()


    def onClearButtonClicked(self):
        self.tableModel.tableData = []
        self.tableModel.tableHeader = []
        self.tableModel.layoutChanged.emit()

    def onExportButtonClicked(self):
        exampleFileName = str(date.today()) + '_CombinedResults.csv'
        fileName = QFileDialog.getSaveFileName(self, "Save As...", os.path.join(getWorkingDirectory(), exampleFileName), "Table Data (*.csv)")

        if fileName[0] != "":
            with open(fileName[0], 'w', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(self.tableModel.tableHeader)
                writer.writerows(self.tableModel.tableData)
                f.close()
            setWorkingDirectory(os.path.split(fileName[0])[0])

