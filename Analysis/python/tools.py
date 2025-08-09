# tools.py

import csv
import os
import sys
import shutil
import datetime
import math
import numpy as np
import pandas as pd

# general error code
ERROR_CODE = -999

# creates directory if it does not exist
def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# move file if it exists; if not, print error and exit
def moveFile(source_file, destination_file):
    print("Moving file...")
    print(f" - source file: {source_file}")
    print(f" - destination file: {destination_file}")
    try:
        shutil.move(source_file, destination_file)
    except FileNotFoundError:
        print(f"ERROR: Cannot move the file '{source_file}' as it was not found.")
        sys.exit(1)

# append slash to path if path does not end in slash
def appendSlash(path):
    slash = "/"
    if path[-1] != slash:
        path += slash
    return path

# get today's date
def getTodayDate(date_format="%Y-%m-%d"):
    today_date_object = datetime.datetime.today()
    today_date = today_date_object.strftime(date_format)
    return today_date

# add date to file name
def addDateToFileName(original_file_name):
    print("Adding date to file name...")

    today_date = getTodayDate()
    today_date = today_date.replace("-", "_")
    file_base, file_extension = os.path.splitext(original_file_name)
    new_file_name = f"{file_base}_{today_date}{file_extension}"
    
    print(f" - today's date: {today_date}")
    print(f" - original file name: {original_file_name}")
    print(f" - new file name: {new_file_name}")
    
    return new_file_name

# export Excel sheet to CSV
def exportExcelSheetToCSV(excel_file, excel_sheet):
    print("Exporting Excel sheet to CSV...")
    print(f" - Excel file: {excel_file}")
    print(f" - Excel sheet: {excel_sheet}")
    try:
        df = pd.read_excel(excel_file, sheet_name=excel_sheet)
        base, extension = os.path.splitext(excel_file)
        csv_file = base + '.csv'
        df.to_csv(csv_file, index=False)
    except Exception as e:
        print(f"ERROR: {e}")

# check if string can be converted to int
def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

# check if string can be converted to float
def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# convert values to floats
def convertToFloats(values):
    result = [float(value) for value in values]
    return result

# check that all values are valid
def validValues(values):
    for value in values:
        # require that values are floats
        if is_float(value): 
            # require that values are not inf
            if math.isinf(float(value)):
                return False
            # require that values are not nan
            if math.isnan(float(value)):
                return False
        else: 
            return False
    return True

# get keys common to two dictionaries
def getMatchingKeys(dict_1, dict_2):
    keys = []
    for key in dict_1:
        if key in dict_2:
            keys.append(key)
    keys.sort()
    return keys

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
    
    if not os.path.exists(input_file):
        print(f"ERROR in getData(): The input file '{input_file}' does not exist.")
        return data
    
    with open(input_file, newline='', encoding='latin1') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    return data

# input: data (matrix), x and y column indices; output: lists of x and y values
def getXYData(data, x_column_index, y_column_index, verbose):
    x_vals  = []
    y_vals  = []
    # get x, y, and data label
    for i, row in enumerate(data):
        # second row is the beginning of data values
        if i > 0:
            # WARNING: make sure to convert strings to floats!
            x = float(row[x_column_index])
            y = float(row[y_column_index])
            x_vals.append(x)
            y_vals.append(y)
        if verbose:
            print("{0}: {1}".format(i, row[y_column_index]))
    return x_vals, y_vals

def getAdditionError(dx, dy):
    # q  = x + y
    # q  = x - y
    # dq = sqrt( dx^2 + dy^2 )
    return np.sqrt( dx**2 + dy**2 )

def getAdditionErrorList(dx_list):
    # q  = x + y + ...
    # q  = x - y - ...
    # dq = sqrt( dx^2 + dy^2 + ... )
    dx2_list = [dx**2 for dx in dx_list]
    return np.sqrt(sum(dx2_list))

def getConstantMultiplicationError(a, dx):
    # a is a constant
    # q  = a * x
    # dq = |a| * dx
    return abs(a) * dx

def getMultiplicationError(q, x, dx, y, dy):
    # q = x * y 
    # q = x / y 
    # dq = abs(q) * sqrt( (dx/x)^2 + (dy/y)^2 )
    verbose = True
    if x == 0.0 or y == 0.0:
        if verbose:
            print("ERROR in getMultiplicationError(): Cannot divide by zero.")
        return ERROR_CODE
    return abs(q) * np.sqrt( (dx/x)**2 + (dy/y)**2 )

def getMultiplicationErrorList(q, x_list, dx_list):
    # q = x * y * ...
    # q = x / y / ...
    # dq = abs(q) * sqrt( (dx/x)^2 + (dy/y)^2 + ... )
    verbose = True
    if len(x_list) != len(dx_list):
        if verbose:
            print("ERROR in getMultiplicationErrorList(): x_list and dx_list do not have the same length.")
        return ERROR_CODE
    s = 0.0
    for i in xrange(len(x_list)):
        if x_list[i] == 0.0:
            if verbose:
                print("ERROR in getMultiplicationErrorList(): Cannot divide by zero.")
            return ERROR_CODE
        s += (dx_list[i] / x_list[i]) ** 2
    return abs(q) * np.sqrt(s)

