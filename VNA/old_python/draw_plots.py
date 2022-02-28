#!/usr/bin/env python

import subprocess
from plotVNAFeatures import analyze

options = [
            # createS2p, inputDir, inputTxtFiles, cableName, cableLength (cm), t1, t2, outputTouchstoneSubFile, SParamterComp
            # [1, '../example_data',                'input_cable_data.txt',         '',                          '35',  0.2,   0.4, '0', '11'], #S11
            # [0, '../example_data',                'input_cable_data.txt',         '',                          '35',  0.2,   0.4, '0', '12'], #S12
            # [0, '../example_data',                'input_cable_data.txt',         '',                          '35',  0.2,   0.4, '1', '21'], #S21
            # [1, '../data',                        'johncable3_2m.txt',            'johncable3_2m',            '200',  3.0,  15.0, '0', '11'], #S11
            # [0, '../data',                        'johncable3_2m.txt',            'johncable3_2m',            '200',  3.0,  15.0, '0', '12'], #S12
            # [0, '../data',                        'johncable3_2m.txt',            'johncable3_2m',            '200',  3.0,  15.0, '1', '21'], #S21
            # [1, '../data',                        'johncable4.txt',               'johncable4',               '100',  2.0,  10.0, '0', '12'], #S12
            #[1, '../data/JohnCable4/', 'JohnCable4.txt', 'JohnCable4', '80',  2.0,  8.0, '0', '12'], #S12
            #[1, '../data/JohnCable5/', 'JohnCable5.txt', 'JohnCable5', '80',  2.0,  8.0, '0', '12'], #S12
            #[1, 'data/Cable_120_beforeLashing',  'data/Cable_120_beforeLashing.txt',  'Cable_120_beforeLashing',   '80',  2.0,   8.0, '0', '12'], #S12
            #[1, 'data/Cable_120_afterLashing',   'data/Cable_120_afterLashing.txt',   'Cable_120_afterLashing',    '80',  2.0,   8.0, '0', '12'], #S12
            #[1, '../data/Comparison_2021_07_26', 'Comparison_2021_07_26.txt', 'Comparison_2021_07_26', '100', 0.5, 1.0, '0', '12'], #S12
            [1, 'data/Cable_203', 'Cable_203.txt', 'Cable_203', '100', 0.5, 5.5, '0', '12'], #S12
	  ]

for opt in options:
    # use "times" to specify different time windows per cable
    times = []
    
    # v1 of times
    #times.append([0.5, 1.0])
    #times.append([2.0, 4.0])
    #times.append([2.0, 7.0])
    #times.append([2.0, 4.0])
    #times.append([2.0, 7.0])
    
    # v2 of times
    #times.append([0.5, 1.0])
    #times.append([0.5, 2.5])
    #times.append([0.5, 5.5])
    #times.append([0.5, 2.5])
    #times.append([0.5, 5.5])
    
    print("Analyzing {0}".format(opt[3]))
    #analyze(createS2p, inDir, inputTxtFiles, cableName, cableLength, t1, t2, outDir, s2pDir, subfile, comp)
    analyze(opt[0], opt[1], opt[2], opt[3], opt[4], opt[5], opt[6], "Plots", "s2pDir", opt[7], opt[8], times)

