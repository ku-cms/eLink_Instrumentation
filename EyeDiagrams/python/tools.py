# tools.py

import csv
import os

# creates directory if it does not exist
def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# prints csv file
def printData(input_file):
    with open(input_file, "r") as f:
        reader = csv.reader(f)
        print(" --- print file")
        for line in f:
            print(line, end='')
        # return to start of file
        f.seek(0)
        print(" --- print csv")
        for row in reader:
            print(row)

# takes a csv file as input and outputs data in a matrix
def getData(input_file):
    data = []
    with open(input_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data

