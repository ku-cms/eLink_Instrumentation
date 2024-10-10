# calc_length.py

# Calculate length
def CalculateLength(wiring_type, length_type, n_elinks, loss):
    pass

def run():
    print("Calculating twisted pair wire lengths.")
    print("--------------------------------------")
    
    # User input
    wiring_type = input("Enter e-link wiring type: ")
    length_type = input("Enter e-link length type: ")
    n_elinks    = input("Enter number of e-links: ")
    loss        = input("Enter loss per twisted pair (mm): ")
    
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

