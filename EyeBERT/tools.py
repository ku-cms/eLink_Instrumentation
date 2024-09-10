# tools.py

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

# print 4-point DC values
def PrintDCValues(channel, channel_p, channel_n, value_p, value_n):
    # For values greater than or equal to this cufoff,
    # print INF (consider these values as infinite resistance).
    cutoff = 1e6
    
    value_to_print_p = ""
    value_to_print_n = ""
    if value_p < cutoff:
        value_to_print_p = "{:.2f}".format(value_p)
    else:
        value_to_print_p = "INF"
    if value_n < cutoff:
        value_to_print_n = "{:.2f}".format(value_n)
    else:
        value_to_print_n = "INF"
    
    # print results
    print(" - channel {0:6}: {1:8} = {2:4}, {3:8} = {4:4}".format(channel, channel_p, value_to_print_p, channel_n, value_to_print_n))

# get bad 4-point DC channels
def GetBadDCChannels(measurement_data):
    # resistance threshold for bad channels
    cutoff = 10.0
    bad_channels = {}
    for key in measurement_data:
        value = measurement_data[key]
        if value >= cutoff:
            bad_channels[key] = value
    return bad_channels

# print bad 4-point DC channels and possible causes
def PrintBadDCChannels(bad_channels):
    if bad_channels:
        # print bad 4-point DC channels
        print(Fore.RED + "Warning: The following channels have large 4-point DC resistance (ohms):" + Fore.GREEN)
        for key in bad_channels:
            value = bad_channels[key]
            print(f" - {key:8}: {value}")
        # print possible causes
        print(Fore.RED + "Possible causes:" + Fore.GREEN)
        print(" - The e-link is not connected properly: check continuity using a multimeter!")
        print(" - The SMA cable mapping (connections to the relay board) is not correct for this type of e-link.")
        print(" - There is a break or discontinuity for these channels somewhere in the readout chain: the e-link, the adapter boards, or the SMA cables.")
        print(" - There is a software or firmware bug causing the problem... for example, incorrect mapping.")
        print(" - There is some new and unknown problem...")
        print("Good luck debugging! Be systematic and eliminate one possible cause at a time.")
        print(Fore.RED + "Troubleshooting tips:" + Fore.GREEN)
        print(" - Be systematic.")
        print(" - Only change one variable at at time.")
        print(" - Eliminate one possible cause at at time.")
        print(" - Try to think of additional possible causes.")
        print(" - Ask an expert for help.")
        print(Fore.RED + "Good luck!" + Fore.GREEN)

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
