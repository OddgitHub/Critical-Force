# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MeasurementGui.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLayout, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(635, 488)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.workoutComboBox = QComboBox(Form)
        self.workoutComboBox.setObjectName(u"workoutComboBox")

        self.verticalLayout.addWidget(self.workoutComboBox)

        self.workoutDescriptionLabel = QLabel(Form)
        self.workoutDescriptionLabel.setObjectName(u"workoutDescriptionLabel")

        self.verticalLayout.addWidget(self.workoutDescriptionLabel)

        self.line_3 = QFrame(Form)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.startButton = QPushButton(Form)
        self.startButton.setObjectName(u"startButton")

        self.verticalLayout_2.addWidget(self.startButton)

        self.stopButton = QPushButton(Form)
        self.stopButton.setObjectName(u"stopButton")

        self.verticalLayout_2.addWidget(self.stopButton)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.timerLabel = QLabel(Form)
        self.timerLabel.setObjectName(u"timerLabel")
        self.timerLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.timerLabel)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.weightLabel = QLabel(Form)
        self.weightLabel.setObjectName(u"weightLabel")
        self.weightLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.weightLabel)

        self.taraButton = QPushButton(Form)
        self.taraButton.setObjectName(u"taraButton")

        self.verticalLayout_3.addWidget(self.taraButton)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line_4 = QFrame(Form)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.placeholderLabel = QLabel(Form)
        self.placeholderLabel.setObjectName(u"placeholderLabel")
        self.placeholderLabel.setMinimumSize(QSize(0, 200))

        self.verticalLayout.addWidget(self.placeholderLabel)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.workoutDescriptionLabel.setText(QCoreApplication.translate("Form", u"Please select a workout...", None))
        self.startButton.setText(QCoreApplication.translate("Form", u"Start", None))
        self.stopButton.setText(QCoreApplication.translate("Form", u"Stop", None))
        self.timerLabel.setText(QCoreApplication.translate("Form", u"Paused", None))
        self.weightLabel.setText(QCoreApplication.translate("Form", u"0kg", None))
        self.taraButton.setText(QCoreApplication.translate("Form", u"Tara", None))
        self.placeholderLabel.setText(QCoreApplication.translate("Form", u"Placeholder for plot...", None))
    # retranslateUi

