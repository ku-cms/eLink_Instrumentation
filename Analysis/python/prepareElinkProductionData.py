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

def getTodayDate():
    date_format = "%Y-%m-%d"
    today_date_object = datetime.datetime.today()
    today_date = today_date_object.strftime(date_format)
    return today_date

def addDateToFile(original_file_name):
    today_date = getTodayDate()
    today_date = today_date.replace("-", "_")
    split_name = original_file_name.split(".")
    new_file_name = f"{split_name[0]}_{today_date}.{split_name[1]}"
    print(f" - today's date: {today_date}")
    print(f" - original_file_name: {original_file_name}")
    print(f" - new_file_name: {new_file_name}")

def prepareElinkProductionData(excel_file, download_dir, data_dir):
    print("Preparing e-link production data...")
    full_path = download_dir + excel_file
    addDateToFile(full_path)
    print("Done!")

def main():
    excel_file      = "Harness_Serial_Number.xlsx"
    download_dir    = "~/Downloads"
    data_dir        = "data"
    download_dir    = tools.appendSlash(download_dir)
    data_dir        = tools.appendSlash(data_dir)

    prepareElinkProductionData(excel_file, download_dir, data_dir)

if __name__ == "__main__":
    main()
