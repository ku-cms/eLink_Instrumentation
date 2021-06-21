# tools.py

import csv
import os
import numpy as np

# general error code
ERROR_CODE = -999

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

