# makePlots.py

import numpy as np
import matplotlib.pyplot as plt
import tools

# create plot from intput data file
def plotData(input_file, output_file, plot_dir, title, x_column_index, y_column_index, ylim, drawMean, drawFit):
    verbose = False
    tools.makeDir(plot_dir)
    data = tools.getData(input_file)
    output_png = "{0}/{1}.png".format(plot_dir, output_file)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)

    # get default colors
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors     = prop_cycle.by_key()['color']

    # get data from column
    x_label = ""
    y_label = ""
    x_vals  = []
    y_vals  = []

    # loop over data
    for i, row in enumerate(data):
        # first row has labels
        if i == 0:
            x_label = row[x_column_index]
            y_label = row[y_column_index]
        # second row is the beginning of data values
        else:
            # WARNING: make sure to convert strings to floats!
            x = float(row[x_column_index])
            y = float(row[y_column_index])
            x_vals.append(x)
            y_vals.append(y)
        
        if verbose:
            print("{0}: {1}".format(i, row[y_column_index]))
    
    # plot
    fig, ax = plt.subplots(figsize=(6, 6))

    x_array = np.array(x_vals)
    y_array = np.array(y_vals)
    y_mean  = np.mean(y_array)
    y_std   = np.std(y_array)
    # extend x to define xlim and plot mean and std dev
    step = x_array[1] - x_array[0] 
    x_extended = np.insert(x_array, 0, float(x_array[0]  - step) )
    x_extended = np.append(x_extended, float(x_array[-1] + step) )
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
    ax.set_title(title,      fontsize=16)
    ax.set_xlabel(x_label,   fontsize=12)
    ax.set_ylabel(y_label,   fontsize=12)
    
    p1 = plt.scatter(x_array, y_array, color=colors[0], label="data")
    objects = [p1]

    # draw mean and std dev on plot
    if drawMean:
        p2 = plt.axline((x_extended[0], y_mean), (x_extended[-1], y_mean), color=colors[0], linestyle="--", label="mean")
        p3 = plt.fill_between(x_extended, y_mean - y_std, y_mean + y_std, color=colors[0], alpha=0.2, label="std dev")
        objects = [p1, p2, p3]
        # text
        text_x = xlim[0] + 0.1 * (xlim[1] - xlim[0])
        text_y = ylim[0] + 0.9 * (ylim[1] - ylim[0])
        equation = r"$\mu = {0:.2f} \pm {1:.2f}$".format(y_mean, y_std)
        ax.text(text_x, text_y, equation, fontsize=15)
    
    # draw fit on plot
    if drawFit:
        model = np.polyfit(x_array, y_array, 1)
        predict = np.poly1d(model)
        #print(predict)
        p4 = plt.plot(x_array, predict(x_array), label='fit', color='red', linestyle='dashed')
        #objects = [p1, p4]
        # text
        text_x = xlim[0] + 0.1 * (xlim[1] - xlim[0])
        text_y = ylim[0] + 0.9 * (ylim[1] - ylim[0])
        f_x = "{0}".format(predict)
        # remove whitespace and newlines
        f_x = f_x.strip()
        equation = r"y = {0}".format(f_x)
        ax.text(text_x, text_y, equation, fontsize=15)

    # specify order for legend
    labels = [o.get_label() for o in objects]
    
    plt.legend(objects, labels, loc='upper right', prop={'size': 12})
    plt.savefig(output_png)
    plt.savefig(output_pdf)

# primary make plots function
# plot data for one cable
def makePlots(cable_number, input_file, plot_dir):
    drawMean        = True
    drawFit         = False
    
    # Heights
    output_file     = "Cable_{0}_EyeDiagram_Heights".format(cable_number)
    title           = "Cable {0} Eye Diagram Heights".format(cable_number)
    x_column_index  = 0
    y_column_index  = 3
    ylim            = [0.0, 400.0]
    plotData(input_file, output_file, plot_dir, title, x_column_index, y_column_index, ylim, drawMean, drawFit)
    
    # Jitters
    output_file     = "Cable_{0}_EyeDiagram_Jitters".format(cable_number)
    title           = "Cable {0} Eye Diagram Jitters".format(cable_number)
    x_column_index  = 0
    y_column_index  = 4
    ylim            = [0.0, 400.0]
    plotData(input_file, output_file, plot_dir, title, x_column_index, y_column_index, ylim, drawMean, drawFit)
    
    # Widths
    output_file     = "Cable_{0}_EyeDiagram_Widths".format(cable_number)
    title           = "Cable {0} Eye Diagram Widths".format(cable_number)
    x_column_index  = 0
    y_column_index  = 5
    ylim            = [0.0, 600.0]
    plotData(input_file, output_file, plot_dir, title, x_column_index, y_column_index, ylim, drawMean, drawFit)

# plot data from scan
def makePlotsScan(input_file, plot_dir):
    drawMean        = False
    drawFit         = True

    # Heights
    output_file     = "EyeDiagram_Heights"
    title           = "Eye Diagram Heights"
    x_column_index  = 1
    y_column_index  = 2
    ylim            = [0.0, 800.0]
    plotData(input_file, output_file, plot_dir, title, x_column_index, y_column_index, ylim, drawMean, drawFit)
    
    # Jitters
    output_file     = "EyeDiagram_Jitters"
    title           = "Eye Diagram Jitters"
    x_column_index  = 1
    y_column_index  = 3
    ylim            = [0.0, 400.0]
    plotData(input_file, output_file, plot_dir, title, x_column_index, y_column_index, ylim, drawMean, drawFit)
    
    # Widths
    output_file     = "EyeDiagram_Widths"
    title           = "Eye Diagram Widths"
    x_column_index  = 1
    y_column_index  = 4
    ylim            = [0.0, 800.0]
    plotData(input_file, output_file, plot_dir, title, x_column_index, y_column_index, ylim, drawMean, drawFit)

def main():
    # testing
    
    cable_number    = 158
    input_file      = "tables/Cable_{0}_EyeDiagrams_beforeLashing.csv".format(cable_number)
    plot_dir        = "plots/Cable_{0}_beforeLashing".format(cable_number)
    makePlots(cable_number, input_file, plot_dir)
    
    cable_number    = 120
    input_file      = "tables/Cable_{0}_EyeDiagrams_beforeLashing.csv".format(cable_number)
    plot_dir        = "plots/Cable_{0}_beforeLashing".format(cable_number)
    makePlots(cable_number, input_file, plot_dir)
    
    cable_number    = 120
    input_file      = "tables/Cable_{0}_EyeDiagrams_afterLashing.csv".format(cable_number)
    plot_dir        = "plots/Cable_{0}_afterLashing".format(cable_number)
    makePlots(cable_number, input_file, plot_dir)

    input_file      = "tables/TAP0_Scan_2021_11_11.csv"
    plot_dir        = "plots/TAP0_Scan_2021_11_11"
    makePlotsScan(input_file, plot_dir)
    
    input_file      = "tables/RD53A_EyeDiagram_TAP0_Scan_2021_11_11.csv"
    plot_dir        = "plots/RD53A_EyeDiagram_TAP0_Scan_2021_11_11"
    makePlotsScan(input_file, plot_dir)
    
    input_file      = "tables/RD53B_EyeDiagram_TAP0_Scan_2022_08_26.csv"
    plot_dir        = "plots/RD53B_EyeDiagram_TAP0_Scan_2022_08_26"
    makePlotsScan(input_file, plot_dir)

if __name__ == "__main__":
    main()

