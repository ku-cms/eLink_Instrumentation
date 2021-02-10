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

y_plot_value=[]
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
    y_plot_value.append(int(Z_mean.values))
    print(y_plot_value)
    x_coor = [t1, t2]
    y_coor = [Z_mean, Z_mean]
    ax.plot(x_coor, y_coor, color=col, linewidth=1, label='', linestyle='--')
    return Z_mean, Z_mean_std

def set_axes(ax, title, ymin, ymax, xmin, xmax, nolim):
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.grid(True, color='0.8', which='minor')
    ax.grid(True, color='0.4', which='major')
    ax.set_title(title) #Time domain
    if nolim==False:
        ax.set_xlim((xmin, xmax))
        ax.set_ylim((ymin, ymax))
    plt.tight_layout()

#####################
cable_length = '20'; G1 = '36'; G2 = '34'; G3='32'

subfile = '0'; comp=''; S_ij=''

if   subfile == '0':    comp = '12'#12
elif subfile == '1':    comp = '21'

if comp == '11' and subfile == '0': S_ij = '11'
elif comp == '12'and subfile == '0': S_ij = '21'
elif comp == '21' and subfile == '1': S_ij = '11'

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

## NAMES AS APPEARED IN MY FOLDER

#[TP_1m_23_ChD1_redo.vna, TP_1m_54_ChD1.vna, TP_1m_55_ChD1.vna, TP_53_1m_ChD1_redo.vna, TP_1m_13_ChD3_ChCMD.vna][G1, G1, G2, G2, G3]
#[TP_2m_72_ChD1.vna, TP_2m_74_ChD1.vna, TP_2m_46_ChD1.vna][G1, G1, G2]
#[TP_1p4m_35_ChD0.vna, TP_1p4m_36_ChD0.vna, TP_1p4m_41_ChD0.vna, TP_1p4m_42_ChD1.vna] [G1, G1, G2, G2]
#[TP_62_35cm_ChD1.vna, TP_63_35cm_ChD1.vna, TP_60_35cm_ChD1.vna, TP_61_35cm_ChD1.vna, TP_35cm_57_ChD1.vna] [G1, G1, G2, G2, G2]
#


all_channels = ['calibration_test.vna', 'TP_1m_54_ChCMD.vna', 'TP_1m_54_ChD0.vna',
                'TP_1m_54_ChD1.vna', 'TP_1m_53_ChCMD_redo.vna', 'TP_1m_53_ChD1_redo.vna',
                'TP_1m_53_ChD0_redo.vna', 'TP_1m_55_ChCMD.vna', 'TP_1m_55_ChD0.vna',
                'TP_1m_55_ChD1.vna', 'TP_2m_46_ChD1_redo_v2.vna', 'TP_2m_46_ChD0_redo_v2.vna',
                'TP_2m_46_ChCMD_redo_v2.vna', 'TP_2m_72_ChD0.vna','TP_2m_72_ChD1.vna',
                'TP_2m_72_ChCMD.vna','TP_2m_74_ChD1.vna', 'TP_2m_74_ChD0.vna',
                'TP_2m_74_ChCMD.vna' ]
all_gauges = [G1, G2, G2,
              G2, G1, G1,
              G2, G2, G2,
              G2, G2, G2,
              G2, G1, G1,
              G1, G1, G1,
              G1]

n = len(all_channels)
COLOR = cm.rainbow(np.linspace(0,1,n))
map_ch = zip(all_channels, all_gauges, COLOR)

fig = plt.figure(figsize=(15, 20))
fig.patch.set_facecolor('xkcd:black')
plt.style.use('dark_background')  #This is what worked for the background style

ax0=plt.subplot(3,1,1)
ax1=plt.subplot(3,1,2)
ax2=plt.subplot(3,1,3)
x_labels=[]

counter = 0
length = ''

for ch, awg, c in map_ch:

    if   '2m' in ch: lo = 5; hi=18 ; length = '2m'
    elif '1m' in ch: lo = 4; hi=12 ; length = '1m'
    else:            lo = 0; hi=30 ; length = ''

    f = 'Plots/Redo_VNA/'+ch

    net = rf.Network(f+'_'+subfile+'.s2p', f_unit='ghz')
    net_dc   = net[i,j].extrapolate_to_dc(kind='linear')

    f_lab = getLabelFromFile(f)
    x_label = (f_lab+'_'+awg+'G').replace('TP_', '')#.replace('ChD0_', '').replace('ChD1_', '').replace('ChCMD_', '')
    x_labels.append(x_label)

    net_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', '+f_lab+'('+awg+')', ax=ax0, color=c)
    #ax0.legend(loc="lower left", ncol=n)
    ax0.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
    Z_mean, Z_mean_std = get_display_mean_impedance(ax0, lo, hi, c)
    set_axes(ax0, 'Time Domain', 0.0, 400.0, 0.0, 30.0, 0)

    ax1.errorbar(counter, Z_mean, Z_mean_std, linestyle='None', marker='o', color=c)
    set_axes(ax1, 'Cable Vs Impedance', 50.0, 200.0, 0, n, 0)
    counter = counter+1

fig.subplots_adjust(bottom=0.05, hspace=0.4)
ax1.set_xlabel('cable channels')
ax1.set_ylabel('Z (ohms)')
#print(x_labels)
ax1.set_xticks(np.arange(0,10,1), x_labels)
ax1.set_xticklabels(x_labels, rotation='45', fontsize=8)
x_va=[154,153, 155,246,272,274]
y_va=[(150,159,157),(140,142,146),(155,158,154),(152,154,154),(144,141,144),(139,139,138)]
ax2.plot(x_va,y_va,'ro')
set_axes(ax2,'Summary',45.0,200.0,152,276,0)
tooltip = mpld3.plugins.PointLabelTooltip(y_va,labels=all_channels)
mpld3.plugins.connect(fig, tooltip)
plt.show()
