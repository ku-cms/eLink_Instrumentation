#!/usr/bin/env python
  
import subprocess


#if   subfile == '0':    comp = '12'#12
#elif subfile == '1':    comp = '21'

options = [
    ['2m',   '0', '12'],
    ['1p4m', '0', '12'],
    ['1m',   '0', '12'],
    ['35cm', '0', '12']
    ['',     '0', '12']
]

command = 'python plotImpedance_summary.py --group={0:s} --subfile={1:s} --comp={2:s}'

for opt in options:
    s = command.format(
      	opt[0], opt[1], opt[2]
	)
	
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo %s"%s,""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)

    subprocess.call( [s, ""], shell=True )	
