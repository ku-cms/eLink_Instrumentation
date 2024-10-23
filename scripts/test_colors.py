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

from colorama import Fore, Back, Style, init
import sys

# Check operating system (platform)
if sys.platform == "win32":
    # For Windows Command Prompt, fix colors using convert=True:
    init(convert=True)
else:
    # For other OS/platforms, use convert=False:
    init(convert=False)

# test colors
def test_colors():
    print(f"Operating System (platform): {sys.platform}")
    print("Testing colors...")
    print("1 - " + Fore.BLACK    + "BLACK"    + Fore.RESET)
    print("2 - " + Fore.RED      + "RED"      + Fore.RESET)
    print("3 - " + Fore.GREEN    + "GREEN"    + Fore.RESET)
    print("4 - " + Fore.YELLOW   + "YELLOW"   + Fore.RESET)
    print("5 - " + Fore.BLUE     + "BLUE"     + Fore.RESET)
    print("6 - " + Fore.MAGENTA  + "MAGENTA"  + Fore.RESET)
    print("7 - " + Fore.CYAN     + "CYAN"     + Fore.RESET)
    print("8 - " + Fore.WHITE    + "WHITE"    + Fore.RESET)
    print("9 - " + Fore.RESET    + "RESET"    + Fore.RESET)
    print("Done!")

def main():
    test_colors()

if __name__ == "__main__":
    main()
