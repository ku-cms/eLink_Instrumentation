# test_colors.py
#
# Colorama:
# https://pypi.org/project/colorama/
#
# Warning:
#
# By default, colors will not work in Windows Command Prompt;
# you will only get ANSI escape codes.
#
# For Windows, use this line:
# init(convert=True)
#
# For other operating systems (platforms), use this line:
# init(convert=False)
#
# Fix colors for Windows Command Prompt:
# https://stackoverflow.com/questions/9848889/colorama-for-python-not-returning-colored-print-lines-on-windows
#

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

def test_colors_v1():
    print(f"Operating System (platform): {sys.platform}")
    print("Testing 9 colors...")
    print("\t1 - " + Fore.BLACK    + "BLACK"    + Fore.RESET)
    print("\t2 - " + Fore.RED      + "RED"      + Fore.RESET)
    print("\t3 - " + Fore.GREEN    + "GREEN"    + Fore.RESET)
    print("\t4 - " + Fore.YELLOW   + "YELLOW"   + Fore.RESET)
    print("\t5 - " + Fore.BLUE     + "BLUE"     + Fore.RESET)
    print("\t6 - " + Fore.MAGENTA  + "MAGENTA"  + Fore.RESET)
    print("\t7 - " + Fore.CYAN     + "CYAN"     + Fore.RESET)
    print("\t8 - " + Fore.WHITE    + "WHITE"    + Fore.RESET)
    print("\t9 - " + Fore.RESET    + "RESET"    + Fore.RESET)
    print("Done!")

def test_colors_v2(colors):
    n_colors = len(colors)
    print(f"Operating System (platform): {sys.platform}")
    print(f"Testing {n_colors} colors...")
    for i, color in enumerate(colors, start=1):
        print(f"\t{i} - {color}")
    print("Done!")

def main():
    # specify length of line for printing
    line_length = 50
    
    colors = ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE", "RESET"]
    
    script_tools.printLine(line_length)
    print("Running test_colors_v1():")
    script_tools.printLine(line_length)
    test_colors_v1()

    script_tools.printLine(line_length)
    print("Running test_colors_v2(colors):")
    script_tools.printLine(line_length)
    test_colors_v2(colors)

if __name__ == "__main__":
    main()
