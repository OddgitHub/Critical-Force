from PySide6.QtWidgets import QVBoxLayout, QWidget, QLineEdit

class DataGui(QWidget):
    def __init__(self):
        super().__init__()        

        pageLayout = QVBoxLayout()


        nameEdit = QLineEdit()
        nameEdit.setPlaceholderText("Enter your name")
        pageLayout.addWidget(nameEdit)

        self.setLayout(pageLayout)