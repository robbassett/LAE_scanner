# LAE_scanner

LAE_scanner is the ultimate tool for identifying those pesky emission line only sources from your MAGPI datacube. The required inputs are a MAGPI cube (.fits) and the associated LSDcat catalog (.cat), the latter will be provided. LAE_scanner is still under development, please email any bug notices or feature requests to rbassett.astro@gmail.com. 

Note that here are a couple of known bugs that I'm still sorting out, but these will not cause issue 99% of the time. First, occasionally the plotting script will fail for some objects and no images will appear. In this case please add a comment to your classification and mark the object as "unsure" (see below). Second, the app will suffer from a memory overload and simply crash if too many objects are classified in one session (~200-300). When this happens the most recent classifications will not have been saved. For now I have implemented an autosave function that activates every 10 classifications so at most you will have to redo 10 objects in the event of an unexpected crash.

# "Installation"

To get started (assuming you have git) simply move to the folder where you want LAE_scanner to live and enter this command into the terminal:

git clone https://github.com/robbassett/LAE_scanner.git

Congratulations, LAE_scanner is "installed"!

(Note: LAE_scanner was written on OSX Catalina with python 3.8.3, if you are having difficulties perhaps try creating a clean python 3.8 environment with Anaconda)

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

To get started press the first button "--Enter Classifier--" and enter your ID without spaces. Then press "--Select Cube--" and navigate the to datacube file you are going to classify. Next press "--Select Catalog--" and navigate to the LSDcat output (.cat) file you will be using as your reference catalog. Finally, press "--Start Classifying--" to get started. The first thing that happens is that LAE_scanner will produce a series of smaller cubes by clipping the full cube along the wavelength axis (but not spatially). This process takes a bit of time, so there will be a bit of a pause before the first object is displayed.

Each object will display a aperture spectrum with the signal in black and noise in red (note the two y-axes are not the same scaling) in the left panel, and the narrowband image in the right panel. The green area in the left panel shows the wavelengths summed to produce the image in the right panel, and the white circle in the right panel shows the aperture from which the spectrum in the left panel is extracted.

Use the pull down menus to classify the object and give your classification, 'yes', 'no', or 'unsure'. You can also add a comment to your classification by pressing the "comment" button. Once you're satisfied with your classification, press the "next" button to grab the next candidate. You can save your classifications at any time by pressing "save", and if you mess up you can go back (which overwrites your previous classification). Your classifications will also be auto saved every 10 objects using the default file name (unique to your chosen classifier ID, the cube name, and the catalog name). Once you get to the end you will see a special message, your output will be saved, and the program will terminate.

Additionally, you can close the app at any time and begin again later from where you left off. This is done by launching the app and pressing the "Load Previous" button and selecting the save file from your previous session. This will automatically extract the cube name/location and enter your classifier ID, so all that you need to do is press "Start Classifying". LAE_scanner does not assume that the mini cubes in the temporary folder are for the same field, so it reclips all the minicubes. This simply means that you will have to wait a bit before you get started. Once this is done, the first object displayed should be the last object you saw before closing the app in your previous session.
