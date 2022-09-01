# makeTableScan.py

import csv
import glob
import tools

def run(input_files, output_file, settings):
    # define decimal precision for values saved in table
    precision = 3
    # maps to define columns that contain data from raw data csv files
    # row and column indices start from 0 for data matrix
    row_map    = {"label1" : 0, "label2" : 0, "value" : 1}
    column_map = {"height" : 13, "jitter" : 43, "width" : 53}
    unit_map   = {"height" : 10**3, "jitter" : 10**12, "width" : 10**12}
    output_column_titles = ["Index", "TAP0", "Height (mV)", "Jitter (ps)", "Width (ps)"]
    # write to output file
    with open(output_file, 'w', newline='') as output_csv:
        output_writer = csv.writer(output_csv)
        output_writer.writerow(output_column_titles)
        index = 1
        for tap in settings:
            f = input_files[tap]
            print("{0}: {1}, {2}".format(index, tap, f))
            data = tools.getData(f)
            # get values, convert to floats, and convert to standard units
            height = float(data[row_map["value"]][column_map["height"]]) * unit_map["height"]
            jitter = float(data[row_map["value"]][column_map["jitter"]]) * unit_map["jitter"]
            width  = float(data[row_map["value"]][column_map["width"]] ) * unit_map["width"]
            # columns for output table: index, TAP0, height, jitter, width
            output_row = [index, tap, round(height, precision), round(jitter, precision), round(width, precision)]
            output_writer.writerow(output_row)
            index += 1

def makeTableScan(input_dir, output_dir, output_file, settings):
    name = "{0}/{1}".format(output_dir, output_file)
    print("Running over {0} to create {1}".format(input_dir, name))
    input_file_pattern = "{0}/TAP0_*/*.csv".format(input_dir)
    input_files = glob.glob(input_file_pattern)
    # get dictionary mapping TAP0 setting to files
    file_dict = {}
    for tap in settings:
        tap_name = "TAP0_{0}".format(tap)
        tap_match = "/{0}/".format(tap_name)
        for f in input_files:
            if tap_match in f:
                file_dict[tap] = f
    tools.makeDir(output_dir)
    run(file_dict, name, settings)

def main():
    settings = [x for x in range(200, 1100, 100)]
    
    input_dir   = "data/2021_11_11_clean"
    output_dir  = "tables"
    output_file = "RD53A_EyeDiagram_TAP0_Scan_2021_11_11.csv"
    makeTableScan(input_dir, output_dir, output_file, settings)
    
    input_dir   = "data/RD53A_EyeDiagrams_TAP0_2022_08_31_clean"
    output_dir  = "tables"
    output_file = "RD53A_EyeDiagrams_TAP0_2022_08_31.csv"
    makeTableScan(input_dir, output_dir, output_file, settings)
    
    input_dir   = "data/RD53B_EyeDiagrams_TAP0_2022_08_26_clean"
    output_dir  = "tables"
    output_file = "RD53B_EyeDiagram_TAP0_Scan_2022_08_26.csv"
    makeTableScan(input_dir, output_dir, output_file, settings)

if __name__ == "__main__":
    main()

