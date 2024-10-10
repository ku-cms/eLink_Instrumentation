# calc_length.py

# TODO:
# - Require valid user inputs
# - Convert user inputs to int when applicable
# - Create class

# DONE:

# cable branches based on cable type
cable_branches = {
    "3p2" : ["A", "B", "C"],
    "2p2" : ["A", "C"],
    "2p3" : ["A", "B"],
    "1p3" : ["A"]
}

# supported cable types
cable_types = list(cable_branches.keys())

# Calculate length
def CalculateLength(wiring_type, length_type, n_elinks, loss):
    branches = cable_branches[wiring_type]
    print(f"branches: {branches}")

def run():
    print("Calculating twisted pair wire lengths.")
    print("--------------------------------------")
    
    # User input
    wiring_type = input("Enter e-link wiring type: ")
    length_type = input("Enter e-link length type: ")
    n_elinks    = input("Enter number of e-links: ")
    loss        = input("Enter loss per twisted pair (mm): ")

    # Idea:
    # support both formats for type: 3.2 and 3p2
    # convert on format to the other using replace()
    
    print("--------------------------------------")
    print(f"wiring_type: {wiring_type}")
    print(f"length_type: {length_type}")
    print(f"n_elinks: {n_elinks}")
    print(f"loss: {loss} mm")

    # Calculate length
    CalculateLength(wiring_type, length_type, n_elinks, loss)

def main():
    run()

if __name__ == "__main__":
    run()

