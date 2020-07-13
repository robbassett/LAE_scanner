# LAE_scanner

LAE_scanner is the ultimate tool for identifying those pesky emission line only sources from your MAGPI datacube. The required inputs are a MAGPI cube (.fits) and the associated LSDcat catalog (.cat), the latter will be provided. 

# "Installation"

To get started (assuming you have git) simply move to the folder where you want LAE_scanner to live and enter this command into the terminal:
git clone https://github.com/robbassett/LAE_scanner.git

Congratulations, LAE_scanner is "installed"!

# Dependencies
The following python packages are required to run LAE_scanner:

numpy

matplotlib

tkinter

astropy

bottleneck

# Usage
To use LAE_scanner, navigate into the LAE_scanner folder and type this into your terminal:
pythion LAE_gui.py

You will be presented with a tkinter GUI with a nifty procedurally generated artwork for your viewing pleasure. This artwork is designed to get you pumped up for the upcoming (painfully tedious) task of sifting through noise to find LAEs! super lustiges Spiel!

To get started press the first button "--Enter Classifier--" and enter your ID without spaces. Then press "--Select Cube--" and navigate the to datacube file you are going to classify. Next press "--Select Catalog--" and navigate to the LSDcat output (.cat) file you will be using as your reference catalog. Finally, press "--Start Classifying--" to get started.

Each object will display a aperture spectrum with the signal in black and noise in red (note the two y-axes are not the same scaling) in the left panel, and the narrowband image in the right panel. The green area in the left panel shows the wavelengths summed to produce the image in the right panel, and the white circle in the right panel shows the aperture from which the spectrum in the left panel is extracted.

Use the pull down menus to classify the object and give your classification a confidence rating (1=low, 5=high), then press the "next" button to grab the next candidate. You can save your classifications at any time by pressing "save", and if you mess up you can go back (which overwrites your previous classification). Once you get to the end you will see a special message, your output will be saved, and the program will terminate.

In the future, you will be able to resume your classifications at a later time by reading in a previous savefile, but this is not yet implemented.
