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

