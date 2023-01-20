# Critical Force Testing
This is a desktop application to measure climbing specific finger strength metrics such as critical force. With this software, it's possible to capture the force applied to a load-cell and analyse the data.

### What is critical force?
There is a research paper of Dave Giles et al. (Lattice Training Ltd.) that describes why critical force can be a useful metric for climbers and how it can be measured. This whole software is based on this paper. The paper can be accessed via [this link](https://www.researchgate.net/publication/343601001_An_All-Out_Test_to_Determine_Finger_Flexor_Critical_Force_in_Rock_Climbers).

### Which hardware is required?
* A load-cell (preferably S-type) and 2 eyebolts to hang it up. The maximum load should be higher than the force you can apply to a 20mm crimp with one arm. As long as you're not Alex Megos, 100kg should be fine.
* A (wooden) finger rung, that is somehow attached to the load-cell. Preferably 20mm with 10mm radius to ensure comparability.
* A load-cell amplifier (NAU7802). I am using [this one](https://www.sparkfun.com/products/15242) but [this one](https://www.adafruit.com/product/4538) should work as well. Attention! This software is not compatible with the commonly used HX711 amplifier. 
* [An MCP2221A USB board](https://www.adafruit.com/product/4471) to connect the amplifier to a computer via USB.
* A cable to connect the MCP2221A and the NAU7802 (Qwiic/STEMMA QT compatible JST-SH cable).

### Which software is required?
* If you want to use the software, you can download an executable for Windows (64bit) **here** (TODO). Just start the "Critical Force.exe", that's it. No installation required.
* If you want to contribute to the source code, fix some bugs, or change the background color to pink, you need Python 3. I've developed the software with version 3.11. You can use the [requirements.txt](requirements.txt) file to install the required packages with pip.

