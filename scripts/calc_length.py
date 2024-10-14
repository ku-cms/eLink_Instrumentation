# calc_length.py

# TODO:
# - Require valid user inputs
# - Convert user inputs to int when applicable
# - Create class

# DONE:

from colorama import Fore, Back, Style, init
import script_tools

# cable branches based on wiring type
cable_branches = {
    "3.2" : ["A", "B", "C"],
    "2.2" : ["A", "C"],
    "2.3" : ["A", "B"],
    "1.3" : ["A"]
}

# cable lengths from Design B (Axel Filenius, March 1, 2024)
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
    branches = []
    wiring_type_is_valid = script_tools.group_contains_element(wiring_types, wiring_type)
    if wiring_type_is_valid:
        branches = cable_branches[wiring_type]
    else:
        print(Fore.RED + f"ERROR: {wiring_type} is not a valid wiring type." + Fore.RESET)
        print(Fore.RED + f"Please enter a valid wiring type: {wiring_types}" + Fore.RESET)
        return wire_length_elink
    print(f"branches: {branches}")
    return wire_length_elink

# calculate wire length for a batch of n e-links
def CalcWireLengthBatch(n_elinks, wire_length_elink):
    wire_length_batch = n_elinks * wire_length_elink
    return wire_length_batch

def run():
    print("Calculating twisted pair wire length.")
    print("-------------------------------------")
    
    # User input
    wiring_type = input("Enter e-link wiring type: ")
    length_type = input("Enter e-link length type: ")
    loss        = input("Enter loss per twisted pair (mm): ")
    n_elinks    = input("Enter number of e-links: ")

    # FIXME: Convert user inputs to int when applicable

    # Idea:
    # support both formats for type: 3.2 and 3p2
    # convert on format to the other using replace()

    print("-------------------------------------")
    print(f" - wiring_type: {wiring_type}")
    print(f" - length_type: {length_type}")
    print(f" - loss: {loss} mm")
    print(f" - n_elinks: {n_elinks}")
    print("-------------------------------------")

    # Calculate length;
    # may split into two steps: 1 e-link vs. n e-links
    # so that we can print out both...

    # calculate wire length for one e-link
    wire_length_elink = CalcWireLengthElink(wiring_type, length_type, loss)

    # if length < 0 (invalid), return
    if wire_length_elink < 0:
        return

    # calculate wire length for a batch of n e-links
    wire_length_batch = CalcWireLengthBatch(n_elinks, wire_length_elink)

    print(f"wire_length_elink: {wire_length_elink}")
    print(f"wire_length_batch: {wire_length_batch}")

def main():
    run()

if __name__ == "__main__":
    run()

