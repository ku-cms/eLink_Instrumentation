# plotComparison.py

import csv
import os
import numpy as np
import matplotlib.pyplot as plt

def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def printData(input_file):
    with open(input_file, "r") as f:
        reader = csv.reader(f)
        print(" --- print file")
        for line in f:
            print(line, end='')
        # return to start of file
        f.seek(0)
        print(" --- print csv")
        for row in reader:
            print(row)

def getData(input_file):
    data = []
    with open(input_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data

def plotData(input_file, output_file, plot_dir, title, column_indices, xlim, ylim, drawMean):
    verbose = False
    makeDir(plot_dir)
    data = getData(input_file)
    output_png = "{0}/{1}.png".format(plot_dir, output_file)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)

    # get default colors
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors     = prop_cycle.by_key()['color']

    # get data from column
    column_index_1 = column_indices[0]
    column_index_2 = column_indices[1]
    data_label     = ""
    x_vals  = []
    y1_vals = []
    y2_vals = []

    for i, row in enumerate(data):
        # skip first row
        if i < 1:
            continue
        # second row has labels
        elif i == 1:
            data_label = row[column_index_1]
        # third row is the beginning of data values
        else:
            # WARNING: make sure to convert strings to floats!
            x  = float(i - 1)
            y1 = float(row[column_index_1])
            y2 = float(row[column_index_2])
            x_vals.append(x)
            y1_vals.append(y1)
            y2_vals.append(y2)
        
        if verbose:
            print("{0}: {1}, {2}".format(i, row[column_index_1], row[column_index_2]))
    
    # plot
    fig, ax = plt.subplots(figsize=(6, 6))

    x_array  = np.array(x_vals)
    y1_array = np.array(y1_vals)
    y2_array = np.array(y2_vals)
    y1_mean  = np.mean(y1_array)
    y2_mean  = np.mean(y2_array)
    y1_std   = np.std(y1_array)
    y2_std   = np.std(y2_array)
    # extend x to plot mean and std dev
    x_extended = np.insert(x_array, 0, float(x_array[0]  - 1) )
    x_extended = np.append(x_extended, float(x_array[-1] + 1) )
    
    if verbose:
        print("x  = {0}".format(x_array))
        print("x_extended  = {0}".format(x_extended))
        print("y1 = {0}".format(y1_array))
        print("y2 = {0}".format(y2_array))
        print("y1_mean = {0}".format(y1_mean))
        print("y2_mean = {0}".format(y2_mean))
        print("y1_std  = {0}".format(y1_std))
        print("y2_std  = {0}".format(y2_std))
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_title(title,         fontsize=16)
    ax.set_xlabel("Channel",    fontsize=12)
    ax.set_ylabel(data_label,   fontsize=12)
    
    p1 = plt.scatter(x_array, y1_array, color=colors[0], label="before lashing")
    p2 = plt.scatter(x_array, y2_array, color=colors[1], label="after lashing")
    objects = [p1, p2]
    if drawMean:
        p3 = plt.axline((x_extended[0], y1_mean), (x_extended[-1], y1_mean), color=colors[0], linestyle="--", label="mean")
        p4 = plt.axline((x_extended[0], y2_mean), (x_extended[-1], y2_mean), color=colors[1], linestyle="--", label="mean")
        p5 = plt.fill_between(x_extended, y1_mean - y1_std, y1_mean + y1_std, color=colors[0], alpha=0.2, label="std dev")
        p6 = plt.fill_between(x_extended, y2_mean - y2_std, y2_mean + y2_std, color=colors[1], alpha=0.2, label="std dev")
        objects = [p1, p2, p3, p4, p5, p6]
    # specify order for legend
    labels = [o.get_label() for o in objects]
    plt.legend(objects, labels, loc='upper right', prop={'size': 12})
    plt.savefig(output_png)
    plt.savefig(output_pdf)

def makePlots():
    input_file      = "data/Cable_120/Cable_120_EyeDiagrams.csv"
    plot_dir        = "plots"
    drawMean        = True
    
    # Heights
    output_file     = "Cable_120_EyeDiagram_Heights"
    title           = "Cable 120 Eye Diagram Heights"
    column_indices  = [3, 6]
    xlim            = [0.0, 10.0]
    ylim            = [0.0, 200.0]
    plotData(input_file, output_file, plot_dir, title, column_indices, xlim, ylim, drawMean)
    
    # Jitters
    output_file     = "Cable_120_EyeDiagram_Jitters"
    title           = "Cable 120 Eye Diagram Jitters"
    column_indices  = [4, 7]
    xlim            = [0.0, 10.0]
    ylim            = [0.0, 500.0]
    plotData(input_file, output_file, plot_dir, title, column_indices, xlim, ylim, drawMean)
    
    # Widths
    output_file     = "Cable_120_EyeDiagram_Widths"
    title           = "Cable 120 Eye Diagram Widths"
    column_indices  = [5, 8]
    xlim            = [0.0, 10.0]
    ylim            = [0.0, 500.0]
    plotData(input_file, output_file, plot_dir, title, column_indices, xlim, ylim, drawMean)

def main():
    makePlots()

if __name__ == "__main__":
    main()

