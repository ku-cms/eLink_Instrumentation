# plotComparisonMultiInput.py

import numpy as np
import matplotlib.pyplot as plt
import tools

# TODO:
# DONE:
# - Create function to load data from input files
# - Create function to plot data and ratios in two subplots

def plotData(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, drawMean):
    verbose = False
    tools.makeDir(plot_dir)
    # output file names
    output_png = "{0}/{1}.png".format(plot_dir, output_file)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)
    # get default colors
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors     = prop_cycle.by_key()['color']
    # get data
    data_1 = tools.getData(input_file_1)
    data_2 = tools.getData(input_file_2)
    # get data label for y values
    y1_data_label = data_1[0][y_column_index]
    y2_data_label = data_2[0][y_column_index]
    # check that y data labels match
    if y1_data_label != y2_data_label:
        print("ERROR: y1_data_label and y2_data_label do not match! Quitting.")
        print(" - y1_data_label: {0}".format(y1_data_label))
        print(" - y2_data_label: {0}".format(y2_data_label))
        return
    # get x, y values
    x1_vals, y1_vals = tools.getXYData(data_1, x_column_index, y_column_index, verbose)
    x2_vals, y2_vals = tools.getXYData(data_2, x_column_index, y_column_index, verbose)
    # check that x values match
    if x1_vals != x2_vals:
        print("ERROR: x1_vals and x2_vals do not match! Quitting.")
        print(" - x1_vals: {0}".format(x1_vals))
        print(" - x2_vals: {0}".format(x2_vals))
        return

    # plot
    fig, ax = plt.subplots(figsize=(6, 6))

    x_array  = np.array(x1_vals)
    y1_array = np.array(y1_vals)
    y2_array = np.array(y2_vals)
    y1_mean  = np.mean(y1_array)
    y2_mean  = np.mean(y2_array)
    y1_std   = np.std(y1_array)
    y2_std   = np.std(y2_array)
    # take ratio of means
    r21      = y2_mean / y1_mean
    # get error of ratio (assuming independent variables without correlation)
    # q = x / y
    # getMultiplicationError(q, x, dx, y, dy)
    r21_err  = tools.getMultiplicationError(r21, y2_mean, y2_std, y1_mean, y1_std) 
    # extend x to plot mean and std dev
    x_extended = np.insert(x_array, 0, float(x_array[0]  - 1) )
    x_extended = np.append(x_extended, float(x_array[-1] + 1) )
    
    if verbose:
        print("x = {0}".format(x_array))
        print("x_extended = {0}".format(x_extended))
        print("y1 = {0}".format(y1_array))
        print("y2 = {0}".format(y2_array))
        print("y1_mean = {0}".format(y1_mean))
        print("y2_mean = {0}".format(y2_mean))
        print("y1_std  = {0}".format(y1_std))
        print("y2_std  = {0}".format(y2_std))
        print("r21     = {0}".format(r21))
        print("r21_err = {0}".format(r21_err))
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_title(title,             fontsize=16)
    ax.set_xlabel(x_data_label,     fontsize=12)
    ax.set_ylabel(y1_data_label,    fontsize=12)
    
    p1 = plt.scatter(x_array, y1_array, color=colors[0], label=label_1)
    p2 = plt.scatter(x_array, y2_array, color=colors[1], label=label_2)
    objects = [p1, p2]
    if drawMean:
        p3 = plt.axline((x_extended[0], y1_mean), (x_extended[-1], y1_mean), color=colors[0], linestyle="--", label="mean")
        p4 = plt.axline((x_extended[0], y2_mean), (x_extended[-1], y2_mean), color=colors[1], linestyle="--", label="mean")
        p5 = plt.fill_between(x_extended, y1_mean - y1_std, y1_mean + y1_std, color=colors[0], alpha=0.2, label="std dev")
        p6 = plt.fill_between(x_extended, y2_mean - y2_std, y2_mean + y2_std, color=colors[1], alpha=0.2, label="std dev")
        objects = [p1, p2, p3, p4, p5, p6]
        # text
        text_x    = xlim[0] + 0.1 * (xlim[1] - xlim[0])
        text_y1   = ylim[0] + 0.9 * (ylim[1] - ylim[0])
        text_y2   = ylim[0] + 0.8 * (ylim[1] - ylim[0])
        text_y3   = ylim[0] + 0.7 * (ylim[1] - ylim[0])
        equation1 = r"$\mu_1 = {0:.2f} \pm {1:.2f}$".format(y1_mean, y1_std)
        equation2 = r"$\mu_2 = {0:.2f} \pm {1:.2f}$".format(y2_mean, y2_std)
        # use double curly brackets {{21}} so that this is not used as an index by format
        equation3 = r"$r_{{21}} = {0:.2f} \pm {1:.2f}$".format(r21, r21_err)
        ax.text(text_x, text_y1, equation1, fontsize=15)
        ax.text(text_x, text_y2, equation2, fontsize=15)
        ax.text(text_x, text_y3, equation3, fontsize=15)
    # specify order for legend
    labels = [o.get_label() for o in objects]
    plt.legend(objects, labels, loc='upper right', prop={'size': 12})
    plt.savefig(output_png)
    plt.savefig(output_pdf)

def plotDataAndRatio(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, ratio_ylim, ratio_y_label):
    verbose = False
    tools.makeDir(plot_dir)
    # output file names
    output_png = "{0}/{1}.png".format(plot_dir, output_file)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)
    # get default colors
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors     = prop_cycle.by_key()['color']
    # get data
    data_1 = tools.getData(input_file_1)
    data_2 = tools.getData(input_file_2)
    # get data label for y values
    y1_data_label = data_1[0][y_column_index]
    y2_data_label = data_2[0][y_column_index]
    # check that y data labels match
    if y1_data_label != y2_data_label:
        print("ERROR: y1_data_label and y2_data_label do not match! Quitting.")
        print(" - y1_data_label: {0}".format(y1_data_label))
        print(" - y2_data_label: {0}".format(y2_data_label))
        return
    # get x, y values
    x1_vals, y1_vals = tools.getXYData(data_1, x_column_index, y_column_index, verbose)
    x2_vals, y2_vals = tools.getXYData(data_2, x_column_index, y_column_index, verbose)
    # check that x values match
    if x1_vals != x2_vals:
        print("ERROR: x1_vals and x2_vals do not match! Quitting.")
        print(" - x1_vals: {0}".format(x1_vals))
        print(" - x2_vals: {0}".format(x2_vals))
        return

    # plot
    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(6, 6))

    # ratio: y2_vals / y1_vals (RD53B / RD53A)
    ratio_vals  = [a/b for a,b in zip(y2_vals, y1_vals)]
    x_array     = np.array(x1_vals)
    y1_array    = np.array(y1_vals)
    y2_array    = np.array(y2_vals)
    ratio_array = np.array(ratio_vals)
    
    if verbose:
        print("x = {0}".format(x_array))
        print("y1 = {0}".format(y1_array))
        print("y2 = {0}".format(y2_array))
    
    # figure
    fig.suptitle(title)
    # upper plot
    axs[0].set_xlim(xlim)
    axs[0].set_ylim(ylim)
    axs[0].set_ylabel(y1_data_label,    fontsize=12)
    axs[0].grid(b=True, linestyle='dotted')
    # lower plot
    axs[1].set_xlim(xlim)
    axs[1].set_ylim(ratio_ylim)
    axs[1].set_xlabel(x_data_label,     fontsize=12)
    axs[1].set_ylabel(ratio_y_label,    fontsize=12)
    axs[1].grid(b=True, linestyle='dotted')
    
    p1 = axs[0].scatter(x_array, y1_array,      color=colors[0],    label=label_1)
    p2 = axs[0].scatter(x_array, y2_array,      color=colors[1],    label=label_2)
    p3 = axs[1].scatter(x_array, ratio_array,   color="black",      label=ratio_y_label)
    objects_upper = [p1, p2]
    objects_lower = [p3]
    # specify order for legend
    labels_upper = [o.get_label() for o in objects_upper]
    labels_lower = [o.get_label() for o in objects_lower]
    axs[0].legend(objects_upper, labels_upper, loc='upper right', prop={'size': 12})
    axs[1].legend(objects_lower, labels_lower, loc='upper right', prop={'size': 12})
    plt.savefig(output_png)
    plt.savefig(output_pdf)

def makePlotsCable(cable_number, input_file_1, input_file_2, label_1, label_2, plot_dir, drawMean):
    # Heights
    output_file     = "Cable_{0}_EyeDiagram_Heights".format(cable_number)
    title           = "Cable {0} Eye Diagram Heights".format(cable_number)
    x_data_label    = "Channel"
    x_column_index  = 0
    y_column_index  = 3
    xlim            = [0.0, 10.0]
    ylim            = [0.0, 400.0]
    plotData(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, drawMean)
    
    # Jitters
    output_file     = "Cable_{0}_EyeDiagram_Jitters".format(cable_number)
    title           = "Cable {0} Eye Diagram Jitters".format(cable_number)
    x_data_label    = "Channel"
    x_column_index  = 0
    y_column_index  = 4
    xlim            = [0.0, 10.0]
    ylim            = [0.0, 600.0]
    plotData(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, drawMean)
    
    # Widths
    output_file     = "Cable_{0}_EyeDiagram_Widths".format(cable_number)
    title           = "Cable {0} Eye Diagram Widths".format(cable_number)
    x_data_label    = "Channel"
    x_column_index  = 0
    y_column_index  = 5
    xlim            = [0.0, 10.0]
    ylim            = [0.0, 800.0]
    plotData(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, drawMean)

def makePlotsRD53(input_file_1, input_file_2, label_1, label_2, plot_dir, plotRatio):
    # Heights
    output_file     = "EyeDiagram_Heights"
    title           = "Eye Diagram Heights"
    x_data_label    = "TAP0"
    x_column_index  = 1
    y_column_index  = 2
    xlim            = [0.0, 1200.0]
    ylim            = [0.0, 800.0]
    ratio_ylim      = [0.8, 1.2]
    ratio_y_label   = "RD53B / RD53A"
    drawMean        = False
    if plotRatio:
        plotDataAndRatio(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, ratio_ylim, ratio_y_label)
    else:
        plotData(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, drawMean)
    
    # Jitters
    output_file     = "EyeDiagram_Jitters"
    title           = "Eye Diagram Jitters"
    x_data_label    = "TAP0"
    x_column_index  = 1
    y_column_index  = 3
    xlim            = [0.0, 1200.0]
    ylim            = [0.0, 150.0]
    ratio_ylim      = [0.0, 2.0]
    ratio_y_label   = "RD53B / RD53A"
    drawMean        = False
    if plotRatio:
        plotDataAndRatio(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, ratio_ylim, ratio_y_label)
    else:
        plotData(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, drawMean)
    
    # Widths
    output_file     = "EyeDiagram_Widths"
    title           = "Eye Diagram Widths"
    x_data_label    = "TAP0"
    x_column_index  = 1
    y_column_index  = 4
    xlim            = [0.0, 1200.0]
    ylim            = [0.0, 1000.0]
    ratio_ylim      = [0.0, 2.0]
    ratio_y_label   = "RD53B / RD53A"
    drawMean        = False
    if plotRatio:
        plotDataAndRatio(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, ratio_ylim, ratio_y_label)
    else:
        plotData(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, drawMean)

def run():
    # # Cable 120: before lashing vs. after lashing
    # cable_number    = 120
    # input_file_1    = "tables/Cable_120_EyeDiagrams_beforeLashing.csv"
    # input_file_2    = "tables/Cable_120_EyeDiagrams_afterLashing.csv"
    # label_1         = "before lashing"
    # label_2         = "after lashing"
    # plot_dir        = "plots/Cable_120_lashing"
    # drawMean        = True
    # makePlotsCable(cable_number, input_file_1, input_file_2, label_1, label_2, plot_dir, drawMean)
    # 
    # # Cable 120: old settings ("ch1" used for eye diagrams) vs. new settings ("math1" used for eye diagrams)
    # cable_number    = 120
    # input_file_1    = "tables/Cable_120_EyeDiagrams_afterLashing.csv"
    # input_file_2    = "tables/Cable_120_newSetup_EyeDiagrams.csv"
    # label_1         = "old (ch1)"
    # label_2         = "new (math1)"
    # plot_dir        = "plots/Cable_120_settings"
    # drawMean        = True
    # makePlotsCable(cable_number, input_file_1, input_file_2, label_1, label_2, plot_dir, drawMean)
    # 
    # # Cable 121: old settings ("ch1" used for eye diagrams) vs. new settings ("math1" used for eye diagrams)
    # cable_number    = 121
    # input_file_1    = "tables/Cable_121_EyeDiagrams.csv"
    # input_file_2    = "tables/Cable_121_newSetup_EyeDiagrams.csv"
    # label_1         = "old (ch1)"
    # label_2         = "new (math1)"
    # plot_dir        = "plots/Cable_121_settings"
    # drawMean        = True
    # makePlotsCable(cable_number, input_file_1, input_file_2, label_1, label_2, plot_dir, drawMean)

    input_file_1    = "tables/RD53A_EyeDiagrams_TAP0_200to1000_Scan_2021_11_11.csv"
    input_file_2    = "tables/RD53A_EyeDiagrams_TAP0_200to1000_Scan_2022_08_31.csv"
    label_1         = "RD53A (2021_11_11)"
    label_2         = "RD53A (2022_08_31)"
    plot_dir        = "plots/RD53_A_2021vs2022_EyeDiagram_Comparison_v1"
    plot_dir_ratio  = "plots/RD53_A_2021vs2022_EyeDiagram_Comparison_v1_ratio"
    makePlotsRD53(input_file_1, input_file_2, label_1, label_2, plot_dir,       plotRatio=False)
    makePlotsRD53(input_file_1, input_file_2, label_1, label_2, plot_dir_ratio, plotRatio=True)
    
    input_file_1    = "tables/RD53A_EyeDiagrams_TAP0_200to1000_Scan_2021_11_11.csv"
    input_file_2    = "tables/RD53B_EyeDiagrams_TAP0_200to1000_Scan_2022_08_26.csv"
    label_1         = "RD53A"
    label_2         = "RD53B"
    plot_dir        = "plots/RD53_AvsB_EyeDiagram_Comparison_v1"
    plot_dir_ratio  = "plots/RD53_AvsB_EyeDiagram_Comparison_v1_ratio"
    makePlotsRD53(input_file_1, input_file_2, label_1, label_2, plot_dir,       plotRatio=False)
    makePlotsRD53(input_file_1, input_file_2, label_1, label_2, plot_dir_ratio, plotRatio=True)
    
    input_file_1    = "tables/RD53A_EyeDiagrams_TAP0_100to1000_Scan_2022_08_31.csv"
    input_file_2    = "tables/RD53B_EyeDiagrams_TAP0_100to1000_Scan_2022_08_26.csv"
    label_1         = "RD53A"
    label_2         = "RD53B"
    plot_dir        = "plots/RD53_AvsB_EyeDiagram_Comparison_v2"
    plot_dir_ratio  = "plots/RD53_AvsB_EyeDiagram_Comparison_v2_ratio"
    makePlotsRD53(input_file_1, input_file_2, label_1, label_2, plot_dir,       plotRatio=False)
    makePlotsRD53(input_file_1, input_file_2, label_1, label_2, plot_dir_ratio, plotRatio=True)

def main():
    run()

if __name__ == "__main__":
    main()

