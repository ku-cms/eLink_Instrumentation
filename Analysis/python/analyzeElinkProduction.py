# analyzeElinkProduction.py

import plot
import tools
import numpy as np
import pandas as pd

# ---------------------------------------------
# TODO:
# - Convert frequency of date to date with unit count
# - Select production e-links: e-link number >= 700
# - Use data = list(reader) to load csv
# - Plot one line from data
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
# ---------------------------------------------

def createSampleData():
    dates = pd.date_range(start="2025-01-01", periods=5, freq='W')
    production = np.random.randint(0, 20, size=len(dates))
    return (dates, production)

def loadElinkProductionData(input_file):
    data = tools.getData(input_file)
    
    headers = data[0]
    rows = data[1:]
    print(f"headers: {headers}")
    
    # Remove empty date entries
    dates = [row[1] for row in rows if row[1]]
    dates = pd.to_datetime(dates, format='%m-%d-%y')
    # FIXME: For every date, we are setting the number produced to 1 for testing.
    n = len(dates)
    production = [1] * n
    print(f"n: {n}")
    
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

def analyzeElinkProductionData(input_file, plot_dir):
    print("Analyzing e-link production data...")
    print(f" - input file: {input_file}")
    print(f" - plot directory: {plot_dir}")
    
    tools.makeDir(plot_dir)
    dates, production = loadElinkProductionData(input_file)
    cumulative_production = np.cumsum(production)
    print("e-link production data:")
    print(f" - dates: {dates}")
    print(f" - production: {production}")
    print(f" - cumulative_production: {cumulative_production}")

    plot_name = "elink_production"
    title = "Cumulative e-link production"
    x_label = "Time (week)"
    y_label = "Number of e-links"
    x_lim = []
    y_lim = []
    plot.makeCumulativePlot(dates, cumulative_production, plot_dir, plot_name, title, x_label, y_label, x_lim, y_lim)
    
    print("Done!")

def main():
    plot_dir    = "sample_data_plots"
    analyzeSampleData(plot_dir)
    
    input_file  = "data/Harness_Serial_Number_2025_05_21.csv"
    plot_dir    = "elink_production_plots"
    analyzeElinkProductionData(input_file, plot_dir)

if __name__ == "__main__":
    main()
