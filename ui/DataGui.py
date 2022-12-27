# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DataGui.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QLabel,
    QLineEdit, QPlainTextEdit, QSizePolicy, QSpinBox,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(615, 348)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.nameLabel = QLabel(Form)
        self.nameLabel.setObjectName(u"nameLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.nameLabel)

        self.nameLineEdit = QLineEdit(Form)
        self.nameLineEdit.setObjectName(u"nameLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.nameLineEdit)

        self.ageLabel = QLabel(Form)
        self.ageLabel.setObjectName(u"ageLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.ageLabel)

        self.ageSpinBox = QSpinBox(Form)
        self.ageSpinBox.setObjectName(u"ageSpinBox")
        self.ageSpinBox.setMinimum(0)
        self.ageSpinBox.setValue(0)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.ageSpinBox)

        self.genderLabel = QLabel(Form)
        self.genderLabel.setObjectName(u"genderLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.genderLabel)

        self.genderComboBox = QComboBox(Form)
        self.genderComboBox.setObjectName(u"genderComboBox")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.genderComboBox)

        self.heightLabel = QLabel(Form)
        self.heightLabel.setObjectName(u"heightLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.heightLabel)

        self.heightSpinBox = QSpinBox(Form)
        self.heightSpinBox.setObjectName(u"heightSpinBox")
        self.heightSpinBox.setMaximum(300)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.heightSpinBox)

        self.spanLabel = QLabel(Form)
        self.spanLabel.setObjectName(u"spanLabel")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.spanLabel)

        self.routeLabel = QLabel(Form)
        self.routeLabel.setObjectName(u"routeLabel")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.routeLabel)

        self.routeComboBox = QComboBox(Form)
        self.routeComboBox.setObjectName(u"routeComboBox")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.routeComboBox)

        self.boulderLabel = QLabel(Form)
        self.boulderLabel.setObjectName(u"boulderLabel")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.boulderLabel)

        self.boulderComboBox = QComboBox(Form)
        self.boulderComboBox.setObjectName(u"boulderComboBox")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.boulderComboBox)

        self.mailLabel = QLabel(Form)
        self.mailLabel.setObjectName(u"mailLabel")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.mailLabel)

        self.emailLineEdit = QLineEdit(Form)
        self.emailLineEdit.setObjectName(u"emailLineEdit")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.emailLineEdit)

        self.commentLabel = QLabel(Form)
        self.commentLabel.setObjectName(u"commentLabel")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.commentLabel)

        self.commentTextEdit = QPlainTextEdit(Form)
        self.commentTextEdit.setObjectName(u"commentTextEdit")

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.commentTextEdit)

        self.spanSpinBox = QSpinBox(Form)
        self.spanSpinBox.setObjectName(u"spanSpinBox")
        self.spanSpinBox.setMaximum(300)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.spanSpinBox)

        QWidget.setTabOrder(self.nameLineEdit, self.ageSpinBox)
        QWidget.setTabOrder(self.ageSpinBox, self.genderComboBox)
        QWidget.setTabOrder(self.genderComboBox, self.heightSpinBox)
        QWidget.setTabOrder(self.heightSpinBox, self.spanSpinBox)
        QWidget.setTabOrder(self.spanSpinBox, self.routeComboBox)
        QWidget.setTabOrder(self.routeComboBox, self.boulderComboBox)
        QWidget.setTabOrder(self.boulderComboBox, self.emailLineEdit)
        QWidget.setTabOrder(self.emailLineEdit, self.commentTextEdit)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.nameLabel.setText(QCoreApplication.translate("Form", u"Name", None))
        self.nameLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Your name", None))
        self.ageLabel.setText(QCoreApplication.translate("Form", u"Age", None))
        self.ageSpinBox.setSuffix("")
        self.genderLabel.setText(QCoreApplication.translate("Form", u"Gender", None))
        self.heightLabel.setText(QCoreApplication.translate("Form", u"Height", None))
        self.heightSpinBox.setSuffix(QCoreApplication.translate("Form", u" cm", None))
        self.spanLabel.setText(QCoreApplication.translate("Form", u"Arm Span", None))
        self.routeLabel.setText(QCoreApplication.translate("Form", u"Max. Route Grade", None))
        self.boulderLabel.setText(QCoreApplication.translate("Form", u"Max. Boulder Grade", None))
        self.mailLabel.setText(QCoreApplication.translate("Form", u"Email", None))
        self.emailLineEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Your email", None))
        self.commentLabel.setText(QCoreApplication.translate("Form", u"Comment", None))
        self.commentTextEdit.setPlaceholderText(QCoreApplication.translate("Form", u"Comment", None))
        self.spanSpinBox.setSuffix(QCoreApplication.translate("Form", u" cm", None))
    # retranslateUi

