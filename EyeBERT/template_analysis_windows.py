import csv
import matplotlib.pyplot as plt
import numpy as np
import os

# To-Do:
# Working with Windows & existing code
# Display properties (counts for 0s & 1s, counts outside reference template when comparing, etc.)
# Refine comparison templates and construct copy of .csv for comparisons
# Clean up code/classes (maximize reusability)

# Creates directory if it does not exist
def makeDir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# Write csv file: takes data matrix as input and outputs a csv file 
def writeCSV(output_file, data):
    with open(output_file, mode="w", newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            writer.writerow(row)

class EyeBERT:
    def __init__(self, cable, channel, basePath):
        self.cable = cable
        self.channel = channel 
        self.basePath = basePath 
        self.path = self.basePath + "/" + self.cable + "/" + self.cable + "_" + self.channel + "_" # Prefix for new outputted files

    def getPath(self):
        return self.path

    def setPath(self, path):
        self.path = path 

class EyeBERTFile(EyeBERT):
    def __init__(self, cable, channel, basePath):
        super().__init__(cable, channel, basePath)
        self.dataPath = self.basePath + "/" + self.cable # Path to get Eye-BERT data

    def getIndices(self, fileList):
        fileIndices = [] # Initialize list to store 
        for element in fileList:
            i = 0
            underscoreCount = 0
            index = ""
            if element.count("_") == 1:
                index = 0
            else:
                while element[i] != ".":
                    if underscoreCount == 2:
                        index += element[i]
                    if element[i] == "_":
                        underscoreCount += 1
                    i += 1
            index = int(index)
            fileIndices.append((index, element))
        fileIndices.sort(reverse = True)
        return fileIndices

    def getFile(self):
        """Returns latest .csv file for the corresponding channel from the cable's directory."""
        # Initialize empty list to store file names
        channelFiles = [] 
        # Append all .csv files with the corresponding channel from the directory to the list
        for file in os.listdir(self.dataPath):
            if self.channel in file and ".csv" in file:
                channelFiles.append(file)
        # Sort file names in descending order to ensure latest file will always be at index 0 
        channelFiles = self.getIndices(channelFiles)
        # Return the file name at index 0 (latest file for that channel)
        index, recent = channelFiles[0]
        return recent

    def getFilename(self):
        """Returns corresponding filename to cable and channel."""
        filename = self.dataPath + "/" + self.getFile()

        print(f"getFilename(): filename = {filename}")

        return filename

    def readFile(self):
        """Reads data from file to return raw data."""
        filename = self.getFilename()
        
        path = filename.replace(".csv", "_")
        self.setPath(path)
        
        print(f"readFile(): filename = {filename}")
        print(f"readFile(): path = {path}")

        data = []
        with open(filename, "r") as file: 
            search = list(csv.reader(file)) 
            for r in range(21, 46, 1): 
                row = [] 
                for c in range(1, 66, 1): 
                    value = float(search[r][c]) 
                    row.append(value)
                data.append(row)
        writeCSV(self.path + "data.csv", data)     
        return data

    def getData(self):
        """Returns raw data from file as list of lists."""
        return self.readFile()

    def getTemplate(self):
        """Returns template data as list of lists."""
        data = self.getData()
        template = []
        for r in data:
            row = []
            for value in r:
                if value < 2.0e-7:
                    row.append(0)
                else:
                    row.append(1)
            template.append(row)
        writeCSV(self.path + "template.csv", template)
        return template

    def analyze(self):
        """Returns EyeBERTAnalysis object using data read from file."""
        # Make directory to store results if one does not already exist
        makeDir("AnalysisOutputs")
        # Make directory for cable if one does not already exist
        makeDir("AnalysisOutputs/" + self.cable)
        return EyeBERTAnalysis(self.cable, self.channel, self.getData(), self.getTemplate(), self.basePath)

class EyeBERTAnalysis(EyeBERT):
    def __init__(self, cable, channel, data, template, basePath):
        super().__init__(cable, channel, basePath)
        self.data = np.array(data)
        self.template = np.array(template)

    def graph(self):
        """Returns plots for raw Eye-BERT data and Eye-BERT template."""
        fig, (ax0, ax1) = plt.subplots(2, 1)
        fig.suptitle(f"Cable: {self.cable}, Channel: {self.channel.upper()}")
        fig.tight_layout(h_pad=3)
        # Plot for raw Eye-BERT data
        im = ax0.pcolormesh(self.data, cmap="nipy_spectral")
        ax0.set_title("Raw Eye-BERT Data")
        fig.colorbar(im, ax=ax0, location="bottom")
        # Plot for Eye-BERT template
        im = ax1.pcolormesh(self.template, cmap="binary")
        ax1.set_title("Eye-BERT Template")
        fig.colorbar(im, ax=ax1, location="bottom")
        #plt.show()
        fig.savefig(self.path + "plots.pdf")   
        plt.close(fig)    

    def createTemplate(self):
        """Returns template as Template class object."""
        return Template(self.template, self.cable, self.channel, self.path)

    # To output to text file:
    def writeText(self):
        """Write properties to output text file."""
        templateObj = self.createTemplate()

        f = open(self.path + "properties.txt", "w")
        if templateObj.verify(): # Check if template is correct
            f.write(f"Cable {self.cable}, Channel {self.channel.upper()}\nNUMBER OF 0s: {templateObj.zeros}\nNUMBER OF 1s: {templateObj.ones}")
        f.close()

    def verify(self):
        """Verify values in template are correct based on raw data values."""
        for i in range(0, 25):
            for j in range(0, 65):
                if self.data[i][j] < 2.0e-7 and self.template[i][j] != 0:
                    return False
                if self.data[i][j] >= 2.0e-7 and self.template[i][j] != 1:
                    return False
        return True
    
# Reference Class
class Reference:
    def __init__(self, cable, channel, filename, path):
        self.cable = cable
        self.channel = channel
        self.filename = filename
        self.path = path 

    def getReference(self):
        data = []
        with open(self.filename, "r") as file: 
            search = list(csv.reader(file)) 
            for r in range(0, 25): 
                row = [] 
                for c in range(0, 65): 
                    value = int(search[r][c])
                    row.append(value)
                data.append(row)    
        return data    
    
    def createTemplate(self):
        return Template(np.array(self.getReference()), self.cable, self.channel, self.path)


# Template Class to compare templates
class Template:
    def __init__(self, templateData, cable, channel, path):
        self.cable = cable
        self.channel = channel 
        self.templateData = templateData.astype(int)
        self.ones = np.count_nonzero(self.templateData==1)
        self.zeros = np.count_nonzero(self.templateData==0)
        self.total = self.templateData.size
        self.path = path

        print(f"Template class: self.path: {self.path}")

    def view(self):
        for row in self.templateData:
            print(row)

    def verify(self):
        if self.ones + self.zeros != self.total:
            return False
        return True

    def __gt___(self, other):
        if self.zeros > other.zeros:
            return True
        return False

    def __lt__(self, other):
        if self.zeros < other.zeros:
            return True
        return False

    def __eq__(self, other):
        if np.array_equal(self.templateData, other.templateData):
            return True
        else:
            return False
    
    def __sub__(self, other):
        # Initialize array of zeros to store difference template values
        diffArr = other.templateData
        outCounts = 0
        inCounts = 0
        for i in range(0, 25):
            for j in range(0, 65):
                # Update count of points not in the eye of the reference
                #if other.templateData[i][j] == 0 and self.templateData[i][j] != 0:
                if self.templateData[i][j] == 0 and other.templateData[i][j] != 0:
                    outCounts += 1 # update count for elements in eye of current cable, but not in eye of reference 
                if other.templateData[i][j] == 0 and self.templateData[i][j] != 0:
                    inCounts += 1
                if self.templateData[i][j] == 0:
                    diffArr[i][j] = diffArr[i][j] - 1
                else:
                    if self.templateData[i][j] != other.templateData[i][j]:
                        diffArr[i][j] = diffArr[i][j] - 2
        self.counts(outCounts, inCounts)

        #print(diffCounts) # NEED TO OUTPUT TO .TXT: count for differing elements in matrix outside of reference's eye 
        # ADDITION: count for elements that are the same
        return diffArr 
    
    def plot(self, reference):
        # Difference array as Template Object
        #diff = self.__sub__(reference) 
        fig, (ax0, ax1, ax2) = plt.subplots(3, 1)
        fig.suptitle(f"Cable: {self.cable}, Channel: {self.channel.upper()}")
        fig.tight_layout(h_pad=3)
        # Original template plot
        #im = ax0.pcolormesh(self.templateData, cmap="binary")
        im = ax0.pcolormesh(self.templateData, cmap="binary", vmin=0, vmax=1)
        ax0.set_title("Eye-BERT Original Template")
        #fig.colorbar(im, ax=ax0, location="bottom")

        #im = ax1.pcolormesh(reference.templateData, cmap="binary")
        im = ax1.pcolormesh(reference.templateData, cmap="binary", vmin=0, vmax=1)
        ax1.set_title("Reference Template")
        #fig.colorbar(im, ax=ax1, location="bottom")

        diff = self.__sub__(reference) 
        # Difference template plot
        #im = ax2.pcolormesh(diff, cmap="binary")
        im = ax2.pcolormesh(diff, cmap="binary", vmin=-2, vmax=1)
        ax2.set_title("Eye-BERT Difference Template")
        #fig.colorbar(im, ax=ax2, location="bottom")

        #plt.show()

        print(f"Template.plot(): path: {self.path}")

        fig.savefig(self.path + "template_plots.pdf")   
        plt.close(fig)    
        
    def counts(self, outCounts, inCounts):
        print(f"Cable: {self.cable}, Channel: {self.channel.upper()}")
        self.printProperties()
        print(f"Eye-BERT values OUTSIDE the reference's eye: {outCounts}")
        print(f"Reference's Eye-BERT values OUTSIDE the cable's eye: {inCounts}")

    def printProperties(self):
        print(f"Number of 0s: {self.zeros}")
        print(f"Number of 1s: {self.ones}")


# Creating reference templates to compare to as objects of the Template class
# Current template references: 539 CMD, 540 CMD
# ref539cmd = EyeBERTFile("539", "cmd").analyze()
# ref540cmd = EyeBERTFile("540", "cmd").analyze()
# if ref539cmd.verify() and ref540cmd.verify():
#     ref539cmd = ref539cmd.createTemplate()
#     ref540cmd = ref540cmd.createTemplate()

def main():
    # Obtain cable and channel from user
    cable = str(input("Cable: "))
    channel = str(input("Channel: "))
    # Create EyeBERTFile object, cleaning user input, to read data from file
    eyebert = EyeBERTFile(cable.replace(" ", ""), channel.replace(" ", "").lower())
    # Call analyze method to obtain graphs and properties
    analysis = eyebert.analyze()
    if analysis.verify(): # Only continue if template passes verifcation
        #analysis.graph() 
        #analysis.writeText()
        
        #writeCSV("AnalysisOutputs/" + "reference_temp.csv", ref540cmd.templateData)
        #ref = np.loadtxt("reference_temp.csv", delimiter=",", dtype=int)
        #print(ref)

        # print("\nREFERENCE - Properties:")
        # refTemp.printProperties()
        # print("\n")

        # In progress testing for comparison analysis:
        template = analysis.createTemplate()

        ref = Reference("540", "CMD", "reference_tempv2.csv", )
        refTemp = ref.createTemplate()
        
        # EDIT: reference needs to be a template object
        template.plot(refTemp) 
        print("\n")
    else:
        print(f"Error for cable {cable} and channel {channel.upper()}: Template failed verification step.")


if __name__ == "__main__":
    main()