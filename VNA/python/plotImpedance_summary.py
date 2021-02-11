#!/usr/bin/env python3
from itertools import islice
import sys, re, os
import numpy as np
import statistics
import skrf as rf
#print(rf.__version__)
#print(.__version__)
#rf.stylely()

import pylab
import pandas as pd
import mpld3
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm
from matplotlib.ticker import AutoMinorLocator
from matplotlib import style
import pickle as pl

def getLabelFromFile(ff):
    fullpath = ff
    filename = str(fullpath).split('.vna')[0].split('/')[-1:][0]
    if 'redo' in filename:
        filename = filename.replace('_redo', '')
    #print (filename)
    return filename

def split(word):
    return [char for char in word]

def display_mean_mean_impedance(ax, arr_N, arr_Z,col):
    df = pd.DataFrame()
    df['arr_Z'] = arr_Z
    Z_mean_mean     = df.agg({'arr_Z': 'mean'})
    Z_mean_mean_std = df.agg({'arr_Z': 'std'})
    print(Z_mean_mean)
    x_coor = [arr_N[0],arr_N[-1]]
    y_coor = [Z_mean_mean, Z_mean_mean]
    #print('x_coor:', x_coor, ', y_coor:', y_coor)
    ax.plot(x_coor, y_coor, color=col, linewidth=2, label='', linestyle='-')
    
def get_display_mean_impedance(ax, t1, t2, col):##https://www.tutorialfor.com/questions-285739.htm
    
    lines = ax.get_lines()
    
    # delete any other array correponding to a line drawn in ax but the last one. This is a
    # brute force way of resetting the line data to the data current line    
    if len(lines)>1:
        del lines[:-1]

    # ressure that length of line is 1.
    #print('size of lines:', len(lines))

    # store the line arrays into list. Every line drawn on the ax is considered as data
    Y = [line.get_ydata() for line in lines]
    X = [line.get_xdata() for line in lines]

    # create a table, and since the list X and Y should have size=1, place the first
    # element (array) in pandas table columns t and Z    
    df = pd.DataFrame()
    #print (df)
    df['t'] = X[0]
    df['Z'] = Y[0]

    # get the mean value of Z for a given time difference
    Z_mean     = df.query('t >=@t1 & t<=@t2').agg({'Z': 'mean'})
    Z_mean_std = df.query('t >=@t1 & t<=@t2').agg({'Z': 'std'})    

    print("Mean imepdance from [%.1f, %.1f]ns = %.4f +/- %.4f for %s" % 
      (t1, t2, Z_mean.values[0], Z_mean_std.values[0], lines[0]))
    
    # plot the average line
    x_coor = [t1, t2]
    y_coor = [Z_mean, Z_mean]    
    #ax.plot(x_coor, y_coor, color=col, linewidth=1, label='', linestyle='--')
    return Z_mean, Z_mean_std
    
def set_axes(ax, title, ymin, ymax, xmin, xmax, nolim):
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.grid(True, color='0.8', which='minor')
    ax.grid(True, color='0.4', which='major')
    #ax.set_title(title) #Time domain
    if nolim==False:
        ax.set_xlim((xmin, xmax))
        ax.set_ylim((ymin, ymax))
    plt.tight_layout()

    
#####################
from optparse import OptionParser
parser = OptionParser()

parser.add_option('--group', metavar='T', type='string', action='store',
                  default='1m', #31, 15, 33 #calibration_test.vna 
                  dest='group',
                  help='length group')

parser.add_option('--subfile', metavar='T', type='string', action='store',
                  default='0', #31, 15, 33 #calibration_test.vna 
                  dest='subfile',
                  help='.s2p file to be read')

parser.add_option('--comp', metavar='T', type='string', action='store',
                  default='12', #31, 15, 33 #calibration_test.vna 
                  dest='comp',
                  help='componenet to plot from .s2p, if subfile=0, comp=12,11; if subfile=1, comp=21')

parser.add_option('--outDir', metavar='T', type='string', action='store',
                  default='Plots',
                  dest='outDir',
                  help='directory to store plots')
#####################
(options,args) = parser.parse_args()
option_dict = vars(options)

print(option_dict)
outDir = options.outDir
lg = options.group

if lg == '35cm':
    all_channels ={
               'Calibration_1m_':['straight_SMA.vna'],
               '62_35cm_36G': ['TP_35cm_62_ChD0_redo.vna', '082820_TP_62_35cm_ChD1_KA.vna','TP_35cm_62_ChCMD_redo.vna'],
               '63_35cm_36G': ['TP_35cm_63_ChD0_redo.vna', '082820_TP_63_35cm_ChD1_KA.vna','TP_35cm_63_ChCMD_redo.vna'],
               '57_35cm_34G': ['TP_35cm_57_ChD0_redo_v1.vna', 'TP_35cm_57_ChD1_redo_v1.vna', 'TP_35cm_57_ChCMD_redo_v1.vna'],
               '60_35cm_34G': ['TP_35cm_60_ChD0_redo.vna', '082820_TP_60_35cm_ChD1_KA.vna', 'TP_35cm_60_ChCMD_redo.vna'],
               '61_35cm_34G': ['TP_35cm_61_ChD0_redo.vna', '082820_TP_61_35cm_ChD1_KA.vna','TP_35cm_61_ChCMD_redo.vna']               
              }

elif lg == '1m':
    all_channels ={
               'Calibration_1m_':['straight_SMA.vna'],
               '23_1m_36G': ['TP_1m_23_ChD0_redo_v1.vna', 'TP_1m_23_ChD1_redo_v1.vna', 'TP_1m_23_ChCMD_redo_v1.vna'],
               '53_1m_36G': ['TP_1m_53_ChD0_redo.vna', 'TP_1m_53_ChD1_redo.vna', 'TP_1m_53_ChCMD_redo.vna'],
               '54_1m_34G': ['TP_1m_54_ChD0.vna', 'TP_1m_54_ChD1.vna', 'TP_1m_54_ChCMD.vna'],
               '55_1m_34G': ['TP_1m_55_ChD0.vna', 'TP_1m_55_ChD1.vna', 'TP_1m_55_ChCMD.vna'],
               '13_1m_32G': ['TP_1m_13_ChD3_ChCMD.vna']
              }

elif lg == '1p4m':
    all_channels ={
               'Calibration_1m_':['straight_SMA.vna'],
               '35_1p4m_36G': ['TP_1p4m_35_ChD0.vna', 'TP_1p4m_35_ChD1_redo_v1.vna', 'TP_1p4m_35_ChCMD_redo_v1.vna'],
               '36_1p4m_36G': ['TP_1p4m_36_ChD0_redo_v2.vna', 'TP_1p4m_36_ChD1_redo_v3.vna', 'TP_1p4m_36_ChCMD_redo_v3.vna'],
               '41_1p4m_34G': ['TP_1p4m_41_ChD0_redo_v2.vna', 'TP_1p4m_41_ChD1_redo_v2.vna', 'TP_1p4m_41_ChCMD_redo_v3.vna'],
               '42_1p4m_34G': ['TP_1p4m_42_ChD0.vna', 'TP_1p4m_42_ChD1.vna', 'TP_1p4m_42_ChCMD_redo.vna']
              }
    
elif lg == '2m':
    all_channels= {
               'Calibration_1m_':['straight_SMA.vna'],
               '72_2m_36G': ['TP_2m_72_ChD0.vna', 'TP_2m_72_ChD1.vna', 'TP_2m_72_ChCMD.vna'],
               '74_2m_36G': ['TP_2m_74_ChD0.vna', 'TP_2m_74_ChD1.vna', 'TP_2m_74_ChCMD.vna'],
               '46_2m_34G': ['TP_2m_46_ChD0_redo_v2.vna', 'TP_2m_46_ChD1_redo_v2.vna', 'TP_2m_46_ChCMD_redo_v2.vna']
              }
else:
    all_channels = {
               'Calibration_1m_':['straight_SMA.vna'],
               '62_35cm_36G': ['TP_35cm_62_ChD0_redo.vna', '082820_TP_62_35cm_ChD1_KA.vna','TP_35cm_62_ChCMD_redo.vna'],
               '63_35cm_36G': ['TP_35cm_63_ChD0_redo.vna', '082820_TP_63_35cm_ChD1_KA.vna','TP_35cm_63_ChCMD_redo.vna'],
               '23_1m_36G':   ['TP_1m_23_ChD0_redo_v1.vna', 'TP_1m_23_ChD1_redo_v1.vna', 'TP_1m_23_ChCMD_redo_v1.vna'],
               '53_1m_36G':   ['TP_1m_53_ChD0_redo.vna', 'TP_1m_53_ChD1_redo.vna', 'TP_1m_53_ChCMD_redo.vna'],   
               '35_1p4m_36G': ['TP_1p4m_35_ChD0.vna', 'TP_1p4m_35_ChD1_redo_v1.vna', 'TP_1p4m_35_ChCMD_redo_v1.vna'],
               '36_1p4m_36G': ['TP_1p4m_36_ChD0_redo_v2.vna', 'TP_1p4m_36_ChD1_redo_v3.vna', 'TP_1p4m_36_ChCMD_redo_v3.vna'],
               '72_2m_36G':   ['TP_2m_72_ChD0.vna', 'TP_2m_72_ChD1.vna', 'TP_2m_72_ChCMD.vna'],
               '74_2m_36G':   ['TP_2m_74_ChD0.vna', 'TP_2m_74_ChD1.vna', 'TP_2m_74_ChCMD.vna'],        
               '57_35cm_34G': ['TP_35cm_57_ChD0_redo_v1.vna', 'TP_35cm_57_ChD1_redo_v1.vna', 'TP_35cm_57_ChCMD_redo_v1.vna'],
               '60_35cm_34G': ['TP_35cm_60_ChD0_redo.vna', '082820_TP_60_35cm_ChD1_KA.vna', 'TP_35cm_60_ChCMD_redo.vna'],
               '61_35cm_34G': ['TP_35cm_61_ChD0_redo.vna', '082820_TP_61_35cm_ChD1_KA.vna','TP_35cm_61_ChCMD_redo.vna'],
               '54_1m_34G': ['TP_1m_54_ChD0.vna', 'TP_1m_54_ChD1.vna', 'TP_1m_54_ChCMD.vna'],
               '55_1m_34G': ['TP_1m_55_ChD0.vna', 'TP_1m_55_ChD1.vna', 'TP_1m_55_ChCMD.vna'],
               '41_1p4m_34G': ['TP_1p4m_41_ChD0_redo_v2.vna', 'TP_1p4m_41_ChD1_redo_v2.vna', 'TP_1p4m_41_ChCMD_redo_v3.vna'],
               '42_1p4m_34G': ['TP_1p4m_42_ChD0.vna', 'TP_1p4m_42_ChD1.vna', 'TP_1p4m_42_ChCMD_redo.vna'],        
               '46_2m_34G': ['TP_2m_46_ChD0_redo_v2.vna', 'TP_2m_46_ChD1_redo_v2.vna', 'TP_2m_46_ChCMD_redo_v2.vna'],              
               '13_1m_32G': ['TP_1m_13_ChD3_ChCMD.vna']
    }

subfile = options.subfile
comp = options.comp
    
if comp == '11' and subfile == '0': S_ij = '11'
elif comp == '12'and subfile == '0': S_ij = '21'
elif comp == '21' and subfile == '1': S_ij = '11'
else: S_ij = ''

i = int(split(S_ij)[0])
j = int(split(S_ij)[1])
#print('S_ij ----->', i, j)

out_dir = 'Plots'
sub_out_dir = 'Redo_VNA'

#####################
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
#######################

fig = plt.figure(figsize=(12,8))
fig.patch.set_facecolor('xkcd:black')
plt.style.use('dark_background')

ax0=plt.subplot(3,1,1)
ax1=plt.subplot(3,1,2)
ax2=plt.subplot(3,1,3)

n = len(all_channels)
COLOR = cm.rainbow(np.linspace(0,1,n))
counter = 0
x_labels=[]
y_va = []##??
all_meas = []
l_36 = []; n_36 =0
l_34 = []; n_34 =0

ax0.set_title('TD'+comp)
for key, ls_ch in all_channels.items():
    
    c = COLOR[counter]
    if   '2m'   in key: lo = 5; hi=18 ;
    elif '1p4m' in key: lo = 4; hi=12 ;
    elif '1m'   in key: lo = 4; hi=8 ; 
    elif '35cm' in key: lo = 2; hi=4.5 ;
    elif '20cm' in key: lo = 2; hi=4  ; 
    else:               lo = 0; hi=30 ; 
    
    awg = key.split('_')[2]
    if '36' in awg: axsub=ax0
    else: axsub=ax1

    if   '36' in awg: n_36 = n_36+1
    elif '34' in awg: n_34 = n_34+1

    if 'Calibration' in key: key = 'Calibration'
    x_labels.append(key)
    y_va_tuble =()
    for l_counter, ch in enumerate(ls_ch):
        f = 'Plots/Redo_VNA/'+ch
        #print(f)
        net = rf.Network(f+'_'+subfile+'.s2p', f_unit='ghz')
        net_dc   = net[i,j].extrapolate_to_dc(kind='linear')
       
        if 'D0' in ch:   ch_name = 'D0'
        elif 'D1' in ch: ch_name = 'D1'
        elif 'CMD' in ch: ch_name = 'CMD'
        else: ch_name = ''
        x_lab = key+'_'+ch_name
        
        if   l_counter == 0: ls = 'solid'
        elif l_counter == 1: ls = 'dotted'
        elif l_counter == 2: ls = 'dashed'
        elif l_counter == 3: ls = 'dashdot'
        elif l_counter == 4: ls = '---'
        
        net_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label=x_lab, ax=axsub, color=c, linestyle=ls)
        #ax0.legend(loc="lower left", ncol=n)
        axsub.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, 1.0),
                     fancybox=True, shadow=False, ncol=7)
        Z_mean, Z_mean_std = get_display_mean_impedance(axsub, lo, hi, c)
        set_axes(axsub, 'Time Domain (TD'+comp+')', 50.0, 300.0, 0.0, 30.0, 0)
        
        if   '36' in awg: l_36.append(Z_mean)
        elif '34' in awg: l_34.append(Z_mean)
        
        ax2.errorbar(counter, Z_mean, Z_mean_std, linestyle='None', marker='o', color=c)
        set_axes(ax2, 'Cable Vs Ave Impedance (TD'+comp+')', 100.0, 200.0, 0, n, 0)
        y_va_tuble = y_va_tuble+(Z_mean,)
        all_meas.append(x_lab)

    counter = counter+1    
    y_va.append(y_va_tuble)

fig.subplots_adjust(bottom=0.15, hspace=0.4)    
ax2.set_xlabel('Cable Name')
ax2.set_ylabel('Ave Z (ohms)')
ax2.set_xticks(np.arange(0,n,1))
ax2.set_xticklabels(x_labels, rotation='45', fontsize=8)

arr_N_36 = np.arange(1,n_36+1,1)
display_mean_mean_impedance(ax2, arr_N_36, l_36, 'b')
arr_N_34 = np.arange(n_36+1, n_36+n_34+1,1)
display_mean_mean_impedance(ax2, arr_N_34, l_34, 'r')

tooltip = mpld3.plugins.PointLabelTooltip(y_va,labels=all_meas)
mpld3.plugins.connect(fig, tooltip)            
plt.show()    

fig.savefig(outDir+'/TP_'+lg+'_'+comp+'_summary.png')

