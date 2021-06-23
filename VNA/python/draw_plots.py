#!/usr/bin/env python

import subprocess

options = [
            # createS2p, inputDir, inputTxtFiles, cableName, cableLength (cm), t1, t2, outputTouchstoneSubFile, SParamterComp
            # [1, '../example_data',                'input_cable_data.txt',         '',                          '35',  0.2,   0.4, '0', '11'], #S11
            # [0, '../example_data',                'input_cable_data.txt',         '',                          '35',  0.2,   0.4, '0', '12'], #S12
            # [0, '../example_data',                'input_cable_data.txt',         '',                          '35',  0.2,   0.4, '1', '21'], #S21
            # [1, '../data',                        'johncable3_2m.txt',            'johncable3_2m',            '200',  3.0,  15.0, '0', '11'], #S11
            # [0, '../data',                        'johncable3_2m.txt',            'johncable3_2m',            '200',  3.0,  15.0, '0', '12'], #S12
            # [0, '../data',                        'johncable3_2m.txt',            'johncable3_2m',            '200',  3.0,  15.0, '1', '21'], #S21
            # [1, '../data',                        'johncable4.txt',               'johncable4',               '100',  2.0,  10.0, '0', '12'], #S12
            #[1, '../data/Cable_120_beforeLashing',  'Cable_120_beforeLashing.txt',  'Cable_120_beforeLashing',   '80',  2.0,   8.0, '0', '12'], #S12
            [1, '../data/Cable_120_afterLashing',   'Cable_120_afterLashing.txt',   'Cable_120_afterLashing',    '80',  2.0,   8.0, '0', '12'], #S12
            #[1, '../data/JohnCable4/', 'JohnCable4.txt', 'JohnCable4', '80',  2.0,  8.0, '0', '12'], #S12
            #[1, '../data/JohnCable5/', 'JohnCable5.txt', 'JohnCable5', '80',  2.0,  8.0, '0', '12'], #S12
	  ]

command = 'python3 plotVNAFeatures.py --createS2p={0:<3.0f} --inputDir={1:s} --inputTxtFiles={2:s} --cableName={3:s} --cableLength={4:s} --t1={5:<3.2f} --t2={6:<3.2f} --outputTouchstoneSubFile={7:s} --SParamterComp={8:s}'

for opt in options:
    s = command.format(opt[0], opt[1], opt[2], opt[3], opt[4], opt[5], opt[6], opt[7], opt[8])
    print(s)
    subprocess.call( [s, ""], shell=True )	

