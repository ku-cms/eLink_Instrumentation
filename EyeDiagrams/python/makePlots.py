# makePlots.py

import numpy as np
import matplotlib.pyplot as plt
import tools

# create plot from intput data file
def plotData(input_file, output_file, plot_dir, title, column_index, ylim, drawMean):
    verbose = False
    tools.makeDir(plot_dir)
    data = tools.getData(input_file)
    output_png = "{0}/{1}.png".format(plot_dir, output_file)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)

    # get default colors
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors     = prop_cycle.by_key()['color']

    # get data from column
    data_label = ""
    x_vals     = []
    y_vals     = []

    # loop over data
    for i, row in enumerate(data):
        # first row has labels
        if i == 0:
            data_label = row[column_index]
        # second row is the beginning of data values
        else:
            # WARNING: make sure to convert strings to floats!
            x = float(i)
            y = float(row[column_index])
            x_vals.append(x)
            y_vals.append(y)
        
        if verbose:
            print("{0}: {1}".format(i, row[column_index]))
    
    # plot
    fig, ax = plt.subplots(figsize=(6, 6))

    x_array = np.array(x_vals)
    y_array = np.array(y_vals)
    y_mean  = np.mean(y_array)
    y_std   = np.std(y_array)
    # extend x to define xlim and plot mean and std dev
    x_extended = np.insert(x_array, 0, float(x_array[0]  - 1) )
    x_extended = np.append(x_extended, float(x_array[-1] + 1) )
    xlim = [x_extended[0], x_extended[-1]]
    
    if verbose:
        print("x = {0}".format(x_array))
        print("x_extended = {0}".format(x_extended))
        print("xlim = {0}".format(xlim))
        print("y = {0}".format(y_array))
        print("y_mean = {0}".format(y_mean))
        print("y_std  = {0}".format(y_std))
    
    # format plot
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_title(title,         fontsize=16)
    ax.set_xlabel("Channel",    fontsize=12)
    ax.set_ylabel(data_label,   fontsize=12)
    
    p1 = plt.scatter(x_array, y_array, color=colors[0], label="data")
    objects = [p1]

    # draw mean and std dev on plot
    if drawMean:
        p2 = plt.axline((x_extended[0], y_mean), (x_extended[-1], y_mean), color=colors[0], linestyle="--", label="mean")
        p3 = plt.fill_between(x_extended, y_mean - y_std, y_mean + y_std, color=colors[0], alpha=0.2, label="std dev")
        objects = [p1, p2, p3]
    
    # specify order for legend
    labels = [o.get_label() for o in objects]
    
    plt.legend(objects, labels, loc='upper right', prop={'size': 12})
    plt.savefig(output_png)
    plt.savefig(output_pdf)

# primary make plots function
def makePlots(cable_number, input_file, plot_dir):
    drawMean        = True
    
    # Heights
    output_file     = "Cable_{0}_EyeDiagram_Heights".format(cable_number)
    title           = "Cable {0} Eye Diagram Heights".format(cable_number)
    column_index    = 3
    ylim            = [0.0, 200.0]
    plotData(input_file, output_file, plot_dir, title, column_index, ylim, drawMean)
    
    # Jitters
    output_file     = "Cable_{0}_EyeDiagram_Jitters".format(cable_number)
    title           = "Cable {0} Eye Diagram Jitters".format(cable_number)
    column_index    = 4
    ylim            = [0.0, 500.0]
    plotData(input_file, output_file, plot_dir, title, column_index, ylim, drawMean)
    
    # Widths
    output_file     = "Cable_{0}_EyeDiagram_Widths".format(cable_number)
    title           = "Cable {0} Eye Diagram Widths".format(cable_number)
    column_index    = 5
    ylim            = [0.0, 500.0]
    plotData(input_file, output_file, plot_dir, title, column_index, ylim, drawMean)

def main():
    # testing
    
    #cable_number    = 158
    #input_file      = "tables/Cable_158_EyeDiagrams_beforeLashing.csv"
    #plot_dir        = "plots/Cable_{0}_beforeLashing".format(cable_number)
    
    cable_number    = 121
    input_file      = "tables/Cable_121_EyeDiagrams.csv"
    plot_dir        = "plots/Cable_{0}".format(cable_number)
    
    makePlots(cable_number, input_file, plot_dir)

if __name__ == "__main__":
    main()

