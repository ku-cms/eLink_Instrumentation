# wire_length.py
#
# Developed by the KU CMS group.
#
# -------------------------- #
# Wire Length Calculator
# Author:   Caleb Smith
# Date:     October 23, 2024
# -------------------------- #
#
# Computes the total wire length for 1 e-link and n e-links based on user input.
# Also computes new wire log entry.
#
# The user must input the following information:
# - e-link wiring type
# - e-link length type
# - loss per twisted pair (mm); now hardcoded
# - number of e-links
# - previous wire log (ft)
#
# Output:
# - Wire length for 1 e-link.
# - Wire length for n e-links.
# - New wire log entry.
#
# TODO:
#
# DONE:
# - Process input wiring type to support these formats: 3.2, 3p2, and 3P2.
# - Process input length type to support these formats: R1_G1, r1_g1, R1 G1, and r1 g1.
# - Convert user inputs to int when applicable
# - Require valid user inputs
# - Print results in mm and ft
# - Ask user for previous wire log value in feet (remaining length of wire in spool)
# - Print the new wire log value in feet (after subtracting used wire)
# - Hardcode estimated loss per twisted pair (mm)
# - Create WireLengthCalculator class in a different file
# - Customize the "fix color" init() command based on the operating system.

from WireLengthCalculator import WireLengthCalculator
import script_tools
from colorama import Fore, Back, Style, init
import sys

# Check operating system (platform)
if sys.platform == "win32":
    # For Windows Command Prompt, fix colors using convert=True:
    init(convert=True)
else:
    # For other OS/platforms, use convert=False:
    init(convert=False)

# run wire length calculator
def run():
    # version
    version = 2.0

    # specify length of line for printing
    line_length = 50

    # hardcode estimated loss per twisted pair (mm)
    loss = 128

    script_tools.printLine(line_length)
    print(Fore.GREEN + f"Wire Length Calculator (version {version})" + Fore.RESET)
    print(Fore.GREEN + f"Operating System (platform): {sys.platform}" + Fore.RESET)
    print(Fore.GREEN + "Calculating twisted pair wire length." + Fore.RESET)
    script_tools.printLine(line_length)

    # User input
    wiring_type     = input(Fore.GREEN + "Enter e-link wiring type: " + Fore.RESET)
    length_type     = input(Fore.GREEN + "Enter e-link length type: " + Fore.RESET)
    #loss            = float(input(Fore.GREEN + "Enter loss per twisted pair (mm): " + Fore.RESET))
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

    # initialize calculator
    calculator = WireLengthCalculator(wiring_type, length_type, loss, line_length)

    # calculate wire length for one e-link
    wire_length_elink_mm = calculator.CalcWireLengthElink()
    wire_length_elink_ft = script_tools.convert_mm_to_ft(wire_length_elink_mm)

    # if length < 0 (invalid), return
    if wire_length_elink_mm < 0:
        return

    # calculate wire length for a batch of n e-links
    wire_length_batch_mm = calculator.CalcWireLengthBatch(n_elinks, wire_length_elink_mm)
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
