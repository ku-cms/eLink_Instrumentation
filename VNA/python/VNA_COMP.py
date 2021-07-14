#!/usr/bin/env python3

#Predefined Libraries
import os
from optparse import OptionParser
import pandas as pd
import skrf as rf
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib import style
import pickle as pl



#Transfered from other Scripts
def name(x):
    return x.strip(".vna").replace('Data/'+str(cable_number)+'/Plots/s2p/', "").strip("TP_")
def split(word):
    return [char for char in word]
y_plot_value=[]
def display_mean_impedance(ax, t1, t2, col):##https://www.tutorialfor.com/questions-285739.htm

    lines = ax.get_lines()

    # delete any other array correponding to a line drawn in ax but the last one. This is a
    # brute force way of resetting the line data to the data current line
    if len(lines)>1:
        del lines[:-1]

    # ressure that length of line is 1.
    #print('size of lines:', len(lines))

    # store the line arrays into list. Every line drawn on the ax is considered as data
    Y = [line.get_ydata() for line in lines]
    X = [line.get_xdata() for line in lines]

    # create a table, and since the list X and Y should have size=1, place the first
    # element (array) in pandas table columns t and Z
    df = pd.DataFrame()
    df['t'] = X[0]
    df['Z'] = Y[0]

    # get the mean value of Z for a given time difference
    Z_mean =  df.query('t >=@t1 & t<=@t2').agg({'Z': 'mean'})
    print('Mean impedance from', t1, 'ns and', t2, 'ns =', Z_mean.values, 'for', lines[0])
    # plot the average line
    x_coor = [t1, t2]
    y_coor = [Z_mean, Z_mean]
    y_plot_value.append(int(Z_mean.values))
    ax.plot(x_coor, y_coor, color=col, linewidth=1, label='', linestyle='--')

def set_axes(ax, title, ymin, ymax, xmin, xmax, nolim):
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.grid(True, color='0.8', which='minor')
    ax.grid(True, color='0.4', which='major')
    ax.set_title(title) #Time domain
    if nolim==False:
        ax.set_xlim((xmin, xmax))
        ax.set_ylim((ymin, ymax))
    plt.tight_layout()


parser= OptionParser()



#NN = input("Are your file names have similar format to: TP_0.8m_115_M1CMD.vna.txt? (Lenght in m)(y = 1/ n = 0)")
#if NN == "1":
#    print("Extraction Possible")
#elif NN == "0":
#    print("Please change your file name")
#    exit()
cable_length = input("What is the cable length? (35, 80, 100, 140, 160, 200. )")
cable_number = str(input("What is the cable number?"))
cable_type = int(input("What is the cable type? (1,2,3,4)"))

Pre_list = []

print("\n Detecting Files...")
for root, dirs, files in os.walk("./Data/"+cable_number, topdown=False):
   for name in files:
      if ".txt" in os.path.join(name):
        Pre_list.append(os.path.join(name))
print(" Files detected")
print(Pre_list)


for i in range(1,len(Pre_list)+1):
    globals()[f"ff{i}"]= f"Data/"+cable_number+f"/{Pre_list[i-1]}"
    globals()[f"filename{i}"]= f"{Pre_list[i-1]}"


IDchecker = 0
Breaker = True
while Breaker == True:

    Breaker = True
    FILE = Pre_list[IDchecker]
    print("Creating s2p files for ", FILE)

    parser.add_option('--basename', metavar='T', type='string', action='store',
                      default='Data/'+str(cable_number)+'/'+FILE, #31, 15, 33 #calibration_test.vna
                      dest='basename',
                      help='input text file')

    parser.add_option('--directory', metavar='T', type='string', action='store',
                      default='Data/'+str(cable_number)+'/'+'Plots/',
                      dest='directory',
                      help='directory to store plots')

    (options,args) = parser.parse_args()
    # ==========end: options =============
    basename1 = options.basename
    basename2 = basename1.replace('Data/'+str(cable_number)+'/', 'Data/'+str(cable_number)+'/'+'Plots/s2p/')
    dir_in= options.directory
    cable = basename1.replace('Data/'+str(cable_number)+'/', "")


    infile = pd.read_csv(basename1, names=['pt','f','s11R','s11I','s12R','s12I','s13R','s13I','s14R','s14I'], delim_whitespace=True, skiprows=1)
    infile.dropna(how='all')

    pd.set_option("display.max_rows", 5)

    fileindex = 0
    prevF = 0
    for i, row in infile.iterrows():
        if row['pt'] == 'PARAMETER:':
            # new set of points
            try:
                if not f.closed:
                    f.close()
            except:
                pass
            filename = basename2.replace(".txt","")+ '_' + str(fileindex)+'.s2p'
            fileindex += 1
            f = open(filename,'w')
            f.write('# GHZ	S	RI	R	50.0\n')

            try:
                #print (row['f'][1:-1], row['s11R'][1:-1], row['s11I'][1:-1], row['s12R'][1:-1] )
                f.write(f"!freq       Rel{row['f'][1:-1]}       Im{row['f'][1:-1]}      Rel{row['s11R'][1:-1]}       Im{row['s11R'][1:-1]}        Rel{row['s11I'][1:-1]}        Im{row['s11I'][1:-1]}         Rel{row['s12R'][1:-1]}      Im{row['s12R'][1:-1]}\n")
            except:
                if row['f'][1:-1] == 'SDD':
                     f.write(f"!freq\tRelS11\tImS11\n")
            prevF = 0
        try:
            if float(row['s11R']) == float(row['s11R']) and float(row['f'])>prevF:
                f.write(f"{float(row['f']):.3f}\t{float(row['s11R'])}\t{float(row['s11I'])}\t{float(row['s12R'])}\t{float(row['s12I'])}\t{float(row['s13R'])}\t{float(row['s13I'])}\t{float(row['s14R'])}\t{float(row['s14I'])}\n")
                prevF = float(row['f'])
        except:
            pass

    example = rf.Network(basename2.replace(".txt","")+'_0.s2p', f_unit='ghz')


    print("Plotting the data.\n")
    with style.context('seaborn-ticks'):
        #Time domain reflectometry, measurement vs simulation
        fig0 = plt.figure(figsize=(8,4))
        fig0.patch.set_facecolor('xkcd:black')
        plt.style.use('dark_background')
        ax0=plt.subplot(1,2,1)
        #major_ticks = np.arange(0, 6.5, 0.5)
        #minor_ticks = np.arange(0, 6.5, 0.1)
        ax0.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax0.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax0.grid(True, color='0.8', which='minor')
        ax0.grid(True, color='0.4', which='major')
        #ax0.legend()
        example_dc = example.extrapolate_to_dc(kind='linear')
        plt.title('Frequency')
        example_dc.s11.plot_s_db(label='S11')
        example_dc.s21.plot_s_db(label='S12')
        plt.ylim((-200.0, 100.0))
        plt.xlim((100000, 2500000000))
        ax1=plt.subplot(1,2,2)
        ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax1.grid(True, color='0.8', which='minor')
        ax1.grid(True, color='0.4', which='major')
        plt.title('Time domain reflection step response (DC extrapolation)') #The time_step component of the z-matrix vs frequency
        example_dc.s11.plot_z_time_step(attribute='z_time_step', pad=2000, window='hamming', z0=50, label='TD11')
        example_dc.s21.plot_z_time_step(attribute='z_time_step',pad=2000, window='hamming', z0=50, label='TD12')
        plt.ylim((-500.0, 500.0))
        plt.xlim((0, 30))
        plt.tight_layout()
        #ax1.legend()
        fig0.savefig(dir_in+cable.replace(".vna.txt","")+'_freq_time_Z_rf.png')

        # Gating the Reflection of Interest
        s11_gated = example.s11.time_gate()#(center=0, span=.2)#autogate on the fly
        s11_gated.name='gated '
        fig1 = plt.figure(figsize=(8,4))
        plt.subplot(121)
        example.s11.plot_s_db()
        s11_gated.plot_s_db() #s11.time_gate()
        plt.title('Frequency Domain')
        plt.subplot(122)
        example.s11.plot_s_db_time()
        s11_gated.plot_s_db_time()
        plt.title('Time Domain')
        plt.xlim((-5, 5))
        plt.tight_layout()
        #plt.show()
        fig1.savefig(dir_in+cable.replace(".vna.txt","")+'_fref_time_rf.png')

        fig = plt.figure(figsize=(14,6))
        for i in range(6):
           ax = fig.add_subplot(2,3,i+1)
           if i==0 :
             plt.axis([-1.1,2.1,-1.1,1.1])
             example.plot_s_smith(draw_labels=True,m=0, n=0, label='S11')
             example.plot_s_smith(draw_labels=True,m=1, n=0, label='S12')
           elif i==1:
               example.plot_z_re(m=0,n=0,label='Z11')
               example.plot_z_re(m=1,n=0,label='Z12')
           elif i==2:
               example.plot_z_im(m=0,n=0,label='Z11')
               example.plot_z_im(m=1,n=0,label='Z12')
           elif i==3:
               example.plot_s_db(m=0, n=0, label='S11') # 10
               example.plot_s_db(m=1, n=0, label='S12')
           elif i==4:
               example.plot_s_db_time(m=0, n=0, label='S11') # employs windowing before plotting to enhance impluse resolution.
               example.plot_s_db_time(m=1, n=0, label='S12')
           elif i==5:
               example.plot_z_time_db(m=0, n=0, label='Z11')    #plot_z_re_time
               example.plot_z_time_db(m=1, n=0, label='Z12')

        parser.remove_option('--basename')
        parser.remove_option('--directory')

        fig.savefig(dir_in+cable.replace(".vna.txt","")+'_rf.png')


        IDchecker +=1

        if IDchecker >(len(Pre_list)-1):
            break

print("Plots can be now found in the Plots folder of the Cable\n")


print()
print()










comps = ['11','12','21']
subfiles = ['0','0','1']

IDchecker = 0
Breaker = True

print("List of Cables being analysed",Pre_list,"\n")

while Breaker == True:
    Breaker = True
    comp = comps[IDchecker]
    subfile = subfiles[IDchecker]

    if comp == '11' and subfile == '0': S_ij = '11'
    elif comp == '12'and subfile == '0': S_ij = '21'
    elif comp == '21' and subfile == '1': S_ij = '11'

    i = int(split(S_ij)[0])
    j = int(split(S_ij)[1])

    print("\nParameter being analyzed\n","S"+comp)


    if cable_length == '35':
        net4 = rf.Network("Data/"+cable_number+"/Plots/s2p/"+filename1.replace(".txt","")+'_'+subfile+'.s2p', f_unit='ghz')
        net5 = rf.Network("Data/"+cable_number+"/Plots/s2p/"+filename2.replace(".txt","")+'_'+subfile+'.s2p', f_unit='ghz')
        net6 = rf.Network("Data/"+cable_number+"/Plots/s2p/"+filename3.replace(".txt","")+'_'+subfile+'.s2p', f_unit='ghz')
        #net8 = rf.Network(ff4+'_'+subfile+'.s2p', f_unit='ghz')
        #net10 = rf.Network(ff5+'_'+subfile+'.s2p', f_unit='ghz')



    #netref = rf.network.Network(out_dir+'/'+sub_out_dir+'/straight_SMA.vna_'+subfile+'.s2p', f_unit='ghz')

    with style.context('seaborn-darkgrid'):

        fig0 = plt.figure(figsize=(10,4))
        fig0.patch.set_facecolor('xkcd:black')
        plt.style.use('dark_background')
        ax0=plt.subplot(1,2,1)
        ax1=plt.subplot(1,2,2)

        ax0.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax0.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax0.grid(True, color='0.8', which='minor')
        ax0.grid(True, color='0.4', which='major')


        if cable_length == '35':
            net4_dc = net4[i,j].extrapolate_to_dc(kind='linear')
            net5_dc = net5[i,j].extrapolate_to_dc(kind='linear')
            net6_dc = net6[i,j].extrapolate_to_dc(kind='linear')
            #net8_dc = net8[i,j].extrapolate_to_dc(kind='linear')
            #net10_dc = net10[i,j].extrapolate_to_dc(kind='linear')
            #netref_dc = netref[i,j].extrapolate_to_dc(kind='linear')

            net4_dc.plot_s_db(label='S'+comp+ff1.split('.vna')[0].split('/')[-1:][0], ax=ax0, color='b')
            net5_dc.plot_s_db(label='S'+comp+ff2.split('.vna')[0].split('/')[-1:][0], ax=ax0, color='r')
            net6_dc.plot_s_db(label='S'+comp+ff3.split('.vna')[0].split('/')[-1:][0], ax=ax0, color='g')
            #net8_dc.plot_s_db(label='S'+comp+ff4, ax=ax0, color='w')
            #net10_dc.plot_s_db(label='S'+comp+ff5, ax=ax0, color='m')



            net4_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+ff1.split('.vna')[0].split('/')[-1:][0], ax=ax1, color='b')
            display_mean_impedance(ax1,2.0,5.0,'b')
            net5_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+ff2.split('.vna')[0].split('/')[-1:][0], ax=ax1, color='r')
            display_mean_impedance(ax1, 2.0, 5.0, 'r')
            net6_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+ff3.split('.vna')[0].split('/')[-1:][0], ax=ax1, color='g')
            display_mean_impedance(ax1, 2.0, 5.0, 'g')
            #net8_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+ff4, ax=ax1, color='w')
            #display_mean_impedance(ax1, 2.0, 5.0, 'w')
            #net10_dc.plot_z_time_step(pad=0, window='hamming', z0=50, label='TD'+comp+ff5, ax=ax1, color='m')
            #display_mean_impedance(ax1, 2.0, 5.0, 'm')



        fig0.savefig("Data/"+cable_number+"/Plots/"+cable_number+'cm_freq_time_Z_rf_'+"S"+comp+'.png')

        #plt.show()
        IDchecker+=1

        if IDchecker >2:
            break
print("Data analysed. Plots stored in Plots folder.")
