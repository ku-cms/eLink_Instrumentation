#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created by the KU CMS team.

# Import libraries
import os
from optparse import OptionParser
import pandas as pd
import skrf as rf
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import style
import pickle as pl
import csv

def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def name(x):
    return x.strip(".vna").replace('Data/'+cable_number_str+'/Plots/s2p/', "").strip("TP_")

def split(word):
    return [char for char in word]

# https://www.tutorialfor.com/questions-285739.htm
def display_mean_impedance(ax, t1, t2, col, y_plot_value):
    lines = ax.get_lines()

    # Delete any other array correponding to a line drawn in ax but the last one.
    # This is a brute force way of resetting the line data to the data current line.
    # Afterward, the length of lines should be 1.
    if len(lines) > 1:
        del lines[:-1]

    # store the line arrays into list. Every line drawn on the ax is considered as data
    X = [line.get_xdata() for line in lines]
    Y = [line.get_ydata() for line in lines]

    # create a table, and since the list X and Y should have size=1, place the first
    # element (array) in pandas table columns t and Z
    df = pd.DataFrame()
    df['t'] = X[0]
    df['Z'] = Y[0]

    # get the mean value of Z for a given time difference
    Z_mean =  df.query('t >=@t1 & t<=@t2').agg({'Z': 'mean'})
    print('Mean impedance from', t1, 'ns to', t2, 'ns =', Z_mean.values, 'for', lines[0])
    # plot the average line
    x_coor = [t1, t2]
    y_coor = [Z_mean, Z_mean]
    y_plot_value.append(int(Z_mean.values))
    ax.plot(x_coor, y_coor, color=col, linewidth=1, label='', linestyle='--')

def set_axes(ax, title, ymin, ymax, xmin, xmax, nolim):
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.grid(True, color='0.8', which='minor')
    ax.grid(True, color='0.4', which='major')
    ax.set_title(title) #Time domain
    if nolim == False:
        ax.set_xlim((xmin, xmax))
        ax.set_ylim((ymin, ymax))
    plt.tight_layout()

# Analyze data for one cable; iterates over all files (e.g. channels) for a cable
def analyze(cable_number, cable_type, cable_length, int_window, Comment):
    parser = OptionParser()
    
    cable_number_str = str(cable_number)
    cable_type_str   = str(cable_type)
    cable_length_str = str(cable_length)
    
    file_list = []
    y_plot_value = []
    
    print()
    print("Loading files...")
    for root, dirs, files in os.walk("./Data/"+cable_number_str, topdown=False):
       for name in files:
          if ".txt" in os.path.join(name):
            file_list.append(os.path.join(name))
    
    n_channels = len(file_list)
    
    print("Found {0} files to analyze.".format(n_channels))
    print("List of files: {0}".format(file_list))
    
    ff_list = []
    filename_list = []
    color_list = ['b', 'r', 'g', 'w', 'm']
    
    for i in range(n_channels):
        ff_list.append(f"Data/"+cable_number_str+f"/{file_list[i]}")
        filename_list.append(f"{file_list[i]}")
    
    makeDir("Data/"+cable_number_str+"/Plots")
    makeDir("Data/"+cable_number_str+"/Plots/s2p")
    
    iterator = 0
    Breaker = True
    
    while Breaker == True:
        FILE = file_list[iterator]
        print("Creating s2p files for {0}".format(FILE))
    
        parser.add_option('--basename', metavar='T', type='string', action='store',
                          default='Data/'+cable_number_str+'/'+FILE, #31, 15, 33 #calibration_test.vna
                          dest='basename',
                          help='input text file')
    
        parser.add_option('--directory', metavar='T', type='string', action='store',
                          default='Data/'+cable_number_str+'/'+'Plots/',
                          dest='directory',
                          help='directory to store plots')
    
        (options,args) = parser.parse_args()
        # ==========end: options =============
        basename1 = options.basename
        basename2 = basename1.replace('Data/'+cable_number_str+'/', 'Data/'+cable_number_str+'/'+'Plots/s2p/')
        dir_in = options.directory
        cable = basename1.replace('Data/'+cable_number_str+'/', "")
    
        infile = pd.read_csv(basename1, names=['pt','f','s11R','s11I','s12R','s12I','s13R','s13I','s14R','s14I'], delim_whitespace=True, skiprows=1)
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
                filename = basename2.replace(".txt","")+ '_' + str(fileindex)+'.s2p'
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
    
        example = rf.Network(basename2.replace(".txt","")+'_0.s2p', f_unit='ghz')
    
        # Create Plots
        with style.context('seaborn-ticks'):
            #Time domain reflectometry, measurement vs simulation
            fig0 = plt.figure(figsize=(8,4))
            fig0.patch.set_facecolor('xkcd:black')
            plt.style.use('dark_background')
            ax0=plt.subplot(1,2,1)
            #major_ticks = np.arange(0, 6.5, 0.5)
            #minor_ticks = np.arange(0, 6.5, 0.1)
            ax0.xaxis.set_minor_locator(AutoMinorLocator(2))
            ax0.yaxis.set_minor_locator(AutoMinorLocator(2))
            ax0.grid(True, color='0.8', which='minor')
            ax0.grid(True, color='0.4', which='major')
            #ax0.legend()
            example_dc = example.extrapolate_to_dc(kind='linear')
            plt.title('Frequency')
            example_dc.s11.plot_s_db(label='S11')
            example_dc.s21.plot_s_db(label='S12')
            plt.ylim((-100.0, 0))
            plt.xlim((100000, 2500000000))
            ax1=plt.subplot(1,2,2)
            ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
            ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
            ax1.grid(True, color='0.8', which='minor')
            ax1.grid(True, color='0.4', which='major')
            plt.title('Time domain reflection step response (DC extrapolation)') #The time_step component of the z-matrix vs frequency
            example_dc.s11.plot_z_time_step(attribute='z_time_step', pad=2000, window='hamming', z0=50, label='TD11')
            example_dc.s21.plot_z_time_step(attribute='z_time_step',pad=2000, window='hamming', z0=50, label='TD12')
            plt.ylim((0.0, 250.0))
            plt.xlim((0, 30))
            plt.tight_layout()
            #ax1.legend()
            fig0.savefig(dir_in+cable.replace(".vna.txt","")+'_freq_time_Z_rf.png')
    
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
            fig1.savefig(dir_in+cable.replace(".vna.txt","")+'_fref_time_rf.png')
    
            fig = plt.figure(figsize=(14,6))
            for i in range(6):
               ax = fig.add_subplot(2,3,i+1)
               if i == 0 :
                 plt.axis([-1.1,2.1,-1.1,1.1])
                 example.plot_s_smith(draw_labels=True,m=0, n=0, label='S11')
                 example.plot_s_smith(draw_labels=True,m=1, n=0, label='S12')
               elif i == 1:
                   example.plot_z_re(m=0,n=0,label='Z11')
                   example.plot_z_re(m=1,n=0,label='Z12')
               elif i == 2:
                   example.plot_z_im(m=0,n=0,label='Z11')
                   example.plot_z_im(m=1,n=0,label='Z12')
               elif i == 3:
                   example.plot_s_db(m=0, n=0, label='S11') # 10
                   example.plot_s_db(m=1, n=0, label='S12')
               elif i == 4:
                   example.plot_s_db_time(m=0, n=0, label='S11') # employs windowing before plotting to enhance impluse resolution.
                   example.plot_s_db_time(m=1, n=0, label='S12')
               elif i == 5:
                   example.plot_z_time_db(m=0, n=0, label='Z11')    #plot_z_re_time
                   example.plot_z_time_db(m=1, n=0, label='Z12')
    
            parser.remove_option('--basename')
            parser.remove_option('--directory')
    
            fig.savefig(dir_in+cable.replace(".vna.txt","")+'_rf.png')
    
            iterator +=1
    
            if iterator >= n_channels:
                break
    
    # specify time integration window as a function of length
    if int_window == 0:
        t1 = 2.00
        t2 = 5.00
    elif int_window == 1:
        t1 = 8.00
        t2 = 11.00
    elif int_window == 2:
        if cable_length == 0:
            t1 = 0.00
            t2 = 1.50
        elif cable_length == 35:
            t1 = 2.00
            t2 = 4.00
        elif cable_length == 80:
            t1 = 2.00
            t2 = 6.00
        elif cable_length == 100:
            t1 = 2.00
            t2 = 7.00
        elif cable_length == 140:
            t1 = 2.00
            t2 = 9.00
        elif cable_length == 160:
            t1 = 2.00
            t2 = 10.00
        elif cable_length == 180:
            t1 = 2.00
            t2 = 11.00
        elif cable_length == 200:
            t1 = 2.00
            t2 = 12.00
        else:
            print("ERROR: the cable length '{0}' is not valid; it must be one of these: [0, 35, 80, 100, 140, 160, 180, 200] cm.".format(cable_length))
            t1 = 0.00
            t2 = 0.00
    else:
        print("ERROR: the integration window '{0}' is not valid; it must be one of these: [0,1,2].".format(int_window))
        t1 = 0.00
        t2 = 0.00
    
    comps = ['11','12', '21']
    subfiles = ['0','0','1',]
    
    iterator = 0
    Breaker = True
    
    # Create plots
    while Breaker == True:
        comp = comps[iterator]
        subfile = subfiles[iterator]
        S_name = "S" + comp
    
        if   comp == '11' and subfile == '0': S_ij = '11'
        elif comp == '12' and subfile == '0': S_ij = '21'
        elif comp == '21' and subfile == '1': S_ij = '11'
    
        i = int(split(S_ij)[0])
        j = int(split(S_ij)[1])
        
        print()
        print("Parameter being analyzed: {0}".format(S_name))
    
        net_list = []
        for channel in range(n_channels):
            net_list.append(rf.Network("Data/"+cable_number_str+"/Plots/s2p/"+filename_list[channel].replace(".txt","")+'_'+subfile+'.s2p', f_unit='ghz'))
    
        #netref = rf.network.Network(out_dir+'/'+sub_out_dir+'/straight_SMA.vna_'+subfile+'.s2p', f_unit='ghz')
    
        with style.context('seaborn-darkgrid'):
    
            fig0 = plt.figure(figsize=(10,4))
            fig0.patch.set_facecolor('xkcd:black')
            plt.style.use('dark_background')
            ax0 = plt.subplot(1,2,1)
            ax1 = plt.subplot(1,2,2)
    
            ax0.xaxis.set_minor_locator(AutoMinorLocator(2))
            ax0.yaxis.set_minor_locator(AutoMinorLocator(2))
            ax0.grid(True, color='0.8', which='minor')
            ax0.grid(True, color='0.4', which='major')
    
            net_dc = []
            for channel in range(n_channels):
                this_net = net_list[channel]
                net_dc.append(this_net[i,j].extrapolate_to_dc(kind='linear'))
                net_dc[channel].plot_s_db(label='S'+comp+ff_list[channel].split('.vna')[0].split('/')[-1:][0], ax=ax0, color=color_list[channel])
                net_dc[channel].plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+ff_list[channel].split('.vna')[0].split('/')[-1:][0], ax=ax1, color=color_list[channel])
                display_mean_impedance(ax1, t1, t2, color_list[channel], y_plot_value)
    
            with open("Impedence_List.csv", "a") as Ana:
                Ana.write("Cable_number,Length,Type, Time Interval, S11, S12, S21, Comments")
                Ana.write(cable_number_str+","+cable_length_str+","+cable_type_str+","+str(t1)+ "-"+str(t2)+","+str(Comment)+",")
                for i in y_plot_value:
                    Ana.write(str(i)+",")
                Ana.write("\n")
                Ana.close()
    
            with open("Data/"+cable_number_str+"/Impedence_List.csv", "a") as Ana2:
                Ana2.write("Cable_number,Length,Type, Time Interval, S11, S12, , Comments")
                Ana2.write(cable_number_str+","+cable_length_str+","+cable_type_str+","+str(t1)+ "-"+str(t2)+","+str(Comment)+",")
                for i in y_plot_value:
                    Ana2.write(str(i)+",")
                Ana2.write("\n")
                Ana2.close()
    
            y_plot_value.clear()
    
            set_axes(ax1, 'Time Domain', 0.0, 200.0, 0.0, 30.0, 0)
            set_axes(ax0, 'Time Domain', -75.0, 75.0, 0.0, 6.0, 0)
    
            fig0.savefig("Data/"+cable_number_str+"/Plots/"+cable_number_str+'cm_freq_time_Z_rf_'+"S"+comp+'.png')
    
            iterator += 1
    
            if iterator > 2:
                break
    
    print()
    print("Analysis complete for cable {0}. To view plots, see the 'Plots' directory for cable {0}.".format(cable_number_str))

# run analysis
def run():
    # Input parameters from user
    cable_number = int(input("Enter cable number: "))
    cable_type   = int(input("Enter cable type [0, 1, 2, 3, 4]: "))
    cable_length = int(input("Enter cable length in cm [0, 35, 80, 100, 140, 160, 180, 200]: "))
    int_window   = int(input("Enter integration window [2-5ns (0), 8-11ns (1), variable (2)]: "))
    Comment      = input("Enter comments for this run; if there are no comments, leave blank: ")
    
    # Analyze data for cable
    analyze(cable_number, cable_type, cable_length, int_window, Comment)

def main():
    run()

if __name__ == "__main__":
    main()

