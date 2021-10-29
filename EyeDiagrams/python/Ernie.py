# Ernie.py

import numpy as np
import matplotlib.pyplot as plt
import tools

datasets = ["dataset_1", "dataset_2"]
channels = ["A", "B", "C", "D"]
amplitudes = [269.0, 741.0, 1119.0]
separations = [0, 1, 2]
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

def plot(input_values, title, labels, output_name):
    fig, ax = plt.subplots(figsize=(6, 6))
    for i, separation in enumerate(separations):
        x_values = input_values[separation]["x_values"]
        y_values = input_values[separation]["y_values"]
        y_errors = input_values[separation]["y_errors"]
        label = "{0} mm spacing".format(separation)
        color = colors[i]
        plt.errorbar(x_values, y_values, yerr=y_errors, fmt='o', label=label, color=color, alpha=0.5)
    output_png = "{0}.png".format(output_name)
    output_pdf = "{0}.pdf".format(output_name)
    print(output_png)
    print(output_pdf)
    plt.savefig(output_png, bbox_inches='tight')
    plt.savefig(output_pdf, bbox_inches='tight')
    # close to avoid memory warning 
    plt.close('all')

def makePlots(input_file, plot_dir):
    tools.makeDir(plot_dir)
    data_map = readData(input_file)
    for cable_number in data_map:
        cable_dir = "{0}/Cable_{1}".format(plot_dir, cable_number)
        tools.makeDir(cable_dir)
        for dataset in datasets:
            input_values = {}
            for separation in separations:
                input_values[separation] = {}
                stats_map = getStats(data_map, cable_number, separation)
                input_values[separation]["x_values"] = amplitudes
                input_values[separation]["y_values"] = stats_map[dataset]["averages"]
                input_values[separation]["y_errors"] = stats_map[dataset]["std_devs"]
                print(cable_number, separation)
            title = "title"
            labels = ["x", "y"]
            output_name = "{0}/ratios_{1}".format(cable_dir, dataset)
            plot(input_values, title, labels, output_name)

def main():
    input_file  = "data/Ernie/ErnieMeasurements-2021-10-29.csv"
    plot_dir    = "plots/Ernie"
    makePlots(input_file, plot_dir)

if __name__ == "__main__":
    main()

