#!/usr/bin/env python

import subprocess

# WARNING:
# Write file names ending in .vna
# Do not include .txt (do not use .vna.txt)

options = [
           #['Redo_VNA', 'TP_1p4m_35_ChD0.vna'],
           #['Redo_VNA', 'TP_1p4m_35_ChD1_redo_v1.vna'],
           #['Redo_VNA', 'TP_1p4m_35_ChCMD_redo_v1.vna'],

           #['Redo_VNA', 'TP_35cm_60_ChD0_redo.vna'],
           #['Redo_VNA', '082820_TP_60_35cm_ChD1_KA.vna'],
           #['Redo_VNA', 'TP_35cm_60_ChCMD_redo.vna'],
            
            # using Cu calibration plate
            #['data', '9_feb_2021_test1_1.vna'],
            #['data', '9_feb_2021_test1_2.vna'],
            #['data', '9_feb_2021_test1_3.vna'],
            #['data', '9_feb_2021_test1_4.vna'],
            #['data', '9_feb_2021_test1_5.vna'],
            
            # cable 100
            #['data', 'TP_35cm_100_test1_1.vna'],
            
            # calibration
            #['data', 'calibration_test.vna'],
            #['data', 'small_SMA.vna'],
            #['data', 'straight_SMA.vna'],
            
            # cable 129
            #['data', 'TP_0p35m_129_ChCMD.vna'],
            #['data', 'TP_0p35m_129_ChD0.vna'],
            #['data', 'TP_0p35m_129_ChD1.vna'],
            #['data', 'TP_0p35m_129_ChD2.vna'],
            #['data', 'TP_0p35m_129_ChD3.vna'],

            # cable 100
            # CMD_v1: CMD on 33pin conenctions: VNA 1 to CMD_P (12), VNA 2 to CMD_N (13)
            # CMD_v2: CMD on 33pin conenctions: VNA 1 to CMD_D (13), VNA 2 to CMD_P (12)
            ['data', 'TP_35cm_100_33pin_CMD_v2.vna'],
            ['data', 'TP_35cm_100_33pin_D0.vna'],
            ['data', 'TP_35cm_100_33pin_D1.vna'],
            ['data', 'TP_35cm_100_33pin_D2.vna'],
            ['data', 'TP_35cm_100_33pin_D3.vna'],

            # loopback cable, 45 pin
            ['data', 'loopback_45pin_36tpi_27tpi.vna'],
            ['data', 'loopback_45pin_18tpi_9tpi.vna'],
    
	  ]

command = 'python python/readVNADataSKRF.py --data_directory={0:s} --basename={1:s}'

for opt in options:
    s = command.format(opt[0], opt[1])
    print(s)
    subprocess.call( [s, ""], shell=True )	

