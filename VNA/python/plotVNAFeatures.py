#!/usr/bin/env python3
'''
Created on Mon Mar 1 02:21:48 2021

@author: skhalil

The script writes the data collected by VNA (.txt) into .s2p format, and 
plot the S paramters in frequency domain, and impedance in time domain. 
Some manupulation of S parameter indices is done since the data is for 4-point 
VNA measurements, where as the skrf library understands it for the 2-point 
VNA measurements.

    # *.s2p Files format
    # Each record contains 1 stimulus value and 4 S-parameters (total of 9 values)
    #Stim  Real (S11)  Imag(S11)  Real(S21)  Imag(S21)  Real(S12)  Imag(S12)  Real(S22)  Imag(S22)

    # ==== our file format for vna_0: ====
    #!freq  RelS11    ImS11    RelS12    ImS12    RelS13    ImS13    RelS14   ImS14

    # parameter in file => read from software

    # S11 S13          00  01            S11 S12
    #            ---->           ---->
    # S12 S14          10  11            S21 S22


    # ==== our file format for vna_1: ====
    #!freq  RelS21    ImS21    RelS22    ImS22    RelS23    ImS23    RelS24   ImS24

    # parameter in file => read from software

    # S21 S23          00  01            S11 S12
    #            ---->           ---->
    # S22 S24          10  11            S21 S22

'''

import sys, re, os
from pylab import *
import numpy as np
import skrf as rf
import pylab
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import style
import statistics

#rf.stylely()
#print(rf.__version__)

###################
# helper functions
###################

def ensure_dir(file_name):
    if not os.path.exists(file_name):
        os.mkdir(file_name)
        
def createLabels():
    x_labels=[]
    for i in range(len(files)):
        ff    = str(outDir+"/"+files[i]) 
        label = ff.split('.vna')[0].split('/')[-1:][0]
        x_labels.append(label)
    return x_labels

def set_axes(ax, title, xmin, xmax, ymin, ymax, nolim):
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.grid(True, color='0.8', which='minor')
    ax.grid(True, color='0.4', which='major')
    ax.set_title(title) # Time domain
    if not nolim:
        ax.set_xlim((xmin, xmax))
        ax.set_ylim((ymin, ymax))
    plt.tight_layout()

# https://www.tutorialfor.com/questions-285739.htm
def display_mean_impedance(ax, t1, t2, col): 
    lines = ax.get_lines()

    # Delete all elements of the array (except the last one) correponding to a line drawn in ax.
    # This is a brute force way of resetting the line data to the data current line.
    if len(lines)>1:
        del lines[:-1]

    # store the line arrays into list. Every line drawn on the ax is considered as data
    Y = [line.get_ydata() for line in lines]
    X = [line.get_xdata() for line in lines]

    # create a table, and since the list X and Y should have size=1, place the first
    # element (array) in pandas table columns t and Z
    df = pd.DataFrame()
    df['t'] = X[0]
    df['Z'] = Y[0]

    # get the mean value of Z for a given time difference
    Z_mean =  df.query('t >=@t1 & t<=@t2').agg({'Z': 'mean'})
    print("Mean impedance [{0} ns, {1} ns] = {2:.2f} ohms for {3}".format(t1, t2, Z_mean.values[0], lines[0]))
    # plot the average line
    x_coor = [t1, t2]
    y_coor = [Z_mean, Z_mean]
    ax.plot(x_coor, y_coor, color=col, linewidth=1, label='', linestyle='--')

def getName(input_string):
    match = re.match(r'TP_\w+_\d+', input_string)
    name  = match.group()
    if '1p4' in name:
        name = name.replace('1p4', '1.4')
    return name

#######################################
#            Options                  #
#######################################
from optparse import OptionParser
parser = OptionParser()

parser.add_option('--createS2p', type='int', action='store',
                      default=1,
                      dest='createS2p',
                      help='bool if 1 then create .s2p files, if 0 then they already exist and no need to recreate them')

parser.add_option('--inputDir',  metavar='T', type='string', action='store',
                      default='../example_data',
                      dest='inputDir',
                      help='directory with example input files')

parser.add_option('--inputTxtFiles', metavar='F', type='string', action='store',
                      default = "input_cable_data.txt",
                      dest='inputTxtFiles',
                      help='Input txt files')

parser.add_option('--cableName',  metavar='T', type='string', action='store',
                      default='',
                      dest='cableName',
                      help='cable name (required for non-standard names)')

parser.add_option('--cableLength', metavar='F', type='string', action='store',
                      default = "35",
                      dest='cableLength',
                      help='cable lenght in cm')

parser.add_option('--t1', metavar='F', type='float', action='store',
                      default = 0.2,
                      dest='t1',
                      help='start time to take the average on the time domain plot')

parser.add_option('--t2', metavar='F', type='float', action='store',
                      default = 0.4,
                      dest='t2',
                      help='stop time to take the average on the time domain plot')

parser.add_option('--outputDir', metavar='T', type='string', action='store',
                      default='Plots',
                      dest='outputDir',
                      help='directory to store plots')

parser.add_option('--outputTouchstone', metavar='T', type='string', action='store',
                      default='s2pDir',
                      dest='outputTouchstone',
                      help='directory to store resulted touch stone files')

parser.add_option('--outputTouchstoneSubFile', metavar='T', type='string', action='store',
                      default='0',
                      dest='outputTouchstoneSubFile',
                      help='subfile to open from one of the 10 created .s2p files')

parser.add_option('--SParamterComp', metavar='T', type='string', action='store',
                      default='11',
                      dest='SParamterComp',
                      help='S-paramter to draw')

(options,args)  = parser.parse_args()
createS2p       = bool(options.createS2p)
inDir           = options.inputDir
inputTxtFiles   = options.inputTxtFiles
cableName       = options.cableName
cableLength     = options.cableLength
t1              = options.t1
t2              = options.t2
outDir          = options.outputDir
s2pDir          = options.outputTouchstone
subfile         = options.outputTouchstoneSubFile
comp            = options.SParamterComp

# ========= end: options ============= #

verbose = False

files = []
with open(inputTxtFiles, 'r') as fl:
    for line in fl.readlines():
        files.append(line.strip())
    fl.close    

if verbose:
    print("input file list: {0}".format(inputTxtFiles))
    for f in files:
        print (" - {0}".format(f))

ensure_dir(outDir)
ensure_dir(s2pDir)

############################
# Create the .s2p files
############################
if createS2p:
    # convert the .txt files into table with columns corresponding to .s2p format
    for f in files:
        infile = pd.read_csv(inDir+'/'+f+'.txt', names=['pt','f','s11R','s11I','s12R','s12I','s13R','s13I','s14R','s14I'], delim_whitespace=True, skiprows=1)
        infile.dropna(how='all')
        pd.set_option("display.max_rows", 5)
          
        fileindex = 0 # this will be increment to upto 9 corresponding to 10 .s2p files
        prevF     = 0
        basename = f.rpartition('.')[0]
        if verbose:
            print("f: {0}, basename: {1}".format(f, basename))
           
        for i, row in infile.iterrows():
            if row['pt'] == 'PARAMETER:':
                # new set of points
                try:
                    if not f.closed:
                        f.close()
                except:
                    pass
                filename = s2pDir+'/'+basename+ '_' + str(fileindex)+'.s2p'
                fileindex += 1
                f = open(filename,'w')
                f.write('# GHZ	S	RI	R	50.0\n')
            
                try:
                    #print (row['f'][1:-1], row['s11R'][1:-1], row['s11I'][1:-1], row['s12R'][1:-1] )
                    f.write(f"!freq       Rel{row['f'][1:-1]}       Im{row['f'][1:-1]}      Rel{row['s11R'][1:-1]}       Im{row['s11R'][1:-1]}        Rel{row['s11I'][1:-1]}        Im{row['s11I'][1:-1]}         Rel{row['s12R'][1:-1]}      Im{row['s12R'][1:-1]}\n")
                except:
                    if row['f'][1:-1] == 'SDD':
                        f.write(f"!freq\tRelS11\tImS11\n")
                prevF = 0
            try:
                if float(row['s11R']) == float(row['s11R']) and float(row['f'])>prevF:
                    f.write(f"{float(row['f']):.3f}\t{float(row['s11R'])}\t{float(row['s11I'])}\t{float(row['s12R'])}\t{float(row['s12I'])}\t{float(row['s13R'])}\t{float(row['s13I'])}\t{float(row['s14R'])}\t{float(row['s14I'])}\n")
                    prevF = float(row['f'])
            except:
                pass

########################
#        Plots         #
########################
S_ij = ''
if   comp == '11' and subfile == '0': S_ij = '11'
elif comp == '12' and subfile == '0': S_ij = '21'
elif comp == '21' and subfile == '1': S_ij = '11'
i = int(S_ij[0])
j = int(S_ij[1])

labels = createLabels()

colors = [
            'xkcd:cherry red',
            'xkcd:tangerine',
            'xkcd:green',
            'xkcd:neon green',
            'xkcd:azure',
            'xkcd:cyan',
            'xkcd:neon purple',
            'xkcd:coral',
            'xkcd:magenta',
            'xkcd:goldenrod',
            'xkcd:seafoam green',
            'xkcd:lavender',
            'xkcd:turquoise',
            'xkcd:electric blue',
            'xkcd:purple',
]

with style.context('seaborn-darkgrid'):    
    fig0 = plt.figure(figsize=(10,4))
    fig0.patch.set_facecolor('xkcd:black')
    plt.style.use('dark_background')
    ax0=plt.subplot(1,2,1)
    ax1=plt.subplot(1,2,2)
    
    ax0.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax0.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax0.grid(True, color='0.8', which='minor')
    ax0.grid(True, color='0.4', which='major')

    for n in range(len(labels)):
        label = labels[n]
        color = colors[n]
        net = rf.Network(s2pDir+'/'+label+'_'+subfile+'.s2p', f_unit='ghz') # 33
        
        ## ---Frequency Domain Plots---:
        net_dc = net[i,j].extrapolate_to_dc(kind='linear')       
        net_dc.plot_s_db(label='S'+comp+','+label, ax=ax0, color=color)  
        # set_axes(ax, title, xmin, xmax, ymin, ymax, nolim)
        set_axes(ax0, 'Frequency Domain', 0.0, 6.0e9, -50.0, 100.0, nolim=False)

        ## ---Time Domain Plots---:
        net_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+','+label, ax=ax1, color=color)
        display_mean_impedance(ax1, t1, t2, "xkcd:light magenta")
        # set_axes(ax, title, xmin, xmax, ymin, ymax, nolim)
        set_axes(ax1, 'Time Domain', 0.0, 30.0, 0.0, 400.0, nolim=False)

    if cableName:
        cable_ID = cableName
    else:
        cable_ID = getName(labels[0])   
    
    if verbose:
        print("labels[0]: {0}, cable_ID: {1}".format(labels[0], cable_ID))
    
    fig0.savefig("{0}/{1}_freq_time_Z_rf_S{2}.png".format(outDir, cable_ID, comp))

#pylab.show()        
#input('hold on')

