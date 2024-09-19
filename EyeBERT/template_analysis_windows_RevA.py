import csv
import matplotlib.pyplot as plt
import numpy as np
import os

# To-Do:
# Add branch to Template class and to plot title if applicable
# Simplify the function getIndexedFiles(). Create a simpler version and test before replacing.
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
    def __init__(self, cable, branch, channel, basePath):
        self.cable      = cable
        self.branch     = branch
        self.channel    = channel
        self.basePath   = basePath
        self.debug      = False
                
        # The path is the prefix for new output files.
        # The path is dependent on if the cable has branches.
        if self.branch:
            self.path = f"{self.basePath}/{self.cable}/{self.cable}_{self.branch}_{self.channel}_"
        else:
            self.path = f"{self.basePath}/{self.cable}/{self.cable}_{self.channel}_"
        if self.debug:
            print(f"EyeBERT: self.path = {self.path}")

    def getPath(self):
        return self.path

    def setPath(self, path):
        self.path = path

class EyeBERTFile(EyeBERT):
    def __init__(self, cable, branch, channel, basePath):
        super().__init__(cable, branch, channel, basePath)
        self.dataPath = self.basePath + "/" + self.cable # Path to get Eye-BERT data
        if self.debug:
            print(f"EyeBERTFile: self.dataPath = {self.dataPath}")

    # Get indexed files sorted by index in decreasing order
    # TODO: Simplify function! For example, remove ".csv" from the file name and then split by "_".
    def getIndexedFiles(self, fileList):
        fileIndices = [] # Initialize list to store the index and file name as an ordered pair
        if self.debug:
            print(f"In getIndexedFiles(): fileList = {fileList}")
        # Assign the maximum number of underscores in the file name based on if the cable has branches
        if self.branch:
            max_underscores = 3
        else:
            max_underscores = 2
        
        for element in fileList: # Iterate over each file name stored in the list
            i = 0 # Initialize i to iterate over each character in the file name string 
            underscoreCount = 0 # Initialize count for the underscore character in the file name to track the number of its occurrences 
            index = "" # Initialize chosen index as an empty string 
            if element.count("_") == max_underscores - 1: # Check if the file name has one less underscore than the max (this means this is the earliest data)
                index = 0 # Set index to 0, as this would be the earliest data 
            else:
                while element[i] != ".": # Iterate over the file name until a period is reached (this means we will reach ".csv")
                    if underscoreCount == max_underscores: # Check if the underscore counter has reached the max (this means the correct index will begin in the file name)
                        index += element[i] # Add the character to the index (string operation, to ensure digit remains in its corresponding place)
                    if element[i] == "_": # Check if the character is an underscore
                        underscoreCount += 1 # Update the count for the number of underscore characters iterated if necessary
                    i += 1 # Increment iterator to iterate over the next character
            if self.debug:
                print(f"In getIndexedFiles(): index = {index}")
            index = int(index) # Convert the index to an integer... we assume this will work... when it does not, we have to debug...
            fileIndices.append((index, element)) # Append the resulting index to the list as an ordered pair with its corresponding original file name
        fileIndices.sort(reverse = True) # Sort the list in descending order based on the index (therefore, more recent the file (higher index), the closer to the beginning of the list it will be)
        return fileIndices # Return the completed list with the file names and their corresponding indices as ordered pairs

    # Get latest file for the cable, branch (if applicable), and channel
    def getLatestFile(self):
        """Returns latest .csv file for the corresponding channel from the cable's directory."""
        
        # Get a list of file names for the cable, branch (if applicable), and channel
        channelFiles = []
        for file in os.listdir(self.dataPath):
            # determine if we should include this file
            include_file = False
            # require a csv file with channel in the file name
            if self.channel in file and ".csv" in file:
                # require that data and template are not in the file name
                if "data" not in file and "template" not in file:
                    # require the branch in the file name if the cable has branches
                    if self.branch:
                        if self.branch in file:
                            include_file = True
                    else:
                        include_file = True
            # If the file meets the requirements, append it to the list
            if include_file:
                channelFiles.append(file)
        
        # Call method to obtain a sorted list of file names with their corresponding indices in order of most recent file to oldest
        channelFiles = self.getIndexedFiles(channelFiles)

        # Get the index and file name of the latest file
        index, latest_file = channelFiles[0]
        if self.debug:
            print(f"In getLatestFile(): channelFiles = {channelFiles}")
            print(f"In getLatestFile(): index = {index}, latest_file = {latest_file}")
        
        # Return the latest file
        return latest_file

    def getFilename(self):
        """Returns corresponding filename to cable and channel."""
        filename = self.dataPath + "/" + self.getLatestFile()

        return filename

    def readFile(self):
        """Reads data from file to return raw data."""
        filename = self.getFilename()
        
        path = filename.replace(".csv", "_")
        self.setPath(path)

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
        return EyeBERTAnalysis(self.cable, self.branch, self.channel, self.getData(), self.getTemplate(), self.basePath)

class EyeBERTAnalysis(EyeBERT):
    def __init__(self, cable, branch, channel, data, template, basePath):
        super().__init__(cable, branch, channel, basePath)
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
        return Template(self.template, self.cable, self.branch, self.channel, self.path)

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
    def __init__(self, cable, branch, channel, filename, path):
        self.cable = cable
        self.branch = branch
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
        return Template(np.array(self.getReference()), self.cable, self.branch, self.channel, self.path)


# Template Class to compare templates
# TODO: Add branch to Template class and to plot title if applicable
class Template:
    def __init__(self, templateData, cable, branch, channel, path):
        self.cable      = cable
        self.branch     = branch 
        self.channel    = channel 
        self.templateData = templateData.astype(int)
        self.ones       = np.count_nonzero(self.templateData==1)
        self.zeros      = np.count_nonzero(self.templateData==0)
        self.total      = self.templateData.size
        self.path       = path
        self.verbose    = False
        if self.verbose:
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
        
        # Save counts
        self.outCounts = outCounts
        self.inCounts  = inCounts
        # Once the counts are saved, we can print values
        self.printProperties()

        #print(diffCounts) # NEED TO OUTPUT TO .TXT: count for differing elements in matrix outside of reference's eye 
        # ADDITION: count for elements that are the same
        return diffArr 
    
    def plot(self, reference):
        # Difference array as Template Object
        #diff = self.__sub__(reference) 
        fig, (ax0, ax1, ax2) = plt.subplots(3, 1)
        if self.branch:
            fig.suptitle(f"Cable: {self.cable}, Branch: {self.branch}, Channel: {self.channel.upper()}")
        else:
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

        fig.savefig(self.path + "template_plots.pdf")   
        plt.close(fig)    

    def getZeros(self):
        return self.zeros
    
    def getOnes(self):
        return self.ones
    
    def getOutCounts(self):
        return self.outCounts

    def getInCounts(self):
        return self.inCounts

    def printProperties(self):
        print(f"Cable: {self.cable}, Channel: {self.channel.upper()}, eye-diagram template analysis:")
        print(f" - Number of 0s (points in open area): {self.zeros}")
        print(f" - Number of 1s (points in closed area): {self.ones}")
        print(f" - Number of 0s outside reference eye: {self.outCounts}")
        print(f" - Number of 1s inside reference eye: {self.inCounts}")

def main():
    # Obtain cable and channel from user
    cable = str(input("Cable: "))
    channel = str(input("Channel: "))
    base_path = "/Users/caleb/CMS/Tracker/e-links/eLink_Instrumentation/EyeBERT/EyeBERT_data"
    # Create EyeBERTFile object, cleaning user input, to read data from file
    eyebert = EyeBERTFile(cable.replace(" ", ""), channel.replace(" ", "").lower(), base_path)
    # Call analyze method to obtain graphs and properties
    analysis = eyebert.analyze()
    # Warning: .getPath() must be called AFTER .analyze()
    refPath = eyebert.getPath()
    if analysis.verify(): # Only continue if template passes verification
        # In progress testing for comparison analysis:
        template = analysis.createTemplate()

        reference_template_file = "EyeBERT/reference_template_v2.csv"
        print(f"Using this reference template data file: {reference_template_file}")
        
        ref = Reference("540", eyebert.branch, "CMD", reference_template_file, refPath)
        refTemp = ref.createTemplate()
        
        # EDIT: reference needs to be a template object
        template.plot(refTemp) 
        print("\n")
    else:
        print(f"Error for cable {cable} and channel {channel.upper()}: Template failed verification step.")


if __name__ == "__main__":
    main()
