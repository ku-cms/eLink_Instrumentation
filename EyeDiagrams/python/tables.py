# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv
import os
import pandas as pd

#print('Enter the name of the Cable Folder:')
#folder = input()
df = pd.DataFrame(columns = ['Cable', 'D3', 'D2', 'D1', 'D0', 'CMD'])

def getArea(files):
    with open(files) as file_obj:
        reader_obj = csv.reader(file_obj)
        df = pd.DataFrame(reader_obj)
        cell = df.iloc[6, 1]
        return(cell)
folder = []
directory = os.listdir()
ext = ('.csv')
index = 0
fileLen = len(os.listdir()) - 2
csvfiles = os.listdir()
files_txt = [i for i in csvfiles if i.endswith('.csv')]
for i in range(0,len(files_txt),5):
    for x in range(5):
       files = files_txt
       filename = str(files[i + x])
       cable_number = filename.split('_')[1]
       df.at[index, 'Cable'] = cable_number
    
       channel = filename.split('_')[2]
       area = getArea(filename)
       
       if channel == 'CMD':
           df.at[index,'CMD'] = area
       if channel == 'D0':
           df.at[index, 'D0'] = area
       if channel == 'D1':
           df.at[index,'D1'] = area
       if channel == 'D2':
           df.at[index, 'D2'] = area
       if channel == 'D3':
           df.at[index,'D3'] = area
       else:
          continue
    index = index +1
        
#
print(df)



df.to_excel("areas.xlsx", index = None)


