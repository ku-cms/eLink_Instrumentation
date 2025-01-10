# getElinkResults.py
#
# Developed by the KU CMS group.
#
# -------------------------- #
# Get Elink Results
# Author:   Caleb Smith
# Date:     January 10, 2025
# -------------------------- #

import script_tools
import sys

def getElinkResults(min_elink_num, max_elink_num):
    print("Getting results for e-links {0} to {1}.".format(min_elink_num, max_elink_num))
    #target_dir = "results_elinks_{0}_to_{1}".format(min_elink_num, max_elink_num)
    #makeDir(target_dir)
    for number in range(min_elink_num, max_elink_num + 1):
        print(" - Copying results for e-link {0}".format(number))

def main():
    # User input
    print("Please enter a range of e-link numbers (min and max) to include:")
    min_elink_num = int(input("Enter minimum e-link number: "))
    max_elink_num = int(input("Enter maximum e-link number: "))

    if min_elink_num > max_elink_num:
        print("ERROR: Invalid range of e-link numbers: [{0}, {1}]".format(min_elink_num, max_elink_num))
        print("The maximum e-link number must be greater than or equal to the minimum e-link number.")
        print("Please try again.")
        sys.exit(1) 
    
    getElinkResults(min_elink_num, max_elink_num)

if __name__ == "__main__":
    main()

