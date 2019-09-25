# Resistivity
Induced Polarization (Frequency and Time Domain) and DC Resistivity acquisition and processing.

This is a pycharm project.

The folder is structured in the following format,

1. **main**
   * Contains all the data with data acquisition and processing scripts.
    1. **DC Resistivity**
        * **ScreenShot.py** takes a screenshot of the oscilloscope screen.
        * **A2B/S11T/DC_Resistivity.bmp** is the screenshot of the oscilloscope when the rock sample was connected to the Auto bridge balancing circuit. The readings can be taken from this screenshot to obtain resistivity in different modes.
        * **H2C/S11T/DC_Resistivity.bmp** is the screenshot of the oscilloscope when the rock sample was connected to the Auto bridge balancing circuit. The readings can be taken from this screenshot to obtain resistivity in different modes.
    2. **Frequency Domain IP**
        * **Samples** folder has all the recorded data for Auto-Bridge Balancing and Howland Constant Current Circuit along with the inverted data and a powerpoint presentation showing comparing the inversion parameter with the data
        * **DataAcquire.py** is a python script that communicates with the oscilloscope using the custom-built python class **pyMSO5104** to record data on all the channels which are saved into an excel file. This script can do a frequency sweep over a list of given frequency sweep, average the data given number of times to improve signal to noise ratio and make and save multiple measurements.
        * **ProcessWaveforms.py** inverts the waveform excel files acquired by **DataAcquire.py** for the cosine wave parameters amplitude, frequency, phase and dc offset and saves it in excel file.
        * **Impedance.mlapp** is a Matlab GUI program that loads the processed waveform excel file and allows the user to select the experimental setup configuration to process the data and display the results.
        * **WaveformQC.py** is a quality check python script that outputs a powerpoint presentation with the plots of data and synthetic fit using the inverted parameters.
    3. **Time Domain IP**
        * **H3C/S11T** folder contains the time series data for all the channels
        * **DataAcquire** acquires the data for the time domain IP based on the user input. It can average the reading for a given number of times to improve the signal to noise ratio.
2. **model**
    * Contains all the supporting files to make a successful measurement
    1. **data** 
        * Contains various data objects to hold various types of data.
    2. **hardware**
        * Contains hardware-specific python object to communicate with various hardware used in the measurement.
        * **mso5104** contains python object for communicating with the Rigol MSO5104 Oscilloscope. It communicates to the oscilloscope using the visa interface.
    3. **inversion**
        * **CosFit.pyd** is a C++ compiled sine waveform inversion algorithm that uses the optimizer from ALGLIB to minimized the difference between the model and the data and optimize the parameters in the process. The C++ files can be found at [https://github.com/sanjaykpandit/Sine-Wave-Inversion].
