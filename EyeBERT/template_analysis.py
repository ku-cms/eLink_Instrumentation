import csv

def view(template):
    for r in template:
        print(r)

def main():
    file_path = "EyeBERT_data/541/541_cmd_3.csv" # temporary default to Eye-BERT result of CMD for 541
    template = []
    with open(file_path, "r") as file: 
        search = list(csv.reader(file)) # convert to list to index through
        for r in range(21, 46, 1): # iterate over each row
            row = []
            for c in range(1, 66, 1): # iterate over each column
                value = float(search[r][c])
                if value < 2.0e-7:
                    row.append(1)
                else:
                    row.append(0)
            template.append(row)
    view(template)

if __name__ == "__main__":
    main()