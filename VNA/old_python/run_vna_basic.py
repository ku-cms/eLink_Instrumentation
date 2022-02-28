import argparse
import glob
import os
from readVNADataSKRF import plot

# inputs:
# - data directory
# - plot directory

# outputs:
# - basic VNA plots

def main():
    # options
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--data_dir",  "-d",   default="", help="directory for input data files")
    parser.add_argument("--plot_dir",  "-p",   default="", help="directory for output plot files")
    options     = parser.parse_args()
    data_dir    = options.data_dir
    plot_dir    = options.plot_dir
    
    if not os.path.exists(data_dir):
        print("The directory \"{0}\" does not exist.".format(data_dir))
        print("Provide an input data directory using the -d option.")
        return

    if not plot_dir:
        print("Provide an output plot directory using the -p option.")
        return
    
    input_file_pattern = "{0}/*.vna.txt".format(data_dir)
    # get files with only file name (not full path)
    # https://stackoverflow.com/questions/7336096/python-glob-without-the-whole-path-only-the-filename
    input_files = [os.path.basename(f) for f in glob.glob(input_file_pattern)]
    # remove .txt from file names
    # https://stackoverflow.com/questions/678236/how-to-get-the-filename-without-the-extension-from-a-path-in-python
    input_files = [os.path.splitext(f)[0] for f in input_files]
    print(data_dir)
    for data_file in input_files:
        print(" - {0}".format(data_file))
        plot(data_file, data_dir, plot_dir)

if __name__ == "__main__":
    main()

