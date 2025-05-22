# analyzeElinkProduction.py

import plot
import tools
import numpy as np
import pandas as pd
import datetime

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
    print("Sample data:")
    print(f" - dates: {dates}")
    print(f" - production: {production}")
    print(f" - cumulative_production: {cumulative_production}")

    plot_name = "cumulative_plot_example"
    title = "Cumulative plot example: units produced over time"
    x_label = "Time"
    y_label = "Number of units"
    x_lim = []
    y_lim = []
    plot.makeCumulativePlot(dates, cumulative_production, plot_dir, plot_name, title, x_label, y_label, x_lim, y_lim)
    
    print("Done!")

def loadElinkProductionData(input_file, column_name):
    data = tools.getData(input_file)
    
    # Separate headers from data
    headers = data[0]
    rows = data[1:]
    
    if column_name not in headers:
        print(f"ERROR: The column_name '{column_name}' is not in headers!")
    
    # Get column index based on column name
    column_index = headers.index(column_name)
    print(f" - headers: {headers}")
    print(f" - column_name: {column_name}")
    print(f" - column_index: {column_index}")
    
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
    print("e-link production data:")
    print(" - daily_counts:")
    print(daily_counts)
    print(" - cumulative_counts:")
    print(cumulative_counts)
    # print(" - cumulative_counts.index:")
    # print(cumulative_counts.index)
    # print(" - cumulative_counts.values:")
    # print(cumulative_counts.values)

    plot_name   = f"elink_production_{column_name.lower()}"
    title       = f"Cumulative e-link production: {column_name}"
    x_label     = "Time"
    y_label     = "Number of e-links"
    x_lim       = []
    y_lim       = []
    plot.makeCumulativePlot(cumulative_counts.index, cumulative_counts.values, plot_dir, plot_name, title, x_label, y_label, x_lim, y_lim)
    
    print("Done!")

def loadElinkProductionDataMultiStage(input_file, min_elink_number, stages):
    df = pd.read_csv(input_file, encoding="latin1")

    df["Harness #"] = pd.to_numeric(df["Harness #"], errors="coerce")
    df = df[df["Harness #"] >= min_elink_number]

    # Convert date strings to datetime objects
    for stage in stages:
        df[stage] = pd.to_datetime(df[stage], format='%m-%d-%y', errors='coerce')
    
    # Compute cumulative counts
    cumulative_data = {}
    for stage in stages:
        stage_dates = df[stage].dropna()
        counts = stage_dates.value_counts().sort_index()
        full_range = pd.date_range(start=stage_dates.min(), end=stage_dates.max())
        counts = counts.reindex(full_range, fill_value=0)
        cumulative_data[stage] = counts.cumsum()
    
    return cumulative_data


def analyzeElinkProductionDataMultiStage(input_file, plot_dir):
    print("Analyzing e-link production data, multi stage...")
    print(f" - input file: {input_file}")
    print(f" - plot directory: {plot_dir}")

    tools.makeDir(plot_dir)
    min_elink_number = 700
    stages = ['Cut', 'Stripped', 'Soldered', 'Epoxy', 'Turned over', 'Shipped']
    cumulative_data = loadElinkProductionDataMultiStage(input_file, min_elink_number, stages)

    start_date = datetime.datetime(2024, 4, 1)
    end_date   = datetime.datetime(2025, 5, 31)

    plot_name   = "elink_production"
    title       = "Cumulative e-link production"
    x_label     = "Time"
    y_label     = "Number of e-links"
    x_lim       = [start_date, end_date]
    y_lim       = []
    plot.makeCumulativePlotMultiStage(cumulative_data, plot_dir, plot_name, title, x_label, y_label, x_lim, y_lim)
    
    print("Done!")

def main():
    plot_dir    = "sample_data_plots"
    analyzeSampleData(plot_dir)
    
    input_file  = "data/Harness_Serial_Number_2025_05_21.csv"
    plot_dir    = "elink_production_plots"
    analyzeElinkProductionData(input_file, plot_dir)
    analyzeElinkProductionDataMultiStage(input_file, plot_dir)

if __name__ == "__main__":
    main()
