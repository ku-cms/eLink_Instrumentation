#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------- #
# Created by the KU CMS team.
# - Analyzes VNA data
# - Creates plots
# - Calculates impedance
# - Prints impedance and saves to table (csv)
# - Uses the scikit-rf library (skrf)
# - See https://scikit-rf.readthedocs.io/en/latest/index.html
# ------------------------------------- #

# Import libraries
import os
from optparse import OptionParser
import math
import pandas as pd
import skrf as rf
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import style
import csv

# TODO:
# - Test a smaller, lower integration window near 1.0 ns (e.g. 0.5 to 1.5 ns); this should give smaller Z values.
# - Integration window: time = 1 / frequency, with frequency = 1.28 GHz

# DONE
# - Improve impedance print statements
# - Improve plot colors
# - Fix frequency summary plot (with all channels)
# - Fix grid: major/minor emphasis
# - Fix output csv files
# - Make function and dictionary to get integration window.
# - For output csv, make separate columns for cable number and channel number. Add column for comments.

# Make directory if directory does not exist
def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def name(x):
    return x.strip(".vna").replace('Data/'+cable_number_str+'/Plots/s2p/', "").strip("TP_")

def split(word):
    return [char for char in word]

# write csv file: takes data matrix as input and outputs a csv file
def writeCSV(output_file, data):
    with open(output_file, mode="w", newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            writer.writerow(row)

# Get channel name from 2D line object
def getChannelFromLine(line):
    result = str(line)
    result = result.replace("Line2D", "")
    result = result.replace("(", "")
    result = result.replace(")", "")
    return result

# Get channel name from file name
def getChannelFromFile(file_name):
    f = file_name.split("/")[-1]
    result = f.replace(".vna.txt", "")
    return result

# Get short channel name from long channel name
def getShortChannelName(long_channel_name):
    result = long_channel_name.split("_")[-1]
    return result

# Get integration window (ns) based on window selection and cable length (cm)
def getWindow(window_selection, cable_length):
    # Default starting values
    t1 = 0.00
    t2 = 0.00

    # Integration windows (ns) based on cable length (cm)
    windows_for_lengths = {
        0   : [0.0, 1.5],
        35  : [2.0, 4.0],
        80  : [2.0, 6.0],
        100 : [2.0, 7.0],
        140 : [2.0, 9.0],
        160 : [2.0, 10.0],
        180 : [2.0, 11.0],
        200 : [2.0, 12.0],
    }

    if window_selection == 0:
        t1 = 2.00
        t2 = 5.00
    elif window_selection == 1:
        t1 = 8.00
        t2 = 11.00
    elif window_selection == 2:
        if cable_length in windows_for_lengths:
            t1, t2 = windows_for_lengths[cable_length]
        else:
            print("ERROR: the cable length '{0}' is not valid; it must be one of these: [0, 35, 80, 100, 140, 160, 180, 200] cm.".format(cable_length))
    else:
        print("ERROR: the integration window '{0}' is not valid; it must be one of these: [0,1,2].".format(window_selection))

    return t1, t2

# Calculate, print, and plot mean impedance
# See https://www.tutorialfor.com/questions-285739.htm
def calc_and_plot_mean_impedance(long_channel_name, ax, t1, t2, color):
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

    # get the mean value of Z for a given time range
    Z_mean_query = df.query('t >=@t1 & t<=@t2').agg({'Z': 'mean'})
    Z_mean = Z_mean_query.values[0]
    Z_mean_int = round(Z_mean)

    # print mean Z value
    print("{0}: Z = {1:.2f} ohms = {2} ohms".format(long_channel_name, Z_mean, Z_mean_int))

    # plot the average line
    x_coor = [t1, t2]
    y_coor = [Z_mean, Z_mean]
    ax.plot(x_coor, y_coor, color=color, linewidth=1, label='', linestyle='--')

    # return mean impedance
    return Z_mean

# Setup axes
def setup_axes(ax, title, xlim, ylim):
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.grid(True, color='1.0', which='major')
    ax.grid(True, color='0.5', which='minor')
    ax.set_title(title)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

# Analyze data for one cable; iterates over all files (e.g. channels) for a cable
def analyze(cable_number, cable_type, cable_length, window_selection, Comments):
    parser = OptionParser()

    cable_number_str = str(cable_number)
    cable_type_str   = str(cable_type)
    cable_length_str = str(cable_length)

    file_list = []
    ff_list = []
    filename_list = []

    # list of colors for plots
    color_list = [
        "xkcd:shamrock green",
        "xkcd:cyan",
        "xkcd:bright blue",
        "xkcd:bright violet",
        "xkcd:bright magenta",
        "xkcd:cerise",
        "xkcd:aqua",
        "xkcd:green apple",
        "xkcd:cerulean blue",
        "xkcd:bright lavender",
    ]

    # titles
    signal_vs_freq_title = "Signal magnitude vs. frequency"
    impedance_vs_time_title = "Impedance vs. time"

    # x and y axis limits for plots (v1)
    signal_vs_freq_xlim     = [0.0, 2.5e9]
    signal_vs_freq_ylim     = [-200.0, 0.0]
    impedance_vs_time_xlim  = [0.0, 10.0]
    impedance_vs_time_ylim  = [0.0, 300.0]

    # x and y axis limits for plots (v2)
    #signal_vs_freq_xlim     = [0.0, 2.5e9]
    #signal_vs_freq_ylim     = [-100.0, 0.0]
    #impedance_vs_time_xlim  = [0.0, 10.0]
    #impedance_vs_time_ylim  = [0.0, 200.0]

    print()
    print("Loading files...")
    for root, dirs, files in os.walk("./Data/"+cable_number_str, topdown=False):
       for name in files:
          if ".txt" in os.path.join(name):
            file_list.append(os.path.join(name))

    n_channels = len(file_list)

    # Print files that are found.
    print("Found {0} files to analyze.".format(n_channels))
    print("List of files: {0}".format(file_list))

    # If no files are found, print helpful error message and return.
    if n_channels == 0:
        print("ERROR: No files found for the cable '{0}'.".format(cable_number))
        print(" - Create directory for this cable in the 'Data' directory.")
        print(" - Copy the VNA data files for this cable to the directory that you created.")
        return

    for i in range(n_channels):
        ff_list.append(f"Data/"+cable_number_str+f"/{file_list[i]}")
        filename_list.append(f"{file_list[i]}")

    makeDir("Data/"+cable_number_str+"/Plots")
    makeDir("Data/"+cable_number_str+"/Plots/s2p")

    iterator = 0
    Breaker = True

    while Breaker == True:
        # ---------------------------------------------- #
        # --- Use .vna.txt files to create s2p files --- #
        # ---------------------------------------------- #
        
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

                #print("file index = {0}, row index = {1}".format(fileindex, i))

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
                # Require that "f" is not "nan" and is increasing
                if not math.isnan(float(row['f'])) and float(row['f']) > prevF:
                    f.write(f"{float(row['f']):.3f}\t{float(row['s11R'])}\t{float(row['s11I'])}\t{float(row['s12R'])}\t{float(row['s12I'])}\t{float(row['s13R'])}\t{float(row['s13I'])}\t{float(row['s14R'])}\t{float(row['s14I'])}\n")
                    prevF = float(row['f'])
                else:
                    #print("Found exception: s11R = {0}, prev f = {1}, f = {2}".format(float(row['s11R']), prevF, float(row['f'])))
                    pass
            except:
                pass

        # -------------------------------------------- #
        # --- Analyze/plot VNA data from s2p files --- #
        # -------------------------------------------- #

        # Get Network
        # - Class: skrf.network
        # - See https://scikit-rf.readthedocs.io/en/latest/api/network.html
        example = rf.Network(basename2.replace(".txt","")+'_0.s2p', f_unit='ghz')

        # --- Create plots for each channel --- #
        with style.context('seaborn-ticks'):
            # setup plot
            fig0 = plt.figure(figsize=(8,4))
            fig0.patch.set_facecolor('xkcd:black')
            plt.style.use('dark_background')
            # get axes
            ax0 = plt.subplot(1,2,1)
            ax1 = plt.subplot(1,2,2)

            # Signal magnitude vs frequency subplot
            # - Method: skrf.network.Network.plot_s_db
            # - See https://scikit-rf.readthedocs.io/en/latest/api/generated/skrf.network.Network.plot_s_db.html
            example_dc = example.extrapolate_to_dc(kind='linear')
            example_dc.s11.plot_s_db(ax=ax0, label='S11', color=color_list[0])
            example_dc.s21.plot_s_db(ax=ax0, label='S12', color=color_list[1])

            # Impedance vs time subplot
            # - Method: skrf.network.Network.plot_z_time_step
            # - See https://scikit-rf.readthedocs.io/en/latest/api/generated/skrf.network.Network.plot_z_time_step.html
            example_dc.s11.plot_z_time_step(ax=ax1, attribute='z_time_step', pad=2000, window='hamming', z0=50, label='TD11', color=color_list[0])
            example_dc.s21.plot_z_time_step(ax=ax1, attribute='z_time_step', pad=2000, window='hamming', z0=50, label='TD12', color=color_list[1])

            # setup axes
            setup_axes(ax0, signal_vs_freq_title, signal_vs_freq_xlim, signal_vs_freq_ylim)
            setup_axes(ax1, impedance_vs_time_title, impedance_vs_time_xlim, impedance_vs_time_ylim)
            plt.tight_layout()

            fig0.savefig(dir_in+cable.replace(".vna.txt","")+'_freq_time_Z_rf.png')

            # Gating the Reflection of Interest
            s11_gated = example.s11.time_gate() # (center=0, span=.2) # autogate on the fly
            s11_gated.name='gated'
            fig1 = plt.figure(figsize=(8,4))
            # Frequency Domain Plot
            plt.subplot(121)
            example.s11.plot_s_db(color=color_list[0])
            s11_gated.plot_s_db(color=color_list[1])        # s11.time_gate()
            plt.title('Frequency Domain')
            # Time Domain Plot
            plt.subplot(122)
            example.s11.plot_s_db_time(color=color_list[0])
            s11_gated.plot_s_db_time(color=color_list[1])   # s11.time_gate()
            plt.title('Time Domain')
            plt.xlim((-5, 5))
            plt.tight_layout()
            fig1.savefig(dir_in+cable.replace(".vna.txt","")+'_fref_time_rf.png')

            # Create 6 plots in a grid
            fig = plt.figure(figsize=(14,6))
            for i in range(6):
               ax = fig.add_subplot(2,3,i+1)
               if i == 0 :
                 plt.axis([-1.1,2.1,-1.1,1.1])
                 example.plot_s_smith(draw_labels=True,m=0, n=0, label='S11', color=color_list[0])
                 example.plot_s_smith(draw_labels=True,m=1, n=0, label='S12', color=color_list[1])
               elif i == 1:
                   example.plot_z_re(m=0,n=0,label='Z11', color=color_list[0])
                   example.plot_z_re(m=1,n=0,label='Z12', color=color_list[1])
               elif i == 2:
                   example.plot_z_im(m=0,n=0,label='Z11', color=color_list[0])
                   example.plot_z_im(m=1,n=0,label='Z12', color=color_list[1])
               elif i == 3:
                   example.plot_s_db(m=0, n=0, label='S11', color=color_list[0]) # 10
                   example.plot_s_db(m=1, n=0, label='S12', color=color_list[1])
               elif i == 4:
                   example.plot_s_db_time(m=0, n=0, label='S11', color=color_list[0]) # employs windowing before plotting to enhance impluse resolution.
                   example.plot_s_db_time(m=1, n=0, label='S12', color=color_list[1])
               elif i == 5:
                   example.plot_z_time_db(m=0, n=0, label='Z11', color=color_list[0]) # plot_z_re_time
                   example.plot_z_time_db(m=1, n=0, label='Z12', color=color_list[1])

            parser.remove_option('--basename')
            parser.remove_option('--directory')

            fig.savefig(dir_in+cable.replace(".vna.txt","")+'_rf.png')

            # close all plots to avoid memory warning
            plt.close('all')

            iterator += 1

            if iterator >= n_channels:
                break

    # Get integration window (ns)
    t1, t2 = getWindow(window_selection, cable_length)

    # ------------------------------------------
    # The strange S parameter mapping
    # See https://github.com/skhalil/Instrumentation/blob/master/VNA/readVNADataSKRF.py#L101-L111
    #
    # The map to read the correct values is the one on right side:
    #
    # S11 S13          00  01            S11 S12
    #            ---->           ----> 
    # S12 S14          10  11            S21 S22
    #
    # Do the following to read the right elements rather than the default in touchstone files:
    #
    # S11 : s[:,0,0]
    # S12 : s[:,1,0]
    # S13 : s[:,0,1]
    # S14 : s[:,1,1]
    #
    # s2p file contents:
    # - subfile 0 contains S11, S12, S13, S14
    # - subfile 1 contains S21, S22, S23, S24
    # - subfile 2 contains S31, S32, S33, S34
    # - subfile 3 contains S41, S42, S43, S44
    # ------------------------------------------

    comps       = ['11', '12', '21']
    subfiles    = ['0', '0', '1']

    iterator = 0
    Breaker = True

    while Breaker == True:
        comp = comps[iterator]
        subfile = subfiles[iterator]
        S_name = "S" + comp

        # comp is the S parameter we want to measure
        # S_ij is the matrix element of the ith row, jth column
        # subfile is the s2p file index for different s2p files
        # Note: The S21 parameter is stored in a different subfile;
        #       for S21, we use subfile '1' and matrix element '11'.
        if   comp == '11' and subfile == '0': S_ij = '11'
        elif comp == '12' and subfile == '0': S_ij = '21'
        elif comp == '21' and subfile == '1': S_ij = '11'

        i = int(S_ij[0])
        j = int(S_ij[1])

        print()
        print("Parameter: {0}".format(S_name))
        #print("S_ij = {0}".format(S_ij))
        #print("i = {0}, j = {1}".format(i, j))
        print("Time range: [{0} ns, {1} ns]".format(t1, t2))

        # Get list of networks
        network_list = []
        for channel in range(n_channels):
            network_list.append(rf.Network("Data/"+cable_number_str+"/Plots/s2p/"+filename_list[channel].replace(".txt","")+'_'+subfile+'.s2p', f_unit='ghz'))

        # --- Create summary plots with all channels --- #
        with style.context('seaborn-ticks'):
            # setup plot
            fig0 = plt.figure(figsize=(8,4))
            fig0.patch.set_facecolor('xkcd:black')
            plt.style.use('dark_background')
            # get axes
            ax0 = plt.subplot(1,2,1)
            ax1 = plt.subplot(1,2,2)

            net_dc = []
            data_for_csv = []

            # add header to csv data
            header = ["Cable", "Channel", "Parameter", "Mean Impedance (ohms)", "Comments"]
            data_for_csv.append(header)

            for channel in range(n_channels):
                file_name           = ff_list[channel]
                long_channel_name   = getChannelFromFile(file_name)
                short_channel_name  = getShortChannelName(long_channel_name)

                #print("file_name: {0}, long_channel_name: {1}, short_channel_name: {2}".format(file_name, long_channel_name, short_channel_name))

                S_label = "S{0}_{1}".format(comp, long_channel_name)
                T_label = "TD{0}_{1}".format(comp, long_channel_name)

                # plot data
                this_net = network_list[channel]
                net_dc.append(this_net[i,j].extrapolate_to_dc(kind='linear'))
                net_dc[channel].plot_s_db(label=S_label, ax=ax0, color=color_list[channel])
                net_dc[channel].plot_z_time_step(pad=0, window='hamming', z0=50, label=T_label, ax=ax1, color=color_list[channel])

                # calculate and plot impedance
                mean_impedance = calc_and_plot_mean_impedance(long_channel_name, ax1, t1, t2, color_list[channel])

                # add row to csv data
                row = [cable_number, short_channel_name, S_name, mean_impedance, Comments]
                data_for_csv.append(row)

            # Note: we should only record S12 impedance values
            if S_name == "S12":
                output_csv_file = "Data/{0}/Mean_Impedance.csv".format(cable_number_str)
                writeCSV(output_csv_file, data_for_csv)

            # setup axes
            setup_axes(ax0, signal_vs_freq_title, signal_vs_freq_xlim, signal_vs_freq_ylim)
            setup_axes(ax1, impedance_vs_time_title, impedance_vs_time_xlim, impedance_vs_time_ylim)
            plt.tight_layout()

            fig0.savefig("Data/"+cable_number_str+"/Plots/"+cable_number_str+'_freq_time_Z_rf_'+"S"+comp+'.png')

            # close all plots to avoid memory warning
            plt.close('all')

            iterator += 1

            if iterator > 2:
                break

    print()
    print("Analysis complete for cable {0}. To view plots, see the 'Plots' directory for cable {0}.".format(cable_number_str))

# run analysis
def run():
    # Input parameters from user
    cable_number        = int(input("Enter cable number: "))
    cable_type          = int(input("Enter cable type [0, 1, 2, 3, 4]: "))
    cable_length        = int(input("Enter cable length in cm [0, 35, 80, 100, 140, 160, 180, 200]: "))
    window_selection    = int(input("Enter integration window [2-5ns (0), 8-11ns (1), variable (2)]: "))
    Comments            = input("Enter comments for this run; if there are no comments, leave blank: ")

    # Analyze data for cable
    analyze(cable_number, cable_type, cable_length, window_selection, Comments)

def main():
    run()

if __name__ == "__main__":
    main()
