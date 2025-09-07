# test_colors.py
#
# Colorama:
# https://pypi.org/project/colorama/
#
# Print all colorama colors:
# https://stackoverflow.com/questions/61686780/python-colorama-print-all-colors
#
# Fix colors for Windows Command Prompt:
# https://stackoverflow.com/questions/9848889/colorama-for-python-not-returning-colored-print-lines-on-windows
#
# Warning for Windows:
#
# By default, colors will not work in Windows Command Prompt;
# you will only get ANSI escape codes.
#
# Option 1: For Windows, use this line (since colorama v0.4.6):
# just_fix_windows_console()
#
# Option 2: For Windows, use this line:
# init(convert=True)
#
# For other operating systems (platforms), use this line:
# init(convert=False)
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

def test_colors(colors):
    n_colors = len(colors)
    print(f"Operating System (platform): {sys.platform}")
    print(f"Testing {n_colors} colors...")
    for i, color in enumerate(colors, start=1):
        color_fore = script_tools.getColorFore(color)
        message = f"\t{i} - " + color_fore + f"{color}" + Fore.RESET
        print(message)
    print("Done!")

def main():
    # specify length of line for printing
    line_length = 40
    
    # list of colors to test (including reset)
    colors = ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE", "RESET"]
    
    script_tools.printLine(line_length)
    print("Running test_colors")
    script_tools.printLine(line_length)
    test_colors(colors)
    script_tools.printLine(line_length)

if __name__ == "__main__":
    main()
