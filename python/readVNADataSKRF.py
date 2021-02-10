#!/usr/bin/env python3
from itertools import islice
import sys, re
import numpy as np
import skrf as rf
#rf.stylely()

import pylab
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import style
import pickle as pl

def name(input):
    match = re.match(r'TP_\w+_\d+', input)
    name = match.group()
    if '1p4' in name: name = name.replace('1p4', '1.4')
    return name

from optparse import OptionParser
parser = OptionParser()

# (35: 17, 18, 19, 26, 27, 28, 29, 56, 57, 58) 'TP_35cm_XX_ChD1.vna
# (35 redo: 56, 60) 
# (1 : 20, 21, 23, 32, 33) TP_1m_XX_ChD1.vna # 20,21 went wrong
# (1 redo: 53, 53_D0, 55)
# (1p4: 35, 36, 37, 38, 39, 40) TP_1p4m_XX_ChD1.vna. #38, 40 went wrong
# (1p4: 35, 36, 41, 42
# (2 : 46, 47) TP_2m_47_ChD1
# (2: 46)




parser.add_option('--basename', metavar='T', type='string', action='store',
                  default='Redo_VNA/straight_SMA.vna', #31, 15, 33 #calibration_test.vna 
                  dest='basename',
                  help='input text file')

parser.add_option('--directory', metavar='T', type='string', action='store',
                  default='Plots',
                  dest='directory',
                  help='directory to store plots')

(options,args) = parser.parse_args()
# ==========end: options =============
basename = options.basename
dir_in= options.directory
if '_\d+' in basename:
    cable = name(basename)
else: cable = basename    
#date  = ''

#basename = 'TP_1m_23_ChD1.vna' #TP_1m_33_ChD1.vna calibration_test
#cable = name(basename)

infile = pd.read_csv(basename+'.txt', names=['pt','f','s11R','s11I','s12R','s12I','s13R','s13I','s14R','s14I'], delim_whitespace=True, skiprows=1)
infile.dropna(how='all')

pd.set_option("display.max_rows", 5)

fileindex = 0
prevF = 0
for i, row in infile.iterrows():
    if row['pt'] == 'PARAMETER:':
        # new set of points
        try:
            if not f.closed:
                f.close()
        except:
            pass
        filename = dir_in+'/'+basename+ '_' + str(fileindex)+'.s2p'
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
    
example = rf.Network(dir_in+'/'+basename+'_0.s2p', f_unit='ghz')

# .s2p format consist of following columns
# Stim  Real (S11)  Imag(S11)  Real(S21)  Imag(S21)  Real(S12)  Imag(S12)  Real(S22)  Imag(S22)

# however our columns and rows in 4x4 matrix are swaped
#print (example.s)

# the map to read the correct values is going to be the one on right side

# S11 S13          00  01            S11 S12
#            ---->           ----> 
# S12 S14          10  11            S21 S22

# do the following to read the right elements rather than the default in touchstone files.
# S11 : s[:,0,0]
# S12 : s[:,1,0]
# S13 : s[:,0,1]
# S14 : s[:,1,1]

#https://teledynelecroy.com/doc/an-introduction-to-sparameters
with style.context('seaborn-ticks'):
    #Time domain reflectometry, measurement vs simulation
    fig0 = plt.figure(figsize=(10,4))
    ax0=plt.subplot(1,2,1)
    #major_ticks = np.arange(0, 6.5, 0.5)
    #minor_ticks = np.arange(0, 6.5, 0.1)
    ax0.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax0.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax0.grid(True, color='0.8', which='minor')
    ax0.grid(True, color='0.4', which='major')
    example_dc = example.extrapolate_to_dc(kind='linear')
    plt.title('Frequency Domain')
    example_dc.s11.plot_s_db(label='S11')
    example_dc.s21.plot_s_db(label='S12')
    plt.ylim((-50.0, 50.0))
    plt.xlim((100000, 6000000000))
    ax1=plt.subplot(1,2,2)
    ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.grid(True, color='0.8', which='minor')
    ax1.grid(True, color='0.4', which='major')
    plt.title('Time domain') #The time_step component of the z-matrix vs frequency
    example_dc.s11.plot_z_time_step(attribute='z_time_step', pad=2000, window='hamming', z0=50, label='TD11')
    example_dc.s21.plot_z_time_step(pad=2000, window='hamming', z0=50, label='TD12')
    plt.ylim((0.0, 200.0))
    plt.xlim((0, 35))
    plt.tight_layout()
    fig0.savefig(dir_in+'/'+cable+'_freq_time_Z_rf.png')
    
    # Gating the Reflection of Interest
    s11_gated = example.s11.time_gate()#(center=0, span=.2)#autogate on the fly
    s11_gated.name='gated '
    fig1 = plt.figure(figsize=(8,4))
    plt.subplot(121)
    example.s11.plot_s_db()
    s11_gated.plot_s_db() #s11.time_gate()
    plt.title('Frequency Domain')
    plt.subplot(122)
    example.s11.plot_s_db_time()
    s11_gated.plot_s_db_time()
    plt.title('Time Domain')
    plt.xlim((-5, 5))
    
    plt.tight_layout()
    #plt.show()
    fig1.savefig(dir_in+'/'+cable+'_fref_time_rf.png')
    
    fig = plt.figure(figsize=(14,6))
    #ax0 = fig.add_subplot(1, 2, 2)
    #example.plot_s_smith(draw_labels=True,m=1, n=0)
    #example.plot_s_smith(draw_labels=True)
    #plt.xlabel('Real Part');
    #plt.ylabel('Imaginary Part');
    #plt.title('Smith Chart');
    #plt.axis([-1.1,2.1,-1.1,1.1])
    #plt.legend(loc=5)
    for i in range(6):
       ax = fig.add_subplot(2,3,i+1)
       if i==0 :
         plt.axis([-1.1,2.1,-1.1,1.1])
         example.plot_s_smith(draw_labels=True,m=0, n=0, label='S11')
         example.plot_s_smith(draw_labels=True,m=1, n=0, label='S12')
       elif i==1:
           example.plot_z_re(m=0,n=0,label='Z11')
           example.plot_z_re(m=1,n=0,label='Z12')
       elif i==2:
           example.plot_z_im(m=0,n=0,label='Z11')
           example.plot_z_im(m=1,n=0,label='Z12')
       elif i==3:
           example.plot_s_db(m=0, n=0, label='S11') # 10
           example.plot_s_db(m=1, n=0, label='S12')
       elif i==4:
           example.plot_s_db_time(m=0, n=0, label='S11') # employs windowing before plotting to enhance impluse resolution.
           example.plot_s_db_time(m=1, n=0, label='S12')
       elif i==5:
           example.plot_z_time_db(m=0, n=0, label='Z11')    #plot_z_re_time
           example.plot_z_time_db(m=1, n=0, label='Z12')
#plt.figure(1)
#pylab.title('S_{12}')
#    example.plot_s_db(m=1, n=0)
    #pylab.show()
    #tight_layout()
    fig.savefig(dir_in+'/'+cable+'_rf.png')
    pl.dump(fig, open(dir_in+'/'+cable+'.pickle', 'wb'))
#plt.draw()

#print ('ch impedance:', example.z0)


#input("hold")    
