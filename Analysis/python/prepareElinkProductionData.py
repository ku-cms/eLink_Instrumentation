# prepareElinkProductionData.py
#
# Developed by the KU CMS group.
#
# -------------------------- #
# Author:   Caleb Smith
# Date:     August 7, 2025
# -------------------------- #

import tools

# ---------------------------------------------
# TODO:
# - Export the Production tab to a .csv file (same file name, but change extension to .csv).
# ---------------------------------------------
# DONE:
# - Rename the Excel file: append today's date to the end.
# - Move the Excel file to the working area: .../eLink_Instrumentation/Analysis/data.
# ---------------------------------------------

def prepareElinkProductionData(excel_file, excel_sheet, download_dir, data_dir):
    print("Preparing e-link production data...")

    tools.makeDir(data_dir)

    source_file         = download_dir + excel_file
    destination_file    = data_dir + excel_file
    destination_file    = tools.addDateToFileName(destination_file)
    
    tools.moveFile(source_file, destination_file)

    tools.exportExcelSheetToCSV(excel_file, excel_sheet)
    
    print("Done!")

def main():
    excel_file      = "Harness_Serial_Number.xlsx"
    excel_sheet     = "Production"
    download_dir    = "/Users/caleb/Downloads"
    data_dir        = "data"

    download_dir    = tools.appendSlash(download_dir)
    data_dir        = tools.appendSlash(data_dir)

    prepareElinkProductionData(excel_file, excel_sheet, download_dir, data_dir)

if __name__ == "__main__":
    main()
