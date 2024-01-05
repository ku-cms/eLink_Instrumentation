import csv
import matplotlib.pyplot as plt
import numpy as np

# Temporarily set cable 541, channel CMD
# To-Do: inputs for cable number and channel, updating file path

# Returns plots for raw Eye-BERT data and Eye-BERT template
def graph():
    data = read_data() 
    
    raw = np.array(data)
    template = np.array(get_template(data))

    fig, (ax0, ax1) = plt.subplots(2, 1)

    fig.tight_layout(h_pad=4)

    # Plot for raw Eye-BERT data
    im = ax0.pcolormesh(raw, cmap="binary")
    ax0.set_title("Raw Eye-BERT Data")
    fig.colorbar(im, ax=ax0, location="bottom")

    # Plot for Eye-BERT template
    im = ax1.pcolormesh(template, cmap="binary")
    ax1.set_title("Eye-BERT Template")
    fig.colorbar(im, ax=ax1, location="bottom")
    
    plt.show()

# Function to display data of matrix by row
def view(data):
    for r in data:
        print(r)

# Function returning matrix of values for Eye-BERT raw data
def read_data():
    data = []
    with open("541_cmd_3.csv", "r") as file: 
        search = list(csv.reader(file)) 
        for r in range(21, 46, 1): 
            row = [] 
            for c in range(1, 66, 1): 
                value = float(search[r][c]) 
                row.append(value)
            data.append(row)
    return data

# Function returning matrix of values for Eye-BERT template
def get_template(data):
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

def main():
    graph()
    
if __name__ == "__main__":
    main()