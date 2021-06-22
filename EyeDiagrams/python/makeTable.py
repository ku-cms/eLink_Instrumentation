# makeTable.py

import csv
import glob
import tools

# get file for specific module and channel from list of files
def getFile(input_files, module, channel, requireModule):
    matching_files = []
    for f in input_files:
        # require module and channel
        if requireModule:
            if module in f and channel in f:
                matching_files.append(f)
        # require channel only
        else:
            if channel in f:
                matching_files.append(f)

    # number of matching files
    n_matching = len(matching_files)

    # return matching file
    if n_matching == 1:
        return matching_files[0]
    # if not exactly 1 match, print error
    else:
        print("ERROR: For module {0} channel {1}, there are {2} matching files found (should be 1).".format(module, channel, n_matching))
        print("matching files: {0}".format(matching_files))
        return ""

# create table using intput files
def run(input_files, output_file, modules, channels, requireModule):
    verbose   = False
    # define decimal precision for values saved in table
    precision = 3
    # maps to define columns that contain data from raw data csv files
    # row and column indices start from 0 for data matrix
    
    # raw data
    #row_map    = {"label1" : 32, "label2" : 33, "value" : 34}
    #column_map = {"height" : 13, "jitter" : 43, "width" : 53}
    # clean data
    row_map    = {"label1" : 0, "label2" : 0, "value" : 1}
    column_map = {"height" : 13, "jitter" : 43, "width" : 53}
    
    unit_map   = {"height" : 10**3, "jitter" : 10**12, "width" : 10**12}
    output_column_titles = ["Index", "Module", "Channel", "Height (mV)", "Jitter (ps)", "Width (ps)"]
    # write to output file
    with open(output_file, 'w', newline='') as output_csv:
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
                # get values, convert to floats, and convert to standard units
                height = float(data[row_map["value"]][column_map["height"]]) * unit_map["height"]
                jitter = float(data[row_map["value"]][column_map["jitter"]]) * unit_map["jitter"]
                width  = float(data[row_map["value"]][column_map["width"]] ) * unit_map["width"]
                # columns for output table: index, module, channel, height, jitter, width
                output_row = [index, module, channel, round(height, precision), round(jitter, precision), round(width, precision)]
                output_writer.writerow(output_row)
                index += 1

# primary make table function
def makeTable(input_dir, output_dir, output_file_name, cable_type):
    # setup input and output
    output_file = "{0}/{1}".format(output_dir, output_file_name)
    input_file_pattern = "{0}/*.csv".format(input_dir)
    tools.makeDir(output_dir)
    input_files = glob.glob(input_file_pattern)

    # map to define modules and channels for each cable type
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

    # get values from map
    modules         = cable_type_map[cable_type]["modules"]
    channels        = cable_type_map[cable_type]["channels"]
    requireModule   = cable_type_map[cable_type]["requireModule"]

    # create table
    run(input_files, output_file, modules, channels, requireModule)

def main():
    # testing
    input_dir           = "data/Cable_121"
    table_output_dir    = "tables"
    output_file_name    = "Cable_121_EyeDiagrams.csv"
    cable_type          = 4
    makeTable(input_dir, table_output_dir, output_file_name, cable_type)

if __name__ == "__main__":
    main()
