# processData.py

import argparse
import os
from makePlots import makePlots
from makeTable import makeTable

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

    # Check for valid options:
    # - cable number and cable type are required
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

    # Make table and plots
    output_file = "{0}/{1}".format(table_output_dir, output_file_name)
    makeTable(input_dir, table_output_dir, output_file_name, cable_type)
    makePlots(cable_number, output_file, plot_output_dir)

if __name__ == "__main__":
    main()
