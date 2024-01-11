import csv
import matplotlib.pyplot as plt
import numpy as np
import os

# To-Do:
# Template comparisons --- standard template to compare to?
# Working with Windows & existing code
# Edit properties text file (ex. open area vs. number of 0's, etc., utilize Template class)
# Display original EyeBERT plot with other plots?
# Account cable lengths?

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
    def __init__(self, cable, channel):
        self.cable = cable
        self.channel = channel 
        self.path = "AnalysisOutputs/" + self.cable + "/" + self.cable + "_" + self.channel + "_" # Prefix for new outputted files

class EyeBERTFile(EyeBERT):
    def __init__(self, cable, channel):
        super().__init__(cable, channel)
        self.dataPath = "EyeBERT/EyeBERT_data/" + self.cable # Path to get Eye-BERT data

    def getFile(self):
        """Returns latest .csv file for the corresponding channel from the cable's directory."""
        # Initialize empty list to store file names
        channelFiles = [] 
        # Append all .csv files with the corresponding channel from the directory to the list
        for file in os.listdir(self.dataPath):
            if self.channel in file and ".csv" in file:
                channelFiles.append(file)
        # Sort file names in descending order to ensure latest file will always be at index 0 
        channelFiles.sort(reverse=True)
        # Return the file name at index 0 (latest file for that channel)
        return channelFiles[0]

    def getFilename(self):
        """Returns corresponding filename to cable and channel."""
        filename = self.dataPath + "/" + self.getFile()
        return filename

    def readFile(self):
        """Reads data from file to return raw data."""
        filename = self.getFilename()
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
        return EyeBERTAnalysis(self.cable, self.channel, self.getData(), self.getTemplate())

class EyeBERTAnalysis(EyeBERT):
    def __init__(self, cable, channel, data, template):
        super().__init__(cable, channel)
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
        return Template(self.template, self.cable, self.channel)

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
                if self.data[i][j] > 2.0e-7 and self.template[i][j] != 1:
                    return False
        return True

# Template Class to compare templates
class Template:
    def __init__(self, templateData, cable, channel):
        self.cable = cable
        self.channel = channel 
        self.templateData = templateData.astype(int)
        self.ones = np.count_nonzero(self.templateData==1)
        self.zeros = np.count_nonzero(self.templateData==0)
        self.total = self.templateData.size

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
        if self.templateData == other.templateData:
            return True
        return False

def main():
    # Obtain cable and channel from user
    cable = str(input("Cable: "))
    channel = str(input("Channel: "))
    # Create EyeBERTFile object, cleaning user input, to read data from file
    eyebert = EyeBERTFile(cable.replace(" ", ""), channel.replace(" ", "").lower())
    # Call analyze method to obtain graphs and properties
    analysis = eyebert.analyze()
    if analysis.verify(): # Only continue if template passes verifcation
        analysis.graph() 
        analysis.writeText()

if __name__ == "__main__":
    main()