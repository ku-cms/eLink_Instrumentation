import csv
import matplotlib.pyplot as plt
import numpy as np

class EyeBERTAnalysis:
    def __init__(self, cable, channel):
        self.cable = cable
        self.channel = channel

    def get_filename(self):
        """Returns corresponding filename to cable and channel."""
        filename = self.cable + "_" + self.channel + "_" + "3" # NEED: search for most recent file
        return filename

    def read_data(self):
        """Returns matrix of data for raw Eye-BERT values."""
        filename = self.get_filename()
        
        data = []
        
        with open(filename + ".csv", "r") as file: 
            search = list(csv.reader(file)) 
            for r in range(21, 46, 1): 
                row = [] 
                for c in range(1, 66, 1): 
                    value = float(search[r][c]) 
                    row.append(value)
                data.append(row)
                
        return data

    def get_template(self):
        """Returns matrix of values for the Eye-BERT template."""
        data = self.read_data()
        
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

    def graph(self):
        """Returns plots for raw Eye-BERT data and Eye-BERT template."""
        data = self.read_data() 
    
        raw = np.array(data)
        template = np.array(self.get_template())

        fig, (ax0, ax1) = plt.subplots(2, 1)

        fig.suptitle(f"Cable: {self.cable}, Channel: {self.channel.upper()}")

        fig.tight_layout(h_pad=3)

        # Plot for raw Eye-BERT data
        im = ax0.pcolormesh(raw, cmap="binary")
        ax0.set_title("Raw Eye-BERT Data")
        fig.colorbar(im, ax=ax0, location="bottom")

        # Plot for Eye-BERT template
        im = ax1.pcolormesh(template, cmap="binary")
        ax1.set_title("Eye-BERT Template")
        fig.colorbar(im, ax=ax1, location="bottom")
    
        plt.show()

    def counts(self):
        template = np.array(self.get_template())

        #total = template.size
        count_0s = np.count_nonzero(template==0)
        count_1s = np.count_nonzero(template==1)
        total = count_0s + count_1s
        actual_total = template.size
        
        return print(f"Total: {total}, {actual_total}\n0s: {count_0s}\n1s: {count_1s}")

def view(data):
    """View data by each row of matrix."""
    for r in data:
        print(r)

def main():

    # Obtain cable and channel from user
    cable = str(input("Cable: "))
    channel = str(input("Channel: "))

    # Create EyeBERT object, cleaning user input
    eyebert = EyeBERTAnalysis(cable.replace(" ", ""), channel.replace(" ", "").lower())
    
    eyebert.counts()
    eyebert.graph()
    
if __name__ == "__main__":
    main()
