# analyzeElinkProduction.py

import plot
import tools
import numpy as np
import pandas as pd

def createSampleData():
    dates = pd.date_range(start="2025-01-01", periods=10, freq='W')
    weekly_production = np.random.randint(0, 20, size=len(dates))
    return (dates, weekly_production)

def analyzeElinkProduction(input_file, plot_dir):
    print("Analyzing e-link production...")
    print(f" - input file: {input_file}")
    print(f" - plot directory: {plot_dir}")
    
    tools.makeDir(plot_dir)

    dates, weekly_production = createSampleData()
    cumulative_production = np.cumsum(weekly_production)

    plot_name = "cumulative_plot_example"
    title = "Cumulative Plot Example"
    x_label = "Time"
    y_label = "Number of units"
    x_lim = []
    y_lim = []
    plot.makeCumulativePlot(dates, cumulative_production, plot_dir, plot_name, title, x_label, y_label, x_lim, y_lim)
    
    print("Done!")

def main():
    input_file  = ""
    plot_dir    = "elink_production_plots"
    analyzeElinkProduction(input_file, plot_dir)

if __name__ == "__main__":
    main()
