# getElinkResults.py
#
# Developed by the KU CMS group.
#
# -------------------------- #
# Author:   Caleb Smith
# Date:     January 10, 2025
# -------------------------- #

import script_tools
import argparse
import sys
import os
import shutil
import glob
from datetime import datetime

# TODO:

# DONE:
# - Print total number of e-links that had results copied.
# - Print number of files copied for each e-link.
# - Only copy files from the largest run number.
# - Print e-link branches that were copied.
# - Add date to output directory.
# - Add ability to skip e-links (for e-links that already have plots in the database).

def main():
    # Arguments
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--source_dir", "-s", default="", help="Source directory")
    parser.add_argument("--target_dir", "-t", default="", help="Target directory")
    
    options     = parser.parse_args()
    source_dir  = options.source_dir
    target_dir  = options.target_dir

    if not source_dir:
        print("Please provide a source directory using the -s option.")
        sys.exit(1) 
    
    if not target_dir:
        print("Please provide a target directory using the -t option.")
        sys.exit(1) 

    # Additional user input
    print("Please enter a range of e-link numbers (min and max) to include:")
    min_elink_num = int(input(" - Enter minimum e-link number: "))
    max_elink_num = int(input(" - Enter maximum e-link number: "))

    if min_elink_num > max_elink_num:
        print("ERROR: Invalid range of e-link numbers: [{0}, {1}]".format(min_elink_num, max_elink_num))
        print("The maximum e-link number must be greater than or equal to the minimum e-link number.")
        print("Please try again.")
        sys.exit(1) 
    
    copyElinkResults(source_dir, target_dir, min_elink_num, max_elink_num)

def copyElinkResults(source_dir, target_dir, min_elink_num, max_elink_num):
    today = datetime.today().strftime("%Y_%m_%d")    
    output_dir = "{0}/EyeBERT_plots_elinks_{1}_to_{2}_date_{3}".format(target_dir, min_elink_num, max_elink_num, today)
    script_tools.makeDir(output_dir)
    
    print(" - Input directory:  {0}".format(source_dir))
    print(" - Output directory: {0}".format(output_dir))
    print("Copying results for e-links {0} to {1}.".format(min_elink_num, max_elink_num))

    # list of e-links to skip (already have plots in the database)
    elinks_to_skip = [904, 958, 988]
    print("elinks_to_skip: {0}".format(elinks_to_skip))
    
    elink_branches = ["A", "B", "C"]
    num_elinks_copied = 0
    
    for number in range(min_elink_num, max_elink_num + 1):
        
        if number in elinks_to_skip:
            print(" - Skipping e-link {0}".format(number))
            continue
        
        elink_input_dir  = "{0}/{1}".format(source_dir, number)
        elink_output_dir = "{0}/{1}".format(output_dir, number)
        
        if os.path.isdir(elink_input_dir):
            script_tools.makeDir(elink_output_dir)
            
            num_files_per_elink = 0
            branches_copied = []
            for branch in elink_branches:
                latest_run = findLatestRunForBranch(elink_input_dir, number, branch)                
                pattern = getPattern(elink_input_dir, number, branch, latest_run)

                if not pattern:
                    continue

                file_list = glob.glob(pattern)
                num_files_per_branch = len(file_list)
                num_files_per_elink += num_files_per_branch
                branches_copied.append(branch)

                for file in file_list:
                    #print(file)
                    shutil.copy(file, elink_output_dir)
            
            print(" - e-link {0}: copied {1} files for branches {2}".format(number, num_files_per_elink, branches_copied))
            num_elinks_copied += 1
    
    print("Copied results for {0} e-links.".format(num_elinks_copied))

def findLatestRunForBranch(directory, elink_number, elink_branch):
    result = -1
    elink_channel = "cmd"
    
    file_path = "{0}/{1}_{2}_{3}.png".format(directory, elink_number, elink_branch, elink_channel)
    if os.path.isfile(file_path):
        result = 1
    
    run = 2
    file_path = "{0}/{1}_{2}_{3}_{4}.png".format(directory, elink_number, elink_branch, elink_channel, run)
    while os.path.isfile(file_path):
        result = run
        run += 1
        file_path = "{0}/{1}_{2}_{3}_{4}.png".format(directory, elink_number, elink_branch, elink_channel, run)

    return result

def getPattern(directory, elink_number, elink_branch, latest_run):
    if latest_run <= 0:
        pattern = ""
        return pattern
    elif latest_run == 1:
        pattern = "{0}/{1}_{2}_*.png".format(directory, elink_number, elink_branch)
        return pattern
    else:
        pattern = "{0}/{1}_{2}_*_{3}.png".format(directory, elink_number, elink_branch, latest_run)
        return pattern

if __name__ == "__main__":
    main()

