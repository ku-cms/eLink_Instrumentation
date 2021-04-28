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

def plotData(input_file, output_file, plot_dir, title, column_indices, xlim, ylim):
    verbose = False
    makeDir(plot_dir)
    data = getData(input_file)
    output_png = "{0}/{1}.png".format(plot_dir, output_file)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)

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
    
    if verbose:
        print(x_array)
        print(y1_array)
        print(y2_array)
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_title(title,         fontsize=16)
    ax.set_xlabel("Channel",    fontsize=12)
    ax.set_ylabel(data_label,   fontsize=12)
    
    plt.scatter(x_array, y1_array, label="Before Lashing")
    plt.scatter(x_array, y2_array, label="After Lashing")
    plt.legend(loc='upper right', prop={'size': 12})
    plt.savefig(output_png)
    plt.savefig(output_pdf)

def makePlots():
    input_file      = "Cable_120_EyeDiagrams.csv"
    plot_dir        = "plots"
    
    # Heights
    output_file     = "Cable_120_EyeDiagram_Heights"
    title           = "Cable 120 Eye Diagram Heights"
    column_indices  = [3, 6]
    xlim            = [0.0, 10.0]
    ylim            = [0.0, 200.0]
    plotData(input_file, output_file, plot_dir, title, column_indices, xlim, ylim)
    
    # Jitters
    output_file     = "Cable_120_EyeDiagram_Jitters"
    title           = "Cable 120 Eye Diagram Jitters"
    column_indices  = [4, 7]
    xlim            = [0.0, 10.0]
    ylim            = [0.0, 400.0]
    plotData(input_file, output_file, plot_dir, title, column_indices, xlim, ylim)
    
    # Widths
    output_file     = "Cable_120_EyeDiagram_Widths"
    title           = "Cable 120 Eye Diagram Widths"
    column_indices  = [5, 8]
    xlim            = [0.0, 10.0]
    ylim            = [0.0, 400.0]
    plotData(input_file, output_file, plot_dir, title, column_indices, xlim, ylim)

def main():
    makePlots()

if __name__ == "__main__":
    main()

