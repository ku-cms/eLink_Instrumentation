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
    makeDir(plot_dir)
    data = getData(file_name)

    # get data from column
    column_index = 3
    label  = ""
    x_vals = []
    y_vals = []

    for i, row in enumerate(data):
        # skip
        if i < 1:
            continue
        elif i == 1:
            label = row[column_index]
        else:
            # WARNING: make sure to convert strings to floats!
            x = float(i - 1)
            y = float(row[column_index])
            x_vals.append(x)
            y_vals.append(y)
        
        #print("{0}: {1}".format(i, row[column_index]))
    
    # plot
    x_array = np.array(x_vals)
    y_array = np.array(y_vals)
    #print(x_array)
    #print(y_array)
    
    plt.scatter(x_array, y_array)
    plt.show()

def main():
    file_name = "Cable_120_EyeDiagrams.csv"
    plot_dir  = "plots"
    
    #printData(file_name)
    plotData(file_name, plot_dir)

if __name__ == "__main__":
    main()


