# Eye Diagrams 

Scripts to analyze oscilloscope data take for "e-link" cables.
Specifically, analyze eye diagram data to measure parameters such as height and jitter.

## Setup
Follow the instrutions [here](https://github.com/ku-cms/eLink_Instrumentation).

## Instructions
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

