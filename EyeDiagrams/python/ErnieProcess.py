# ErnieProcess.py

import os
import csv
import tools

channels = ["A", "B", "C", "D"]
amplitudes = [269.0, 741.0, 1119.0]
separations = [0, 1, 2]

file_names = [
    "Scan{0}_primary_741mV_secondary_269mV.csv",
    "Scan{0}_all_ch_741mV.csv",
    "Scan{0}_primary_741mV_secondary_1119mV.csv",
    "Scan{0}_all_ch_269mV.csv",
    "Scan{0}_all_ch_1119mV.csv",
]

# get open area stored from csv file
def getArea(input_file):
    data = tools.getData(input_file)
    area = int(data[6][1])
    return area

# collect all data for a cable into one csv file
def process(cable_number, input_dir, output_dir, output_file):
    print("Processing Cable {0}".format(cable_number))
    tools.makeDir(output_dir)
    out = "{0}/{1}".format(output_dir, output_file)
    output_column_titles = ["Cable Number",
                            "Separation (mm)",
                            "Primary Link (Channel)",
                            "Primary 741 mV, Secondary 269mV",
                            "Primary 741 mV, Secondary 741mV",
                            "Primary 741 mV, Secondary 1119mV",
                            "All 269mV",
                            "All 1119mV",
    ]

    # write to output file
    with open(out, 'w', newline='') as output_csv:
        output_writer = csv.writer(output_csv)
        output_writer.writerow(output_column_titles)
        for separation in separations:
            for channel in channels:
                # one row of output csv file
                output_row = [cable_number, separation, channel]
                data_dir = "{0}/{1}mm_spacing/Link_{2}".format(input_dir, separation, channel)
                for name in file_names:
                    f = name.format(channel)
                    input_file = "{0}/{1}".format(data_dir, f)
                    # check that file exists
                    if not os.path.exists(input_file):
                        print("ERROR: Required input file does not exist: {0}".format(input_file))
                        return
                    area = getArea(input_file)
                    output_row.append(area)
                output_writer.writerow(output_row)

def main():
    cable_number = 207
    input_dir   = "data/Ernie/cable207_2021_11_04"
    output_dir  = "data/Ernie/cable207_2021_11_04/tables"
    output_file = "output.csv"
    process(cable_number, input_dir, output_dir, output_file)

if __name__ == "__main__":
    main()

