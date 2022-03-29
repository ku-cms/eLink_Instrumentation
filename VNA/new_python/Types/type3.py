#!/usr/bin/python3
import config
import skrf as rf
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import style

IDchecker = 0
Breaker = True

print("List of Cables being analysed", config.Pre_list, "\n")


def split(word):
    return [char for char in word]


for i in range(1, len(config.Pre_list) + 1):
    globals()[f"ff{i}"] = f"Data/" + config.cable_number + f"/{config.Pre_list[i - 1]}"
    globals()[f"filename{i}"] = f"{config.Pre_list[i - 1]}"

with open("Data/" + config.cable_number + "/Impedence_List.csv", "a") as Ana2:
    Ana2.write(
        "Cable Number,Length,Type, Parameter, M1CMD (Normal),M1CMD (2-5), M1D0 (Normal), M1D0 (2-5), M1D1(Normal), M1D1 (2-5), M2CMD (Normal),M2CMD (2-5), M2D0 (Normal), M2D0 (2-5), M2D1(Normal), M2D1 (2-5),\n")
    Ana2.close()

while Breaker == True:

    config.comp = config.comps[IDchecker]
    config.subfile = config.subfiles[IDchecker]

    if config.comp == '11' and config.subfile == '0':
        S_ij = '11'
    elif config.comp == '12' and config.subfile == '0':
        S_ij = '21'
    elif config.comp == '21' and config.subfile == '1':
        S_ij = '11'

    i = int(split(S_ij)[0])
    j = int(split(S_ij)[1])

    print("\nParameter being analyzed\n", "S" + config.comp)

    net4 = rf.Network(
        "Data/" + config.cable_number + "/Plots/s2p/" + filename1.replace(".txt", "") + '_' + config.subfile + '.s2p',
        f_unit='ghz')
    net5 = rf.Network(
        "Data/" + config.cable_number + "/Plots/s2p/" + filename2.replace(".txt", "") + '_' + config.subfile + '.s2p',
        f_unit='ghz')
    net6 = rf.Network(
        "Data/" + config.cable_number + "/Plots/s2p/" + filename3.replace(".txt", "") + '_' + config.subfile + '.s2p',
        f_unit='ghz')
    net8 = rf.Network(
        "Data/" + config.cable_number + "/Plots/s2p/" + filename4.replace(".txt", "") + '_' + config.subfile + '.s2p',
        f_unit='ghz')
    net10 = rf.Network(
        "Data/" + config.cable_number + "/Plots/s2p/" + filename5.replace(".txt", "") + '_' + config.subfile + '.s2p',
        f_unit='ghz')
    net12 = rf.Network(
        "Data/" + config.cable_number + "/Plots/s2p/" + filename6.replace(".txt", "") + '_' + config.subfile + '.s2p',
        f_unit='ghz')

    # netref = rf.network.Network(out_dir+'/'+sub_out_dir+'/straight_SMA.vna_'+config.subfile+'.s2p', f_unit='ghz')

    with style.context('seaborn-darkgrid'):

        fig0 = plt.figure(figsize=(10, 10))
        fig0.patch.set_facecolor('xkcd:black')
        plt.style.use('dark_background')
        ax0 = plt.subplot(2, 2, 1)
        ax1 = plt.subplot(2, 2, 2)
        ax2 = plt.subplot(2, 2, 3)
        ax3 = plt.subplot(2, 2, 4)

        ax0.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax0.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax0.grid(True, color='0.8', which='minor')
        ax0.grid(True, color='0.4', which='major')

        ax2.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax2.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax2.grid(True, color='0.8', which='minor')
        ax2.grid(True, color='0.4', which='major')

        net4_dc = net4[i, j].extrapolate_to_dc(kind='linear')
        net5_dc = net5[i, j].extrapolate_to_dc(kind='linear')
        net6_dc = net6[i, j].extrapolate_to_dc(kind='linear')
        net8_dc = net8[i, j].extrapolate_to_dc(kind='linear')
        net10_dc = net10[i, j].extrapolate_to_dc(kind='linear')
        net12_dc = net12[i, j].extrapolate_to_dc(kind='linear')
        #   netref_dc = netref[i,j].extrapolate_to_dc(kind='linear')

        net4_dc.plot_s_db(label='S' + config.comp + ff1.split('.vna')[0].split('/')[-1:][0], ax=ax0, color='b')
        net5_dc.plot_s_db(label='S' + config.comp + ff2.split('.vna')[0].split('/')[-1:][0], ax=ax0, color='r')
        net6_dc.plot_s_db(label='S' + config.comp + ff3.split('.vna')[0].split('/')[-1:][0], ax=ax0, color='g')
        net8_dc.plot_s_db(label='S' + config.comp + ff4.split('.vna')[0].split('/')[-1:][0], ax=ax2, color='w')
        net10_dc.plot_s_db(label='S' + config.comp + ff5.split('.vna')[0].split('/')[-1:][0], ax=ax2, color='m')
        net12_dc.plot_s_db(label='S' + config.comp + ff6.split('.vna')[0].split('/')[-1:][0], ax=ax2, color='c')

        net4_dc.plot_z_time_step(pad=0, window='hamming', z0=50,
                                 label='TD' + config.comp + ff1.split('.vna')[0].split('/')[-1:][0], ax=ax1, color='b')
        config.display_mean_impedance(ax1, config.t1, config.t2, config.dt1, config.dt2, 'b')

        net5_dc.plot_z_time_step(pad=0, window='hamming', z0=50,
                                 label='TD' + config.comp + ff2.split('.vna')[0].split('/')[-1:][0], ax=ax1, color='r')
        config.display_mean_impedance(ax1, config.t1, config.t2, config.dt1, config.dt2, 'r')

        net6_dc.plot_z_time_step(pad=0, window='hamming', z0=50,
                                 label='TD' + config.comp + ff3.split('.vna')[0].split('/')[-1:][0], ax=ax1, color='g')
        config.display_mean_impedance(ax1, config.t1, config.t2, config.dt1, config.dt2, 'g')

        net8_dc.plot_z_time_step(pad=0, window='hamming', z0=50,
                                 label='TD' + config.comp + ff4.split('.vna')[0].split('/')[-1:][0], ax=ax3, color='w')
        config.display_mean_impedance(ax3, config.t1, config.t2, config.dt1, config.dt2, 'w')
        net10_dc.plot_z_time_step(pad=0, window='hamming', z0=50,
                                  label='TD' + config.comp + ff5.split('.vna')[0].split('/')[-1:][0], ax=ax3, color='m')
        config.display_mean_impedance(ax3, config.t1, config.t2, config.dt1, config.dt2, 'm')
        net12_dc.plot_z_time_step(pad=0, window='hamming', z0=50,
                                  label='TD' + config.comp + ff6.split('.vna')[0].split('/')[-1:][0], ax=ax3, color='c')
        config.display_mean_impedance(ax3, config.t1, config.t2, config.dt1, config.dt2, 'c')

        with open("Records/Impedence_List_type3.csv", "a") as Ana:
            Ana.write(
                str(config.cable_number) + "," + str(config.cable_length) + "," + str(config.cable_type) + "," + str(
                    "S" + config.comp + ","))
            for i in config.y_plot_value:
                Ana.write(str(i) + ",")
            Ana.write("\n")
            Ana.close()

        with open("Data/" + config.cable_number + "/Impedence_List.csv", "a") as Ana2:
            Ana2.write(
                "Cable Number,Length,Type, Parameter, M1CMD (Normal),M1CMD (2-5), M1D0 (Normal), M1D0 (2-5), M1D1(Normal), M1D1 (2-5), M2CMD (Normal),M2CMD (2-5), M2D0 (Normal), M2D0 (2-5), M2D1(Normal), M2D1 (2-5),\n")
            Ana2.write(
                str(config.cable_number) + "," + str(config.cable_length) + "," + str(config.cable_type) + "," + str(
                    "S" + config.comp + ","))
            for i in config.y_plot_value:
                Ana2.write(str(i) + ",")
            Ana2.write("\n")
            Ana2.close()

        config.y_plot_value.clear()

        config.set_axes(ax1, 'Time Domain', 0.0, 200.0, 0.0, 25.0, 0)
        config.set_axes(ax3, 'Time Domain', 0.0, 200.0, 0.0, 25.0, 0)

        fig0.savefig(
            "Data/" + config.cable_number + "/Plots/" + config.cable_number + 'cm_freq_time_Z_rf_' + "S" + config.comp + '.png')

        plt.close()
        IDchecker += 1

        if IDchecker > 2:
            break
print("\nData analysed. Plots stored in Plots folder.")
