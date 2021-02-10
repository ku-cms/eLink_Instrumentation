#!/Users/skhalil/miniconda2/envs/Python37
from itertools import islice
import re, decimal
import matplotlib.pyplot as plt
#import matplotlib.ticker as ticker
import numpy as np
import pickle as pl

def name(input):    
    match = re.match(r'TP_\w+_\d+', input)
    name = match.group()
    if '1p4' in name: name = name.replace('1p4', '1.4')
    return name

def Z_in(Z0, S11_r, S11_i):
    Z_in_R = Z0*( (1 - pow(S11_r,2) - pow(S11_i,2) )/( pow((1-S11_r),2) + pow(S11_i,2)) )
    Z_in_I = Z0*( (2*S11_i)/(pow((1 - S11_r),2) +  pow(S11_i,2)) )
    return Z_in_R, Z_in_I


from optparse import OptionParser
parser = OptionParser()
parser.add_option('--input', metavar='T', type='string', action='store',
                  default='TP_1m_33_ChD1.vna.txt',
                  dest='input',
                  help='input text file')

parser.add_option('--directory', metavar='T', type='string', action='store',
                  default='Plots',
                  dest='directory',
                  help='directory to store plots')

(options,args) = parser.parse_args()
# ==========end: options =============
input = options.input
dir_in= options.directory
cable = name(input)
date  = ''

data_groups = []
group_1 = [ ['index', 'freq', 'S11_Real', 'S11_Img', 'S12_Real', 'S12_Img', 'S13_Real', 'S13_Img', 'S14_Real', 'S14_Img']]
group_2 = [ ['index', 'freq', 'S21_Real', 'S21_Img', 'S22_Real', 'S22_Img', 'S23_Real', 'S23_Img', 'S24_Real', 'S24_Img']]

# split the file into data chunks corresponding to S parameter matrix by date
# ---------------------------------------------------------------------------
with open(input) as f:
    for i, line in enumerate(f):   
        z = re.match(r'MODEL:\s+DATE:\s+\d+/\d+/\d+', line)
        if z:
            date = z.group().split()[2] 
            data_groups.append(i)            
    print ('line boundaries for data group: ', data_groups)   
f.close()

print ('Data was taken on: ', date)

# reopen the text file, and jump to lines of interests correponding to different data groups.
# ------------------------------------------------------------------------------------------
with open(input) as f:    
    found_S11=False; start_reading=False;
    for i, l in enumerate(f):
        # group 1: 
        if i >= int(data_groups[0]) and i < data_groups[1]:
            # make sure that the group includes S11 parameter
            check = re.findall(r'PARAMETER:\s+(.\w+.)\s+(.\w+.)\s+(.\w+.)\s+(.\w+.)\s+', l)           
            if len(check)!= 0:
                if 'S11' in check[0][0]: found_S11=True
                else:
                    print ('1st parameter: ',check[0][0], 'better adapt the script to read S11')
                    break
            # find a starting line to read the tables
            start = re.match(r'FREQUENCY\s+POINTS:\s+',l)            
            if start: start_reading = True
            if found_S11 and start_reading:    
                rows = l.strip().split('\n')[0].split('\t')
                # start writting from 1st row of the table index
                if not rows[0].isdigit(): continue
                group_1.append(l.strip().split('\t'))
          

# draw the plots:
# ---------------
freq, z_in_real=[],[]
freq, z_in_img =[],[]
for i, c in enumerate(group_1):
    if i==0: continue; # skip the title row
    freq.append(float(c[1]))
    #time.append(1./float(c[1]))    
    S11_r_in = float(c[2])
    S11_i_in = float(c[3])
    S12_r_in = float(c[4])
    S12_i_in = float(c[5])
    #print('S12_r', S12_r_in)
    Z_in_real, Z_in_img = Z_in(50.0, S11_r_in, S11_i_in )
    #Z_in_real = Z_in(50.0, S11_r_in, S11_i_in )
    z_in_real.append(Z_in_real)
    z_in_img.append(Z_in_img)


#print ('freq: ', freq)
#print ('Z_real: ', z_in_real)
#print ('time: ', time)

fig = plt.figure(figsize=(8,5))
ax0 = fig.add_subplot(1,2,1)
major_ticks = np.arange(0, 6.5, 0.5)
minor_ticks = np.arange(0, 6.5, 0.1)
ax0.set_xticks(major_ticks)
ax0.set_xticks(minor_ticks, minor=True)
ax0.grid(which='minor', alpha=0.2)
ax0.grid(which='major', alpha=0.5)
ax0.set_xlabel('Frequency (GHz)')
ax0.set_ylabel('Z (Real) (\u03A9)')
plt.plot(freq, z_in_real, 'r', linewidth=2.0, label=cable)
ax0.legend()
fig1 = plt.gcf()
ax1 = fig.add_subplot(1,2,2)
ax1.set_xticks(major_ticks)
ax1.set_xticks(minor_ticks, minor=True)
ax1.set_xlabel('Frequency (GHz)')
ax1.set_ylabel('Z (Img) (\u03A9)')
ax1.grid(which='minor', alpha=0.2)
ax1.grid(which='major', alpha=0.5)
plt.plot(freq, z_in_img, 'b', linewidth=2.0, label=cable)
plt.show()
plt.draw()
fig1.savefig(dir_in+'/'+cable+'.png')
pl.dump(fig1, open(dir_in+'/'+cable+'.pickle', 'wb'))


    
