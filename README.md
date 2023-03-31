![A load-cell with a 20mm testing rung](https://philaudio.files.wordpress.com/2023/02/dscf4199-1.jpg?w=1024)

# Critical Force Testing
This is a desktop application to measure climbing specific finger strength metrics such as critical force. With this software, it's possible to capture the force applied to a load-cell and analyse the data.

### What is critical force?
There is a research paper of Dave Giles et al. (Lattice Training Ltd.) that describes why critical force can be a useful metric for climbers and how it can be measured. This whole software is based on this paper. The paper can be accessed via [this link](https://www.researchgate.net/publication/343601001_An_All-Out_Test_to_Determine_Finger_Flexor_Critical_Force_in_Rock_Climbers).

[Here](https://youtu.be/_EY3XA7e-pw?t=10m45s) you can find a video of Dave MacLeod doing the test at Lattice, including some explanations.

### Which hardware is required?
![The electronic components, connected to the load-cell](https://philaudio.files.wordpress.com/2023/01/hardware.jpg?w=1024)
* A load-cell (preferably S-type) and 2 eyebolts to hang it up. The maximum load should be higher than the force you can apply to a 20mm crimp with one arm. As long as you're not Alex Megos, 100kg should be fine.
* A (wooden) finger rung, that is somehow attached to the load-cell. Preferably 20mm with 10mm radius to ensure comparability.
* A load-cell amplifier (NAU7802). I am using [this one](https://www.sparkfun.com/products/15242) but [this one](https://www.adafruit.com/product/4538) should work as well. Attention! This software is not compatible with the commonly used HX711 amplifier. 
* [An MCP2221A USB board](https://www.adafruit.com/product/4471) to connect the amplifier to a computer via USB.
* A cable to connect the MCP2221A and the NAU7802 (Qwiic/STEMMA QT compatible JST-SH cable).

See also [this blog](https://philaudio.wordpress.com/projects/climbing/).

### Which software is required?
![Screenshot of the measurement view](https://philaudio.files.wordpress.com/2023/01/screenshot1-1.png)

This software contains everything you need, to connect to the load-cell, run a workout, and analyze the data.

#### Use the software
If you want to use the software, you can download the latest release here:
* [Executable for Windows (64bit)](https://github.com/OddgitHub/Critical-Force/releases/download/v1.2.0/Critical.Force.exe)
* [Application for Macs with Apple M chips](https://github.com/OddgitHub/Critical-Force/releases/download/v1.1.0/Critical.Force.app.zip) (unzip and allow app start)

#### Contribute to the source code
If you want to contribute to the source code, fix some bugs, or change the background color to pink, you need Python >=3.9. I've developed the software with version 3.11. You can use the [requirements.txt](requirements.txt) file to install the required packages with `pip install -r requirements.txt`.

The app is started via `python start.py`.

You can compile an executable/application for windows/mac via `pyinstaller start_win.spec` or `pyinstaller start_mac.spec`.

# License
Copyright 2023 Dr.-Ing. Philipp Bulling
	
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
