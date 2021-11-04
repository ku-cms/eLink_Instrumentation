# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 13:39:53 2021

@author: japat
"""
from tools import printData
from tools import getData
import numpy as np
import matplotlib.pyplot as plt
import os
import re

def getHeights(cable_data_csv):
    heights = []
    for i in range(len(cable_data_csv)):
        if i < 1:
            continue
        height = float(cable_data_csv[i][3])
        heights.append(height)
    return heights

#printData("../tables/Cable_121_EyeDiagrams.csv")
#printData("../HarnessSerialNumber.csv")
    
p = re.compile(r'\d+')
cable_nums = []
cable_data = {}
cable_heights = {}
means =[]
remove_zero = True
for filename in os.listdir("../tables"):
    if filename.endswith(".csv"):
        print(filename)
        cable_num = -1
        matches = p.findall(filename)
        if len(matches) == 1:
            cable_num = int(matches[0])
            cable_nums.append(cable_num)
        else:
            print("Error: Unique Number not found")
            print(matches)
            
        #TO DO: FIX CABLE HEIGHTS (they are currently overwritten for multiple measurements)
        
        cable_data[filename] = getData("../tables/" + filename)
        cable_heights[cable_num] = getHeights(cable_data[filename])
        print(cable_heights[cable_num])
        means.append(np.mean(cable_heights[cable_num]))
        print(np.std(cable_heights[cable_num]))

print(cable_nums)
print(np.mean(means))
#print(cable_heights[])
#print(np.mean(cable_heights))
#print(np.std(cable_heights))

cableInfo = getData("../HarnessSerialNumber.csv")
    
cableMap = {}

for i in range(len(cableInfo)):
    if i < 4:
        continue
    try:
        cableNumber = int(cableInfo[i][0])
    except:
        cableNumber = cableInfo[i][0]
    cableMap[cableNumber] = {}
    cableMap[cableNumber]["type"] = cableInfo[i][2]
    cableMap[cableNumber]["gauge"] = cableInfo[i][3]
    try:
        cableMap[cableNumber]["length"] = float(cableInfo[i][4])
    except:
        cableMap[cableNumber]["length"] = cableInfo[i][4]
 
cable_len = []
list_of_heights = []
cable_means = []
cable_std = []

for i in cable_nums:
    cable_len.append(cableMap[i]["length"])
    list_of_heights.append(cable_heights[i])
    temp_list = [] 
    for j in cable_heights[i]:
        if remove_zero:
            if j != 0 :
                temp_list.append(j)  
        else:
            temp_list.append(j)
    cable_means.append(np.mean(temp_list))
    cable_std.append(np.std(temp_list))
    
print(cable_len)
print(list_of_heights)
print(cable_means)
print(cable_std)

x = cable_len
y = cable_means

plt.scatter(x, y)
plt.errorbar(x, y, yerr= cable_std, fmt = "o")
plt.show()




































