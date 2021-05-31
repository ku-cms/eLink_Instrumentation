# Eye Diagrams 

Scripts to analyze oscilloscope data take for "e-link" cables.
Specifically, analyze eye diagram data to measure parameters such as height and jitter.


## Setup
Follow the setup instrutions [here](https://github.com/ku-cms/eLink_Instrumentation).


## Instructions


### Processing Data

The primary data processing script is "processData.py."
This script should be run for each cable after taking eye diagram data, and the output should be copied to a central location.
It takes a directory of eye diagram statistics tables (csv files) as input.
It collects this data into a single table and outputs this as a new csv file.
In addition, it creates plots of this data and outputs these as pdf/png files.

First, eye diagram data is required.
- The statistics table for each channel should be saved as a csv file.
- These files should be put into a directory for the respective cable, for example "data/Cable_121".
- This directory containing the raw data is the input directory for processData.py.

Use -h to see the help menu, which displays the options:
```
python3 python/processData.py -h
```

The required options are cable number (-n) and cable type (-t).
There are other options, but they will use default values if they are not specified.
```
python3 python/processData.py -n 121 -t 4
```
Here is an example of specifying more options.
Here the values specified are the default values, so the input/output will be the same.
Non-default values can be provided if needed.
```
python3 python/processData.py -i data/Cable_121 -o tables -p plots/Cable_121 -f Cable_121_EyeDiagrams.csv -n 121 -t 4
```
In both of these example, the intput directory is "data/Cable_121."
The script will output the data to "tables/Cable_121_EyeDiagrams.csv," and the plots will be saved in "plots/Cable_121."


### Additional Scripts

There is a script for making comparison plots.
This can be used to compare different cables, or to compare different datasets for the same cable (e.g. before/after lashing).
It can be run like this:
```
python3 python/plotComparison.py
```

There are other scripts that require additional python packages.
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

