from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from util.params import Params

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        aboutLabel = QLabel(
            "This software tool can be used to capture climbing specific finger strength measures, such as critical force. "
            "The software is free. It requires a fingerboard, attached to a load-cell. "
            "The load-cell has to be connected to a NAU7802 amplifier. The amplifier has to be connected to a MCP2221A "
            "breakout board via I2C.")
        aboutLabel.setWordWrap(True)

        linkLabel = QLabel("<a href=\"https://philaudio.wordpress.com/projects/climbing\">More information can be found here.</a>" )
        linkLabel.setOpenExternalLinks(True)

        licenseLabel = QLabel("The graphical user interface was built with PySide6 and PyQtGraph and therefore this software licensed under GPLv2.\n\n"
            "If you encounter any issues, please reach out to philippbulling@gmail.com.")
        licenseLabel.setWordWrap(True)

        nameLabel = QLabel("Dr.-Ing. Philipp Bulling, 2023")
        versionLabel = QLabel("Software Version: " + Params.version.value)

        layout.addWidget(aboutLabel)
        layout.addWidget(linkLabel)
        layout.addWidget(licenseLabel)
        layout.addWidget(nameLabel)
        layout.addWidget(versionLabel)
        self.setLayout(layout)
        self.resize(430, 300)