# makeTables.py

import glob
import tools

def makeTables():
    input_file_pattern = "data/Cable_158_beforeLashing/*.csv"
    input_files = glob.glob(input_file_pattern)
    for f in input_files:
        print(f)
        tools.printData(f)

def main():
    makeTables()

if __name__ == "__main__":
    main()


