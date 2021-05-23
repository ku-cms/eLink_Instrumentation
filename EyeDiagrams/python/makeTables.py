# makeTables.py

import csv
import glob
import tools

def makeTable(input_files, output_file):
    verbose = False
    # row, column indices start from 0 for data matrix
    row_map    = {"label1" : 32, "label2" : 33, "value" : 34}
    column_map = {"height" : 13, "jitter" : 43, "width" : 53}
    label_map  = {"height" : "Height (mV)", "jitter" : " Jitter (ps)", "width" : "Width (ps)"}
    unit_map   = {"height" : 10**3, "jitter" : 10**12, "width" : 10**12}
    output_column_titles = ["Index", "Module", "Channel", "Height (mV)", "Jitter (ps)", "Width (ps)"]
    with open(output_file, "w") as output_csv:
        output_writer = csv.writer(output_csv)
        output_writer.writerow(output_column_titles)
        for i, f in enumerate(input_files):
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
            output_row = [i+1, 0, 0, round(height, 3), round(jitter, 3), round(width, 3)]
            output_writer.writerow(output_row)

def makeTables():
    table_dir = "tables"
    input_file_pattern = "data/Cable_158_beforeLashing/*.csv"
    output_file = "{0}/Cable_158_EyeDiagrams_beforeLashing.csv".format(table_dir)
    tools.makeDir(table_dir)
    input_files = glob.glob(input_file_pattern)
    makeTable(input_files, output_file)

def main():
    makeTables()

if __name__ == "__main__":
    main()


