# VNA Data Processing

Input files: VNA output files (.vna.txt) from Matlab data taking program.

## Setup

### Windows 10

If python is not already installed, download and install the latest version of python 3.

https://www.python.org/downloads/

Open CMD shell.

Type “python” and hit enter to check that python is installed and in the path.

Update to latest version of pip (can only be done per user due to permissions):

```
pip install --upgrade pip –user
```

Install required packages:

```
pip install numpy
pip install pandas
pip install matplotlib
pip install scikit-rf
```

Check list of installed python packages:

```
pip list
```

## Processing Data

### Windows 10

Python should be setup (if not, see previous section).

The VNA data analysis script can be found [here](https://github.com/ku-cms/eLink_Instrumentation/blob/main/VNA/python/VNA_COMP.py).

Your user will need to have access to the R drive. To access the R drive, your KU user needs to be added to the group "phsx_r_bean" on groups.ku.edu. You can ask Prof. Alice Bean to be added to this group.

Make sure data has been taken for all channels of the e-link before running the script. The script analyzes data for all e-link channels.

To analyze data, first create a directory for the cable that you want to analyze using the cable number on the R drive with this path:
```
R:\BEAN_GRP\4portvnadata\VNA_analysis\Data\<cable_number>
```
Then, copy the VNA data files (.vna.txt) for that cable from the folder
```
R:\BEAN_GRP\4portvnadata\Cable_<cable_number>
```
to the folder
```
R:\BEAN_GRP\4portvnadata\VNA_analysis\Data\<cable_number>
```

This is the path to the production version of VNA analysis script on the network R drive:
```
R:\BEAN_GRP\4portvnadata\VNA_analysis\VNA_Comp.py
```

Open file explorer on the Windows 10 computer and navigate to this directory:
```
R:\BEAN_GRP\4portvnadata\VNA_analysis
```

Click on the full path tab at the top and enter “cmd.”

A Command Prompt shell should open with the working directory “R:\BEAN_GRP\4portvnadata \VNA_analysis” .

You can enter the command “cd” to print the current working directory.

Run the following python analysis script and enter the requested parameters.
```
python VNA_Comp.py
```

- Enter cable number.
- Enter cable type (1, 2, 3, 4).
- Enter cable length in cm (35, 80, 100, 140, 160, 200).

Note: To analyze data for "Type 0" cables, enter "Type 1" for this script.

At the end, enter comments (if any) and press enter. If not comments, just press enter.
The program prints impedance values and saves them in a csv file.
The program also creates plots.

### macOS, Linux

<details>

<summary>Conda Setup</summary>

First, follow the instructions [here](https://github.com/ku-cms/eLink_Instrumentation). Then, if you want to setup conda to install necessary python packages, follow these instructions.

Certain python packages are required, so you will need to setup your python environment to use them.
The main package that is used for VNA data analysis is called scikit-rf with documentation [here](https://scikit-rf.readthedocs.io/en/latest/index.html) and installation instructions [here](https://scikit-rf.readthedocs.io/en/latest/tutorials/Installation.html).
I recommend creating a python environment using conda in order to install the necessary packages.
See the conda documentation [here](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html).
Also, for new Macs (2020 and later) that have an Apple M1 chip (which uses a new architecture), look [here](https://www.jimbobbennett.io/installing-scikit-learn-on-an-apple-m1/).

To install conda, go [here](https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/index.html), choose your operating system, and follow the instructions.
Once conda is installed, you can run these commands in your terminal (for Mac or Linux... I'm not sure about Windows!).
```
conda update -n base -c defaults conda
conda config --set auto_activate_base false
```
Then you can create a new python environment.
```
conda create -n .venv python
```
To activate the environment, do
```
conda activate .venv
```
When the environment is active, install scikit-rf (for VNA data analysis) and other packages (for eye diagram analysis).
```
conda install -c conda-forge  scikit-rf
conda install pandas
conda install xlrd
conda install openpyxl
```
To list installed packages, do
```
conda list
```
To deactivate the environment, do
```
conda deactivate
```
You can now activate and deactivate your conda environment as needed.
You will need to activate it before running the scripts that use scikit-rf and other required packages.

</details>
