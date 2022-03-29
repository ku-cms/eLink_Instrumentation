#!/usr/bin/python3
# Importing modules
import os

# Import other classes
import config
import shelve
from tkinter import *
from tkinter import ttk

cable = shelve.open("cable.txt")


def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)


config.cable_number_list = str(input("What is the cable number: "))
redo = int(input("Redo s2p files [1 Yes, 0 No]: "))
config.cable_number_list = config.cable_number_list.split()
if config.cable_number_list[0] == "all":
    folderFiles = os.listdir("./Data/")
    config.cable_number_list.clear()
    for i in range(len(folderFiles)):
        config.cable_number_list.append(folderFiles[i])

for config.cable_number in config.cable_number_list:
    config.cable_length = cable.get(str(config.cable_number))[0]
    config.cable_type = int(cable.get(str(config.cable_number))[1])
    # print("Number:", config.cable_number, "\nLength:", config.cable_length, "\nType:", config.cable_type)

    print("\n Detecting Files...")
    for root, dirs, files in os.walk("./Data/" + config.cable_number, topdown=False):
        config.Pre_list.clear()
        for name in files:
            if ".txt" in os.path.join(name):
                config.Pre_list.append(os.path.join(name))

    print(" Files detected")
    print(config.Pre_list)

    if len(os.path.join('Data/' + str(config.cable_number) + '/Plots/s2p')) == 0:
        execfile("createS2P.py")
    elif redo == 1:
        execfile("createS2P.py")
    elif redo == 0:
        pass

    if config.cable_length == "35":
        config.t1 = 2.00
        config.t2 = 4.00
    elif config.cable_length == "80":
        config.t1 = 2.00
        config.t2 = 6.00
    elif config.cable_length == "100":
        config.t1 = 2.00
        config.t2 = 7.00
    elif config.cable_length == "140":
        config.t1 = 2.00
        config.t2 = 9.00
    elif config.cable_length == "160":
        config.t1 = 2.00
        config.t2 = 10.00
    elif config.cable_length == "180":
        config.t1 = 2.00
        config.t2 = 11.00
    elif config.cable_length == "200":
        config.t1 = 2.00
        config.t2 = 12.00
    elif config.cable_length == "0":
        config.t1 = 0.00
        config.t2 = 1.50
    else:
        config.t1 = 0
        config.t2 = 0

    try:
        if config.cable_type == 1:
            execfile("Types/type1.py")
        elif config.cable_type == 2:
            execfile("Types/type2.py")
        elif config.cable_type == 3:
            execfile("Types/type3.py")
        elif config.cable_type == 4:
            execfile("Types/type4.py")
    except NameError:
        print("Files Not Detected!!")

cable.close()
