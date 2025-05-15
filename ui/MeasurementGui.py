# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MeasurementGui.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFrame,
    QHBoxLayout, QLabel, QLayout, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(595, 488)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.workoutComboBox = QComboBox(Form)
        self.workoutComboBox.setObjectName(u"workoutComboBox")

        self.horizontalLayout_2.addWidget(self.workoutComboBox)

        self.bodyWeightLabel = QLabel(Form)
        self.bodyWeightLabel.setObjectName(u"bodyWeightLabel")
        self.bodyWeightLabel.setLayoutDirection(Qt.LeftToRight)
        self.bodyWeightLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.bodyWeightLabel)

        self.bodyWeightSpinBox = QDoubleSpinBox(Form)
        self.bodyWeightSpinBox.setObjectName(u"bodyWeightSpinBox")
        self.bodyWeightSpinBox.setDecimals(1)
        self.bodyWeightSpinBox.setMinimum(40.000000000000000)
        self.bodyWeightSpinBox.setMaximum(200.000000000000000)
        self.bodyWeightSpinBox.setValue(70.000000000000000)

        self.horizontalLayout_2.addWidget(self.bodyWeightSpinBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.workoutDescriptionLabel = QLabel(Form)
        self.workoutDescriptionLabel.setObjectName(u"workoutDescriptionLabel")

        self.verticalLayout.addWidget(self.workoutDescriptionLabel)

        self.line_3 = QFrame(Form)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.line_4 = QFrame(Form)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_4)

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

        self.workoutLabel = QLabel(Form)
        self.workoutLabel.setObjectName(u"workoutLabel")
        self.workoutLabel.setMinimumSize(QSize(70, 0))
        font = QFont()
        font.setPointSize(13)
        self.workoutLabel.setFont(font)
        self.workoutLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.workoutLabel)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tareLabel_1 = QLabel(Form)
        self.tareLabel_1.setObjectName(u"tareLabel_1")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tareLabel_1.sizePolicy().hasHeightForWidth())
        self.tareLabel_1.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(15)
        self.tareLabel_1.setFont(font1)
        self.tareLabel_1.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.tareLabel_1)

        self.tareLabel_2 = QLabel(Form)
        self.tareLabel_2.setObjectName(u"tareLabel_2")
        self.tareLabel_2.setFont(font1)
        self.tareLabel_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.tareLabel_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.tareButton_1 = QPushButton(Form)
        self.tareButton_1.setObjectName(u"tareButton_1")

        self.horizontalLayout_4.addWidget(self.tareButton_1)

        self.tareButton_2 = QPushButton(Form)
        self.tareButton_2.setObjectName(u"tareButton_2")

        self.horizontalLayout_4.addWidget(self.tareButton_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.graphicsView = PlotWidget(Form)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout.addWidget(self.graphicsView)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.bodyWeightLabel.setText(QCoreApplication.translate("Form", u"Body Weight", None))
        self.bodyWeightSpinBox.setSuffix(QCoreApplication.translate("Form", u"kg", None))
        self.workoutDescriptionLabel.setText(QCoreApplication.translate("Form", u"Please select a workout...", None))
        self.startButton.setText(QCoreApplication.translate("Form", u"Start", None))
        self.stopButton.setText(QCoreApplication.translate("Form", u"Stop", None))
        self.workoutLabel.setText(QCoreApplication.translate("Form", u"Stopped", None))
        self.tareLabel_1.setText(QCoreApplication.translate("Form", u"0kg", None))
        self.tareLabel_2.setText(QCoreApplication.translate("Form", u"0kg", None))
        self.tareButton_1.setText(QCoreApplication.translate("Form", u"Tare 1", None))
        self.tareButton_2.setText(QCoreApplication.translate("Form", u"Tare 2", None))
    # retranslateUi

