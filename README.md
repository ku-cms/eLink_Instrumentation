# eLink_Instrumentation

- VNA data processing scripts to study e-link impedance ([here](https://github.com/ku-cms/eLink_Instrumentation/tree/main/VNA)).
- Oscilloscope data processing scripts to study e-link eye diagrams ([here](https://github.com/ku-cms/eLink_Instrumentation/tree/main/EyeDiagrams)).
- Aurora bitstream used to emulate RD53A bitstream in order to test the Ernie board ([here](https://github.com/ku-cms/eLink_Instrumentation/tree/main/Aurora_bitstream)).


## Setup

### Download
Download the repository and create directories for VNA data and plots.
```
git clone https://github.com/ku-cms/eLink_Instrumentation.git
cd eLink_Instrumentation/VNA
mkdir -p data
mkdir -p plots
cd ..
```

### Conda
Certain python packages are required, so you will need to setup your python environment to use them.
The main package that is used for VNA data analysis is called scikit-rf with documentation [here](https://scikit-rf.readthedocs.io/en/latest/index.html) and installation instructions [here](https://scikit-rf.readthedocs.io/en/latest/tutorials/Installation.html).
I recommend creating a python environment using conda in order to install the necessary packages.
See the conda documentation [here](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html).
Also, for new Macs (2020 and later) that have an Apple M1 chip (which uses a new architecture), look [here](https://www.jimbobbennett.io/installing-scikit-learn-on-an-apple-m1/).

To install conda, go [here](https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/index.html), choose your operating system, and follow the instructions.
Once conda is installed, you can run these commands in your terminal (for Mac or Linux... I'm not sure about Windows!).
```
conda update -n base conda
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

