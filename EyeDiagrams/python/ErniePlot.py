# Ernie.py

import numpy as np
import matplotlib.pyplot as plt
import tools

datasets = ["dataset_1", "dataset_2"]
channels = ["A", "B", "C", "D"]
amplitudes = [269.0, 741.0, 1119.0]
separations = [0, 1, 2]

x_axis_labels = {}
x_axis_labels["dataset_1"] = "Aggressor amplitude (mV)"
x_axis_labels["dataset_2"] = "All channel amplitude (mV)"

colors = [
            "xkcd:cherry red",
            "xkcd:apple green",
            "xkcd:bright blue",
            "xkcd:tangerine",
            "xkcd:electric purple",
            "xkcd:aqua blue",
            "xkcd:grass green",
            "xkcd:lilac",
            "xkcd:coral",
            "xkcd:fuchsia"
]

def readData(input_file):
    result = {} 
    data = tools.getData(input_file)
    for i, row in enumerate(data):
        # skip empty rows
        if row[0]:
            # skip first row of labels
            if i > 0:
                cable_number = int(row[0])
                separation   = int(row[1])
                channel      = row[2]
                values = []
                # skip rows that are not channel data
                if channel in channels:
                    for j in range(3, len(row)):
                        values.append(int(row[j]))
                    dataset_1 = values[:3]
                    dataset_2 = [values[3], values[1], values[4]]
                    #print(row)
                    #print(values)
                    #print(dataset_1)
                    #print(dataset_2)
                    if cable_number not in result:
                        result[cable_number] = {}
                    if separation not in result[cable_number]:
                        result[cable_number][separation] = {}
                    if channel not in result[cable_number][separation]:
                        result[cable_number][separation][channel] = {}
                    result[cable_number][separation][channel]["dataset_1"] = dataset_1
                    result[cable_number][separation][channel]["dataset_2"] = dataset_2
    return result

def getStats(data_map, cable_number, separation):
    result = {}
    datalength = 3
    for dataset in datasets:
        averages = []
        std_devs = []
        for i in range(datalength):
            values = []
            for channel in data_map[cable_number][separation]:
                data = data_map[cable_number][separation][channel][dataset]
                values.append(data[i])
            averages.append(np.mean(values))
            std_devs.append(np.std(values))
        result[dataset] = {}
        result[dataset]["averages"] = averages
        result[dataset]["std_devs"] = std_devs
    return result

def plot(input_values, ordered_keys, limits, title, labels, label_format, output_name, doRatio):
    fig, ax = plt.subplots(figsize=(6, 6))
    for i, key in enumerate(ordered_keys):
        x_values = np.array(input_values[key]["x_values"]) 
        y_values = np.array(input_values[key]["y_values"])
        y_errors = np.array(input_values[key]["y_errors"])
        # for ratio, divide by central value
        if doRatio:
            scale = y_values[1]
            y_values = y_values / scale 
            y_errors = y_errors / scale 
        #print("doRatio: {0}, y_values: {1}, y_errors: {2}".format(doRatio, y_values, y_errors))
        label = label_format.format(key)
        color = colors[i]
        plt.errorbar(x_values, y_values, yerr=y_errors, fmt='o', label=label, color=color, alpha=0.5)
    
    legend_font_size = 12
    x_label = labels[0]
    y_label = labels[1]
    xlim    = limits[0]
    ylim    = limits[1]
    ax.legend(loc='upper right', prop={'size': legend_font_size})
    ax.set_title(title,     fontsize=16)
    ax.set_xlabel(x_label,  fontsize=16)
    ax.set_ylabel(y_label,  fontsize=16)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.tick_params(axis='both', which='minor', labelsize=12)
    
    output_png = "{0}.png".format(output_name)
    output_pdf = "{0}.pdf".format(output_name)
    #print(output_png)
    #print(output_pdf)
    plt.savefig(output_png, bbox_inches='tight')
    plt.savefig(output_pdf, bbox_inches='tight')
    # close to avoid memory warning 
    plt.close('all')

def makePlots(input_file, plot_dir):
    tools.makeDir(plot_dir)
    data_map = readData(input_file)
    for cable_number in data_map:
        print("Plotting Cable {0}".format(cable_number))
        cable_dir = "{0}/Cable_{1}".format(plot_dir, cable_number)
        tools.makeDir(cable_dir)
        for dataset in datasets:
            separation_input_values = {}
            for separation in separations:
                stats_map = getStats(data_map, cable_number, separation)
                separation_input_values[separation] = {}
                separation_input_values[separation]["x_values"] = amplitudes
                separation_input_values[separation]["y_values"] = stats_map[dataset]["averages"]
                separation_input_values[separation]["y_errors"] = stats_map[dataset]["std_devs"]

                channel_input_values = {}
                for channel in channels:
                    #print("{0}: {1}".format(channel,
                    #                        data_map[cable_number][separation][channel][dataset],
                    #                       )
                    #)
                    channel_input_values[channel] = {} 
                    channel_input_values[channel]["x_values"] = amplitudes
                    channel_input_values[channel]["y_values"] = data_map[cable_number][separation][channel][dataset]
                    channel_input_values[channel]["y_errors"] = np.zeros(len(amplitudes))
                
                # Vary channels
                # No error bars
                title        = "Cable {0} Areas ({1}mm spacing)".format(cable_number, separation)
                x_label      = x_axis_labels[dataset]
                y_label      = "Area"
                labels       = [x_label, y_label]
                label_format = "Link {0}" 
                xlim         = [0.0, 1.5e3]
                ylim         = [0.0, 1.0e5]
                limits       = [xlim, ylim]
                output_name  = "{0}/vary_channel_areas_{1}mm_spacing_{2}".format(cable_dir, separation, dataset)
                doRatio      = False
                plot(channel_input_values, channels, limits, title, labels, label_format, output_name, doRatio)
            
            # Vary separations
            # For each separation, plot average over channels
            # The std dev over channels is used for error bars
            title        = "Cable {0} Ave. Areas".format(cable_number)
            x_label      = x_axis_labels[dataset]
            y_label      = "Ave. Area"
            labels       = [x_label, y_label]
            label_format = "{0} mm spacing" 
            xlim         = [0.0, 1.5e3]
            ylim         = [0.0, 1.0e5]
            limits       = [xlim, ylim]
            output_name  = "{0}/vary_separation_areas_{1}".format(cable_dir, dataset)
            doRatio      = False
            plot(separation_input_values, separations, limits, title, labels, label_format, output_name, doRatio)
            
            title        = "Cable {0} Ratios of Ave. Areas".format(cable_number)
            x_label      = x_axis_labels[dataset]
            y_label      = "Ratio of Ave. Areas"
            labels       = [x_label, y_label]
            label_format = "{0} mm spacing" 
            xlim         = [0.0, 1.5e3]
            ylim         = [0.0, 2.0]
            limits       = [xlim, ylim]
            output_name  = "{0}/vary_separation_ratios_{1}".format(cable_dir, dataset)
            doRatio      = True
            plot(separation_input_values, separations, limits, title, labels, label_format, output_name, doRatio)

def main():
    input_file  = "data/Ernie/ErnieMeasurements-2021-10-29.csv"
    plot_dir    = "plots/Ernie"
    makePlots(input_file, plot_dir)

if __name__ == "__main__":
    main()

