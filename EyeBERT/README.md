# Eye BERT

This directory contains the necessary files to run Eye BERT scans on e-links
using a KC705, SMA cables, and yellow e-link to SMA adapter boards.
The project is designed to run on Windows 10 using Vivado 2020.2.
However, the project should be able to run on Linux with some modifications.

## The Windows Batch File: run_test.bat

First, download this repository.
```
git clone https://github.com/ku-cms/eLink_Instrumentation.git
```

Then, create a new directory on your computer for the Eye BERT Vivado project.
Copy these files from the "EyeBERT" directory to the new project folder that you created:
```
eLink_Instrumentation/EyeBERT/Bert_Icon_v1.ico
eLink_Instrumentation/EyeBERT/Bert_Icon_v2.ico
eLink_Instrumentation/EyeBERT/README.md
eLink_Instrumentation/EyeBERT/cable_test_705.bit
eLink_Instrumentation/EyeBERT/run_test.bat
eLink_Instrumentation/EyeBERT/run_test.tcl
```

The Windows batch file (.bat) that is used to load the Vivado project is "run_test.bat".
To run on Linux, a similar bash script (.sh) could be created.
Here are the contents of "run_test.bat":
```
cd C:\Users\Public\Documents\cable_tests

d:\vivado\2020.2\bin\vivado.bat -mode batch -source run_test.tcl
exit
```
The paths in "run_test.bat" should be modified and set to the correct paths for your computer.
The first path `C:\Users\Public\Documents\cable_tests` should be set to the directory for the project that you created
(where run_test.bat, run_test.tcl, cable_test_705.bit, etc. are located).
The second path `d:\vivado\2020.2\bin\vivado.bat` should be set to the path of the Vivado 2020.2 executable
(in Windows, this is also a bat file).

## The TCL file: run_test.tcl

TODO: fix typos in TCL file and test:
Change "firt_bit_file" to "first_bit_file".
Change "targu" to "target".

Next, the TCL file "run_test.tcl" is used to setup the Vivado project. 

In "run_test.tcl", the path in this line should be changed to point to the path of the "cable_test_705.bit" file.
```
set firt_bit_file "C:/Users/Public/Documents/cable_tests/cable_test_705.bit"
```
The file "cable_test_705.bit" is the KC705 firmware for the Eye BERT project.

In "run_test.tcl", the path in this line should be set to the project directory.
```
cd "C:/Users/Public/Documents/cable_tests/"
```

In Windows, create a shortcut to "run_test.bat" file. 
Modify the shortcut properties to set the icon image to one of these files (take your pick):
- Bert_Icon_v1.ico
- Bert_Icon_v2.ico


## The BIT file:
cable_test_705.bit

## The ICO image files:
Bert_Icon_v1.ico
Bert_Icon_v2.ico


