# Ernie.py

import numpy as np
import tools

def readData(input_file):
    channels = ["A", "B", "C", "D"]
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
    datasets = ["dataset_1", "dataset_2"]
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

def makePlots(input_file):
    data_map = readData(input_file)
    for cable_number in data_map:
        for separation in data_map[cable_number]:
            print(cable_number, separation)
            stats_map = getStats(data_map, cable_number, separation)
            print(stats_map)

def main():
    input_file = "data/Ernie/ErnieMeasurements-2021-10-29.csv"
    makePlots(input_file)

if __name__ == "__main__":
    main()

