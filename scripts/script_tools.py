# script_tools.py

# This is a place for utility functions (tools).

# To use these functions in another file, add this import statement:
# import tools

# Then, call functions as needed, for example:
# tools.makeDir(dir_name)

import os
from colorama import Fore, Back, Style, init

# creates directory if it does not exist
def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# get adapter board channel
def getAdapterBoardChannel(cable_type, channel):
    channel_map = {
                "cmd" : "cmd", 
                "d2" : "d1",
                "d1" : "d2",
                "d0" : "d3"
    }
    if cable_type == "2p3" or cable_type == "1p3":
        return channel_map[channel]
    else:
        return channel 

# determine if cable type is valid
def is_valid_cable_type(cable_types, cable_type):
    if cable_type in cable_types:
        return True
    else:
        return False
    
# determine if branch is valid
def is_valid_branch(branches, branch):
    if branch in branches:
        return True
    else:
        return False
