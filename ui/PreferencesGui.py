# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PreferencesGui.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(342, 272)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.sampFreqLabel = QLabel(Form)
        self.sampFreqLabel.setObjectName(u"sampFreqLabel")

        self.gridLayout.addWidget(self.sampFreqLabel, 0, 0, 1, 1)

        self.sampFreqSpinBox = QSpinBox(Form)
        self.sampFreqSpinBox.setObjectName(u"sampFreqSpinBox")
        self.sampFreqSpinBox.setMaximum(100)

        self.gridLayout.addWidget(self.sampFreqSpinBox, 0, 1, 1, 1)

        self.delayCompLabel = QLabel(Form)
        self.delayCompLabel.setObjectName(u"delayCompLabel")

        self.gridLayout.addWidget(self.delayCompLabel, 1, 0, 1, 1)

        self.delayCompSpinBox = QSpinBox(Form)
        self.delayCompSpinBox.setObjectName(u"delayCompSpinBox")
        self.delayCompSpinBox.setMaximum(1000)

        self.gridLayout.addWidget(self.delayCompSpinBox, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.saveButton = QPushButton(Form)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout.addWidget(self.saveButton)

        self.cancelButton = QPushButton(Form)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout.addWidget(self.cancelButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.sampFreqLabel.setText(QCoreApplication.translate("Form", u"Sampling Frequency Weight Sensor:", None))
        self.sampFreqSpinBox.setSuffix(QCoreApplication.translate("Form", u" Hz", None))
        self.delayCompLabel.setText(QCoreApplication.translate("Form", u"Delay Compensation Audio Playback:", None))
        self.delayCompSpinBox.setSuffix(QCoreApplication.translate("Form", u" ms", None))
        self.saveButton.setText(QCoreApplication.translate("Form", u"Save", None))
        self.cancelButton.setText(QCoreApplication.translate("Form", u"Cancel", None))
    # retranslateUi

