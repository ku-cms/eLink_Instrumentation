# makeTables.py

import glob
import tools

def makeTables():
    input_file_pattern = "data/Cable_158_beforeLashing/*.csv"
    input_files = glob.glob(input_file_pattern)
    # row, column indices start from 0 for data matrix
    row_map    = {"label1" : 32, "label2" : 33, "value" : 34}
    column_map = {"height" : 13, "jitter" : 43, "width" : 53}
    for f in input_files:
        print(f)
        #tools.printData(f)
        data = tools.getData(f)
        for key in column_map:
            # remove space from strings
            # convert values to floats
            label1 = data[row_map["label1"]][column_map[key]].strip()
            label2 = data[row_map["label2"]][column_map[key]].strip()
            value  = float(data[row_map["value"]][column_map[key]])
            print(" - {0}: {1} = {2:.2E}".format(label1, label2, value))

def main():
    makeTables()

if __name__ == "__main__":
    main()


