import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates  as mdates

input_data          = "raw_data_1.csv"
headers             = ['Time','Voltage','Jitter']
df                  = pd.read_csv(input_data, names=headers,index_col=0)
df["Voltagemod"]    = df["Time"] * 1000 / df["Voltage"]

print(df)
x = df['Time']
y = df['Jitter']
z = df['Voltagemod']

fig0 = plt.figure(figsize=(12,15))
fig0.patch.set_facecolor('xkcd:black')
plt.style.use('dark_background')
ax0 = plt.subplot(1,1,1)
#ax1= plt.subplot(2,2,2)
#ax3=plt.subplot(2,2,3)
#ax4= plt.subplot(2,2,4)
ax0.plot(z,'or')
plt.show()

