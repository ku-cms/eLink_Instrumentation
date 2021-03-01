# VNA Data Processing

Input files: touchstone or .txt

## Scripts

### VNADataInspection.py
Reads .s4p file

### readVNAData.py
Extracts Z-impedance parameters from input text files using self defined function

### readVNADataSKRF.py
Converts .txt files to .s2p files and analyzes S-parameter properties using skrf library

### create_all_s2p.py
Calls readVNADataSKRF.py on a list of files

### plotImpedance.py
Plots S11 and TD11 using .s2p input files

### plotVNAFeatures.py
Merge of the steps of creating .s2p files and plotting the S-parameters and Impedance in frequency and time domain. 

### draw_plots.py 
Driver script to plot all other S-parameters options such as S12 and S21 and execute 'plotVNAFeatures.py'. 

### input_cable_data.txt
The input for 'plotVNAFeatures.py' script which are set of measurements for all channels of a particular cable, with last file reserved to compare with the calibration data. 

