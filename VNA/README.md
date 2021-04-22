# VNA Data Processing

Input files: touchstone file (.s2p, .s4p) or VNA output file (.vna.txt)

## Setup
Follow the instrutions [here](https://github.com/ku-cms/eLink_Instrumentation).

## Scripts
First activate the conda environment with the necessary packages based on the instructions [here](https://github.com/ku-cms/eLink_Instrumentation).
```
conda activate .venv
```

Then you can try running some of these scripts.

### create_all_s2p.py
Calls 'readVNADataSKRF.py' on a list of files.
```
cd VNA
python3 python/create_all_s2p.py
```

### draw_plots.py 
Driver script to plot all other S-parameters options such as S12 and S21 and execute 'plotVNAFeatures.py'. 
```
cd VNA/python
python3 draw_plots.py
```

### VNADataInspection.py
Reads .s4p file.

### readVNAData.py
Extracts Z-impedance parameters from input text files using self defined function.

### readVNADataSKRF.py
Converts .txt files to .s2p files and analyzes S-parameter properties using skrf library.

### plotImpedance.py
Plots S11 and TD11 using .s2p input files.

### plotVNAFeatures.py
Merge of the steps of creating .s2p files and plotting the S-parameters and Impedance in frequency and time domain.

### input_cable_data.txt
The input for 'plotVNAFeatures.py' script which are set of measurements for all channels of a particular cable, with last file reserved to compare with the calibration data. 

