import csv
import matplotlib.pyplot as plt
import numpy as np
import os

# To-Do: Writing to text files, saving outputs in new directory based on cable
# Interface class?

class EyeBERTFile:
    def __init__(self, cable, channel):
        self.cable = cable
        self.channel = channel
        self.path = "EyeBERT/EyeBERT_data/" + self.cable # Need to change

    def get_file(self):
        """Returns latest .csv file for the corresponding channel from the cable's directory."""
        # Initialize empty list to store file names
        channel_files = [] 

        # Append all .csv files with the corresponding channel from the directory to the list
        for file in os.listdir(self.path):
            if self.channel in file and ".csv" in file:
                channel_files.append(file)

        # Sort file names in descending order to ensure latest file will always be at index 0 
        channel_files.sort(reverse=True)

        # Return the file name at index 0 (latest file for that channel)
        return channel_files[0]

    def get_filename(self):
        """Returns corresponding filename to cable and channel."""
        filename = self.path + "/" + self.get_file()
        return filename

    def read_file(self):
        """Reads data from file to return raw data."""
        filename = self.get_filename()

        data = []

        with open(filename, "r") as file: 
            search = list(csv.reader(file)) 
            for r in range(21, 46, 1): 
                row = [] 
                for c in range(1, 66, 1): 
                    value = float(search[r][c]) 
                    row.append(value)
                data.append(row)
                
        return data

    def get_data(self):
        """Returns raw data from file as list of lists."""
        return self.read_file()

    def get_template(self):
        """Returns template data as list of lists."""
        data = self.get_data()
        
        template = []
        
        for r in data:
            row = []
            for value in r:
                if value < 2.0e-7:
                    row.append(0)
                else:
                    row.append(1)
            template.append(row)
        
        return template

    def analyze(self):
        """Returns EyeBERTAnalysis object using data read from file."""
        # Make directory to store results if one does not already exist
        #try:
            #os.mkdir("Analysis_Outputs")
        #except:
            #pass
        
        return EyeBERTAnalysis(self.cable, self.channel, self.get_data(), self.get_template())


class EyeBERTAnalysis:
    def __init__(self, cable, channel, data, template):
        self.cable = cable
        self.channel = channel
        self.data = np.array(data)
        self.template = np.array(template)

        self.name = self.cable + "_" + self.channel

    #def make_directory(self):
        # Make a directory to store results 
        #try:
            #os.mkdir("Analysis/" + self.cable)
        #except:
            #return

    def graph(self):
        """Returns plots for raw Eye-BERT data and Eye-BERT template."""
        fig, (ax0, ax1) = plt.subplots(2, 1)

        fig.suptitle(f"Cable: {self.cable}, Channel: {self.channel.upper()}")

        fig.tight_layout(h_pad=3)

        # Plot for raw Eye-BERT data
        im = ax0.pcolormesh(self.data, cmap="nipy_spectral") # Different colors 
        ax0.set_title("Raw Eye-BERT Data")
        fig.colorbar(im, ax=ax0, location="bottom")

        # Plot for Eye-BERT template
        im = ax1.pcolormesh(self.template, cmap="binary")
        ax1.set_title("Eye-BERT Template")
        fig.colorbar(im, ax=ax1, location="bottom")
    
        #plt.show()

        fig.savefig(self.cable + "_" + self.channel + ".pdf")   
        plt.close(fig)    


    # To output to text file:

    def write_text(self):
        np.savetxt(self.name + "_template.txt", self.template)
        np.savetxt(self.name + "_raw.txt", self.data)

        f = open(self.name + "_template.txt", "a")
        f.write(self.counts())
        f.close()

        #np.savetxt(self.name + "_template.csv", self.template, delimiter=",")
        #np.savetxt(self.name + "_raw.csv", self.data, delimiter=",")

    def counts(self):
        """Returns the counts of 1's and 0's in the template."""
        #total = template.size
        count_0s = np.count_nonzero(self.template==0)
        count_1s = np.count_nonzero(self.template==1)
        total = count_0s + count_1s
        actual_total = self.template.size

        return f"Total: {total}, {actual_total}\n0s: {count_0s}\n1s: {count_1s}"


def main():
    # Obtain cable and channel from user
    cable = str(input("Cable: "))
    channel = str(input("Channel: "))

    # Create EyeBERTFile object, cleaning user input, to read data from file
    eyebert = EyeBERTFile(cable.replace(" ", ""), channel.replace(" ", "").lower())

    # Call analyze method to obtain graphs and properties
    analysis = eyebert.analyze()

    analysis.graph()
    #analysis.counts()

    # TESTING -- writing to text file output
    analysis.write_text()

if __name__ == "__main__":
    main()
