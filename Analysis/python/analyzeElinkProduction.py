# analyzeElinkProduction.py

import plot
import tools
import numpy as np
import pandas as pd

# ---------------------------------------------
# TODO:
# - Select production e-links: e-link number >= 700
# - Use data = list(reader) to load csv
# - Plot multiple lines from data on one plot
# - Add legend
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
    print(f"headers: {headers}")
    print(f"column_index: {column_index}")
    
    # Collect dates for a specific column and remove empty entries
    dates = [row[column_index] for row in rows if row[column_index]]
    # Convert to datetime objects
    dates = pd.to_datetime(dates, format='%m-%d-%y')
    # Count occurrences of each date
    daily_counts = pd.Series(dates).value_counts()
    # Sort by date
    daily_counts = daily_counts.sort_index()
    
    print("daily_counts:")
    print(daily_counts)
        
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
    print(" - cumulative_counts.index:")
    print(cumulative_counts.index)
    print(" - cumulative_counts.values:")
    print(cumulative_counts.values)

    plot_name = "elink_production"
    title = "Cumulative e-link production"
    x_label = "Time"
    y_label = "Number of e-links"
    x_lim = []
    y_lim = []
    plot.makeCumulativePlot(cumulative_counts.index, cumulative_counts.values, plot_dir, plot_name, title, x_label, y_label, x_lim, y_lim)
    
    print("Done!")

def main():
    plot_dir    = "sample_data_plots"
    analyzeSampleData(plot_dir)
    
    input_file  = "data/Harness_Serial_Number_2025_05_21.csv"
    plot_dir    = "elink_production_plots"
    analyzeElinkProductionData(input_file, plot_dir)

if __name__ == "__main__":
    main()
