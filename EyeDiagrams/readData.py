import pandas as pd


type1_cols_height_34 = [3, 4, 5]
type1_rows_height_34 = [0, 1, 2]
type1_height_34g = pd.read_excel('Data1.xlsx', sheet_name ='Data', header = None, usecols=type1_cols_height_34, skiprows = type1_rows_height_34)
type1_height_34g = type1_height_34g.drop(range(11, 31))
#print(y_height_34g)

type1_cols_width_34 = [6, 7, 8]
type1_rows_width_34 = [0, 1, 2]
type1_width_34g = pd.read_excel('Data1.xlsx', sheet_name ='Data', header = None, usecols=type1_cols_width_34, skiprows = type1_rows_width_34)
type1_width_34g = type1_width_34g.drop(range(11, 31))
#print(y_width_34g)

test_cols_height_34 = [3, 4, 5, 6]
test_rows_height_34 = range(0, 16)
test_height_34g = pd.read_excel('Data1.xlsx', sheet_name ='Data', header = None, usecols=test_cols_height_34, skiprows = test_rows_height_34)
test_height_34g = test_height_34g.drop(range(6, 18))
#print(L_heights_34g)

test_cols_width_34 = [7, 8, 9, 10]
test_rows_width_34 = range(0, 16)
test_width_34g = pd.read_excel('Data1.xlsx', sheet_name ='Data', header = None, usecols= test_cols_width_34, skiprows = test_rows_width_34)
test_width_34g = test_width_34g.drop(range(6, 18))
#print(L_width_34g)


#36

type3_cols_height_36 = [3, 4, 5, 6, 7, 8]
type3_rows_height_36 = range(0, 30)
type3_height_36g = pd.read_excel('Data1.xlsx', sheet_name ='Data', header = None, usecols=type3_cols_height_36, skiprows = type3_rows_height_36)
type3_height_36g = type3_height_36g.drop(range(2, 5))
#print(y_heights_36g)

type3_cols_width_36 = [9, 10, 11, 12, 13, 14]
type3_rows_width_36 = range(0, 30)
type3_width_36g = pd.read_excel('Data1.xlsx', sheet_name ='Data', header = None, usecols=type3_cols_width_36, skiprows = type3_rows_width_36)
type3_width_36g = type3_width_36g.drop(range(2, 5))
#print(y_width_36g)

type4_cols_height_36 = [3, 4, 5, 6, 7, 8]
type4_rows_height_36 = range(0, 35)
type4_height_36g = pd.read_excel('Data1.xlsx', sheet_name ='Data', header = None, usecols=type4_cols_height_36, skiprows = type4_rows_height_36)

#print(L_height_36g)

type4_cols_width_36 = [9, 10, 11, 12, 13, 14]
type4_rows_width_36 = range(0, 35)
type4_width_36g = pd.read_excel('Data1.xlsx', sheet_name ='Data', header = None, usecols= type4_cols_width_36, skiprows = type4_rows_width_36)

#print(L_width_36g)
n_rows = type1_height_34g.shape[0]
type1_height_for_34g = []

for i in range(n_rows):
    type1_height_for_34g.append(tuple(type1_height_34g.values[i]))
print(type1_height_for_34g)

n_rows = test_height_34g.shape[0]
test_height_for_34g = []

for i in range(n_rows):
    test_height_for_34g.append(tuple(test_height_34g.values[i]))
print(test_height_for_34g)

n_rows = type3_height_36g.shape[0]
type3_height_for_36g = []

for i in range(n_rows):
    type3_height_for_36g.append(tuple(type3_height_36g.values[i]))
print(type3_height_for_36g)

n_rows = type4_height_36g.shape[0]
type4_height_for_36g = []

for i in range(n_rows):
    type4_height_for_36g.append(tuple(type4_height_36g.values[i]))
print(type4_height_for_36g)

