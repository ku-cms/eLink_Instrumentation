# analyze.py

import plot
import tools
import numpy as np

# -------------------------------------
# TODO: 
# - plot DC resistance vs. Eye BERT area
# - plot impedance vs. DC resistance 
#
# DONE:
# - plot DC resistance vs. length
# - plot impedance area vs. length
# - plot Eye BERT area vs. length
# - plot RD53A Min TAP0 vs. length
# - plot RD53A Min TAP0 vs. Eye BERT area
# - plot impedance vs. Eye BERT area
# - make function to get x, y, and y_err values for x = length
# - do not use 'inf' or 'nan' values
# - write number of e-links included in plot
# - require gauge to be 36
# -------------------------------------

# given column name, return column index (starting from 0)
# based on TP_Cables_Production2020_2023 spreadsheet (version from March 6, 2023), data for Type 1 cables
def getColumnNum(name):
    result = -1
    column_map = {
        "cable_name"                : 0,
        "cable_number"              : 6,
        "type"                      : 7,
        "gauge"                     : 8,
        "length"                    : 9,
        "eye_bert_area_D3"          : 10,
        "eye_bert_area_D2"          : 11,
        "eye_bert_area_D1"          : 12,
        "eye_bert_area_D0"          : 13,
        "eye_bert_area_CMD"         : 14,
        "DC_4pt_resistance_D3_N"    : 21,
        "DC_4pt_resistance_D3_P"    : 22,
        "DC_4pt_resistance_D2_N"    : 23,
        "DC_4pt_resistance_D2_P"    : 24,
        "DC_4pt_resistance_D1_N"    : 25,
        "DC_4pt_resistance_D1_P"    : 26,
        "DC_4pt_resistance_D0_N"    : 27,
        "DC_4pt_resistance_D0_P"    : 28,
        "DC_4pt_resistance_CMD_N"   : 29,
        "DC_4pt_resistance_CMD_P"   : 30,
        "impedance_2to5ns_CMD"      : 34,
        "impedance_2to5ns_D0"       : 35,
        "impedance_2to5ns_D1"       : 36,
        "impedance_2to5ns_D2"       : 37,
        "impedance_2to5ns_D3"       : 38,
        "RD53A_MinTAP0_D0"          : 48,
        "RD53A_MinTAP0_D3"          : 50,
    }
    if name in column_map:
        result = column_map[name]
    else: 
        print("ERROR in getColumnNum(): the name '{0}' is not a valid column!".format(name))
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

# get cable gauges
def getGauges(data):
    result = {}
    cable_number_index  = getColumnNum("cable_number")
    gauge_index         = getColumnNum("gauge")
    for row in data:
        cable_number    = row[cable_number_index]
        gauge           = row[gauge_index]
        valid_cable     = tools.is_int(cable_number)
        valid_gauge     = tools.is_int(gauge)
        if valid_cable and valid_gauge:
            cable_number    = int(cable_number)
            gauge           = int(gauge)
            result[cable_number] = gauge
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
        valid_values    = tools.validValues(raw_values)
        if valid_cable and valid_values:
            cable_number = int(cable_number)
            values  = tools.convertToFloats(raw_values)
            mean    = np.mean(values) 
            std     = np.std(values) 
            result[cable_number] = {}
            result[cable_number]["mean"]    = mean
            result[cable_number]["std"]     = std

    return result

# get x, y, and y_err values for x = length
def getXYValuesForLengths(gauge_map, length_map, value_map, max_rel_err):
    verbose = False
    x_vals = []
    y_vals = []
    y_errs = []

    # get list of cables present in both dictionaries
    cables = tools.getMatchingKeys(length_map, value_map)
    
    for cable_number in cables:
        gauge   = gauge_map[cable_number]
        length  = length_map[cable_number]
        mean    = value_map[cable_number]["mean"]
        std     = value_map[cable_number]["std"]
        rel_err = std / mean
        # require gauge = 36
        if gauge == 36:
            if verbose:
                print("cable number: {0}, length: {1} m, mean: {2:.1f}, std: {3:.1f}, rel_err: {4:.3f}".format(cable_number, length, mean, std, rel_err))
            # do not include e-link if relative error is too large
            if rel_err > max_rel_err:
                print("WARNING: not including e-link {0}, length {1} m due to a large relative error: {2:.3f}".format(cable_number, length, rel_err))
            else:
                x_vals.append(length)
                y_vals.append(mean)
                y_errs.append(std)
    
    print("Number of values: {0}".format(len(x_vals)))
    return x_vals, y_vals, y_errs

# get x, y, and y_err values general x and y
def getXYValuesGeneral(gauge_map, x_value_map, y_value_map, max_rel_err):
    verbose = False
    x_vals = []
    y_vals = []
    y_errs = []
    
    # get list of cables present in both dictionaries
    cables = tools.getMatchingKeys(x_value_map, y_value_map)
    
    for cable_number in cables:
        gauge       = gauge_map[cable_number]
        x_mean      = x_value_map[cable_number]["mean"]
        x_std       = x_value_map[cable_number]["std"]
        y_mean      = y_value_map[cable_number]["mean"]
        y_std       = y_value_map[cable_number]["std"]
        x_rel_err   = x_std / x_mean
        y_rel_err   = y_std / y_mean
        # require gauge = 36
        if gauge == 36:
            if verbose:
                print("cable number: {0}, x_mean: {1:.1f}, x_std: {2:.1f}, x_rel_err: {3:.3f}, y_mean: {4:.1f}, y_std: {5:.1f}, y_rel_err: {6:.3f}".format(cable_number, x_mean, x_std, x_rel_err, y_mean, y_std, y_rel_err))
            # do not include e-link if relative error is too large
            if x_rel_err > max_rel_err:
                print("WARNING: not including e-link {0} due to a large x value relative error: {1:.3f}".format(cable_number, x_rel_err))
            if y_rel_err > max_rel_err:
                print("WARNING: not including e-link {0} due to a large y value relative error: {1:.3f}".format(cable_number, y_rel_err))
            else:
                x_vals.append(x_mean)
                y_vals.append(y_mean)
                y_errs.append(y_std)
    
    print("Number of values: {0}".format(len(x_vals)))
    return x_vals, y_vals, y_errs

# ----------------------------------- #
# --- Plot measurements vs length --- # 
# ----------------------------------- #

# plot resistance vs length
def plot_resistance_vs_length(gauges, lengths, resistances, plot_dir):
    print(" - Plotting resistance vs. length.")
    
    #max_rel_err = 0.20
    max_rel_err = 0.30
    #max_rel_err = 1.00
    x_vals, y_vals, y_errs = getXYValuesForLengths(gauges, lengths, resistances, max_rel_err) 

    output_file = "{0}/resistance_vs_length.pdf".format(plot_dir)
    title   = "DC 4-point Resistance"
    x_label = "length (m)"
    y_label = "Avg. resistance (ohms)"
    x_lim   = [0.0, 2.5]
    y_lim   = [0.0, 5.0]
    plot.plot(x_vals, y_vals, y_errs, output_file, title, x_label, y_label, x_lim, y_lim)

# plot impedance vs length
def plot_impedance_vs_length(gauges, lengths, impedances, plot_dir):
    print(" - Plotting impedance vs. length.")
    
    #max_rel_err = 0.20
    max_rel_err = 0.30
    #max_rel_err = 1.00
    x_vals, y_vals, y_errs = getXYValuesForLengths(gauges, lengths, impedances, max_rel_err) 

    output_file = "{0}/impedance_vs_length.pdf".format(plot_dir)
    title   = "Impedance"
    x_label = "length (m)"
    y_label = "Avg. impedance (ohms)"
    x_lim   = [0.0, 2.5]
    y_lim   = [0.0, 200.0]
    plot.plot(x_vals, y_vals, y_errs, output_file, title, x_label, y_label, x_lim, y_lim)

# plot area vs length
def plot_area_vs_length(gauges, lengths, eye_bert_areas, plot_dir):
    print(" - Plotting Eye BERT area vs. length.")

    #max_rel_err = 0.20
    max_rel_err = 0.30
    #max_rel_err = 1.00
    x_vals, y_vals, y_errs = getXYValuesForLengths(gauges, lengths, eye_bert_areas, max_rel_err) 
    
    output_file = "{0}/eye_bert_area_vs_length.pdf".format(plot_dir)
    title       = "Eye BERT Area"
    x_label     = "length (m)"
    y_label     = "Avg. Eye BERT area"
    x_lim       = [0.0, 2.5]
    y_lim       = [0.0, 8.0e4]
    
    plot.plot(x_vals, y_vals, y_errs, output_file, title, x_label, y_label, x_lim, y_lim)

# plot RD53A_MinTAP0 vs length
def plot_RD53A_MinTAP0_vs_length(gauges, lengths, RD53A_MinTAP0s, plot_dir):
    print(" - Plotting RD53A MinTAP0 vs. length.")
    
    #max_rel_err = 0.20
    max_rel_err = 0.30
    #max_rel_err = 1.00
    x_vals, y_vals, y_errs = getXYValuesForLengths(gauges, lengths, RD53A_MinTAP0s, max_rel_err) 

    output_file = "{0}/RD53A_MinTAP0_vs_length.pdf".format(plot_dir)
    title   = "RD53A BERT TAP0 Scans"
    x_label = "length (m)"
    y_label = "Avg. TAP0 for BER = 1e-10"
    x_lim   = [0.0, 2.5]
    y_lim   = [0.0, 400.0]
    plot.plot(x_vals, y_vals, y_errs, output_file, title, x_label, y_label, x_lim, y_lim)

# ----------------------------------------- #
# --- Plot measurements vs measurements --- # 
# ----------------------------------------- #

# plot RD53A_MinTAP0 vs area
def plot_RD53A_MinTAP0_vs_area(gauges, eye_bert_areas, RD53A_MinTAP0s, plot_dir):
    print(" - Plotting RD53A MinTAP0 vs. area.")
    
    #max_rel_err = 0.20
    max_rel_err = 0.30
    #max_rel_err = 1.00
    x_vals, y_vals, y_errs = getXYValuesGeneral(gauges, eye_bert_areas, RD53A_MinTAP0s, max_rel_err) 

    output_file = "{0}/RD53A_MinTAP0_vs_area.pdf".format(plot_dir)
    title   = "RD53A BERT TAP0 Scans"
    x_label = "Avg. Eye BERT area"
    y_label = "Avg. TAP0 for BER = 1e-10"
    x_lim   = [2.5e4, 6.5e4]
    y_lim   = [0.0, 400.0]
    plot.plot(x_vals, y_vals, y_errs, output_file, title, x_label, y_label, x_lim, y_lim)

# plot impedance vs area
def plot_impedance_vs_area(gauges, eye_bert_areas, impedances, plot_dir):
    print(" - Plotting impedance vs. area.")
    
    #max_rel_err = 0.20
    max_rel_err = 0.30
    #max_rel_err = 1.00
    x_vals, y_vals, y_errs = getXYValuesGeneral(gauges, eye_bert_areas, impedances, max_rel_err) 

    output_file = "{0}/impedance_vs_area.pdf".format(plot_dir)
    title   = "Impedance"
    x_label = "Avg. Eye BERT area"
    y_label = "Avg. impedance (ohms)"
    x_lim   = [2.5e4, 6.5e4]
    y_lim   = [0.0, 200.0]
    plot.plot(x_vals, y_vals, y_errs, output_file, title, x_label, y_label, x_lim, y_lim)

# analyze data from input file
def analyze(input_file, plot_dir):
    print(" - Analyzing input file '{0}'".format(input_file))
    tools.makeDir(plot_dir)
    data    = tools.getData(input_file)
    gauges  = getGauges(data)
    lengths = getLengths(data)

    # Get mean values
    column_names    = ["DC_4pt_resistance_CMD_P", "DC_4pt_resistance_CMD_N", "DC_4pt_resistance_D0_P", "DC_4pt_resistance_D0_N", "DC_4pt_resistance_D1_P", "DC_4pt_resistance_D1_N", "DC_4pt_resistance_D2_P", "DC_4pt_resistance_D2_N", "DC_4pt_resistance_D3_P", "DC_4pt_resistance_D3_N"]
    resistances     = getMeanValues(data, column_names)
    column_names    = ["impedance_2to5ns_CMD", "impedance_2to5ns_D0", "impedance_2to5ns_D1", "impedance_2to5ns_D2", "impedance_2to5ns_D3"]
    impedances      = getMeanValues(data, column_names)
    column_names    = ["eye_bert_area_CMD", "eye_bert_area_D0", "eye_bert_area_D1", "eye_bert_area_D2", "eye_bert_area_D3"]
    eye_bert_areas  = getMeanValues(data, column_names)
    column_names    = ["RD53A_MinTAP0_D0", "RD53A_MinTAP0_D3"]
    RD53A_MinTAP0s  = getMeanValues(data, column_names)

    # Make plots
    
    # resistance vs length
    plot_resistance_vs_length(gauges, lengths, resistances, plot_dir)
    
    # impedance vs length
    plot_impedance_vs_length(gauges, lengths, impedances, plot_dir)
    
    # area vs length
    plot_area_vs_length(gauges, lengths, eye_bert_areas, plot_dir)
    
    # RD53A Min TAP0 vs length
    plot_RD53A_MinTAP0_vs_length(gauges, lengths, RD53A_MinTAP0s, plot_dir)
    
    # RD53A Min TAP0 vs area
    plot_RD53A_MinTAP0_vs_area(gauges, eye_bert_areas, RD53A_MinTAP0s, plot_dir)
    
    # impedance vs area
    plot_impedance_vs_area(gauges, eye_bert_areas, impedances, plot_dir)
    

def main():
    input_file  = "data/TP_Type1_Cables_Production2020_2023_03_06.csv"
    plot_dir    = "plots"
    analyze(input_file, plot_dir)

if __name__ == "__main__":
    main()

