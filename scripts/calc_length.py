# calc_length.py

# TODO:
# - Require valid user inputs
# - Convert user inputs to int when applicable
# - Create class

# DONE:

import tools

# cable branches based on wiring type
cable_branches = {
    "3p2" : ["A", "B", "C"],
    "2p2" : ["A", "C"],
    "2p3" : ["A", "B"],
    "1p3" : ["A"]
}

# supported wiring types
wiring_types = list(cable_branches.keys())

# calculate wire length for one e-link
def CalcWireLengthElink(wiring_type, length_type, loss):
    wire_length_elink = -1
    branches = []
    wiring_type_is_valid = tools.is_valid_cable_type(wiring_types, wiring_type)
    if wiring_type_is_valid:
        branches = cable_branches[wiring_type]
    else:
        print(f"ERROR: {wiring_type} is not a valid wiring type.")
        print(f"Please enter a valid wiring type: {wiring_types}")
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

