# makeTables.py

import argparse
import os
import csv
import glob
import tools

def getFile(input_files, module, channel, requireModule):
    matching_files = []
    for f in input_files:
        if requireModule:
            if module in f and channel in f:
                matching_files.append(f)
        else:
            if channel in f:
                matching_files.append(f)
    n_matching = len(matching_files)
    if n_matching == 1:
        return matching_files[0]
    else:
        print("ERROR: For module {0} channel {1}, there are {2} matching files found (should be 1).".format(module, channel, n_matching))
        print("matching files: {0}".format(matching_files))
        return ""

def run(input_files, output_file, modules, channels, requireModule):
    verbose = False
    # row, column indices start from 0 for data matrix
    row_map    = {"label1" : 32, "label2" : 33, "value" : 34}
    column_map = {"height" : 13, "jitter" : 43, "width" : 53}
    unit_map   = {"height" : 10**3, "jitter" : 10**12, "width" : 10**12}
    output_column_titles = ["Index", "Module", "Channel", "Height (mV)", "Jitter (ps)", "Width (ps)"]
    with open(output_file, "w") as output_csv:
        output_writer = csv.writer(output_csv)
        output_writer.writerow(output_column_titles)
        index = 1
        for module in modules:
            for channel in channels:
                f = getFile(input_files, module, channel, requireModule)
                if not f:
                    print("ERROR: Unique file not found for module {0} channel {1}.".format(module, channel))
                    return
                data = tools.getData(f)
                if verbose:
                    print(f)
                    for key in column_map:
                        # remove space from strings
                        # convert values to floats
                        label1 = data[row_map["label1"]][column_map[key]].strip()
                        label2 = data[row_map["label2"]][column_map[key]].strip()
                        value  = float(data[row_map["value"]][column_map[key]])
                        print(" - {0}: {1} = {2:.2E}".format(label1, label2, value))
                height = float(data[row_map["value"]][column_map["height"]]) * unit_map["height"]
                jitter = float(data[row_map["value"]][column_map["jitter"]]) * unit_map["jitter"]
                width  = float(data[row_map["value"]][column_map["width"]] ) * unit_map["width"]
                # columns: index, module, channel, height, jitter, width
                output_row = [index, module, channel, round(height, 3), round(jitter, 3), round(width, 3)]
                output_writer.writerow(output_row)
                index += 1

def makeTable(input_dir, output_dir, output_file_name):
    output_file = "{0}/{1}".format(output_dir, output_file_name)
    input_file_pattern = "{0}/*.csv".format(input_dir)
    modules  = ["M1"]
    channels = ["CMD", "D0", "D1", "D2", "D3"]
    requireModule = False

    tools.makeDir(output_dir)
    input_files = glob.glob(input_file_pattern)
    run(input_files, output_file, modules, channels, requireModule)

def main():
    # options
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input_dir",          "-i",   default="", help="input directory containing data csv files")
    parser.add_argument("--output_dir",         "-o",   default="", help="output directory for output csv file")
    parser.add_argument("--output_file_name",   "-f",   default="", help="output csv file name")
    
    options             = parser.parse_args()
    input_dir           = options.input_dir
    output_dir          = options.output_dir
    output_file_name    = options.output_file_name
    
    # check for valid options
    if not input_dir:
        print("Provide an input directory using the -i option.")
        return
    if not output_dir:
        print("Provide an output directory using the -o option.")
        return
    if not output_file_name:
        print("Provide an output file name using the -f option.")
        return
    if not os.path.exists(input_dir):
        print("ERROR: The input directory \"{0}\" does not exist.".format(input_dir))
        return

    makeTable(input_dir, output_dir, output_file_name)

if __name__ == "__main__":
    main()

