# VNA Data Processing

Input files: touchstone or .txt

- VNADataInspection.py: reads .s4p file

- readVNAData.py: extracts Z-impedance parameters from input text files using self defined function

- readVNADataSKRF.py: converts .txt files to .s2p files and analyzes S-parameter properties using skrf library

- create_all_s2p.py: calls readVNADataSKRF.py on a list of files

- plotImpedance.py: plots S11 and TD11 using .s2p input files

