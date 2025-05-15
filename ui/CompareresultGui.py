# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CompareresultGui.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QPushButton,
    QSizePolicy, QTableView, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(645, 513)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.loadButton = QPushButton(Form)
        self.loadButton.setObjectName(u"loadButton")

        self.horizontalLayout.addWidget(self.loadButton)

        self.clearButton = QPushButton(Form)
        self.clearButton.setObjectName(u"clearButton")

        self.horizontalLayout.addWidget(self.clearButton)

        self.exportButton = QPushButton(Form)
        self.exportButton.setObjectName(u"exportButton")

        self.horizontalLayout.addWidget(self.exportButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableView = QTableView(Form)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.loadButton.setText(QCoreApplication.translate("Form", u"Load Result Files", None))
        self.clearButton.setText(QCoreApplication.translate("Form", u"Clear Table", None))
        self.exportButton.setText(QCoreApplication.translate("Form", u"Export Table", None))
    # retranslateUi

