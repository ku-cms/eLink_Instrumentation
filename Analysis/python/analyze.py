# analyze.py

import plot
import tools
import numpy as np

def getColumnNum(name):
    result = -1
    column_map = {
        "cable_name"        : 0,
        "cable_number"      : 6,
        "type"              : 7,
        "gauge"             : 8,
        "length"            : 9,
        "eye_bert_area_D3"  : 10,
        "eye_bert_area_D2"  : 11,
        "eye_bert_area_D1"  : 12,
        "eye_bert_area_D0"  : 13,
        "eye_bert_area_CMD" : 14,
    }
    if name in column_map:
        result = column_map[name]
    else: 
        print("ERROR in getColumnNum(): the name '{0}' is not a valid column!".format(name))
    return result

# check that all areas are floats
def validAreas(areas):
    for area in areas:
        if not tools.is_float(area):
            return False
    return True

# convert areas to floats
def convertAreas(areas):
    result = [float(area) for area in areas]
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

# get cable eye bert areas
def getAreas(data):
    result = {}

    cable_number_index      = getColumnNum("cable_number")
    eye_bert_area_CMD_index = getColumnNum("eye_bert_area_CMD")
    eye_bert_area_D0_index  = getColumnNum("eye_bert_area_D0")
    eye_bert_area_D1_index  = getColumnNum("eye_bert_area_D1")
    eye_bert_area_D2_index  = getColumnNum("eye_bert_area_D2")
    eye_bert_area_D3_index  = getColumnNum("eye_bert_area_D3")
    
    for row in data:
        cable_number = row[cable_number_index]
        raw_areas = []
        raw_areas.append(row[eye_bert_area_CMD_index])
        raw_areas.append(row[eye_bert_area_D0_index])
        raw_areas.append(row[eye_bert_area_D1_index])
        raw_areas.append(row[eye_bert_area_D2_index])
        raw_areas.append(row[eye_bert_area_D3_index])
        # check that cable number and areas are valid
        valid_cable = tools.is_int(cable_number)
        valid_areas = validAreas(raw_areas)
        if valid_cable and valid_areas:
            cable_number = int(cable_number)
            areas   = convertAreas(raw_areas)
            mean    = np.mean(areas) 
            std     = np.std(areas) 
            result[cable_number] = {}
            result[cable_number]["eye_bert_area_mean"]    = mean
            result[cable_number]["eye_bert_area_std"]     = std

    return result

def plot_area_vs_length(lengths, eye_bert_areas, plot_dir):
    x_vals = []
    y_vals = []
    y_errs = []
    for cable_number in eye_bert_areas:
        length = lengths[cable_number]
        eye_bert_area_mean  = eye_bert_areas[cable_number]["eye_bert_area_mean"]
        eye_bert_area_std   = eye_bert_areas[cable_number]["eye_bert_area_std"]
        rel_err = eye_bert_area_std / eye_bert_area_mean
        print("cable number: {0}, length: {1} m, eye_bert_area_mean: {2:.1f}, eye_bert_area_std: {3:.1f}, rel_err: {4:.3f}".format(cable_number, length, eye_bert_area_mean, eye_bert_area_std, rel_err))
        # do not include e-link if relative error is too large
        if rel_err > 0.10:
            print("WARNING: not including e-link {0}, length {1} m due to a large relative error: {2:.3f}".format(cable_number, length, rel_err))
        else:
            x_vals.append(length)
            y_vals.append(eye_bert_area_mean)
            y_errs.append(eye_bert_area_std)

    output_file = "{0}/eye_bert_area_vs_length.pdf".format(plot_dir)
    title   = "Eye BERT Areas"
    x_label = "length (m)"
    y_label = "Eye BERT area"
    plot.plot(x_vals, y_vals, y_errs, output_file, title, x_label, y_label)


def analyze(input_file, plot_dir):
    print("Analyzing input file '{0}'".format(input_file))
    data = tools.getData(input_file)

    tools.makeDir(plot_dir)
    
    lengths = getLengths(data)
    eye_bert_areas = getAreas(data)

    plot_area_vs_length(lengths, eye_bert_areas, plot_dir)

def main():
    input_file  = "data/TP_Type1_Cables_Production2020_2023_03_06.csv"
    plot_dir    = "plots"
    analyze(input_file, plot_dir)

if __name__ == "__main__":
    main()

