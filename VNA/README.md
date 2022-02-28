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

Run the following python analysis script and enter the requested parameters.
```
python VNA_Comp.py
```

- Enter cable number.
- Enter cable type (1, 2, 3, 4).
- Enter cable length in cm (35, 80, 100, 140, 160, 200).

Note: To analyze data for "Type 0" cables, enter "Type 1" for this script.

## Setup

First, follow the instrutions [here](https://github.com/ku-cms/eLink_Instrumentation).
Then follow the conda setup instrutions in the next section.

### Conda Setup

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
