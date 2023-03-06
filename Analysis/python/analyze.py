# analyze.py

import plot
import tools
import numpy as np

def getColumnNum(name):
    result = -1
    column_map = {
        "cable_name"            : 0,
        "cable_number"          : 6,
        "type"                  : 7,
        "gauge"                 : 8,
        "length"                : 9,
        "eye_bert_area_D3"      : 10,
        "eye_bert_area_D2"      : 11,
        "eye_bert_area_D1"      : 12,
        "eye_bert_area_D0"      : 13,
        "eye_bert_area_CMD"     : 14,
        "impedance_2to5ns_CMD"  : 34,
        "impedance_2to5ns_D0"   : 35,
        "impedance_2to5ns_D1"   : 36,
        "impedance_2to5ns_D2"   : 37,
        "impedance_2to5ns_D3"   : 38,
    }
    if name in column_map:
        result = column_map[name]
    else: 
        print("ERROR in getColumnNum(): the name '{0}' is not a valid column!".format(name))
    return result

# check that all values are floats
def validValues(values):
    for value in values:
        if not tools.is_float(value):
            return False
    return True

# convert values to floats
def convertToFloats(values):
    result = [float(value) for value in values]
    return result

# get cable lengths
def getLengths(data):
    result = {}
    cable_number_index  = getColumnNum("cable_number")
    length_index        = getColumnNum("length")
    for row in data:
        cable_number    = row[cable_number_index]
        length          = row[length_index]
        valid_cable     = tools.is_int(cable_number)
        valid_length    = tools.is_float(length)
        if valid_cable and valid_length:
            cable_number    = int(cable_number)
            length          = float(length)
            result[cable_number] = length
    return result

# get mean, std from values of specified columns
def getMeanValues(data, column_names):
    result = {}

    cable_number_index = getColumnNum("cable_number")
    value_indices = [getColumnNum(name) for name in column_names]
    
    for row in data:
        cable_number = row[cable_number_index]
        raw_values = [row[i] for i in value_indices]
        
        # check that cable number and values are valid
        valid_cable     = tools.is_int(cable_number)
        valid_values    = validValues(raw_values)
        if valid_cable and valid_values:
            cable_number = int(cable_number)
            values  = convertToFloats(raw_values)
            mean    = np.mean(values) 
            std     = np.std(values) 
            result[cable_number] = {}
            result[cable_number]["mean"]    = mean
            result[cable_number]["std"]     = std

    return result

# plot area vs length
def plot_area_vs_length(lengths, eye_bert_areas, plot_dir):
    print(" - Plotting Eye BERT area vs. length.")
    x_vals = []
    y_vals = []
    y_errs = []
    for cable_number in eye_bert_areas:
        length  = lengths[cable_number]
        mean    = eye_bert_areas[cable_number]["mean"]
        std     = eye_bert_areas[cable_number]["std"]
        rel_err = std / mean
        print("cable number: {0}, length: {1} m, mean: {2:.1f}, std: {3:.1f}, rel_err: {4:.3f}".format(cable_number, length, mean, std, rel_err))
        # do not include e-link if relative error is too large
        if rel_err > 0.10:
            print("WARNING: not including e-link {0}, length {1} m due to a large relative error: {2:.3f}".format(cable_number, length, rel_err))
        else:
            x_vals.append(length)
            y_vals.append(mean)
            y_errs.append(std)

    output_file = "{0}/eye_bert_area_vs_length.pdf".format(plot_dir)
    title   = "Eye BERT Areas"
    x_label = "length (m)"
    y_label = "Eye BERT area"
    plot.plot(x_vals, y_vals, y_errs, output_file, title, x_label, y_label)

# plot impedance vs length
def plot_impedance_vs_length(lengths, impedances, plot_dir):
    print(" - Plotting impedance vs. length.")
    x_vals = []
    y_vals = []
    y_errs = []
    for cable_number in impedances:
        length  = lengths[cable_number]
        mean    = impedances[cable_number]["mean"]
        std     = impedances[cable_number]["std"]
        rel_err = std / mean
        print("cable number: {0}, length: {1} m, mean: {2:.1f}, std: {3:.1f}, rel_err: {4:.3f}".format(cable_number, length, mean, std, rel_err))
        # do not include e-link if relative error is too large
        if rel_err > 0.10:
            print("WARNING: not including e-link {0}, length {1} m due to a large relative error: {2:.3f}".format(cable_number, length, rel_err))
        else:
            x_vals.append(length)
            y_vals.append(mean)
            y_errs.append(std)

    output_file = "{0}/eye_bert_impedance_vs_length.pdf".format(plot_dir)
    title   = "Impedances"
    x_label = "length (m)"
    y_label = "impedance (ohms)"
    plot.plot(x_vals, y_vals, y_errs, output_file, title, x_label, y_label)

def analyze(input_file, plot_dir):
    print(" - Analyzing input file '{0}'".format(input_file))
    data = tools.getData(input_file)

    tools.makeDir(plot_dir)
    
    lengths = getLengths(data)
    
    column_names = ["eye_bert_area_CMD", "eye_bert_area_D0", "eye_bert_area_D1", "eye_bert_area_D2", "eye_bert_area_D3"]
    eye_bert_areas = getMeanValues(data, column_names)
    plot_area_vs_length(lengths, eye_bert_areas, plot_dir)
    
    column_names = ["impedance_2to5ns_CMD", "impedance_2to5ns_D0", "impedance_2to5ns_D1", "impedance_2to5ns_D2", "impedance_2to5ns_D3"]
    impedances = getMeanValues(data, column_names)
    plot_impedance_vs_length(lengths, impedances, plot_dir)

def main():
    input_file  = "data/TP_Type1_Cables_Production2020_2023_03_06.csv"
    plot_dir    = "plots"
    analyze(input_file, plot_dir)

if __name__ == "__main__":
    main()

