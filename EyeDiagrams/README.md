# Eye Diagrams 

Scripts to analyze oscilloscope data take for "e-link" cables.
Specifically, analyze eye diagram data to measure parameters such as height and jitter.

## Setup
Follow the setup instrutions [here](https://github.com/ku-cms/eLink_Instrumentation).

## Instructions

### Processing Data

The primary data processing script takes a directory of csv files that contain eye diagram data as input and combines the data into a single output csv file.
Use -h to see the help menu, which displays the options:
```
python3 python/makeTables.py -h
```
The script requires an input directory (-i), an output directory (-o), and output file name (-f), and a cable type (-t).
Here is an example of running this script:
```
python3 python/makeTables.py -i data/Cable_158_beforeLashing  -o tables -f Cable_158_EyeDiagrams_beforeLashing.csv -t 1
```
This will create the output file tables/Cable_158_EyeDiagrams_beforeLashing.csv.

TODO: Make a plotting script to plot eye diagram data for each cable.

There is a script for making comparison plots.
It can be run like this:
```
python3 python/plotComparison.py
```

### Additional Scripts

First activate the conda environment with the necessary packages based on the instructions [here](https://github.com/ku-cms/eLink_Instrumentation).
```
conda activate .venv
```

One example input file is formatted_data_1.xlsx, which is input for the script readData.py.
You can run the script like this.
```
cd EyeDiagrams
python readData.py
```

Another example input file is raw_data_1.csv, which is input for the script Analyzer.py.
You can run the script like this.
```
cd EyeDiagrams
python Analyzer.py
```

To deactivate conda environment:
```
conda deactivate
```

