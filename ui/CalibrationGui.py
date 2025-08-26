# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CalibrationGui.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.descriptionLabel = QLabel(Form)
        self.descriptionLabel.setObjectName(u"descriptionLabel")

        self.verticalLayout.addWidget(self.descriptionLabel)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.weight1Description = QLabel(Form)
        self.weight1Description.setObjectName(u"weight1Description")

        self.verticalLayout.addWidget(self.weight1Description)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.weight1Label = QLabel(Form)
        self.weight1Label.setObjectName(u"weight1Label")

        self.horizontalLayout.addWidget(self.weight1Label)

        self.weight1SpinBox = QDoubleSpinBox(Form)
        self.weight1SpinBox.setObjectName(u"weight1SpinBox")
        self.weight1SpinBox.setMinimum(5.000000000000000)
        self.weight1SpinBox.setMaximum(20.000000000000000)

        self.horizontalLayout.addWidget(self.weight1SpinBox)

        self.set1Button = QPushButton(Form)
        self.set1Button.setObjectName(u"set1Button")
        self.set1Button.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout.addWidget(self.set1Button)

        self.sensorValue1Label = QLabel(Form)
        self.sensorValue1Label.setObjectName(u"sensorValue1Label")
        self.sensorValue1Label.setMinimumSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.sensorValue1Label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.weight2Description = QLabel(Form)
        self.weight2Description.setObjectName(u"weight2Description")

        self.verticalLayout.addWidget(self.weight2Description)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.weight2Label = QLabel(Form)
        self.weight2Label.setObjectName(u"weight2Label")

        self.horizontalLayout_2.addWidget(self.weight2Label)

        self.weight2SpinBox = QDoubleSpinBox(Form)
        self.weight2SpinBox.setObjectName(u"weight2SpinBox")
        self.weight2SpinBox.setMinimum(60.000000000000000)
        self.weight2SpinBox.setMaximum(90.000000000000000)

        self.horizontalLayout_2.addWidget(self.weight2SpinBox)

        self.set2Button = QPushButton(Form)
        self.set2Button.setObjectName(u"set2Button")
        self.set2Button.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_2.addWidget(self.set2Button)

        self.sensorValue2Label = QLabel(Form)
        self.sensorValue2Label.setObjectName(u"sensorValue2Label")

        self.horizontalLayout_2.addWidget(self.sensorValue2Label)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.line_3 = QFrame(Form)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.saveButton = QPushButton(Form)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_3.addWidget(self.saveButton)

        self.cancelButton = QPushButton(Form)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_3.addWidget(self.cancelButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.descriptionLabel.setText(QCoreApplication.translate("Form", u"In order to calibrate your load-cell, add two different weights to it.\n"
"Click the \"Set\" button as soon as each weight is applied.\n"
"\n"
"The calibration will only become active, after re-starting the application!", None))
        self.weight1Description.setText(QCoreApplication.translate("Form", u"Weight 1 should be between 5 - 20 kg.", None))
        self.weight1Label.setText(QCoreApplication.translate("Form", u"Added weight:", None))
        self.weight1SpinBox.setSuffix(QCoreApplication.translate("Form", u" kg", None))
        self.set1Button.setText(QCoreApplication.translate("Form", u"Set", None))
        self.sensorValue1Label.setText(QCoreApplication.translate("Form", u"0.0", None))
        self.weight2Description.setText(QCoreApplication.translate("Form", u"Weight 2 should be between 60 - 90 kg.", None))
        self.weight2Label.setText(QCoreApplication.translate("Form", u"Added weight:", None))
        self.weight2SpinBox.setSuffix(QCoreApplication.translate("Form", u" kg", None))
        self.set2Button.setText(QCoreApplication.translate("Form", u"Set", None))
        self.sensorValue2Label.setText(QCoreApplication.translate("Form", u"0.0", None))
        self.saveButton.setText(QCoreApplication.translate("Form", u"Save", None))
        self.cancelButton.setText(QCoreApplication.translate("Form", u"Cancel", None))
    # retranslateUi

