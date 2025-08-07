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

def getTodayDate():
    date_format = "%Y-%m-%d"
    today_date_object = datetime.datetime.today()
    today_date = today_date_object.strftime(date_format)
    return today_date

def addDateToFile(original_file_name):
    today_date = getTodayDate()
    today_date = today_date.replace("-", "_")
    # split_name = original_file_name.split(".")
    # new_file_name = f"{split_name[0]}_{today_date}.{split_name[1]}"
    file_base, file_extension = os.path.splitext(original_file_name)
    new_file_name = f"{file_base}_{today_date}{file_extension}"
    print(f" - today's date: {today_date}")
    print(f" - original_file_name: {original_file_name}")
    print(f" - new_file_name: {new_file_name}")
    return new_file_name

def prepareElinkProductionData(excel_file, download_dir, data_dir):
    print("Preparing e-link production data...")
    original_path = download_dir + excel_file
    new_path = addDateToFile(original_path)
    try:
        shutil.move(original_path, new_path)
    except FileNotFoundError:
        print(f"ERROR: Data file '{original_path}' not found.")
        sys.exit(1)
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
