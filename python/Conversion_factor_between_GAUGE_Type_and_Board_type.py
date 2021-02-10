# Conversion factor between GAUGE Type and Board type.
#Sakhare, Suyash Mangesh
# December 06, 2020

#************************************************************************************************************************
#Necessary Imports

import statistics
from matplotlib import pyplot as plt



##########################################################################################################################

# USER DEFINED FUNCTIONS

def avgcreator(p):
    #This user defined function returns a list of averages of a 2-D array
    #For example: [[2,4],[2,6]] ==> [3,4]
    avglist=[]
    for i in range(len(p)):
        y = statistics.mean(p[i])
        avglist.append(y)
    return avglist

def STcreator(p):
    stdlist=[]
    #This user defined function returns a list of Standard deviations of a 2-D array
    #For example: [[2,4],[2,6]] ==> [1,2]
    for i in range(len(p)):
        x = statistics.stdev(p[i])
        stdlist.append(x)
    return stdlist

def ratiocreator(a,b):
    # This user defined function will return create a list of ratios.
    #Each list is an 2-D array.
    # Each element in secondary arrays of list b will be divided by the elements of the secondary arrays of the list a.
    #The ratios will be added to a single list.
    # For example: a = [[1,4],[2]] and b = [[2],[4]]
    #ratiocreator(a,b) = [ 2/1, 2/4, 4/2 ] = [ 2,0.5,2]
    s=[]
    for i in range(len(a)):
        m=[]
        for k in range(len(a[i])):
            for l in range(len(b[j])):
                x = a[i][k]/b[i][l]
                m.append(x)
        s.append(m)
    return s

########################################################################################################################
#NOTES FOR THE SCRIPT
#The dictionary has the lengths ordered in D1, D0, CMD0


#######################################################################################################333333333333#########

                                  #Data

#NOTATION FOR 34 GAUGE WIRES
#Each notation is created by combining the length of cable and the ID of cable.
# For example, Twisted pair 35cm 63 cable will translate to 3563.
#These NOTATION will be used for plotting the graph. Change it whenever necessary.
#Each NOTATION is cable in that particular gague categoty.
COdesfor34g=["3560","3561","3556","3558","3559"]

#NOATIONS FOR 36 GAUGE WIRES
Codesfor36g = ["3562","3563","3550","3551","3552"]

#-----------------------------------------------------------------------------------------------------
#The Measurements in this script is first organized based on gague and the based on the board type (Board used to collect data)
#      The flowchart for categoties
#                                    Cables
#                    ------------------------------------
#                    |                                   |
#                    34 GAUGE                          36 Gauge
#        ---------------------------           --------------------------------
#        |                         |           |                              |
#        Yellowboard         L-Board          Yellowboard                L-Board
#        messurements       Measurements       messurements            Measurements
#                                EACH CATERGORY IS THEN SUBDIVIDED INTO HEIGHTS AND WIDTHS Subcategories
#

# The name of the list will give information about its category
# For example: Yheights_for_34g is the height mesurements of 34 Gague====> Yellowboard =======> Heights
#The lists are 2D arrays. The primary list as a whole give Measurements for each subcategoty.
# The secondary list will give you an idea about each cable in that subcategory.
#The lists have been arranged the same order as the NOTATIONs above.
# For example: Yheights_for_34g[0] will give you Yellow board eye height Measurements for the 34G 35cm 60 cable.
#Yellow board Measurements will have 3 items in the secondary lists. The are ordered D1, D0, CMD0
#L-board Measurements will have 5 items in the secondary lists. The are ordered as D3, D2, D1, D0, CMD0/

#----------------------------------------------------------------------------------------------------------------

#Measurements for 34 G

#YEllow Board ORDERED IN D1, D0, CMD0
Yheights_for_34g=[(221.4,234.4,221.64),
(205.71,232,221.35),
(198.97,223.7,217.61),
(212.24,226.77,204.13),
(215.85,219.97,203.76)]

Ywidths_for_34g=[(412.36,475.22,484.41),
(415.79,485.46,476.93),
(409.26,442.06,379.88),
(420.33,437.16,453.68),
(425.59,396.78,455.57)]

#L-Board ordered in D3, D2, D1, D0, CMD0
Lheigths_for_34g=[(156.39,145.46,157.95,165.08,132.17),
(144.5,151.92,145.38,160.92,144.02),
(161.87,160.2,147.55,165.25,137.32),
(159.66,163.41,146.1,130.46,127.01),
(155.85,148.05,145.95,152.2,142.82)]

Lwidths_for_34g=[(236.92,271.26,294.75,313.9,281.61),
(216.71,253.38,356.32,315.01,253.98),
(310.18,350.38,340.48,364.25,240.57),
(255.2,341.82,322.21,403.75,262.98),
(207.59,185.29,199.29,340.81,204.06)]

#-----------------------------------------------------------------------------------------------------------------
#RESPECTIVE HEIGHTS of 36G


#ORDERED IN CH1, CH0, CMD0
Yheights_for_36g=[(257.75,274.37,261.38),
(263.58,254.71,261.05),
(259.65,273.93,240.93),
(239.65,270.95,248.53),
(233.29,255.77,222.78)]

Ywidths_for_36g=[(496.09,491.04,511.97),
(477.47,485.45,466.37),
(463.3,475.78,438.53),
(459.36,497.69,465.57),
(480.68,454.28,452.34)]

#L-Board ordered in D3, D2, D1, D0, CMD0
Lheigths_for_36g=[(198.49,194.99,182.89,173.6,178.12),
(167.18,166.86,170.66,167.75,167.15),
(151.65,160.43,164.83,165.25,140.24),
(179.49,190.27,152.42,170.34,148.74),
(121.26,142.04,140.07,187.15,174.68)]

Lwidths_for_36g=[(356.28,265.6,329.28,388.76,242.65),
(303.82,298.94,338.26,360.92,250.94),
(357.96,415.94,432.83,462.06,340.23),
(294.75,379.94,454.68,402.98,278.53),
(256.76,373.3,378.54,397.45,239.62)]

#number of elements
#The Yellow board produces 3 eye diagrams and L-board produces 5 eye diagrams
# If the number changes in future, do not forget to change this part.
#in Yellowboard reading
mnyellow = 3
#in L-Baard radings
mnlb = 5

#Labels
#These labels will be used in plotting the 36G Measurements to 34 G Measurements ratios
# The numberators are the numbers of 36G cables and the denominators are 34 G cables.
labelslist=["62/60","62/61","62/56","62/58","62/59",
"63/60","63/61","63/56","63/58","63/59",
"50/60","50/61","50/56","50/58","50/59",
"51/60","51/61","51/56","51/58","51/59",
"52/60","52/61","52/56","52/58","52/59"]
###########################################################################################################################3

#TABLE CREATED
#This part of the script will create a table from each lists.
# It will be easier to understand the data and check it.

#Table and list for the Yellow board ratios (Heights)
print("Yellow board (Heights)")
print("Wire ID\t\tD1\t\t\tD0\t\tCMD0")
#if Boardtype==2:
# For the yellow board
print("For 34G")
for i in range(len(Yheights_for_34g)):
    print(COdesfor34g[i],end="          ")
    for j in range(mnyellow):
        print(f"{Yheights_for_34g[i][j]:2f}\t", end="   ")
    print()
print("For 36 G")
for i in range(len(Yheights_for_36g)):
    print(Codesfor36g[i],end="          ")
    for j in range(mnyellow):
        print(f"{Yheights_for_36g[i][j]:2f}\t", end="   ")
    print()



#Table and list for the Yellow board ratios (Heights)
print("Yellow board (Widths)")
print("Wire ID\t\tD1\t\t\tD0\t\tCMD0")
#if Boardtype==2:
# For the yellow board
print("For 34G")
for i in range(len(Ywidths_for_34g)):
    print(COdesfor34g[i],end="          ")
    for j in range(mnyellow):
        print(f"{Ywidths_for_34g[i][j]:2f}\t", end="   ")
    print()
print("For 36 G")
for i in range(len(Yheights_for_36g)):
    print(Codesfor36g[i],end="          ")
    for j in range(mnyellow):
        print(f"{Ywidths_for_36g[i][j]:2f}\t", end="   ")
    print()

print("\n\n\n")

# L-Board Heights
print('L-Board Heights')
print("Wire ID\t\tD3\t\t\tD2\t\tD1\t\tD0\t\tCMD0")
print("For 34G")
for i in range(len(Lheigths_for_34g)):
    print(COdesfor34g[i],end="          ")
    for j in range(mnlb):
        print(f"{Lheigths_for_34g[i][j]:2f}\t", end="   ")
    print()
print("For 36 G")
for i in range(len(Lheigths_for_36g)):
    print(Codesfor36g[i],end="          ")
    for j in range(mnlb):
        print(f"{Lheigths_for_36g[i][j]:2f}\t", end="   ")
    print()


# L-Board Widths
print('L-Board Width')
print("Wire ID\t\tD3\t\t\tD2\t\tD1\t\tD0\t\tCMD0")
print("For 34G")
for i in range(len(Lwidths_for_34g)):
    print(COdesfor34g[i],end="          ")
    for j in range(mnlb):
        print(f"{Lwidths_for_34g[i][j]:2f}\t", end="   ")
    print()
print("For 36 G")
for i in range(len(Lwidths_for_36g)):
    print(Codesfor36g[i],end="          ")
    for j in range(mnlb):
        print(f"{Lwidths_for_36g[i][j]:2f}\t", end="   ")
    print()


##############################################################################################################################3
                                    #Ratios

#Empty lists for data that will be produce in the next section.
#List of Data for Heights
#List of ratios of height produced by Yellow board for each channel.
CHD1YHeights=[]
CHD0YHeights=[]
CMD0YHeights=[]

#A combination of all the above three lists
CYH = []

#List of ratios of height produced by L-board for each channel.
CHD3LHeights=[]
CHD2LHeights=[]
CHD1LHeights=[]
CHD0LHeights=[]
CMD0LHeights=[]

# A combination of all the above 5 lists
CLH=[]

#Width ratios for both boards
#List of ratios of widths produced by Yellow board for each channel
CHD1YWidths=[]
CHD0YWidths=[]
CMD0YWidths=[]

#A combination of all the above three lists
CYW=[]


#List of ratios of widths produced by L-board for each channel.
CHD3LWidths=[]
CHD2LWidths=[]
CHD1LWidths=[]
CHD0LWidths=[]
CMD0LWidths=[]
# A combination of all the above 5 lists
CLW=[]

#A list of number of
num=[3,5]

#########################################################################################################################################
                                                #HEIGHT AND WIDTH RATIO PROFUCER SECTIOM.
#This section of the script produces ratios of Height and widths mesurements of 36G cables to 34 G cables.
#Since we are looking a general idea about how the measurements change w.r.t gauge, we won't have to worry about the specific channels in consideration.
# However, we will still classify the ratios thos subcategory for simplicity.
#         Classification of ratios will be as follows:            Gauge ====> Cables in consideration ========> Boardtype =======> Channel in consideration.

#The for loops will first choose a 36G and a 34G cabke from the measurements list.
#Then it will choose a channel.
# For example, Yheights_for_34g and Yheights_for_36g hold the measurements for Yellowboard measurements for 34 gauge and 36 gauge wires respectively.
#The measurements of each 34G and 36 G cable are arranged in secondary lists in a order similar to the NOATIONS of those cables which can be found in COdesfor34g and Codesfor36g lists respectively.
#After choosing a cables and the channel. The for loop will divide the measurement of 36G cable by 34 G cable for that channel.
#Then it will add it to the lists from the last section.
#The list name suggest what category they represent.
#There are four additional lists that will hold the data without differentiating between teh channels.

#For yellow Board
for i in range(5): #i is 36 g
    for k in range(5): #k is 34g
        for j in range(mnyellow): # j is channel

            CYH.append(Yheights_for_36g[i][j]/Yheights_for_34g[k][j])
            CYW.append(Ywidths_for_36g[i][j]/Ywidths_for_34g[k][j])
            if j ==0:
                CHD1YHeights.append(Yheights_for_36g[i][j]/Yheights_for_34g[k][j])
                CHD1YWidths.append(Ywidths_for_36g[i][j]/Ywidths_for_34g[k][j])
            elif j ==1:
                CHD0YHeights.append(Yheights_for_36g[i][j]/Yheights_for_34g[k][j])
                CHD0YWidths.append(Ywidths_for_36g[i][j]/Ywidths_for_34g[k][j])
            elif j ==2:
                CMD0YHeights.append(Yheights_for_36g[i][j]/Yheights_for_34g[k][j])
                CMD0YWidths.append(Ywidths_for_36g[i][j]/Ywidths_for_34g[k][j])

#print(" Data for L-Board")
for i in range(5): #i is 36 g
    for k in range(5): #k is 34g
        for j in range(mnlb): # j is channel
            CLH.append(Lheigths_for_36g[i][j]/Lheigths_for_34g[k][j])
            CLW.append(Lwidths_for_36g[i][j]/Lwidths_for_34g[k][j])
            if j ==0:
                CHD3LHeights.append(Lheigths_for_36g[i][j]/Lheigths_for_34g[k][j])
                CHD3LWidths.append(Lwidths_for_36g[i][j]/Lwidths_for_34g[k][j])
            elif j ==1:
                CHD2LHeights.append(Lheigths_for_36g[i][j]/Lheigths_for_34g[k][j])
                CHD2LWidths.append(Lwidths_for_36g[i][j]/Lwidths_for_34g[k][j])
            elif j ==2:
                CHD1LHeights.append(Lheigths_for_36g[i][j]/Lheigths_for_34g[k][j])
                CHD1LWidths.append(Lwidths_for_36g[i][j]/Lwidths_for_34g[k][j])
            elif j ==3:
                CHD0LHeights.append(Lheigths_for_36g[i][j]/Lheigths_for_34g[k][j])
                CHD0LWidths.append(Lwidths_for_36g[i][j]/Lwidths_for_34g[k][j])
            elif j ==4:
                CMD0LHeights.append(Lheigths_for_36g[i][j]/Lheigths_for_34g[k][j])
                CMD0LWidths.append(Lwidths_for_36g[i][j]/Lwidths_for_34g[k][j])



#The four additional lists, namely CYH, CYW, CLH, CLW hold data for a certain Board type.

#The below section of script will find a mean for each of the category and use the Standard deviation as error
# We have succesfully found the conversion factor between 36G and 34 G.


print("Mean reading for Yellow Heights = ",statistics.mean(CYH),' +-', statistics.stdev(CYH))
print("Mean reading for Yellow Widths = ",statistics.mean(CYW),' +-', statistics.stdev(CYW))
print("Mean reading for L-Board Heights = ",statistics.mean(CLH),' +-', statistics.stdev(CLH))
print("Mean reading for L-Board Widths = ",statistics.mean(CLW),' +-', statistics.stdev(CLW))



############################################################################################################################
#PLOTS
#This section plots the list we produced in last section.

#The plots are organized as     Boardtype ======> Ratio type (Heigh or Width)
#Each graph is a scatter plot of ratios of the category.
#The plots will contain 3 or 5 channels depending on the board
#The x-axis shows the cables which were considered.
#For example, a 62/60 mark on the x-axis represents that the ratios of Twisted pair 35cm 36 G 62 cable to Twisted Pair 35cm 34G 60 cable.
#The y-axis wull show the ratios of all the channels for that particular group.
fig1 = plt.figure(figsize=(25, 25))
fig1.patch.set_facecolor('xkcd:black')
plt.style.use('dark_background')  #This is what worked for the background style

#Subplots for each category
ax1=plt.subplot(2,2,1)
ax2=plt.subplot(2,2,2)
ax3=plt.subplot(2,2,3)
ax4= plt.subplot(2,2,4)


fig1.suptitle('Ratio of Gauge Plots for 35cm (Yellow Board and L-Board)', fontsize=16)

#Plot for Yellow Heights
ax1.plot(labelslist,CHD1YHeights,'-ok', color='blue', label='ChD1')
#ax1.errorbar(labelslist,CHD1YHeights, yerr= statistics.stdev(CHD1YHeights), fmt='bo')
ax1.plot(labelslist,CHD0YHeights,'-ok', color='red', label='CHD0')
ax1.plot(labelslist,CMD0YHeights,'-ok' ,color='green', label='CMD0')
ax1.hlines(y=statistics.mean(CYH), xmin=0, xmax=len(labelslist), linewidth=2, color='w')


ax1.set_xlabel('Wire Pair')
ax1.set_title('Ratio of Heights Yellow Board (36G / 34G)')
ax1.set_ylabel('Heigths Ratio')
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

#Plots for Yellow Widths Ratio
ax2.plot(labelslist,CHD1YWidths,'-ok', color='blue', label='ChD1')
ax2.plot(labelslist,CHD0YWidths,'-ok', color='red', label='CHD0')
ax2.plot(labelslist,CMD0YWidths,'-ok' ,color='green', label='CMD0')
ax2.hlines(y=statistics.mean(CYW), xmin=0, xmax=len(labelslist), linewidth=2, color='w')
ax2.set_xlabel('Wire Pair')
ax2.set_title('Ratio of WIdths Yellow Board (36G / 34G)')
ax2.set_ylabel('Width Ratio')
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

#Ratio Plot for L heights
ax3.plot(labelslist,CHD3LHeights,'-ok', color='pink', label='ChD3')
ax3.plot(labelslist,CHD2LHeights,'-ok', color='purple', label='ChD2')
ax3.plot(labelslist,CHD1LHeights,'-ok', color='blue', label='ChD1')
ax3.plot(labelslist,CHD0LHeights,'-ok', color='red', label='ChD0')
ax3.plot(labelslist,CMD0LHeights,'-ok', color='green', label='CMD0')
ax3.hlines(y=statistics.mean(CLH), xmin=0, xmax=len(labelslist), linewidth=2, color='w')
ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
ax3.set_xlabel('Wire Pair')
ax3.set_title('Ratios of Heights L-Board (36G / 34G)')
ax3.set_ylabel('Ratio')

#Ratio Plot for L heights
ax4.plot(labelslist,CHD3LWidths,'-ok', color='pink', label='ChD3')
ax4.plot(labelslist,CHD2LWidths,'-ok', color='purple', label='ChD2')
ax4.plot(labelslist,CHD1LWidths,'-ok', color='blue', label='ChD1')
ax4.plot(labelslist,CHD0LWidths,'-ok', color='red', label='ChD0')
ax4.plot(labelslist,CMD0LWidths,'-ok', color='green', label='CMD0')
ax4.hlines(y=statistics.mean(CLW), xmin=0, xmax=len(labelslist), linewidth=2, color='w')
ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
ax4.set_xlabel('Wire Pair')
ax4.set_title('Ratios of Widths L-Board (36G / 34G)')
ax4.set_ylabel('Ratio')



###################################################################################################################

#Ratio of the Yellow Board messurements to L-Board Measurements


#This section of the script will find out the conversion factor for the boards.

#The ratiocreator function is used to create ratios of each type.
#The ratios are classifoed in Gauge ======>  Ratio type (Heigh or WIDTH)

RH34G = ratiocreator(Lheigths_for_34g, Yheights_for_34g)
RH36G = ratiocreator(Lheigths_for_36g, Yheights_for_36g)
RW34G = ratiocreator(Lwidths_for_34g, Ywidths_for_34g)
RW36G = ratiocreator(Lwidths_for_36g, Ywidths_for_36g)

#We print the average of the list created and usee standard deviation as the error.

print("Ratio average for Heigths 34G",statistics.mean(avgcreator(RH34G)),"+-" ,statistics.stdev(avgcreator(RH34G)))
print("Ratio average for Heigths 36G",statistics.mean(avgcreator(RH36G)),"+-" ,statistics.stdev(avgcreator(RH36G)))
print("Ratio average for Widths 34G",statistics.mean(avgcreator(RW34G)),"+-" ,statistics.stdev(avgcreator(RW34G)))
print("Ratio average for Widths 36G",statistics.mean(avgcreator(RW36G)),"+-" ,statistics.stdev(avgcreator(RW36G)))


####################################################################################################################
#Plot for the value of heights and widths


fig2 = plt.figure(figsize=(25, 25))
fig2.patch.set_facecolor('xkcd:black')
plt.style.use('dark_background')  #This is what worked for the background style

#ax0=plt.subplot(3,1,1)
ax5=plt.subplot(2,2,1)
ax6=plt.subplot(2,2,2)
ax7=plt.subplot(2,2,3)
ax8= plt.subplot(2,2,4)

fig2.suptitle('Heights and Widths Ratio for 35cm (L-Board/Y-Board)', fontsize=16)

#ax5.errorbar(Codesfor36g,avgcreator(Yheights_for_36g), yerr=STcreator(Yheights_for_36g))
#ax5.plot(Yheights_for_34g, 'go')
ax5.hlines(y=statistics.mean(avgcreator(RH34G)), xmin=0, xmax=len(RH34G), linewidth=2, color='w')
ax5.errorbar(COdesfor34g,avgcreator(RH34G), yerr=STcreator(RH34G), fmt='o' )
ax5.set_title('Ratios of Eye Heights (Voltage) for 34 G cables')
ax5.set_xlabel("Wire codes (Lenght + Number)")
ax5.set_ylabel("Ratio Eye height (L-Board to Yellow board)")

ax6.set_title('Ratios of Eye Heights(Voltage) for 36G cables')
ax6.errorbar(Codesfor36g,avgcreator(RH36G), yerr=STcreator(RH36G), fmt='o' )
ax6.hlines(y=statistics.mean(avgcreator(RH36G)), xmin=0, xmax=len(RH36G), linewidth=2, color='w')
ax6.set_xlabel("Wire codes (Lenght + Number)")
ax6.set_ylabel("Ratio Eye height (L-Board to Yellow board)")

ax7.errorbar(COdesfor34g,avgcreator(RW34G), yerr=STcreator(RW34G), fmt='o' )
ax7.set_title('Ratios of Eye WIdths (Time) 34G')
ax7.hlines(y=statistics.mean(avgcreator(RW34G)), xmin=0, xmax=len(RW34G), linewidth=2, color='w')
ax7.set_xlabel("Wire codes (Lenght + Number)")
ax7.set_ylabel("Ratio Eye Width (L-Board to Yellow board)")

ax8.set_title('Ratios of Eye Widths (Time) for 36G')
ax8.errorbar(Codesfor36g,avgcreator(RW36G), yerr=STcreator(RW36G), fmt='o' )
ax8.hlines(y=statistics.mean(avgcreator(RW36G)), xmin=0, xmax=len(RW36G), linewidth=2, color='w')
ax8.set_xlabel("Wire codes (Lenght + Number)")
ax8.set_ylabel("Ratio Eye Width (L-Board to Yellow board)")

#ax6.plot(Codesfor36g,Ywidths_for_36g, 'ro')
plt.show()
