#!/usr/bin/python3
import os
from optparse import OptionParser
import pandas as pd
import skrf as rf
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import style


# Functions
def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


import config

makeDir("Data/" + config.cable_number + "/Plots")
makeDir("Data/" + config.cable_number + "/Plots/s2p")

IDchecker = 0
Breaker = True

parser = OptionParser()

while Breaker == True:

    FILE = config.Pre_list[IDchecker]
    print("Creating s2p files for ", FILE)

    parser.add_option('--basename', metavar='T', type='string', action='store',
                      default='Data/' + str(config.cable_number) + '/' + FILE,  # 31, 15, 33 #calibration_test.vna
                      dest='basename',
                      help='input text file')

    parser.add_option('--directory', metavar='T', type='string', action='store',
                      default='Data/' + str(config.cable_number) + '/' + 'Plots/',
                      dest='directory',
                      help='directory to store plots')

    (options, args) = parser.parse_args()

    # ==========end: options =============
    basename1 = options.basename
    basename2 = basename1.replace('Data/' + str(config.cable_number) + '/',
                                  'Data/' + str(config.cable_number) + '/' + 'Plots/s2p/')
    dir_in = options.directory
    cable = basename1.replace('Data/' + str(config.cable_number) + '/', "")

    infile = pd.read_csv(basename1, names=['pt', 'f', 's11R', 's11I', 's12R', 's12I', 's13R', 's13I', 's14R', 's14I'],
                         delim_whitespace=True, skiprows=1)
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
            filename = basename2.replace(".txt", "") + '_' + str(fileindex) + '.s2p'
            fileindex += 1
            f = open(filename, 'w')
            f.write('# GHZ	S	RI	R	50.0\n')

            try:
                # print (row['f'][1:-1], row['s11R'][1:-1], row['s11I'][1:-1], row['s12R'][1:-1] )
                f.write(
                    f"!freq       Rel{row['f'][1:-1]}       Im{row['f'][1:-1]}      Rel{row['s11R'][1:-1]}       Im{row['s11R'][1:-1]}        Rel{row['s11I'][1:-1]}        Im{row['s11I'][1:-1]}         Rel{row['s12R'][1:-1]}      Im{row['s12R'][1:-1]}\n")
            except:
                if row['f'][1:-1] == 'SDD':
                    f.write(f"!freq\tRelS11\tImS11\n")
            prevF = 0
        try:
            if float(row['s11R']) == float(row['s11R']) and float(row['f']) > prevF:
                f.write(
                    f"{float(row['f']):.3f}\t{float(row['s11R'])}\t{float(row['s11I'])}\t{float(row['s12R'])}\t{float(row['s12I'])}\t{float(row['s13R'])}\t{float(row['s13I'])}\t{float(row['s14R'])}\t{float(row['s14I'])}\n")
                prevF = float(row['f'])
        except:
            pass
    example = rf.Network(basename2.replace(".txt", "") + '_0.s2p', f_unit='ghz')

    print("Plotting the data.\n")
    with style.context('seaborn-ticks'):
        # Time domain reflectometry, measurement vs simulation
        fig0 = plt.figure(figsize=(8, 4))
        fig0.patch.set_facecolor('xkcd:black')
        plt.style.use('dark_background')
        ax0 = plt.subplot(1, 2, 1)
        # major_ticks = np.arange(0, 6.5, 0.5)
        # minor_ticks = np.arange(0, 6.5, 0.1)
        ax0.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax0.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax0.grid(True, color='0.8', which='minor')
        ax0.grid(True, color='0.4', which='major')
        # ax0.legend()
        example_dc = example.extrapolate_to_dc(kind='linear')
        plt.title('Frequency')
        example_dc.s11.plot_s_db(label='S11')
        example_dc.s21.plot_s_db(label='S12')
        plt.ylim((-75.0, 75.0))
        plt.xlim((100000, 2500000000))
        ax1 = plt.subplot(1, 2, 2)
        ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax1.grid(True, color='0.8', which='minor')
        ax1.grid(True, color='0.4', which='major')
        plt.title(
            'Time domain reflection step response (DC extrapolation)')  # The time_step component of the z-matrix vs frequency
        example_dc.s11.plot_z_time_step(attribute='z_time_step', pad=2000, window='hamming', z0=50, label='TD11')
        example_dc.s21.plot_z_time_step(attribute='z_time_step', pad=2000, window='hamming', z0=50, label='TD12')
        plt.ylim((0, 200))
        plt.xlim((0, 25))
        plt.tight_layout()
        # ax1.legend()
        fig0.savefig(dir_in + cable.replace(".vna.txt", "") + '_freq_time_Z_rf.png')

        # Gating the Reflection of Interest
        s11_gated = example.s11.time_gate()  # (center=0, span=.2)#autogate on the fly
        s11_gated.name = 'gated '
        fig1 = plt.figure(figsize=(8, 4))
        plt.subplot(121)
        example.s11.plot_s_db()
        s11_gated.plot_s_db()  # s11.time_gate()
        plt.title('Frequency Domain')
        plt.subplot(122)
        example.s11.plot_s_db_time()
        s11_gated.plot_s_db_time()
        plt.title('Time Domain')
        plt.xlim((-5, 5))
        plt.tight_layout()
        # plt.show()
        fig1.savefig(dir_in + cable.replace(".vna.txt", "") + '_fref_time_rf.png')

        fig = plt.figure(figsize=(14, 6))
        for i in range(6):
            ax = fig.add_subplot(2, 3, i + 1)
            if i == 0:
                plt.axis([-1.1, 2.1, -1.1, 1.1])
                example.plot_s_smith(draw_labels=True, m=0, n=0, label='S11')
                example.plot_s_smith(draw_labels=True, m=1, n=0, label='S12')
            elif i == 1:
                example.plot_z_re(m=0, n=0, label='Z11')
                example.plot_z_re(m=1, n=0, label='Z12')
            elif i == 2:
                example.plot_z_im(m=0, n=0, label='Z11')
                example.plot_z_im(m=1, n=0, label='Z12')
            elif i == 3:
                example.plot_s_db(m=0, n=0, label='S11')  # 10
                example.plot_s_db(m=1, n=0, label='S12')
            elif i == 4:
                example.plot_s_db_time(m=0, n=0,
                                       label='S11')  # employs windowing before plotting to enhance impluse resolution.
                example.plot_s_db_time(m=1, n=0, label='S12')
            elif i == 5:
                example.plot_z_time_db(m=0, n=0, label='Z11')  # plot_z_re_time
                example.plot_z_time_db(m=1, n=0, label='Z12')

        fig.savefig(dir_in + cable.replace(".vna.txt", "") + '_rf.png')
        fig = plt.close()

        parser.remove_option('--basename')
        parser.remove_option('--directory')

        IDchecker += 1
        plt.close()
        if IDchecker > len(config.Pre_list) - 1:
            break

print("Plots can be now found in the Plots folder of the Cable\n")
