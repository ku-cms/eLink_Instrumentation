# Eye Diagrams 

Scripts to analyze oscilloscope data take for "e-link" cables.
Specifically, analyze eye diagram data to measure parameters such as height and jitter.


## Setup

Fist, follow the setup instrutions [here](https://github.com/ku-cms/eLink_Instrumentation).

The scripts should be run using python3.
Depending on you environment, you may need to use "python" or "python3" to do this.
To check your python version, do:
```
python --version
```
or 
```
python3 --version
```

For these scripts, python3 should be used, and numpy and matplotlib should be installed.
Here are installation commands to install numpy and matplotlib.
The option `--user` is only needed if you do not have admin permission.
```
python -m pip install --upgrade pip --user
python -m pip install numpy --user
python -m pip install matplotlib --user
```

Command to launch Git Bash in Windows 10 when shortcut does not work:
```
git -c alias.b=!bash b -l -i
```

## Instructions


### Processing Data

The primary data processing script is "processData.py."
This script should be run for each cable after taking eye diagram data, and the output should be copied to a central location.
It takes a directory of eye diagram statistics tables (csv files) as input.
It collects this data into a single table and outputs this as a new csv file.
In addition, it creates plots of this data and outputs these as pdf/png files.

First, eye diagram data is required.
- The statistics table for each channel should be saved as a csv file.
- Only include the module number (M1, M2, etc.) in the file name for type 3/4 cables.
- Include the channel number (CMD, D0, D1, etc.) in the file name for all cables.
- Example file name (type 1 cable): TP_158_CMD_Stats.csv
- Example file name (type 4 cable): TP_121_M1_CMD_Stats.csv
- These files should be put into a directory for the respective cable, for example "data/Cable_121".
- This directory containing the raw data is the input directory for processData.py.

Data cleaning is required for the raw data files to remove byte 0x96 (`<96>`) that appears in the csv files.

Open the file in vim.
```
vim TP_158_CMD_Stats.csv
```
Use this command in vim to remove byte 0x96 (and actually press control V).
```
:%s/<CTRL-V>x96//g
```
Then use ":x" to save file and exit.
Repeat for other files using vim history to get this command quickly.

If needed, here is an example of renaming a group of files from a terminal.
In this example, "wf" is replaced with "Stats" in the file name for all csv files in the current directory.
This step is not required.
```
for f in *.csv; do mv "$f" "$(echo "$f" | sed s/wf/Stats/g)"; done
```

New data processing script! You need to provide the path to a zip (which has raw csv data files) and the cable number.
```
./scripts/process.sh ~/Downloads/OneDrive_6_6-18-2021.zip 555
```

Note that you may need to use "python3" instead of "python" depending on your environment.

Use -h to see the help menu, which displays the options:
```
python python/processData.py -h
```

The required options are cable number (-n) and cable type (-t).
There are other options, but they will use default values if they are not specified.
```
python python/processData.py -n 121 -t 4
```
Here is an example of specifying more options.
Here the values specified are the default values, so the input/output will be the same.
Non-default values can be provided if needed.
```
python python/processData.py -i data/Cable_121 -o tables -p plots/Cable_121 -f Cable_121_EyeDiagrams.csv -n 121 -t 4
```
In both of these example, the intput directory is "data/Cable_121."
The script will output the data to "tables/Cable_121_EyeDiagrams.csv," and the plots will be saved in "plots/Cable_121."

After running "python/processData.py," copy the output table and plots to a central location.

### Additional Scripts


To process eye diagram data for RD53A/B TAP0 scans, first download the relevant data directory.
Move the zip file to a "storage area" for eye diagram data and unzip it (e.g. /Users/caleb/CMS/Tracker/e-links/EyeDiagramData).
Then use this script and provide a directory that is in the "storage_dir" directory defined in the script. 
You will first need to set "storage_dir" in the script to your local "storage area."
```
./scripts/process_scan.sh <data_directory>
```
A new directory for cleaned data will be created.
For example, running the script on this directory:
```
./scripts/process_scan.sh RD53B_EyeDiagrams_TAP0_2022_08_26
```
creates this directory to store the output:
```
RD53B_EyeDiagrams_TAP0_2022_08_26_clean
```
Copy the data to the data directory:
```
rsync -az /Users/caleb/CMS/Tracker/e-links/EyeDiagramData/RD53B_EyeDiagrams_TAP0_2022_08_26 data
rsync -az /Users/caleb/CMS/Tracker/e-links/EyeDiagramData/RD53B_EyeDiagrams_TAP0_2022_08_26_clean data
```

Create csv tables of the eye diagram parameters with this script:
```
python3 python/makeTableScan.py
```

Plot data from csv tables:
```
python3 python/makePlots.py
```

To compare data from multiple csv files, use this script:
```
python3 python/plotComparisonMultiInput.py
```

To compare data using a signle input csv file, use this script:
```
python python/plotComparison.py
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

