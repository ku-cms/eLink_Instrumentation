#!/usr/bin/env python

import subprocess

options = [
           #['Redo_VNA', 'TP_1p4m_35_ChD0.vna'],
           #['Redo_VNA', 'TP_1p4m_35_ChD1_redo_v1.vna'],
           #['Redo_VNA', 'TP_1p4m_35_ChCMD_redo_v1.vna'],

           #['Redo_VNA', 'TP_35cm_60_ChD0_redo.vna'],
           #['Redo_VNA', '082820_TP_60_35cm_ChD1_KA.vna'],
           #['Redo_VNA', 'TP_35cm_60_ChCMD_redo.vna'],
            
            ['data', '9_feb_2021_test1_5.vna'],
    
	  ]

command = 'python python/readVNADataSKRF.py --data_directory={0:s} --basename={1:s}'

for opt in options:
    s = command.format(opt[0], opt[1])
    print(s)
    subprocess.call( [s, ""], shell=True )	

