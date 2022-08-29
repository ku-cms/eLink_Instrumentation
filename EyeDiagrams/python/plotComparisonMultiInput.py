# plotComparisonMultiInput.py

import numpy as np
import matplotlib.pyplot as plt
import tools

def plotData(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, drawMean):
    verbose = False
    tools.makeDir(plot_dir)
    data_1 = tools.getData(input_file_1)
    data_2 = tools.getData(input_file_2)
    output_png = "{0}/{1}.png".format(plot_dir, output_file)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)

    # get default colors
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors     = prop_cycle.by_key()['color']

    # get data from column
    y_data_label = ""
    x_vals  = []
    y1_vals = []
    y2_vals = []

    # get x, y1, and data label
    for i, row in enumerate(data_1):
        # first row has labels
        if i == 0:
            y_data_label = row[y_column_index]
        # second row is the beginning of data values
        else:
            # WARNING: make sure to convert strings to floats!
            x  = float(row[x_column_index])
            y1 = float(row[y_column_index])
            x_vals.append(x)
            y1_vals.append(y1)
        if verbose:
            print("{0}: {1}".format(i, row[y_column_index]))
    
    # get y2
    for i, row in enumerate(data_2):
        # second row is the beginning of data values
        if i > 0:
            # WARNING: make sure to convert strings to floats!
            y2 = float(row[y_column_index])
            y2_vals.append(y2)
        if verbose:
            print("{0}: {1}".format(i, row[y_column_index]))
    
    # plot
    fig, ax = plt.subplots(figsize=(6, 6))

    x_array  = np.array(x_vals)
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
    ax.set_title(title,         fontsize=16)
    ax.set_xlabel(x_data_label, fontsize=12)
    ax.set_ylabel(y_data_label, fontsize=12)
    
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

def makePlotsRD53(input_file_1, input_file_2, label_1, label_2, plot_dir):
    # Heights
    output_file     = "EyeDiagram_Heights"
    title           = "Eye Diagram Heights"
    x_data_label    = "TAP0"
    x_column_index  = 1
    y_column_index  = 2
    xlim            = [0.0, 1200.0]
    ylim            = [0.0, 600.0]
    drawMean        = False
    plotData(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, drawMean)
    
    # Jitters
    output_file     = "EyeDiagram_Jitters"
    title           = "Eye Diagram Jitters"
    x_data_label    = "TAP0"
    x_column_index  = 1
    y_column_index  = 3
    xlim            = [0.0, 1200.0]
    ylim            = [0.0, 120.0]
    drawMean        = False
    plotData(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, drawMean)
    
    # Widths
    output_file     = "EyeDiagram_Widths"
    title           = "Eye Diagram Widths"
    x_data_label    = "TAP0"
    x_column_index  = 1
    y_column_index  = 4
    xlim            = [0.0, 1200.0]
    ylim            = [0.0, 800.0]
    drawMean        = False
    plotData(input_file_1, input_file_2, label_1, label_2, output_file, plot_dir, title, x_data_label, x_column_index, y_column_index, xlim, ylim, drawMean)

def run():
    # Cable 120: before lashing vs. after lashing
    cable_number    = 120
    input_file_1    = "tables/Cable_120_EyeDiagrams_beforeLashing.csv"
    input_file_2    = "tables/Cable_120_EyeDiagrams_afterLashing.csv"
    label_1         = "before lashing"
    label_2         = "after lashing"
    plot_dir        = "plots/Cable_120_lashing"
    drawMean        = True
    makePlotsCable(cable_number, input_file_1, input_file_2, label_1, label_2, plot_dir, drawMean)
    
    # Cable 120: old settings ("ch1" used for eye diagrams) vs. new settings ("math1" used for eye diagrams)
    cable_number    = 120
    input_file_1    = "tables/Cable_120_EyeDiagrams_afterLashing.csv"
    input_file_2    = "tables/Cable_120_newSetup_EyeDiagrams.csv"
    label_1         = "old (ch1)"
    label_2         = "new (math1)"
    plot_dir        = "plots/Cable_120_settings"
    drawMean        = True
    makePlotsCable(cable_number, input_file_1, input_file_2, label_1, label_2, plot_dir, drawMean)
    
    # Cable 121: old settings ("ch1" used for eye diagrams) vs. new settings ("math1" used for eye diagrams)
    cable_number    = 121
    input_file_1    = "tables/Cable_121_EyeDiagrams.csv"
    input_file_2    = "tables/Cable_121_newSetup_EyeDiagrams.csv"
    label_1         = "old (ch1)"
    label_2         = "new (math1)"
    plot_dir        = "plots/Cable_121_settings"
    drawMean        = True
    makePlotsCable(cable_number, input_file_1, input_file_2, label_1, label_2, plot_dir, drawMean)

    input_file_1    = "tables/RD53A_EyeDiagram_TAP0_Scan_2021_11_11.csv"
    input_file_2    = "tables/RD53B_EyeDiagram_TAP0_Scan_2022_08_26.csv"
    label_1         = "RD53A"
    label_2         = "RD53B"
    plot_dir        = "plots/RD53_AvsB_Comparison"
    makePlotsRD53(input_file_1, input_file_2, label_1, label_2, plot_dir)

def main():
    run()

if __name__ == "__main__":
    main()

