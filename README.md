# Resistivity
Induced Polarization (Frequency and Time Domain) and DC Resistivity acquisition and processing.

This is a pycharm project.

model/ 

contains data objects, hardware specific python classes and C++ base waveform inversion code

main/ 

contains all the resistivity measurement technique codes

main/DC Resistivity/ScreenShot.py

captures the Oscilloscope Screen when setup for DC Measurement.

main/Frequency Domain IP/DataAcquire.py

setups the oscilloscope and records waveforms and rock response for a given set of frequencies

main/Frequency Domain IP/WaveformQC_cCosFit.py

generates a powerpoint presentation with all the data and parameter fit overlay plots.

main/Frequency Domain IP/ProcessWaveforms.py

processes the recorded waveforms into parameter excel file using C++ based waveform inversion code

main/Frequency Domain IP/Impedance.mlapp

is a Matlab GUI program that processes the waveform parameter excel file and plots the resistance or resistivity plots

main/Time Domain IP/DataAcquire.py

Once the oscilloscope is setup, this file records the time domain IP data given number of times, averages them and saves them into a excel file

main/Time Domain IP/TDIP_Process.m

is a Matlab Script to plot the TDIP data on which all the analysis can be done.
