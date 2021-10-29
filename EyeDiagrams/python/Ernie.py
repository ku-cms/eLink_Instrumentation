# Ernie.py

import tools

def readData(input_file):
    channels = ["A", "B", "C", "D"]
    result = {} 
    data = tools.getData(input_file)
    for i, row in enumerate(data):
        if row[0]:
            if i > 0:
                cable_number = int(row[0])
                separation   = int(row[1])
                channel      = row[2]
                values = []
                if channel in channels:
                    for j in range(3, len(row)):
                        values.append(int(row[j]))
                    dataset_1 = values[:3]
                    dataset_2 = [values[3], values[1], values[4]]
                    print(row)
                    print(values)
                    print(dataset_1)
                    print(dataset_2)

def makePlots(input_file):
    data = readData(input_file)

def main():
    input_file = "data/Ernie/ErnieMeasurements-2021-10-29.csv"
    makePlots(input_file)

if __name__ == "__main__":
    main()

