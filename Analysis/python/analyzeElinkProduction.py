# analyzeElinkProduction.py
#
# Developed by the KU CMS group.
#
# -------------------------- #
# Author:   Caleb Smith
# Date:     May 21, 2025
# -------------------------- #

import plot
import tools
import os
import sys
import argparse
import datetime
import numpy as np
import pandas as pd

# ---------------------------------------------
# TODO:
# ---------------------------------------------
# DONE:
# - Load e-link production data
# - Fix CSV encoding error
# - Check if input file exists
# - Separate headers from data
# - Remove empty date entries
# - Convert dates to datetime objects
# - Convert frequency of date to unit count per date
# - Plot one line from data
# - Use data = list(reader) to load csv
# - Select production e-links: e-link number >= 700
# - Plot multiple lines from data on one plot
# - Add legend
# - Add arguments: start date, end date, and input file
# - Write functions to get date objects and create plot name
# ---------------------------------------------

def createSampleData():
    dates = pd.date_range(start="2025-01-01", periods=5, freq='W')
    production = np.random.randint(0, 20, size=len(dates))
    return (dates, production)

def analyzeSampleData(plot_dir):
    print("Analyzing sample data...")
    print(f" - plot directory: {plot_dir}")
    
    tools.makeDir(plot_dir)
    dates, production = createSampleData()
    cumulative_production = np.cumsum(production)
    # print("Sample data:")
    # print(f" - dates: {dates}")
    # print(f" - production: {production}")
    # print(f" - cumulative_production: {cumulative_production}")

    plot_name = "cumulative_plot_example"
    title = "Cumulative plot example: units produced over time"
    x_label = "Time"
    y_label = "Number of units"
    x_lim = []
    y_lim = []
    plot.makeCumulativePlot(dates, cumulative_production, plot_dir, plot_name, title, x_label, y_label, x_lim, y_lim)
    
    print("Done!")

def getValidElinkTypes():
    valid_elink_types = [
        "2.3 R1_G1",
        "2.3 R1_G2",
        "1.3 R1_G3",
        "2.3 R2_G1",
        "2.3 R2_G2",
        "2.3 R2_G3",
        "2.3 R2_G4",
        "3.2 R3_G1",
        "3.2 R3_G2",
        "3.2 R4_G1",
        "3.2 R4_G2",
        "2.2 R4_G3"
    ]
    return valid_elink_types

def checkElinkTypes(df):
    print("Checking that e-link types are valid...")
    valid_elink_types = getValidElinkTypes()
    rows_with_invalid_types = df[~df["Type"].isin(valid_elink_types)]
    n_types = len(valid_elink_types)
    n_rows = len(df["Type"])
    print(f" - number of types: {n_types}")
    print(f" - number of rows: {n_rows}")
    if rows_with_invalid_types.empty:
        print("All e-link types in the data frame are valid.")
    else:
        print("Found invalid e-link types in the data frame:")
        for _, row in rows_with_invalid_types.iterrows():
            serial_number = row["Harness #"]
            elink_type = row["Type"]
            print(f" - serial number: {serial_number}, e-link type: {elink_type}")

def loadElinkProductionData(input_file, column_name):
    data = tools.getData(input_file)
    
    # Separate headers from data
    headers = data[0]
    rows = data[1:]
    
    if column_name not in headers:
        print(f"ERROR: The column_name '{column_name}' is not in headers!")
    
    # Get column index based on column name
    column_index = headers.index(column_name)
    # print(f" - headers: {headers}")
    # print(f" - column_name: {column_name}")
    # print(f" - column_index: {column_index}")
    
    # Collect dates for a specific column and remove empty entries
    dates = [row[column_index] for row in rows if row[column_index]]
    # Convert to datetime objects
    dates = pd.to_datetime(dates, format='%m-%d-%y')
    # Count occurrences of each date
    daily_counts = pd.Series(dates).value_counts()
    # Sort by date
    daily_counts = daily_counts.sort_index()
    
    # print("daily_counts:")
    # print(daily_counts)
        
    return daily_counts

def analyzeElinkProductionData(input_file, plot_dir):
    print("Analyzing e-link production data...")
    print(f" - input file: {input_file}")
    print(f" - plot directory: {plot_dir}")
    
    tools.makeDir(plot_dir)
    
    column_name = "Shipped"
    daily_counts = loadElinkProductionData(input_file, column_name)
    cumulative_counts = daily_counts.cumsum()
    # print("e-link production data:")
    # print(" - daily_counts:")
    # print(daily_counts)
    # print(" - cumulative_counts:")
    # print(cumulative_counts)

    plot_name   = f"elink_production_{column_name.lower()}"
    title       = f"Cumulative e-link production: {column_name}"
    x_label     = "Time"
    y_label     = "Number of e-links"
    x_lim       = []
    y_lim       = []
    plot.makeCumulativePlot(cumulative_counts.index, cumulative_counts.values, plot_dir, plot_name, title, x_label, y_label, x_lim, y_lim)
    
    print("Done!")

def loadElinkProductionDataMultiStage(input_file, min_elink_number, stages):
    cumulative_data = {}
    
    if not os.path.exists(input_file):
        print(f"ERROR in getData(): The input file '{input_file}' does not exist.")
        return cumulative_data

    df = pd.read_csv(input_file, encoding="latin1")

    df["Harness #"] = pd.to_numeric(df["Harness #"], errors="coerce")
    df = df[df["Harness #"] >= min_elink_number]

    # Convert date strings to datetime objects
    for stage in stages:
        # Auto-detect (infer) datetime format
        df[stage] = pd.to_datetime(df[stage], errors='coerce')
    
    checkElinkTypes(df)

    # Compute cumulative counts
    for stage in stages:
        stage_dates = df[stage].dropna()
        total_completed = stage_dates.shape[0]
        print(f"stage: {stage}")
        print(f" - min date: {stage_dates.min()}")
        print(f" - max date: {stage_dates.max()}")
        print(f" - total completed: {total_completed}")
        counts = stage_dates.value_counts().sort_index()
        full_range = pd.date_range(start=stage_dates.min(), end=stage_dates.max())
        counts = counts.reindex(full_range, fill_value=0)
        cumulative_data[stage] = counts.cumsum()
    
    return cumulative_data

def getDateObjects(start_date, end_date):
    date_format = "%Y-%m-%d"
    start_date_object   = datetime.datetime.strptime(start_date, date_format)
    end_date_object     = datetime.datetime.strptime(end_date, date_format)
    return (start_date_object, end_date_object)

def createPlotName(start_date, end_date):
    start_date_for_name = start_date.replace("-", "_")
    end_date_for_name   = end_date.replace("-", "_")
    plot_name           = "elink_production_{0}_to_{1}".format(start_date_for_name, end_date_for_name)
    return plot_name

def analyzeElinkProductionDataMultiStage(start_date, end_date, input_file, plot_dir):
    min_elink_number = 700
    stages = ['Requested', 'Cut', 'Stripped', 'Soldered', 'Epoxy', 'Turned over', 'Shipped']
    
    tools.makeDir(plot_dir)
    
    cumulative_data = loadElinkProductionDataMultiStage(input_file, min_elink_number, stages)
    
    start_date_object, end_date_object = getDateObjects(start_date, end_date)
    
    plot_name = createPlotName(start_date, end_date)

    # Use Tableau colors
    colors = {
        "Requested"     : "tab:pink",
        "Cut"           : "tab:red",
        "Stripped"      : "tab:orange",
        "Soldered"      : "tab:blue",
        "Epoxy"         : "tab:purple",
        "Turned over"   : "tab:green",
        "Shipped"       : "tab:cyan"
    }

    print("Analyzing e-link production data, multi stage...")
    print(f" - start date: {start_date}")
    print(f" - end date: {end_date}")
    print(f" - input file: {input_file}")
    print(f" - plot directory: {plot_dir}")
    print(f" - plot name: {plot_name}")

    title       = "Cumulative e-link production"
    x_label     = "Time"
    y_label     = "Number of e-links"
    x_lim       = [start_date_object, end_date_object]
    y_lim       = []
    plot.makeCumulativePlotMultiStage(cumulative_data, plot_dir, plot_name, title, x_label, y_label, x_lim, y_lim, colors)
    
    print("Done!")

def main():
    # Arguments
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--start_date", "-a", default="", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end_date",   "-b", default="", help="End date (YYYY-MM-DD)")
    parser.add_argument("--input_file", "-c", default="", help="Input file (csv)")

    options     = parser.parse_args()
    start_date  = options.start_date
    end_date    = options.end_date
    input_file  = options.input_file

    if not start_date:
        print("Please provide a start date (YYYY-MM-DD) using the -a option.")
        sys.exit(1)

    if not end_date:
        print("Please provide an end date (YYYY-MM-DD) using the -b option.")
        sys.exit(1)
    
    if not input_file:
        print("Please provide an input file (csv) using the -c option.")
        sys.exit(1)
    
    plot_dir    = "elink_production_plots"
    analyzeElinkProductionDataMultiStage(start_date, end_date, input_file, plot_dir)

if __name__ == "__main__":
    main()
