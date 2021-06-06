import argparse
import json
import os
from readVNADataSKRF import plot

def main():
    # options
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--json_file",  "-j",   default="", help="json file listing data files")
    options     = parser.parse_args()
    json_file   = options.json_file
    
    if not os.path.exists(json_file):
        print("The json file \"{0}\" does not exist.".format(json_file))
        print("Provide a json file using the -j option.")
        return

    with open(json_file, "r") as input_file:
        print(json_file)
        dataMap = json.load(input_file)
        for key in dataMap:
            print(" - {0}".format(key))
            data_file = dataMap[key]["data_file"]
            data_dir  = dataMap[key]["data_dir"]
            plot_dir  = dataMap[key]["plot_dir"]
            plot(data_file, data_dir, plot_dir)

if __name__ == "__main__":
    main()
