# wire_length.py
#
# Developed by the KU CMS group.
#
# ---------------------- #
# Wire Length Calculator
# Author: Caleb Smith
# ---------------------- #
#
# Computes the total wire length for 1 e-link and n e-links based on user input.
# Also computes updated wire log.
#
# The user must input the following information:
# - e-link wiring type
# - e-link length type
# - loss per twisted pair (mm)
# - number of e-links
# - previous wire log (ft)
#
# TODO:
# - Create LengthCalculator or WireLengthCalculator class in a different file
#
# DONE:
# - Process input wiring type to support these formats: 3.2, 3p2, and 3P2.
# - Process input length type to support these formats: R1_G1, r1_g1, R1 G1, and r1 g1.
# - Convert user inputs to int when applicable
# - Require valid user inputs
# - Print results in mm and ft
# - Ask user for previous wire log value in feet (remaining length of wire in spool)
# - Print the new wire log value in feet (after subtracting used wire)

import script_tools
from colorama import Fore, Back, Style, init

# Fixes colors for Windows Command Prompt:
init(convert=True)

# specify length of line for printing
line_length = 50

# cable branches based on wiring type
cable_branches = {
    "3.2" : ["A", "B", "C"],
    "2.2" : ["A", "C"],
    "2.3" : ["A", "B"],
    "1.3" : ["A"]
}

# number of channels per branch based on wiring type
cable_channels_per_branch = {
    "3.2" : 3,
    "2.2" : 3,
    "2.3" : 4,
    "1.3" : 4
}

# cable lengths (mm) from Design B (Axel Filenius, March 1, 2024)
cable_lengths = {
    # Ring 1 (R1)
    "2.3 R1_G1" : {"A" : 280, "B" : 280},
    "2.3 R1_G2" : {"A" : 275, "B" : 330},
    "1.3 R1_G3" : {"A" : 390},
    # Ring 2 (R2)
    "2.3 R2_G1" : {"A" : 200, "B" : 240},
    "2.3 R2_G2" : {"A" : 275, "B" : 330},
    "2.3 R2_G3" : {"A" : 275, "B" : 330},
    "2.3 R2_G4" : {"A" : 337, "B" : 377},
    # Ring 3 (R3)
    "3.2 R3_G1" : {"A" : 200, "B" : 215, "C": 310},
    "3.2 R3_G2" : {"A" : 365, "B" : 435, "C": 510},
    # Ring 4 (R4)
    "3.2 R4_G1" : {"A" : 190, "B" : 200, "C": 235},
    "3.2 R4_G2" : {"A" : 230, "B" : 275, "C": 315},
    "2.2 R4_G3" : {"A" : 360, "C" : 405},
}

# supported wiring types
wiring_types = list(cable_branches.keys())

# supported full types (wiring + length)
full_types = list(cable_lengths.keys())

# calculate wire length for one e-link
def CalcWireLengthElink(wiring_type, length_type, loss):
    wire_length_elink = -1
    full_type = ""
    branches = []
    branch_lengths = {}
    
    # check if wiring type is valid
    wiring_type_is_valid = script_tools.group_contains_element(wiring_types, wiring_type)
    if wiring_type_is_valid:
        # assign branches
        branches = cable_branches[wiring_type]
    else:
        # print error messages and return
        print(Fore.RED + f"ERROR: {wiring_type} is not a valid wiring type." + Fore.RESET)
        print(Fore.RED + f"Please enter a valid wiring type from this list:" + Fore.RESET)
        print(Fore.RED + f"{wiring_types}" + Fore.RESET)
        return wire_length_elink
    
    # get full type (wiring + length)
    full_type = "{0} {1}".format(wiring_type, length_type)
    
    # check if full type (wiring + length) is valid
    full_type_is_valid = script_tools.group_contains_element(full_types, full_type)
    if full_type_is_valid:
        # assign branch lengths
        branch_lengths = cable_lengths[full_type]
    else:
        # print error messages and return
        print(Fore.RED + f"ERROR: {full_type} is not a valid e-link type (defined by wiring and length)." + Fore.RESET)
        print(Fore.RED + f"Please enter a valid combination of e-link wiring and length types from this list:" + Fore.RESET)
        print(Fore.RED + f"{full_types}" + Fore.RESET)
        return wire_length_elink
    
    # get number of channels per branch
    n_channels_per_branch = cable_channels_per_branch[wiring_type]
    
    print(f" - full_type: {full_type}")
    print(f" - branches: {branches}")
    print(f" - n_channels_per_branch: {n_channels_per_branch}")
    print(f" - branch_lengths: {branch_lengths}")
    script_tools.printLine(line_length)

    # calculate wire length for one e-link
    wire_length_elink = 0
    for branch in branches:
        branch_length = branch_lengths[branch]
        length_to_add = n_channels_per_branch * (branch_length + loss)
        wire_length_elink += length_to_add
    return wire_length_elink

# calculate wire length for a batch of n e-links
def CalcWireLengthBatch(n_elinks, wire_length_elink):
    wire_length_batch = n_elinks * wire_length_elink
    return wire_length_batch

# run wire length calculator
def run():
    script_tools.printLine(line_length)
    print(Fore.GREEN + "Calculating twisted pair wire length." + Fore.RESET)
    script_tools.printLine(line_length)
    
    # User input
    wiring_type     = input(Fore.GREEN + "Enter e-link wiring type: " + Fore.RESET)
    length_type     = input(Fore.GREEN + "Enter e-link length type: " + Fore.RESET)
    loss            = float(input(Fore.GREEN + "Enter loss per twisted pair (mm): " + Fore.RESET))
    n_elinks        = int(input(Fore.GREEN + "Enter number of e-links: " + Fore.RESET))
    prev_wire_log   = float(input(Fore.GREEN + "Enter previous wire log entry (ft): " + Fore.RESET))

    # format wiring type
    wiring_type = script_tools.formatWiringType(wiring_type)

    # format length type
    length_type = script_tools.formatLengthType(length_type)

    script_tools.printLine(line_length)
    print(f" - wiring_type: {wiring_type}")
    print(f" - length_type: {length_type}")
    print(f" - loss: {loss} mm")
    print(f" - n_elinks: {n_elinks}")
    print(f" - prev_wire_log: {prev_wire_log} ft")
    script_tools.printLine(line_length)

    # Calculate wire length:
    # Split into two steps (1 e-link and n e-links)
    # so that we can print out both.

    # calculate wire length for one e-link
    wire_length_elink_mm = CalcWireLengthElink(wiring_type, length_type, loss)
    wire_length_elink_ft = script_tools.convert_mm_to_ft(wire_length_elink_mm)

    # if length < 0 (invalid), return
    if wire_length_elink_mm < 0:
        return

    # calculate wire length for a batch of n e-links
    wire_length_batch_mm = CalcWireLengthBatch(n_elinks, wire_length_elink_mm)
    wire_length_batch_ft = script_tools.convert_mm_to_ft(wire_length_batch_mm)

    # calculate new wire log
    new_wire_log = prev_wire_log - wire_length_batch_ft

    # print results
    print(Fore.GREEN + f"Wire length for 1 e-link: " + Fore.RESET)
    print(f"\t{wire_length_elink_mm:.1f} mm = {wire_length_elink_ft:.1f} ft")
    print(Fore.GREEN + f"Wire length for {n_elinks} e-links: " + Fore.RESET)
    print(f"\t{wire_length_batch_mm:.1f} mm = {wire_length_batch_ft:.1f} ft")
    print(Fore.GREEN + f"New wire log entry: " + Fore.RESET)
    print(f"\t{prev_wire_log:.1f} ft - {wire_length_batch_ft:.1f} ft = {new_wire_log:.1f} ft")
    script_tools.printLine(line_length)

def main():
    run()

if __name__ == "__main__":
    run()
