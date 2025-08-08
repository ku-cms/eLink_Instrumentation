# prepareElinkProductionData.py
#
# Developed by the KU CMS group.
#
# -------------------------- #
# Author:   Caleb Smith
# Date:     August 7, 2025
# -------------------------- #

import tools
import datetime
import os
import sys
import shutil

# ---------------------------------------------
# TODO:
# - Export the Production tab to a .csv file (same file name, but change extension to .csv).
# ---------------------------------------------
# DONE:
# - Rename the Excel file: append today's date to the end.
# - Move the Excel file to the working area: .../eLink_Instrumentation/Analysis/data.
# ---------------------------------------------

def getTodayDate():
    date_format = "%Y-%m-%d"
    today_date_object = datetime.datetime.today()
    today_date = today_date_object.strftime(date_format)
    return today_date

def addDateToFileName(original_file_name):
    print("Adding date to file name...")

    today_date = getTodayDate()
    today_date = today_date.replace("-", "_")
    file_base, file_extension = os.path.splitext(original_file_name)
    new_file_name = f"{file_base}_{today_date}{file_extension}"
    
    print(f" - today's date: {today_date}")
    print(f" - original file name: {original_file_name}")
    print(f" - new file name: {new_file_name}")
    
    return new_file_name

def prepareElinkProductionData(excel_file, download_dir, data_dir):
    print("Preparing e-link production data...")

    tools.makeDir(data_dir)
    source_file         = download_dir + excel_file
    destination_file    = data_dir + excel_file
    destination_file    = addDateToFileName(destination_file)
    
    print(f"Moving file...")
    print(f" - source file: {source_file}")
    print(f" - destination file: {destination_file}")
    tools.moveFile(source_file, destination_file)
    
    print("Done!")

def main():
    excel_file      = "Harness_Serial_Number.xlsx"
    download_dir    = "/Users/caleb/Downloads"
    data_dir        = "data"

    download_dir    = tools.appendSlash(download_dir)
    data_dir        = tools.appendSlash(data_dir)

    prepareElinkProductionData(excel_file, download_dir, data_dir)

if __name__ == "__main__":
    main()
