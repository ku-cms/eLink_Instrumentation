#!/usr/bin/env python

import subprocess

options = [
           #['Redo_VNA', 'TP_1p4m_35_ChD0.vna'],
           #['Redo_VNA', 'TP_1p4m_35_ChD1_redo_v1.vna'],
          # ['Redo_VNA', 'TP_1p4m_35_ChCMD_redo_v1.vna'],

           #['Redo_VNA', 'TP_1p4m_36_ChD0_redo_v2.vna'],
           #['Redo_VNA', 'TP_1p4m_36_ChD1_redo_v3.vna'],
           #['Redo_VNA', 'TP_1p4m_36_ChCMD_redo_v3.vna'],

           #['Redo_VNA', 'TP_1p4m_41_ChD0_redo_v2.vna'],
           #['Redo_VNA', 'TP_1p4m_41_ChD1_redo_v2.vna'],
           #['Redo_VNA', 'TP_1p4m_41_ChCMD_redo_v3.vna'],

           #['Redo_VNA', 'TP_1p4m_42_ChD0.vna'],
           #['Redo_VNA', 'TP_1p4m_42_ChD1.vna'],
           #['Redo_VNA', 'TP_1p4m_42_ChCMD_redo.vna'],
          
          # ['Redo_VNA', 'TP_60_35cm_ChD1.vna'],
          # ['Redo_VNA', 'TP_61_35cm_ChD1.vna'],
          # ['Redo_VNA', 'TP_62_35cm_ChD1.vna'],
          # ['Redo_VNA', 'TP_63_35cm_ChD1.vna'],
           #['Redo_VNA', 'TP_1m_54_ChD0.vna'],
           #['Redo_VNA', 'TP_1m_54_ChD1.vna'],
           #['Redo_VNA', 'TP_1m_54_ChCMD.vna'],
          # ['Redo_VNA', 'TP_1m_55_ChD0.vna'],
          # ['Redo_VNA', 'TP_1m_55_ChD1.vna'],
          # ['Redo_VNA', 'TP_1m_55_ChCMD.vna'],
           # ['Redo_VNA', 'TP_1m_53_ChD0_redo.vna'],
           # ['Redo_VNA', 'TP_1m_53_ChD1_redo.vna'],
           # ['Redo_VNA', 'TP_1m_53_ChCMD_redo.vna'],
             #['Redo_VNA', 'TP_1m_23_ChD0_redo_v1.vna'],
           #['Redo_VNA', 'TP_1m_23_ChD1_redo_v1.vna'],
           #['Redo_VNA', 'TP_1m_23_ChCMD_redo_v1.vna'],

           #['Redo_VNA', 'TP_35cm_57_ChD0_redo_v1.vna'],
           #['Redo_VNA', 'TP_35cm_57_ChD1_redo_v1.vna'],
           #['Redo_VNA', 'TP_35cm_57_ChCMD_redo_v1.vna'],

           #['Redo_VNA', 'TP_35cm_60_ChD0_redo.vna'],
           #['Redo_VNA', '082820_TP_60_35cm_ChD1_KA.vna'],
           #['Redo_VNA', 'TP_35cm_60_ChCMD_redo.vna'],

           #['Redo_VNA', 'TP_35cm_61_ChD0_redo.vna'],
           #['Redo_VNA', '082820_TP_61_35cm_ChD1_KA.vna'],
           #['Redo_VNA', 'TP_35cm_61_ChCMD_redo.vna'],

            #['Redo_VNA', 'TP_35cm_62_ChD0_redo.vna'],
            #['Redo_VNA', '082820_TP_62_35cm_ChD1_KA.vna'],
            #['Redo_VNA', 'TP_35cm_62_ChCMD_redo.vna'],

            #['Redo_VNA', 'TP_35cm_63_ChD0_redo.vna'],
            #['Redo_VNA', '082820_TP_63_35cm_ChD1_KA.vna'],
            #['Redo_VNA', 'TP_35cm_63_ChCMD_redo.vna'],
    
	   ]


command = 'python readVNADataSKRF.py --basename={0:s}/{1:s}'

for opt in options:
    s = command.format(
      	opt[0], opt[1]
	)
	
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo %s"%s,""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)

    subprocess.call( [s, ""], shell=True )	


