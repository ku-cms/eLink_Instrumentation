# makeTable.py

import argparse
import os
import csv
import glob
import tools
from makePlots import makePlots

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
    verbose   = False
    precision = 3
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
                output_row = [index, module, channel, round(height, precision), round(jitter, precision), round(width, precision)]
                output_writer.writerow(output_row)
                index += 1

def makeTable(input_dir, output_dir, output_file_name, cable_type):
    output_file = "{0}/{1}".format(output_dir, output_file_name)
    input_file_pattern = "{0}/*.csv".format(input_dir)
    tools.makeDir(output_dir)
    input_files = glob.glob(input_file_pattern)
    
    cable_type_map = {
        1 : {
            "modules"       : ["M1"],
            "channels"      : ["CMD", "D0", "D1", "D2", "D3"],
            "requireModule" : False 
        },
        2 : {
            "modules"       : ["M1"],
            "channels"      : ["CMD", "D0", "D1"],
            "requireModule" : False 
        },
        3 : {
            "modules"       : ["M1", "M2"],
            "channels"      : ["CMD", "D0", "D1"],
            "requireModule" : True 
        },
        4 : {
            "modules"       : ["M1", "M2", "M3"],
            "channels"      : ["CMD", "D0", "D1"],
            "requireModule" : True 
        },
    }

    modules         = cable_type_map[cable_type]["modules"]
    channels        = cable_type_map[cable_type]["channels"]
    requireModule   = cable_type_map[cable_type]["requireModule"]

    run(input_files, output_file, modules, channels, requireModule)

def main():
    # options
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input_dir",          "-i",   default="",         help="input directory containing data (csv files)")
    parser.add_argument("--table_output_dir",   "-o",   default="tables",   help="output directory for table (csv file)")
    parser.add_argument("--plot_output_dir",    "-p",   default="",         help="output directory for plots (pdf/png files)")
    parser.add_argument("--output_file_name",   "-f",   default="",         help="output csv file name")
    parser.add_argument("--cable_number",       "-n",   default=-1,         help="cable number [n > 0]")
    parser.add_argument("--cable_type",         "-t",   default=-1,         help="cable type [1-4]")
    
    options             = parser.parse_args()
    input_dir           = options.input_dir
    table_output_dir    = options.table_output_dir
    plot_output_dir     = options.plot_output_dir
    output_file_name    = options.output_file_name
    cable_number        = int(options.cable_number)
    cable_type          = int(options.cable_type)
    
    # check for valid options
    # - cable number and type are required
    # - other options are optional; defaults are used if they are not provided
    
    if not input_dir:
        input_dir = "data/Cable_{0}".format(cable_number)
    
    if not table_output_dir:
        print("Provide a table output directory using the -o option.")
        return
    
    if not plot_output_dir:
        plot_output_dir = "plots/Cable_{0}".format(cable_number)
    
    if not output_file_name:
        output_file_name = "Cable_{0}_EyeDiagrams.csv".format(cable_number)
    
    if cable_number < 1:
        print("Provide cable number [n > 0] using the -n option.")
        return
    
    if cable_type < 1 or cable_type > 4:
        print("Provide cable type [1-4] using the -t option.")
        return
    
    if not os.path.exists(input_dir):
        print("ERROR: The input directory \"{0}\" does not exist.".format(input_dir))
        return

    # make table and plots 
    output_file = "{0}/{1}".format(table_output_dir, output_file_name)
    makeTable(input_dir, table_output_dir, output_file_name, cable_type)
    makePlots(cable_number, output_file, plot_output_dir)

if __name__ == "__main__":
    main()

