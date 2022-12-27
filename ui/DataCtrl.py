from ui.DataGui import Ui_Form
from PySide6.QtWidgets import QWidget

class DataCtrl(QWidget):
    def __init__(self):
        super().__init__()        

        self.form = Ui_Form()
        self.form.setupUi(self)

        #========================================
        # Setup comboboxes
        #========================================
        self.climbingGradeList = self.createClimbingGradeList()
        for grade in self.climbingGradeList:
            self.form.routeComboBox.addItem(grade)
            self.form.boulderComboBox.addItem(grade)

        self.genderList = ['m','f','x']
        self.form.genderComboBox.addItems(self.genderList)

        #========================================
        # Init class members
        #========================================
        self.data = {}
        self.data['name'] = self.form.nameLineEdit.text()
        self.data['age'] = self.form.ageSpinBox.value()
        self.data['gender'] = self.form.genderComboBox.currentText()
        self.data['height'] = self.form.heightSpinBox.value()
        self.data['span'] = self.form.spanSpinBox.value()
        self.data['routeGrade'] = self.form.routeComboBox.currentText()
        self.data['boulderGrade'] = self.form.boulderComboBox.currentText()
        self.data['email'] = self.form.emailLineEdit.text()
        self.data['comment'] = self.form.commentTextEdit.toPlainText()

        #========================================
        # Connect signals
        #========================================
        self.form.nameLineEdit.textChanged.connect(self.onNameChanged)
        self.form.ageSpinBox.valueChanged.connect(self.onAgeChanged)
        self.form.genderComboBox.currentIndexChanged.connect( self.onGenderChanged )
        self.form.heightSpinBox.valueChanged.connect(self.onHeightChanged)
        self.form.spanSpinBox.valueChanged.connect(self.onSpanChanged)
        self.form.routeComboBox.currentIndexChanged.connect( self.onRouteGradeChanged )
        self.form.boulderComboBox.currentIndexChanged.connect( self.onBoulderGradeChanged )
        self.form.emailLineEdit.textChanged.connect(self.onEmailChanged)
        self.form.commentTextEdit.textChanged.connect(self.onCommentChanged)

    #========================================
    # Helper function
    #========================================
    @staticmethod
    def createClimbingGradeList():
        climbingGradeList = []
        climbingGradeList.append('n/a')
        suffixes = ['a', 'a+', 'b', 'b+', 'c', 'c+']
        for num in range(6,10):
            for suf in suffixes:
                climbingGradeList.append(str(num) + suf)
        return climbingGradeList

    #========================================
    # Slots for gui elements
    #========================================
    def onNameChanged(self, text):
        self.data['name'] = text

    def onAgeChanged(self, age):
        self.data['age'] = age

    def onGenderChanged(self, i):
        self.data['gender'] = self.genderList[i]

    def onHeightChanged(self, height):
        self.data['height'] = height

    def onSpanChanged(self, ape):
        self.data['span'] = ape

    def onRouteGradeChanged(self, i):
        self.data['routeGrade'] = self.climbingGradeList[i]

    def onBoulderGradeChanged(self, i):
        self.data['boulderGrade'] = self.climbingGradeList[i]

    def onEmailChanged(self, email):
        self.data['email'] = email

    def onCommentChanged(self):
        self.data['comment'] = self.form.commentTextEdit.toPlainText()
        
    #========================================
    # Get/set methods
    #========================================
    def getData(self):
        return self.data

    def setData(self, data):
        self.form.nameLineEdit.setText(data['name'])
        self.form.ageSpinBox.setValue(data['age'])
        self.form.genderComboBox.setCurrentIndex(self.genderList.index(data['gender']))
        self.form.heightSpinBox.setValue(data['height'])
        self.form.spanSpinBox.setValue(data['span'])
        self.form.routeComboBox.setCurrentIndex(self.climbingGradeList.index(data['routeGrade']))
        self.form.boulderComboBox.setCurrentIndex(self.climbingGradeList.index(data['boulderGrade']))
        self.form.emailLineEdit.setText(data['email'])
        self.form.commentTextEdit.setPlainText(data['comment'])