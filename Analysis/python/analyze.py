# analyze.py

import tools

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

def analyze(input_file):
    print("Analyzing input file '{0}'".format(input_file))
    #tools.printData(input_file)
    data = tools.getData(input_file)
    #print(data[0])
    length_index = getColumnNum("length")
    eye_bert_area_CMD_index = getColumnNum("eye_bert_area_CMD")
    oops = getColumnNum("oops")
    #print(length_index)
    for row in data:
        #print(row)
        #print(len(row))
        #print(row[length_index])
        print("{0} : {1}".format(row[length_index], row[eye_bert_area_CMD_index]))

def main():
    input_file = "data/TP_Type1_Cables_Production2020_2023_03_06.csv"
    analyze(input_file)

if __name__ == "__main__":
    main()

