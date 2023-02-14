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

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from util.params import Params

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        aboutLabel = QLabel(
            "This software tool can be used to capture climbing specific finger strength measures, such as critical force. "
            "The software is free. It is licensed under GNU General Public License version 3.\n\n"
            "In order to use the software, a fingerboard is required that is attached to a load-cell. "
            "The load-cell has to be connected to a NAU7802 amplifier. The amplifier has to be connected to a MCP2221A "
            "breakout board via I2C.")
        aboutLabel.setWordWrap(True)

        linkLabel = QLabel("<a href=\"https://philaudio.wordpress.com/projects/climbing\">More information on how to build the hardware can be found here.</a>" )
        linkLabel.setOpenExternalLinks(True)

        licenseLabel = QLabel("The graphical user interface was built with PySide6 and PyQtGraph. The Circuit Pyhton driver \"cedargrove_nau7802\" is used to interface the NAU7802 ADC.\n\n"
            "If you encounter any issues, please reach out to philippbulling@gmail.com.")
        licenseLabel.setWordWrap(True)

        nameLabel = QLabel("Copyright 2023 Dr.-Ing. Philipp Bulling")
        versionLabel = QLabel("Software Version: " + Params.version.value)

        layout.addWidget(aboutLabel)
        layout.addWidget(linkLabel)
        layout.addWidget(licenseLabel)
        layout.addWidget(nameLabel)
        layout.addWidget(versionLabel)
        self.setLayout(layout)
        self.resize(430, 350)