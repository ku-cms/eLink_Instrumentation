# VNA_s4p.py

# ------------------------------------- #
# Created by the KU CMS team.
# - Analyzes VNA data using s4p files
# - Creates plots
# - Calculates differential impedance
# - Prints impedance and saves to table (csv)
# - Uses the scikit-rf library (skrf)
# - See https://scikit-rf.readthedocs.io/en/latest/index.html
# ------------------------------------- #

# TODO:
# - Load s4p file in scikit-rf library (skrf)
# - Plot differential impedance vs. frequency
# - Plot differential impedance vs. time
# - Calculate differential impedance
# DONE:
# - Count number of lines in s4p file; check on Windows and Macbook

# Import libraries
import os
import glob

# If file exists, return number of lines in file
def countLines(input_file):
    n_lines = -999
    if os.path.isfile(input_file):
        n_lines = sum(1 for line in open(input_file))
    return n_lines

# Get list of files in a directory matching a pattern.
def getFiles(dir):
    files = glob.glob(dir+"/*.s4p")
    return files

def analyze(cable_number):
    print("Analyzing VNA data for cable {0}.".format(cable_number))
    vna_data_dir = "Data/{0}".format(cable_number)
    data_files = getFiles(vna_data_dir)
    n_files = len(data_files)
    print("Number of files: {0}".format(n_files))
    for data_file in data_files:
        n_lines = countLines(data_file)
        print("Loading file {0}: {1} lines.".format(data_file, n_lines))

# Run analysis
def run():
    # Input parameters from user
    cable_number = int(input("Enter cable number: "))

    # Analyze data for cable
    analyze(cable_number)

def main():
    run()

if __name__ == "__main__":
    main()
