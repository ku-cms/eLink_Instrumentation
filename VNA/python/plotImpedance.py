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

from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import style
import pickle as pl

def split(word):
    return [char for char in word]


def display_mean_impedance(ax, t1, t2, col):##https://www.tutorialfor.com/questions-285739.htm
    
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
    df['t'] = X[0]
    df['Z'] = Y[0]

    # get the mean value of Z for a given time difference
    Z_mean =  df.query('t >=@t1 & t<=@t2').agg({'Z': 'mean'})
    print('Mean impedance from ', t1, 'ns  and ', t2, 'ns =', Z_mean.values, 'for', lines[0])

    # plot the average line
    x_coor = [t1, t2]
    y_coor = [Z_mean, Z_mean]    
    ax.plot(x_coor, y_coor, color=col, linewidth=1, label='', linestyle='--')
        
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
cable_length = '100'

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


if cable_length == '20':
    net1 = rf.Network(out_dir+'/'+sub_out_dir+'/TP_20cm_12_ChD3_ChCMD.vna_'+subfile+'.s2p', f_unit='ghz')#33
    net2 = rf.Network('Plots/TP_20cm_31_ChD1.vna_'+subfile+'.s2p', f_unit='ghz') #23
    net3 = rf.Network('Plots/TP_20cm_49_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
elif cable_length == '35':
    net4 = rf.Network('Plots/Redo_VNA/TP_35cm_57_ChD0.vna_'+subfile+'.s2p', f_unit='ghz')
    net5 = rf.Network('Plots/Redo_VNA/TP_35cm_57_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
    net6 = rf.Network('Plots/Redo_VNA/TP_35cm_57_ChCMD.vna_'+subfile+'.s2p', f_unit='ghz')
    #net8 = rf.Network('Plots/TP_35cm_56_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')   
    #net10 = rf.Network('Plots/Redo_VNA/TP_35cm_60_ChD1_Redo.vna_'+subfile+'.s2p', f_unit='ghz')
elif cable_length == '100':
    #net1 = rf.Network('Plots/Redo_VNA/TP_1m_53_ChD0_rwy.vna_'+subfile+'.s2p', f_unit='ghz')
    net1 = rf.Network('Plots/Redo_VNA/TP_1m_13_ChD3_ChCMD.vna_'+subfile+'.s2p', f_unit='ghz')
    net2 = rf.Network('Plots/Redo_VNA/TP_1m_55_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')    
    #net3 = rf.Network('Plots/Redo_VNA/TP_1m_55_ChCMD.vna_'+subfile+'.s2p', f_unit='ghz')
    net3 = rf.Network('Plots/Redo_VNA/082620_TP_53_1m_ChD0_SK.vna_'+subfile+'.s2p', f_unit='ghz') #55 34G_CHD1
    #net3 = rf.Network('Plots/TP_1m_32_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')        
elif cable_length == '140':    
    net1 = rf.network.Network('Plots/Redo_VNA/TP_1p4m_41_ChD0_redo_v2.vna_'+subfile+'.s2p', f_unit='ghz')
    net2 = rf.network.Network('Plots/Redo_VNA/TP_1p4m_41_ChD1_redo_v2.vna_'+subfile+'.s2p', f_unit='ghz')
    net3 = rf.network.Network('Plots/Redo_VNA/TP_1p4m_41_ChCMD_redo_v2.vna_'+subfile+'.s2p', f_unit='ghz')
elif cable_length == '200':
    print('Plots/Redo_VNA/TP_2m_72_ChD0.vna_'+subfile+'.s2p')
    net1 = rf.network.Network('Plots/Redo_VNA/TP_2m_72_ChD0.vna_'+subfile+'.s2p', f_unit='ghz')
    net2 = rf.network.Network('Plots/Redo_VNA/TP_2m_72_ChD1.vna_'+subfile+'.s2p', f_unit='ghz')
    net3 = rf.network.Network('Plots/Redo_VNA/TP_2m_72_ChCMD.vna_'+subfile+'.s2p', f_unit='ghz')
else:
    filename = out_dir+'/'+sub_out_dir+'/FPC_0p6m.vna_'+subfile+'.s2p'
    net1 = rf.network.Network(filename, f_unit='ghz')#straight_SMA.vna, FPC_0p6

netref = rf.network.Network(out_dir+'/'+sub_out_dir+'/straight_SMA.vna_'+subfile+'.s2p', f_unit='ghz')


with style.context('seaborn-ticks'):
   
    fig0 = plt.figure(figsize=(10,4))
    ax0=plt.subplot(1,2,1)
    ax1=plt.subplot(1,2,2)

    ax0.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax0.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax0.grid(True, color='0.8', which='minor')
    ax0.grid(True, color='0.4', which='major')
    
    if cable_length == '20':

        ## ---Frequency Domain Plots---:        
        net1_dc = net1[i,j].extrapolate_to_dc(kind='linear')
        net2_dc = net2[i,j].extrapolate_to_dc(kind='linear')
        net3_dc = net3[i,j].extrapolate_to_dc(kind='linear')
        netref_dc = netref[i,j].extrapolate_to_dc(kind='linear')
        
        net1_dc.plot_s_db(label='S'+comp+', TP_20cm_12 (32)', ax=ax0, color='b')
        net2_dc.plot_s_db(label='S'+comp+', TP_20cm_31 (36)', ax=ax0, color='r')
        net3_dc.plot_s_db(label='S'+comp+', TP_20cm_49 (34)', ax=ax0, color='c')
        netref_dc.plot_s_db(label='S'+comp+', Calibration', ax=ax0, color='g')    
        set_axes(ax0, 'Frequency Domain', 100000, 6000000000, -50.0, 50.0, 1)

        ## ---Time Domain Plots---:       
        net1_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_20cm_12 (32)', ax=ax1, color='b')
        display_mean_impedance(ax1, 1.0, 4.0, 'b')
        
        net2_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_20cm_31 (36)', ax=ax1, color='r')
        display_mean_impedance(ax1, 1.0, 4.0, 'r')

        net3_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_20cm_49 (34)', ax=ax1, color='c')
        display_mean_impedance(ax1, 1.0, 4.0, 'c')
        
        netref_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', Calibration', ax=ax1, color='g')
        display_mean_impedance(ax1, 0.0, 30.0, 'g')
        
        set_axes(ax1, 'Time Domain', 0.0, 400.0, 0.0, 30.0, 0)
         
        plt.show()
                      
    elif cable_length == '35':
        net4_dc = net4[i,j].extrapolate_to_dc(kind='linear')
        net5_dc = net5[i,j].extrapolate_to_dc(kind='linear')
        net6_dc = net6[i,j].extrapolate_to_dc(kind='linear')
        #net8_dc = net8[i,j].extrapolate_to_dc(kind='linear')
        #net10_dc = net10[i,j].extrapolate_to_dc(kind='linear')
        netref_dc = netref[i,j].extrapolate_to_dc(kind='linear')
        
        net4_dc.plot_s_db(label='S'+comp+', TP_35cm_57_D0 (34)', ax=ax0)
        net5_dc.plot_s_db(label='S'+comp+', TP_35cm_57_D1 (34)', ax=ax0)
        net6_dc.plot_s_db(label='S'+comp+', TP_35cm_57_CMD (34)', ax=ax0)
        #net8_dc.plot_s_db(label='S'+comp+', TP_35cm_56 (34)', ax=ax0)
        #net10_dc.plot_s_db(label='S'+comp+', TP_35cm_60_redo (34)', ax=ax0)
        netref_dc.plot_s_db(label='S'+comp+', Calibration', ax=ax0)    
        set_axes(ax0, 'Frequency Domain', 100000, 6000000000, -50.0, 50.0, 1)

        net4_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_57_D0 (34)', ax=ax1)
        net5_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_57_D1 (34)', ax=ax1)
        net6_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_57_CMD (34)', ax=ax1)
        #net8_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_56 (34)', ax=ax1)
        #net10_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_35cm_60_redo (34)', ax=ax1)
        netref_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', Calibration', ax=ax1)
        set_axes(ax1, 'Time Domain', 0.0, 200.0, 0.0, 30.0, 0)
        

    
    elif cable_length == '100':
        net1_dc   = net1[i,j].extrapolate_to_dc(kind='linear')
        net2_dc   = net2[i,j].extrapolate_to_dc(kind='linear')
        net3_dc   = net3[i,j].extrapolate_to_dc(kind='linear')
        netref_dc = netref[i,j].extrapolate_to_dc(kind='linear')        
        net1_dc.plot_s_db(label='S'+comp+', TP_1m_13 (32)', ax=ax0, color='b')
        net2_dc.plot_s_db(label='S'+comp+', TP_1m_55_D1 (34)', ax=ax0, color='r')
        net3_dc.plot_s_db(label='S'+comp+', TP_1m_53_D0 (36)', ax=ax0, color='k')       
        netref_dc.plot_s_db(label='S'+comp+', Calibration', ax=ax0)    
        set_axes(ax0, 'Frequency Domain', 100000, 6000000000, -50.0, 50.0, 1)
        
        net1_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1m_13 (32)', ax=ax1, color='b')
        display_mean_impedance(ax1, 4.0, 8.0, 'b')

        net2_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1m_55_D1 (34)', ax=ax1, color ='r')
        display_mean_impedance(ax1, 4.0, 8.0, 'r')

        net3_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1m_53_D0 (36)', ax=ax1, color='k')
        display_mean_impedance(ax1, 4.0, 8.0, 'k')
        
        netref_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', Calibration', ax=ax1, color='g')
        display_mean_impedance(ax1, 4.0, 8.0, 'g')
        
        set_axes(ax1, 'Time Domain', 0.0, 200.0, 0.0, 30.0, 0)               

    elif cable_length == '140':
        net1_dc = net1[i,j].extrapolate_to_dc(kind='linear')
        net2_dc = net2[i,j].extrapolate_to_dc(kind='linear')
        net3_dc = net3[i,j].extrapolate_to_dc(kind='linear')
        netref_dc = netref[i,j].extrapolate_to_dc(kind='linear')
        
        net1_dc.plot_s_db(label='S'+comp+', TP_1p4m_41_D0 (34)', ax=ax0)#s11
        net2_dc.plot_s_db(label='S'+comp+', TP_1p4m_41_D1 (34)', ax=ax0)
        net3_dc.plot_s_db(label='S'+comp+', TP_1p4m_41_CMD (34)', ax=ax0)   
        netref_dc.plot_s_db(label='S'+comp+', Calibration', ax=ax0)  #s11  
        set_axes(ax0, 'Frequency Domain', 100000, 6000000000, -200.0, 100.0, 1)
        
        net1_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1p4m_34_D0 (34)', ax=ax1)
        net2_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1p4m_34_D1 (34)', ax=ax1)
        net3_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_1p4m_34_CMD (34)', ax=ax1)      
        netref_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', Calibration', ax=ax1)
        set_axes(ax1, 'Time Domain', 0.0, 300.0, 0.0, 35.0, 0)        
        
    elif cable_length == '200':
        net1_dc = net1[i,j].extrapolate_to_dc(kind='linear')
        net2_dc = net2[i,j].extrapolate_to_dc(kind='linear')
        net3_dc = net3[i,j].extrapolate_to_dc(kind='linear')
        netref_dc = netref[i,j].extrapolate_to_dc(kind='linear')
        
        net1_dc.plot_s_db(label='S'+comp+', TP_2m_72_D0 (36)', ax=ax0)
        net2_dc.plot_s_db(label='S'+comp+', TP_2m_72_D1 (36)', ax=ax0)
        net3_dc.plot_s_db(label='S'+comp+', TP_2m_72_CMD (36)', ax=ax0)
        netref_dc.plot_s_db(label='S'+comp+', Calibration', ax=ax0)    
        set_axes(ax0, 'Frequency Domain', 100000, 6000000000, -50.0, 50.0, 1)

        net1_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_2m_72_D0 (36)', ax=ax1)
        net2_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_2m_72_D1 (36)', ax=ax1)
        net3_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', TP_2m_72_CMD (36)', ax=ax1)
        netref_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', Calibration', ax=ax1)
        set_axes(ax1, 'Time Domain', 0.0, 200.0, 0.0, 35.0, 0)
       
    else:
        # Freq Domain
        net1_dc = net1[i,j].extrapolate_to_dc(kind='linear')
        net1_dc.plot_s_db(label='S'+comp+', FPC_0p6', ax=ax0, color='b')
        #netref_dc = netref[1,1].extrapolate_to_dc(kind='linear')
        #netref_dc.plot_s_db(label='S'+comp+', Calibration', ax=ax0)    
        set_axes(ax0, 'Frequency Domain', 100000, 6000000000, -50.0, 50.0, 1)

        # Time Domain
        net1_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', FPC_0p6', ax=ax1, color='b')
        display_mean_impedance(ax1, 0.0, 4.0, 'b')
        #netref_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+', Calibration', ax=ax1)
        #display_mean_impedance(ax1, 0.0, 4.0, 'b')
        set_axes(ax1, 'Time Domain', 0.0, 200.0, 0.0, 30.0, 0)
        
    #fig0.savefig('Plots/36vs34_'+cable_length+'cm_freq_time_Z_rf_'+comp+redo+'.png')
    #fig0.savefig('Plots/36G_'+cable_length+'cm_freq_time_Z_rf_'+comp+redo+'.png')
    #fig0.savefig('Plots/SMA_'+cable_length+'freq_time_Z_rf_'+comp+redo+'zoomout.png')
    #fig0.savefig('Plots/small_SMA_'+cable_length+'freq_time_Z_rf_'+comp+redo+'zoomout.png')
    #fig0.savefig('Plots/FPC_0p6_'+cable_length+'freq_time_Z_rf_'+comp+redo+'.png')
    fig0.savefig('Plots/TP_'+cable_length+'cm_freq_time_Z_rf_'+comp+'.png')
    
    pylab.show()
