# plotComparison.py

import csv
import os
import numpy as np
import matplotlib.pyplot as plt

def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def printData(file_name):
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        print(" --- print file")
        for line in f:
            print(line, end='')
        # return to start of file
        f.seek(0)
        print(" --- print csv")
        for row in reader:
            print(row)

def getData(file_name):
    data = []
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data

def plotData(file_name, plot_dir):
    verbose = False
    makeDir(plot_dir)
    data = getData(file_name)

    # get data from column
    column_index_1 = 3
    column_index_2 = 6
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
    
    ax.set_xlim([0.0, 10.0])
    ax.set_ylim([0.0, 200.0])
    ax.set_title("Cable 120 Eye Diagram Data",  fontsize=16)
    ax.set_xlabel("Channel",                    fontsize=12)
    ax.set_ylabel(data_label,                   fontsize=12)
    plt.scatter(x_array, y1_array, label="Before Lashing")
    plt.scatter(x_array, y2_array, label="After Lashing")
    plt.legend(loc='upper right', prop={'size': 12})
    plt.show()

def main():
    file_name = "Cable_120_EyeDiagrams.csv"
    plot_dir  = "plots"
    
    #printData(file_name)
    plotData(file_name, plot_dir)

if __name__ == "__main__":
    main()


