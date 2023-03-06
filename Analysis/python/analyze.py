# analyze.py

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

# check that cable number is int
def validCable(cable_number):
    return tools.is_int(cable_number)

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
        valid_cable = validCable(cable_number)
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

def analyze(input_file):
    print("Analyzing input file '{0}'".format(input_file))
    #tools.printData(input_file)
    data = tools.getData(input_file)
    #print(data[0])
    length_index = getColumnNum("length")
    eye_bert_area_CMD_index = getColumnNum("eye_bert_area_CMD")
    #oops = getColumnNum("oops")


    #print(length_index)
    #for row in data:
        #print(row)
        #print(len(row))
        #print(row[length_index])
        #print("{0} : {1}".format(row[length_index], row[eye_bert_area_CMD_index]))
        #print("{0} : {1}".format(row[length_index], type(row[eye_bert_area_CMD_index])))
    
    eye_bert_areas = getAreas(data)

    for cable_number in eye_bert_areas:
        eye_bert_area_mean  = eye_bert_areas[cable_number]["eye_bert_area_mean"]
        eye_bert_area_std   = eye_bert_areas[cable_number]["eye_bert_area_std"]
        print("cable number: {0}, eye_bert_area_mean: {1:.1f}, eye_bert_area_std: {2:.1f}".format(cable_number, eye_bert_area_mean, eye_bert_area_std))

def main():
    input_file = "data/TP_Type1_Cables_Production2020_2023_03_06.csv"
    analyze(input_file)

if __name__ == "__main__":
    main()

