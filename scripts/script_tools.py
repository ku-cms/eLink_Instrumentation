# script_tools.py

# This is a place for utility functions (tools) for scripts.

# To use these functions in another file, add this import statement:
# import script_tools

# Then, call functions as needed, for example:
# script_tools.makeDir(dir_name)

from colorama import Fore
import os

# creates directory if it does not exist
def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# determine if a group contains and element
def group_contains_element(group, element):
    if element in group:
        return True
    else:
        return False

# print line of a specified length
def printLine(length):
    line = "-" * length
    print(line)

# get Fore for a given color
def getColorFore(color):
    result = None
    color_fore_map = {
        "BLACK"     : Fore.BLACK,
        "RED"       : Fore.RED,
        "GREEN"     : Fore.GREEN,
        "YELLOW"    : Fore.YELLOW,
        "BLUE"      : Fore.BLUE,
        "MAGENTA"   : Fore.MAGENTA,
        "CYAN"      : Fore.CYAN,
        "WHITE"     : Fore.WHITE,
        "RESET"     : Fore.RESET
    }
    result = color_fore_map[color]
    return result

# convert mm to ft
def convert_mm_to_ft(value_mm):
    value_ft = value_mm / 304.8
    return value_ft

# convert ft to mm
def convert_ft_to_mm(value_ft):
    value_mm = value_ft * 304.8
    return value_mm

# Process input wiring type to support these formats:
# inputs: 2.3, 2p3, 2P3
# output: 2.3
def formatWiringType(wiring_type):
    # - Remove leading and ending whitespace using strip().
    # - Convert to lowercase.
    # - Replace "p" with ".".
    wiring_type = wiring_type.strip()
    wiring_type = wiring_type.lower()
    wiring_type = wiring_type.replace("p", ".")
    return wiring_type

# Process input length type to support these formats:
# inputs: R1_G1, r1_g1, R1 G1, r1 g1
# output: R1_G1
def formatLengthType(length_type):
    # - Remove leading and ending whitespace using strip().
    # - Convert to uppercase.
    # - Replace " " with "_".
    length_type = length_type.strip()
    length_type = length_type.upper()
    length_type = length_type.replace(" ", "_")
    return length_type

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
