#!/usr/bin/env python

import subprocess

options = [
            # createS2p, inputTxtFiles, cableLength, t1, t2, outputTouchstoneSubFile, SParamterComp
            [1, 'input_cable_data.txt', '35', 0.2, 0.4, '0', '11'], #S11
            [0, 'input_cable_data.txt', '35', 0.2, 0.4, '0', '12'], #S12
            [0, 'input_cable_data.txt', '35', 0.2, 0.4, '1', '21'], #S21
	  ]

command = 'python plotVNAFeatures.py --createS2p={0:<3.0f} --inputTxtFiles={1:s} --cableLength={2:s} --t1={3:<3.2f} --t2={4:<3.2f} --outputTouchstoneSubFile={5:s} --SParamterComp={6:s}'

for opt in options:
    s = command.format(opt[0], opt[1], opt[2], opt[3], opt[4], opt[5], opt[6])
    print(s)
    subprocess.call( [s, ""], shell=True )	

