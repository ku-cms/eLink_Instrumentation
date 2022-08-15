# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 20:27:09 2022

@author: japat
"""

import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stats
from scipy.stats import sem
from iminuit.cost import LeastSquares
from iminuit import Minuit
from distutils.log import error
from pprint import pprint

df = pd.read_excel('areas.xlsx', header = 0, usecols = 'A:F')
print(df)

#graph of all areas vs length

x = [0.35, 0.80, 1.0, 1.4, 1.6, 1.8, 2.0]
y = df['D3']
z = df['D2']
a = df['D1']
b = df['D0'] 
c = df['CMD']
d_err = df['D3'].sem()
z_err = df['D2'].sem()
a_err = df['D1'].sem()
b_err = df['D0'].sem()
c_err = df['CMD'].sem()

height_list = [y, z, a, b, c]
error_list = [z_err,a_err,b_err,c_err]
x_list = [x, x, x, x, x]

#f = plt.figure()
#f.set_figheight(10)

#plt.scatter(x, y, s = 100)
#plt.scatter(x, z, s = 100)
#plt.scatter(x, a, s = 100)
#plt.scatter(x, b, s = 100)
#plt.scatter(x, c, s = 100)

#plt.ylim(25000, 70000)
#plt.legend(['D3', 'D2', 'D1', 'D0', 'CMD'])
#plt.title('Area vs Length')
#plt.xlabel('Length (m)')
#plt.ylabel('Area')
#plt.savefig('Area_vs_length_1.png')
#plt.show()

len35 = df.drop(index = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,38])
len80 = df.drop(index = [0, 1, 2, 8, 9, 10, 11, 12,13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38])
len100 = df.drop(index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37, 38])
len140 = df.drop(index = [0,1,2,3,4,5,6,7,8,9,10,11,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37, 38])
len160 = df.drop(index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,27, 28,29,30,31,32,33,34,35,36,37,38])
len180 = df.drop(index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,37, 38])
len200 = df.drop(index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36])

print(len200)

cmd_avg35 = len35['CMD'].mean()
d0_avg35 = len35['D0'].mean()
d1_avg35 = len35['D1'].mean()
d2_avg35 = len35['D2'].mean()
d3_avg35 = len35['D3'].mean()
list35 = [cmd_avg35, d0_avg35, d1_avg35, d2_avg35]
avg35 = stats.mean(list35)
print(avg35)

cmd_avg80 = len80['CMD'].mean()
d0_avg80 = len80['D0'].mean()
d1_avg80 = len80['D1'].mean()
d2_avg80 = len80['D2'].mean()
d3_avg80 = len80['D3'].mean()
list80 = [cmd_avg80, d0_avg80, d1_avg80, d2_avg80]
avg80 = stats.mean(list80)
print(avg80)

cmd_avg100 = len100['CMD'].mean()
d0_avg100 = len100['D0'].mean()
d1_avg100 = len100['D1'].mean()
d2_avg100 = len100['D2'].mean()
d3_avg100 = len100['D3'].mean()
list100 = [cmd_avg100, d0_avg100, d1_avg100, d2_avg100]
avg100 = stats.mean(list100)
print(avg100)

cmd_avg140 = len140['CMD'].mean()
d0_avg140 = len140['D0'].mean()
d1_avg140 = len140['D1'].mean()
d2_avg140 = len140['D2'].mean()
d3_avg140 = len140['D3'].mean()
list140 = [cmd_avg140, d0_avg140, d1_avg140, d2_avg140]
avg140 = stats.mean(list140)
print(avg140)

cmd_avg160 = len160['CMD'].mean()
d0_avg160 = len160['D0'].mean()
d1_avg160 = len160['D1'].mean()
d2_avg160 = len160['D2'].mean()
d3_avg160 = len160['D3'].mean()
list160 = [cmd_avg160, d0_avg160, d1_avg160, d2_avg160]
avg160 = stats.mean(list160)
print(avg160)

cmd_avg180 = len180['CMD'].mean()
d0_avg180 = len180['D0'].mean()
d1_avg180 = len180['D1'].mean()
d2_avg180 = len180['D2'].mean()
d3_avg180 = len180['D3'].mean()
list180 = [cmd_avg180, d0_avg180, d1_avg180, d2_avg180]
avg180 = stats.mean(list180)
print(avg180)

cmd_avg200 = len200['CMD'].mean()
d0_avg200 = len200['D0'].mean()
d1_avg200 = len200['D1'].mean()
d2_avg200 = len200['D2'].mean()
d3_avg200 = len200['D3'].mean()
list200 = [cmd_avg200, d0_avg200, d1_avg200, d2_avg200]
avg200 = stats.mean(list200)
print(avg200)

len = [0.35, 0.80, 1.00, 1.40, 1.60, 1.80, 2.00]
avg = [avg35, avg80, avg100, avg140, avg160, avg180, avg200]

e, f = np.polyfit(len, avg, 1)

f = plt.figure()
f.set_figheight(10)

#plt.scatter(0.35, cmd_avg35, s = 100)
#plt.scatter(0.35, d0_avg35, s =100)
#plt.scatter(0.35, d1_avg35, s =100)
#plt.scatter(0.35, d2_avg35, s = 100)
#plt.scatter(0.35, d3_avg35, s = 100)
#plt.scatter(0.80, cmd_avg80, s =100)
#plt.scatter(0.80, d0_avg80, s = 100)
#plt.scatter(0.80, d1_avg80, s = 100)
#plt.scatter(0.80, d2_avg80, s = 100)
#plt.scatter(0.80, d3_avg80, s = 100)
#plt.scatter(1.00, cmd_avg100, s = 100)
#plt.scatter(1.00, d0_avg100, s = 100)
#plt.scatter(1.00, d1_avg100,s = 100)
#plt.scatter(1.00, d2_avg100,s = 100)
#plt.scatter(1.00, d3_avg100,s = 100)
#plt.scatter(1.40, cmd_avg140,s = 100)
#plt.scatter(1.40, d0_avg140,s = 100)
#plt.scatter(1.40, d1_avg140,s = 100)
#plt.scatter(1.40, d2_avg140,s = 100)
#plt.scatter(1.40, d3_avg140,s = 100)
#plt.scatter(1.60, cmd_avg160,s = 100)
#plt.scatter(1.60, d0_avg160,s = 100)
#plt.scatter(1.60, d1_avg160,s = 100)
#plt.scatter(1.60, d2_avg160,s = 100)
#plt.scatter(1.60, d3_avg160,s = 100)
#plt.scatter(1.80, cmd_avg180,s = 100)
#plt.scatter(1.80, d0_avg180,s = 100)
#plt.scatter(1.80, d1_avg180,s = 100)
#plt.scatter(1.80, d2_avg180,s = 100)
#plt.scatter(1.80, d3_avg180,s = 100)
#plt.scatter(2.00, cmd_avg200,s = 100)
#plt.scatter(2.00, d0_avg200,s = 100)
#plt.scatter(2.00, d1_avg200,s = 100)
#plt.scatter(2.00, d2_avg200,s = 100)
#plt.scatter(2.00, d3_avg200,s = 100)
#plt.title('Avg Area per Channel vs Length')
#plt.xlabel('Length (m)')
#plt.ylabel('Area')
#plt.legend(['CMD', 'D0', 'D1', 'D2', 'D3'])
#plt.savefig('Channels_vs_Length_1.png')
#plt.show()



std35 = stats.stdev(list35)
std80 = stats.stdev(list80)
std100 = stats.stdev(list100)
std140 = stats.stdev(list140)
std160 = stats.stdev(list160)
std180 = stats.stdev(list180)
std200 = stats.stdev(list100)
std = [std35, std80, std100, std140, std160, std180, std200]
err35 = sem(list35)
print(err35)
err80 = sem(list80)
err100 = sem(list100)
err140 = sem(list140)
err160 = sem(list160)
err180 = sem(list180)
err200 = sem(list200)
error = [err35, err80, err100, err140, err160, err180, err200]
print(error)
errbar = np.array(error)
err = sem(avg)
x_data = len
y = avg

f = plt.figure()
f.set_figwidth(10)
f.set_figheight(10)



def line(x, a, b):
    return a + b*x
least_squares = LeastSquares(x_data, y, error, line)

m = Minuit(least_squares,a=0,b=0)
m.migrad() # finds minimum of least_squares function
m.hesse() 

plt.plot(np.linspace(0.35, 2.00), line(np.linspace(0.35, 2.00), *m.values), label="fit")
plt.errorbar(x_data,y ,yerr=error, fmt="o", label="data")
print(x_data)
print(m.nfit)
print(m.fval)
length = 7
r = m.fval / (length - m.nfit)
fit_info = [ f"$\\chi^2$ / $n_\\mathrm{{dof}}$ = {r}",]
for p, v, e in zip(m.parameters, m.values, m.errors):
    fit_info.append(f"{p} = ${v:.3f} \\pm {e:.3f}$")

plt.legend(title="\n".join(fit_info));

plt.title('Average Area of vs Length', fontsize = 21)
plt.xlabel('Length (m)', fontsize = 14)
plt.ylabel('Average Area (of Eye Diagrams)' , fontsize = 14)
plt.savefig('Avg_Area_vs_Length_1.png')
#plt.show()
plt.clf()











#std = [std35, std80, std100, std140, std160, std180, std200]
stderr = stats.stdev(std)
plt.scatter(0.35, std35)
plt.scatter(0.80, std80)
plt.scatter(1.00, std100)
plt.scatter(1.40, std140)
plt.scatter(1.60, std160)
plt.scatter(1.80, std180)
plt.scatter(2.00, std200)
plt.title('Standard Deviation of Area vs Length')
plt.xlabel('Length (m)')
plt.ylabel('Standard Deviation of Area')
plt.errorbar(0.35, std35, stderr)
plt.errorbar(0.80, std80, stderr)
plt.errorbar(1.00, std100, stderr)
plt.errorbar(1.40, std140, stderr)
plt.errorbar(1.60, std160, stderr)
plt.errorbar(1.80, std180, stderr)
plt.errorbar(2.00, std200, stderr)
plt.savefig('STD_Area_vs_Length.png')
#.show()








